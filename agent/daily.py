"""Livello 2: analisi giornaliera con Claude.

Raccoglie le ultime 24 h della flotta di produzione, le passa a Claude insieme
alla scheda di conoscenza e al registro dei problemi, e riceve in JSON:
riassunto Telegram, report email, registro aggiornato. Il registro diventa
ISSUES.md nel repo: e' il canale verso lo sviluppo.
"""
import json
import re
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import anthropic
import markdown as md

from . import checks, db, state
from . import config as cfg

ROME = ZoneInfo("Europe/Rome")
MODEL = "claude-opus-5-5"
ISSUES_STATE = cfg.STATE_DIR / "issues.json"
ISSUES_MD = cfg.ROOT / "ISSUES.md"
DAILY_LOG = cfg.STATE_DIR / "daily_log.json"

SYSTEM = """Sei l'analista tecnico della flotta CGSLIM (cambiamonete nei centri commerciali).
Ogni giorno ricevi lo stato delle macchine di produzione e gli eventi delle ultime 24 ore.
Il lettore e' lo sviluppatore del firmware e del software (Maurizio): conosce il sistema,
vuole sapere cosa e' cambiato, cosa non va e cosa fare, in italiano semplice e diretto.

Il tuo lavoro:
1. Riconoscere i problemi reali, separandoli dal comportamento normale (spegnimento notturno,
   clienti che annullano, errori transitori gia' rientrati).
2. Collegare i sintomi ai problemi gia' noti (scheda di conoscenza) e al registro esistente.
   Non presentare come scoperta un problema noto: aggiorna la voce del registro.
3. Tenere il registro dei problemi per lo sviluppo: una voce per causa, non per macchina.
   Mantieni gli id esistenti; per le voci nuove usa gli id a partire da quello indicato.
   Chiudi (resolved) una voce solo se i dati mostrano che il problema e' sparito da giorni;
   "monitoring" se non si e' ripresentato oggi ma e' troppo presto per chiuderla.
4. Distinguere fatti e ipotesi. Ogni affermazione sulle macchine deve venire dai dati forniti;
   cita MHD (senza zeri iniziali), orari e numeri. Se un dato manca, dillo.

Stile del report email (markdown): parti da 3-5 righe "In breve", poi sezioni brevi:
Da fare oggi (azioni concrete, chi le fa), Problemi aperti, Novita' rispetto a ieri,
Stato flotta (numeri). Niente frasi di cortesia, niente ripetizioni del registro intero.
Il riassunto Telegram: massimo 6 righe di testo semplice, la prima con il conteggio online."""

ISSUE_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "string", "description": "CG-NNN"},
        "title": {"type": "string"},
        "status": {"type": "string", "enum": ["open", "monitoring", "resolved"]},
        "severity": {"type": "string", "enum": ["high", "medium", "low"]},
        "area": {"type": "string", "enum": ["firmware", "pi", "dashboard", "hardware", "campo", "pos"]},
        "machines": {"type": "array", "items": {"type": "string"}},
        "first_seen": {"type": "string", "description": "YYYY-MM-DD"},
        "last_seen": {"type": "string", "description": "YYYY-MM-DD"},
        "evidence": {"type": "string", "description": "fatti dai dati, con numeri e orari"},
        "hypothesis": {"type": "string"},
        "proposal": {"type": "string", "description": "correzione o verifica proposta"},
        "known_issue": {"type": "string", "description": "riferimento alla scheda di conoscenza, o vuoto"},
    },
    "required": ["id", "title", "status", "severity", "area", "machines", "first_seen",
                 "last_seen", "evidence", "hypothesis", "proposal", "known_issue"],
    "additionalProperties": False,
}
OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "telegram_summary": {"type": "string"},
        "report_markdown": {"type": "string"},
        "issues": {"type": "array", "items": ISSUE_SCHEMA},
    },
    "required": ["telegram_summary", "report_markdown", "issues"],
    "additionalProperties": False,
}


def _load_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def _ts(dt) -> str:
    return dt.astimezone(ROME).strftime("%d/%m %H:%M") if dt else None


def _device_view(d: dict) -> dict:
    """Solo i campi utili all'analisi: il payload completo pesa troppo."""
    st = d.get("status") or {}
    rt, host, app = st.get("runtime") or {}, st.get("host") or {}, st.get("app") or {}
    serial = st.get("serial") or {}
    adapter = serial.get("adapter") or {}
    last_test = serial.get("last_test") or {}
    return {
        "mhd": (d.get("mhd") or "").lstrip("0"), "center": d.get("center"), "label": d.get("label"),
        "last_seen": _ts(d["last_seen"]), "offline_min": d["age_s"] // 60 if d["age_s"] > 35 * 60 else 0,
        "app_version": d.get("app_version"), "fw": d.get("fw_version"), "branch": d.get("git_branch"),
        "git_commit": (d.get("git_commit") or "")[:8], "app_running": d.get("app_running"),
        "mod": rt.get("mod"), "screen": rt.get("screen"), "idle": rt.get("idle"), "hopper": rt.get("hopper"),
        "cashless": rt.get("cashless"), "serial_missing": rt.get("serial_missing"),
        "gmi_blocked": rt.get("gmi_blocked"), "network": rt.get("network"), "rssi": rt.get("rssi"),
        "gmi_serial_counters": (rt.get("serial") or {}).get("gmi"),
        "pi_uart": (rt.get("serial") or {}).get("pi_uart"),
        "host": {k: host.get(k) for k in ("pi_model", "throttled", "cpu_temp_c", "disk_free_mb",
                                          "uptime_s", "clock_skew_s")},
        "updater": app.get("updater"), "services": app.get("services"),
        "adapter": {"chip": adapter.get("chip"), "serial": adapter.get("serial"), "usb_path": adapter.get("usb_path")},
        "line_test": {"ts": last_test.get("ts"), "verdict": last_test.get("verdict")} if last_test else None,
        "pos": st.get("pos"), "card_activity_24h": st.get("card_activity"),
        "device_key_status": d.get("device_key_status"),
    }


def _event_view(e: dict, names: dict) -> dict:
    data = json.dumps(e.get("data") or {}, ensure_ascii=False, default=str)
    # le diagnosi USB pesano kB: bastano l'inizio e il caso
    return {"t": _ts(e["received_at"]), "mhd": names.get(e["device_id"], e["device_id"][-8:]),
            "kind": e["kind"], "data": data[:400]}


def _trx_summary(trx: list[dict]) -> list[dict]:
    by = {}
    for t in trx:
        k = (t.get("mhd") or "").lstrip("0")
        s = by.setdefault(k, {"mhd": k, "n": 0, "outcomes": {}, "errors": {}, "methods": {},
                              "first": None, "last": None, "last_approved": None})
        s["n"] += 1
        s["outcomes"][t.get("outcome") or "?"] = s["outcomes"].get(t.get("outcome") or "?", 0) + 1
        m = t.get("method") or "?"
        s["methods"][m] = s["methods"].get(m, 0) + 1
        s["first"] = s["first"] or _ts(t["ts"])
        s["last"] = _ts(t["ts"])  # transazioni ordinate per ts
        if t.get("outcome") == "approved":
            s["last_approved"] = _ts(t["ts"])
        if t.get("outcome") in ("error", "declined", "timeout"):
            r = f"{_ts(t['ts'])} {(t.get('reason') or '')[:100]}"
            s["errors"][r] = s["errors"].get(r, 0) + 1
    return sorted(by.values(), key=lambda s: -s["n"])


def build_context() -> tuple[dict, list[dict]]:
    with db.connect() as conn:
        devices = db.devices(conn)
        events = db.events(conn, hours=24)
        trx = db.transactions(conn, hours=24)
        changes = db.config_changes(conn, hours=24)
    devices, events = checks.production_only(devices, events)
    ids = {d["device_id"] for d in devices}
    trx = [t for t in trx if t["device_id"] in ids]
    names = {d["device_id"]: (d.get("mhd") or "").lstrip("0") for d in devices}

    alerts = state.load()
    issues = _load_json(ISSUES_STATE, [])
    nums = [int(m.group(1)) for i in issues if (m := re.match(r"CG-(\d+)", i.get("id", "")))]
    now = datetime.now(ROME)
    ctx = {
        "now": now.strftime("%Y-%m-%d %H:%M %A"),
        "fleet": {"machines": len(devices),
                  "online": sum(1 for d in devices if d["age_s"] < 35 * 60),
                  "app_versions": _count(d.get("app_version") for d in devices),
                  "fw_versions": _count(d.get("fw_version") for d in devices),
                  "branches": _count(d.get("git_branch") for d in devices)},
        "level1_open_alerts": list(alerts.get("open", {}).values()),
        "level1_resolved_24h": [h for h in alerts.get("history", [])
                                if h.get("resolved_at", "") > (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()],
        "devices": [_device_view(d) for d in devices],
        "events_24h": [_event_view(e, names) for e in events],
        "transactions_24h_by_machine": _trx_summary(trx),
        "config_changes_24h": [{k: str(v) for k, v in c.items()} for c in changes],
        "previous_reports": _load_json(DAILY_LOG, [])[-3:],
        "next_issue_id": f"CG-{(max(nums) if nums else 0) + 1:03d}",
    }
    return ctx, issues


def _count(values) -> dict:
    out = {}
    for v in values:
        out[v or "?"] = out.get(v or "?", 0) + 1
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))


def analyze(ctx: dict, issues: list[dict]) -> tuple[dict, dict]:
    knowledge = (cfg.KNOWLEDGE_DIR / "KNOWLEDGE.md").read_text(encoding="utf-8")
    client = anthropic.Anthropic()
    with client.beta.messages.stream(
        model=MODEL,
        max_tokens=64000,
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        thinking={"type": "adaptive"},
        output_config={"effort": "high", "format": {"type": "json_schema", "schema": OUTPUT_SCHEMA}},
        # parte fissa prima (scheda di conoscenza), dati del giorno dopo
        system=[{"type": "text", "text": SYSTEM},
                {"type": "text", "text": "# Scheda di conoscenza\n\n" + knowledge,
                 "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": [
            {"type": "text", "text": "# Registro dei problemi attuale\n\n"
             + json.dumps(issues, ensure_ascii=False, indent=1)},
            {"type": "text", "text": "# Dati di oggi\n\n"
             + json.dumps(ctx, ensure_ascii=False, default=str)},
            {"type": "text", "text": "Analizza i dati di oggi e restituisci riassunto Telegram, "
             "report email e registro dei problemi aggiornato e completo (tutte le voci, "
             "anche quelle invariate)."},
        ]}],
    ) as stream:
        msg = stream.get_final_message()
    if msg.stop_reason == "refusal":
        raise RuntimeError(f"Claude ha rifiutato la richiesta: {msg.stop_details}")
    if msg.stop_reason == "max_tokens":
        raise RuntimeError("Risposta troncata (max_tokens)")
    text = next(b.text for b in msg.content if b.type == "text")
    u = msg.usage
    usage = {"input": u.input_tokens, "output": u.output_tokens,
             "cache_read": getattr(u, "cache_read_input_tokens", 0) or 0,
             "cache_write": getattr(u, "cache_creation_input_tokens", 0) or 0}
    usage["cost_usd"] = round((usage["input"] * 4 + usage["cache_write"] * 5 + usage["cache_read"] * 0.2
                               + usage["output"] * 20) / 1e6, 3)
    return json.loads(text), usage


def render_issues_md(issues: list[dict]) -> str:
    order = {"open": 0, "monitoring": 1, "resolved": 2}
    sev = {"high": 0, "medium": 1, "low": 2}
    lines = ["# Registro problemi flotta CGSLIM", "",
             f"Aggiornato dall'agente il {datetime.now(ROME):%d/%m/%Y %H:%M}. "
             "Una voce per causa; MHD senza zeri. Generato: non modificare a mano.", ""]
    for status, label in (("open", "Aperti"), ("monitoring", "In osservazione"), ("resolved", "Risolti")):
        group = sorted((i for i in issues if i["status"] == status),
                       key=lambda i: (sev[i["severity"]], i["id"]))
        if not group:
            continue
        lines += [f"## {label}", ""]
        for i in group:
            lines += [f"### {i['id']} · {i['title']}", "",
                      f"- **Area:** {i['area']} · **Gravita':** {i['severity']} · "
                      f"**Visto:** {i['first_seen']} → {i['last_seen']}",
                      f"- **Macchine:** {', '.join(i['machines']) or '—'}",
                      f"- **Prove:** {i['evidence']}",
                      f"- **Ipotesi:** {i['hypothesis']}",
                      f"- **Proposta:** {i['proposal']}"]
            if i.get("known_issue"):
                lines.append(f"- **Gia' noto:** {i['known_issue']}")
            lines.append("")
    return "\n".join(lines)


def run(send: bool = True) -> dict:
    from . import notify

    ctx, issues = build_context()
    result, usage = analyze(ctx, issues)
    today = datetime.now(ROME).strftime("%Y-%m-%d")

    cfg.STATE_DIR.mkdir(parents=True, exist_ok=True)
    cfg.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    ISSUES_STATE.write_text(json.dumps(result["issues"], ensure_ascii=False, indent=1), encoding="utf-8")
    ISSUES_MD.write_text(render_issues_md(result["issues"]), encoding="utf-8")
    report = result["report_markdown"] + f"\n\n---\n_Analisi {MODEL}, costo stimato {usage['cost_usd']} $_\n"
    (cfg.REPORTS_DIR / f"{today}.md").write_text(report, encoding="utf-8")
    log = _load_json(DAILY_LOG, [])
    log.append({"date": today, "summary": result["telegram_summary"], "usage": usage})
    DAILY_LOG.write_text(json.dumps(log[-30:], ensure_ascii=False, indent=1), encoding="utf-8")

    if send:
        n_open = sum(1 for i in result["issues"] if i["status"] == "open")
        notify.email(f"[CGSLIM Flotta] Report {datetime.now(ROME):%d/%m} · {n_open} problemi aperti",
                     report, _html(report))
        notify.telegram("📋 <b>Report flotta</b>\n" + notify.esc(result["telegram_summary"])
                        + "\n\n<i>Dettagli via email</i>")
    return usage


def _html(text: str) -> str:
    body = md.markdown(text, extensions=["tables", "sane_lists"])
    return ("<html><body style=\"font-family:-apple-system,Segoe UI,sans-serif;font-size:15px;"
            "line-height:1.45;max-width:760px\">" + body + "</body></html>")
