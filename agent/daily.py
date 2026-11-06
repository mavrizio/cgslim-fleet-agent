"""Livello 2: report giornaliero.

Due parti:
- lo script calcola numeri e tabelle (stato flotta, avvisi, pagamenti, eventi): gratis
- Claude scrive solo l'analisi e le modifiche al registro dei problemi, e solo
  nei giorni con novita' (piu' un giro di controllo settimanale). La richiesta
  passa dalla Batch API (meta' prezzo); se fallisce si ripiega sulla chiamata diretta.
Il registro diventa ISSUES.md nel repo: e' il canale verso lo sviluppo.
"""
import json
import re
import time
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import anthropic
import markdown as md

from . import checks, db, state
from . import config as cfg

ROME = ZoneInfo("Europe/Rome")
MODEL = "claude-opus-5-5"
EFFORT = "medium"
PRICE_IN, PRICE_OUT = 4.0, 20.0           # $/MTok, claude-opus-5-5
BATCH_POLL_S, BATCH_MAX_WAIT_S = 30, 3 * 3600
WEEKLY_REVIEW_DAY = 0                      # lunedi': analisi anche senza novita'
ISSUES_STATE = cfg.ROOT / "data" / "issues.json"  # nel repo: il registro non deve vivere solo sul server
ISSUES_MD = cfg.ROOT / "ISSUES.md"
ISSUES_URL = "https://github.com/mavrizio/cgslim-fleet-agent/blob/main/ISSUES.md"
DAILY_LOG = cfg.STATE_DIR / "daily_log.json"

# Eventi che da soli giustificano l'analisi (reboot e cambi versione sono la normalita')
NOTABLE_EVENTS = {"exception", "app_down", "serial_missing", "serial_recovery_exhausted",
                  "gmi_flash_failed", "update_failed", "device_key_enrolled", "first_seen"}

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
   Restituisci SOLO le voci nuove o cambiate (stato, macchine, prove, ipotesi, proposta),
   complete in tutti i campi; le voci che restituisci sostituiscono quelle con lo stesso id.
   Per le voci nuove usa gli id a partire da quello indicato. Chiudi (resolved) una voce solo
   se i dati mostrano che il problema e' sparito; "monitoring" se oggi non si e' ripresentato
   ma e' presto per chiuderla.
4. Distinguere fatti e ipotesi. Ogni affermazione sulle macchine deve venire dai dati forniti;
   cita MHD (senza zeri iniziali), orari e numeri. Se un dato manca, dillo.

I numeri (stato flotta, versioni, pagamenti, conteggio eventi) li mette gia' lo script nel
report: non ripeterli. La tua parte del report (markdown) ha solo tre sezioni brevi:
"In breve" (3-5 righe), "Da fare oggi" (azioni concrete, chi le fa), "Novita' rispetto a ieri".
Il riassunto Telegram: massimo 5 righe di testo semplice, la prima con il conteggio online."""

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
        "analysis_markdown": {"type": "string"},
        "issue_updates": {"type": "array", "items": ISSUE_SCHEMA},
    },
    "required": ["telegram_summary", "analysis_markdown", "issue_updates"],
    "additionalProperties": False,
}


def _load_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def _ts(dt) -> str | None:
    return dt.astimezone(ROME).strftime("%d/%m %H:%M") if dt else None


def _count(values) -> dict:
    out = {}
    for v in values:
        out[v or "?"] = out.get(v or "?", 0) + 1
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))


# --- raccolta dati ------------------------------------------------------------

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
    since = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
    ctx = {
        "now": datetime.now(ROME).strftime("%Y-%m-%d %H:%M %A"),
        "fleet": {"machines": len(devices),
                  "online": sum(1 for d in devices if d["age_s"] < 35 * 60),
                  "app_versions": _count(d.get("app_version") for d in devices),
                  "fw_versions": _count(d.get("fw_version") for d in devices),
                  "branches": _count(d.get("git_branch") for d in devices)},
        "level1_open_alerts": list(alerts.get("open", {}).values()),
        "level1_resolved_24h": [h for h in alerts.get("history", []) if h.get("resolved_at", "") > since],
        "devices": [_device_view(d) for d in devices],
        "events_24h": [_event_view(e, names) for e in events],
        "transactions_24h_by_machine": _trx_summary(trx),
        "config_changes_24h": [{k: str(v) for k, v in c.items()} for c in changes],
        "previous_reports": _load_json(DAILY_LOG, [])[-3:],
        "next_issue_id": f"CG-{(max(nums) if nums else 0) + 1:03d}",
    }
    return ctx, issues


# --- parte calcolata dallo script ------------------------------------------------

def scripted_report(ctx: dict, issues: list[dict]) -> str:
    f = ctx["fleet"]
    fmt = lambda counts: ", ".join(f"{k} ×{v}" for k, v in counts.items())
    offline = [d for d in ctx["devices"] if d["offline_min"]]
    out = ["## Stato flotta", "",
           f"- **Macchine:** {f['machines']}, online {f['online']}"
           + (f" · offline: {', '.join(d['mhd'] + ' (dal ' + d['last_seen'] + ')' for d in offline)}" if offline else ""),
           f"- **App:** {fmt(f['app_versions'])}",
           f"- **Firmware:** {fmt(f['fw_versions'])}",
           f"- **Branch:** {fmt(f['branches'])}", ""]

    alerts = sorted(ctx["level1_open_alerts"], key=lambda a: checks.SEVERITY_ORDER.get(a["severity"], 9))
    if alerts:
        icon = {"crit": "🔴", "warn": "🟠", "info": "⚪"}
        out += ["## Avvisi aperti (controlli ogni 15 min)", ""]
        out += [f"- {icon.get(a['severity'], '')} {a['title']}" + (f" — {a['detail']}" if a.get("detail") else "")
                for a in alerts]
        out.append("")

    trx = ctx["transactions_24h_by_machine"]
    if trx:
        tot = _count(o for t in trx for o, n in t["outcomes"].items() for _ in range(n))
        meth = _count(m for t in trx for m, n in t["methods"].items() for _ in range(n))
        out += ["## Pagamenti ultime 24 h", "",
                f"Totale {sum(t['n'] for t in trx)} · esiti: {fmt(tot)} · metodi: {fmt(meth)}", "",
                "| MHD | Op. | Esiti | Metodi | Ultima approvata |", "|---|---|---|---|---|"]
        out += [f"| {t['mhd']} | {t['n']} | {fmt(t['outcomes'])} | {fmt(t['methods'])} | {t['last_approved'] or '—'} |"
                for t in trx]
        out.append("")

    ev = ctx["events_24h"]
    if ev:
        kinds = _count(e["kind"] for e in ev)
        out += ["## Eventi ultime 24 h", "", fmt(kinds), ""]

    open_issues = [i for i in issues if i["status"] != "resolved"]
    if open_issues:
        out += ["## Registro problemi", ""]
        out += [f"- **{i['id']}** ({i['status']}, {i['severity']}, {i['area']}) {i['title']}" for i in open_issues]
        out.append("")
    return "\n".join(out)


def notable_reasons(ctx: dict, issues: list[dict]) -> list[str]:
    """Motivi per scomodare Claude oggi. Vuoto = giornata tranquilla."""
    since = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
    reasons = []
    if not issues:
        reasons.append("registro vuoto")
    new_alerts = [a for a in ctx["level1_open_alerts"]
                  if a.get("first_seen", "") > since and a["severity"] in ("crit", "warn")]
    if new_alerts:
        reasons.append(f"{len(new_alerts)} avvisi nuovi")
    if ctx["level1_resolved_24h"]:
        reasons.append(f"{len(ctx['level1_resolved_24h'])} avvisi chiusi")
    ev = _count(e["kind"] for e in ctx["events_24h"] if e["kind"] in NOTABLE_EVENTS)
    if ev:
        reasons.append("eventi: " + ", ".join(f"{k} ×{v}" for k, v in ev.items()))
    if datetime.now(ROME).weekday() == WEEKLY_REVIEW_DAY:
        reasons.append("revisione settimanale")
    return reasons


# --- parte di Claude ------------------------------------------------------------

def _request_params(ctx: dict, issues: list[dict]) -> dict:
    knowledge = (cfg.KNOWLEDGE_DIR / "KNOWLEDGE.md").read_text(encoding="utf-8")
    return {
        "model": MODEL,
        "max_tokens": 32000,
        "thinking": {"type": "adaptive"},
        "output_config": {"effort": EFFORT, "format": {"type": "json_schema", "schema": OUTPUT_SCHEMA}},
        "system": [{"type": "text", "text": SYSTEM},
                   {"type": "text", "text": "# Scheda di conoscenza\n\n" + knowledge}],
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": "# Registro dei problemi attuale\n\n"
             + json.dumps(issues, ensure_ascii=False, indent=1)},
            {"type": "text", "text": "# Dati di oggi\n\n" + json.dumps(ctx, ensure_ascii=False, default=str)},
            {"type": "text", "text": "Analizza i dati di oggi: riassunto Telegram, la tua parte del report "
             "e le sole voci del registro nuove o cambiate."},
        ]}],
    }


def _parse(msg) -> dict:
    if msg.stop_reason == "refusal":
        raise RuntimeError(f"rifiuto: {getattr(msg, 'stop_details', None)}")
    if msg.stop_reason == "max_tokens":
        raise RuntimeError("risposta troncata (max_tokens)")
    return json.loads(next(b.text for b in msg.content if b.type == "text"))


def _usage(msg, discount: float) -> dict:
    u = msg.usage
    cost = (u.input_tokens * PRICE_IN + u.output_tokens * PRICE_OUT) / 1e6 * discount
    return {"input": u.input_tokens, "output": u.output_tokens, "cost_usd": round(cost, 3)}


def analyze(ctx: dict, issues: list[dict]) -> tuple[dict, dict]:
    client = anthropic.Anthropic()
    params = _request_params(ctx, issues)
    try:
        batch = client.messages.batches.create(requests=[{"custom_id": "daily", "params": params}])
        deadline = time.monotonic() + BATCH_MAX_WAIT_S
        while batch.processing_status != "ended":
            if time.monotonic() > deadline:
                client.messages.batches.cancel(batch.id)
                raise TimeoutError(f"batch {batch.id} non finito in {BATCH_MAX_WAIT_S // 3600} h")
            time.sleep(BATCH_POLL_S)
            batch = client.messages.batches.retrieve(batch.id)
        result = next(iter(client.messages.batches.results(batch.id))).result
        if result.type != "succeeded":
            raise RuntimeError(f"batch {result.type}")
        msg = result.message
        out = _parse(msg)
        return out, _usage(msg, 0.5) | {"mode": "batch"}
    except Exception as e:  # ripiego: chiamata diretta, con fallback lato server sui rifiuti
        print(f"batch fallito ({e}), chiamata diretta")
    with client.beta.messages.stream(**params, betas=["server-side-fallback-2026-07-01"],
                                     fallbacks="default") as stream:
        msg = stream.get_final_message()
    return _parse(msg), _usage(msg, 1.0) | {"mode": "direct"}


def merge_issues(issues: list[dict], updates: list[dict]) -> list[dict]:
    by_id = {i["id"]: i for i in issues}
    for u in updates:
        by_id[u["id"]] = u
    return sorted(by_id.values(), key=lambda i: i["id"])


def render_issues_md(issues: list[dict]) -> str:
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
            # ancora esplicita: il link dalla mail non dipende dal titolo, che cambia
            lines += [f'<a id="{i["id"].lower()}"></a>', "",
                      f"### {i['id']} · {i['title']}", "",
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


def link_issues(text: str, issues: list[dict]) -> str:
    """Ogni CG-NNN del registro diventa un link alla sua voce in ISSUES.md su GitHub."""
    known = {i["id"] for i in issues}

    def repl(m):
        code = m.group(0)
        return f"[{code}]({ISSUES_URL}#{code.lower()})" if code in known else code

    # non tocca i codici gia' dentro un link [..](..)
    return re.sub(r"(?<!\[)\bCG-\d{3}\b(?!\])", repl, text)


# --- giro completo ---------------------------------------------------------------

def run(send: bool = True, force: bool = False) -> dict:
    from . import notify

    ctx, issues = build_context()
    today = datetime.now(ROME).strftime("%Y-%m-%d")
    reasons = notable_reasons(ctx, issues)

    if reasons or force:
        result, usage = analyze(ctx, issues)
        issues = merge_issues(issues, result["issue_updates"])
        analysis, summary = result["analysis_markdown"], result["telegram_summary"]
        footer = (f"_Analisi {MODEL} ({usage['mode']}, effort {EFFORT}) per: {'; '.join(reasons) or 'richiesta'}"
                  f" · {len(result['issue_updates'])} voci aggiornate · costo stimato {usage['cost_usd']} $_")
    else:
        usage = {"mode": "skipped", "cost_usd": 0}
        f = ctx["fleet"]
        summary = (f"{f['online']}/{f['machines']} online. Nessuna novita' nelle ultime 24 h: "
                   "analisi saltata, solo report calcolato.")
        analysis = "## In breve\n\nNessuna novita' nelle ultime 24 h: nessun avviso nuovo, nessun evento anomalo."
        footer = "_Analisi saltata (giornata tranquilla), costo 0 $_"

    report = link_issues(f"# Report flotta CGSLIM · {datetime.now(ROME):%d/%m/%Y}\n\n{analysis}\n\n"
                         f"{scripted_report(ctx, issues)}\n---\n{footer}\n", issues)

    cfg.STATE_DIR.mkdir(parents=True, exist_ok=True)
    cfg.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    ISSUES_STATE.parent.mkdir(parents=True, exist_ok=True)
    ISSUES_STATE.write_text(json.dumps(issues, ensure_ascii=False, indent=1), encoding="utf-8")
    ISSUES_MD.write_text(render_issues_md(issues), encoding="utf-8")
    (cfg.REPORTS_DIR / f"{today}.md").write_text(report, encoding="utf-8")
    log = _load_json(DAILY_LOG, [])
    log.append({"date": today, "summary": summary, "reasons": reasons, "usage": usage})
    DAILY_LOG.write_text(json.dumps(log[-30:], ensure_ascii=False, indent=1), encoding="utf-8")

    if send:
        n_open = sum(1 for i in issues if i["status"] == "open")
        notify.email(f"[CGSLIM Flotta] Report {datetime.now(ROME):%d/%m} · {n_open} problemi aperti",
                     report, _html(report))
        notify.telegram("📋 <b>Report flotta</b>\n" + notify.esc(summary) + "\n\n<i>Dettagli via email</i>")
    return usage


def _html(text: str) -> str:
    body = md.markdown(text, extensions=["tables", "sane_lists"])
    return ("<html><body style=\"font-family:-apple-system,Segoe UI,sans-serif;font-size:15px;"
            "line-height:1.45;max-width:760px\">" + body + "</body></html>")
