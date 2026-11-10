"""Livello 1: regole deterministiche sullo stato della flotta.

Ogni regola produce Finding con una chiave stabile (regola + macchina): la
stessa chiave tra un giro e l'altro e' lo stesso problema ancora aperto.
Severita':
  crit  Telegram subito, ripetuto ogni RENOTIFY_HOURS finche' resta aperto
  warn  Telegram subito una volta, poi solo nel report giornaliero
  info  solo nel report giornaliero
"""
import json
import re
import subprocess
import zlib
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from . import config as cfg

ROME = ZoneInfo("Europe/Rome")

SEVERITY_ORDER = {"crit": 0, "warn": 1, "info": 2}

# Eventi del reporter che da soli meritano un avviso
EVENT_RULES = {
    "gmi_flash_failed": ("warn", "Aggiornamento firmware GMI fallito"),
    "serial_recovery_exhausted": ("crit", "Seriale GMI persa, recupero esaurito"),
    "app_down": ("warn", "App main.py giu'"),
    # MOD10 tornello: l'hopper non ha dato tutto il resto, il cliente e' entrato lo stesso
    "gate_short_change": ("warn", "Tornello: resto non completato, rifornire l'hopper"),
}


@dataclass
class Finding:
    rule: str
    severity: str
    device_id: str | None
    title: str
    detail: str = ""
    data: dict = field(default_factory=dict)

    @property
    def key(self) -> str:
        if self.device_id is None:  # problemi di flotta: distinti per messaggio
            return f"{self.rule}:fleet:{zlib.crc32(self.detail.encode()):08x}"
        return f"{self.rule}:{self.device_id}"


def machine_name(d: dict) -> str:
    """MHD senza zeri + centro/etichetta: come la chiamano i tecnici."""
    mhd = (d.get("mhd") or "").lstrip("0") or d["device_id"][-8:]
    where = d.get("label") or d.get("center") or d.get("location") or ""
    return f"{mhd} {where}".strip()


def _normalize(msg: str) -> str:
    """Toglie buffer, numeri ed esadecimali: stesse eccezioni = stesso messaggio."""
    msg = re.sub(r"b'[^']*'(\.\.\.)?", "b'…'", msg)
    msg = re.sub(r"0x[0-9a-fA-F]+|\d+", "N", msg)
    return msg[:140]


def _active_hours() -> bool:
    start, end = cfg.ACTIVE_HOURS
    return start <= datetime.now(ROME).hour < end


def _hours_ago(h: float) -> datetime:
    return datetime.now(timezone.utc) - timedelta(hours=h)


def check_devices(devices: list[dict]) -> list[Finding]:
    out: list[Finding] = []
    for d in devices:
        did, name, st = d["device_id"], machine_name(d), d.get("status") or {}
        rt, host = st.get("runtime") or {}, st.get("host") or {}
        age_min = d["age_s"] / 60

        if age_min > cfg.OFFLINE_WARN_MIN:
            sev = "crit" if age_min > cfg.OFFLINE_CRIT_HOURS * 60 else "warn"
            if not _active_hours():
                sev = "info"  # di notte e' spenta per scelta del centro
            last = d["last_seen"].astimezone().strftime("%d/%m %H:%M")
            out.append(Finding("offline", sev, did, f"{name}: offline", f"ultimo report {last}"))
            continue  # il resto dello stato e' vecchio: inutile valutarlo

        if d.get("app_running") is False:
            out.append(Finding("app_not_running", "crit", did, f"{name}: app ferma",
                               "il Pi risponde ma main.py non manda heartbeat"))
        elif rt.get("age_s") is not None and rt["age_s"] > cfg.RUNTIME_STALE_S:
            out.append(Finding("runtime_stale", "warn", did, f"{name}: heartbeat app vecchio",
                               f"runtime di {rt['age_s']} s fa"))

        if rt.get("serial_missing"):
            out.append(Finding("serial_missing", "crit", did, f"{name}: seriale GMI assente",
                               str(rt["serial_missing"])[:200]))
        blk = rt.get("gmi_blocked")
        if blk:
            if isinstance(blk, dict):
                since = datetime.fromtimestamp(blk["since"]).strftime("%d/%m %H:%M") if blk.get("since") else "?"
                detail = f"dal {since}, {blk.get('attempts', '?')} tentativi, {blk.get('firmware', '')}: {blk.get('error', '')}"
            else:
                detail = str(blk)
            out.append(Finding("gmi_blocked", "crit", did, f"{name}: GMI bloccata", detail[:200]))

        chl = rt.get("cashless") or {}
        if chl.get("chl_mode") and chl.get("p95_error"):
            out.append(Finding("pos_error", "warn", did, f"{name}: POS in errore",
                               str(chl["p95_error"])[:200]))

        thr = host.get("throttled")
        if thr:
            bits = int(str(thr), 16)
            if bits & 0x1:
                out.append(Finding("undervoltage_now", "warn", did, f"{name}: sottotensione ADESSO",
                                   f"throttled={thr}: alimentatore/cavo"))
            elif bits & 0x10000:
                out.append(Finding("undervoltage_past", "info", did, f"{name}: sottotensione dal boot",
                                   f"throttled={thr}"))

        temp = host.get("cpu_temp_c")
        if temp and temp > cfg.CPU_TEMP_WARN:
            out.append(Finding("cpu_hot", "warn", did, f"{name}: CPU a {temp:.0f} °C"))
        disk = host.get("disk_free_mb")
        if disk is not None and disk < cfg.DISK_FREE_WARN_MB:
            out.append(Finding("disk_low", "warn", did, f"{name}: disco quasi pieno", f"{disk} MB liberi"))
        skew = host.get("clock_skew_s")
        if skew and abs(skew) > cfg.CLOCK_SKEW_WARN_S:
            out.append(Finding("clock_skew", "info", did, f"{name}: orologio sfasato", f"{skew} s"))

        upd = (st.get("app") or {}).get("updater") or {}
        if upd and upd.get("ok") is False and (upd.get("failures") or 0) >= 3:
            out.append(Finding("updater_failing", "warn", did, f"{name}: aggiornamenti falliti",
                               f"{upd.get('failures')} di fila: {str(upd.get('error'))[:160]}"))

        if d.get("device_key_status") == "mismatch":
            out.append(Finding("device_key_mismatch", "warn", did, f"{name}: chiave macchina non corrisponde"))
    return out


def check_events(devices: list[dict], events: list[dict], window_h: float) -> list[Finding]:
    """window_h: eventi recenti da considerare (le tempeste usano finestre proprie)."""
    out: list[Finding] = []
    by_id = {d["device_id"]: d for d in devices}
    name = lambda did: machine_name(by_id[did]) if did in by_id else did[-8:]

    for kind, (n_min, hours) in (("reboot", cfg.REBOOT_STORM), ("app_restart", cfg.RESTART_STORM)):
        since = _hours_ago(hours)
        counts = Counter(e["device_id"] for e in events if e["kind"] == kind and e["received_at"] > since)
        for did, n in counts.items():
            if n >= n_min:
                label = "riavvii del Pi" if kind == "reboot" else "riavvii dell'app"
                out.append(Finding(f"{kind}_storm", "warn", did, f"{name(did)}: {n} {label} in {hours} h"))

    since = _hours_ago(window_h)
    for e in events:
        if e["received_at"] <= since or e["kind"] not in EVENT_RULES:
            continue
        sev, title = EVENT_RULES[e["kind"]]
        data = e.get("data") or {}
        detail = str(data.get("error") or data.get("case") or "")[:200]
        if e["kind"] == "gate_short_change":
            detail = f"resto {data.get('due', 0) / 100:.2f} euro, erogati {data.get('paid', 0) / 100:.2f}"
        out.append(Finding(e["kind"], sev, e["device_id"], f"{name(e['device_id'])}: {title}", detail))

    # eccezioni: raggruppate per messaggio, vanno al report (info)
    exc = defaultdict(set)
    for e in events:
        if e["kind"] == "exception" and e["received_at"] > since:
            exc[_normalize(str((e.get("data") or {}).get("message", "")))].add(e["device_id"])
    for msg, dids in exc.items():
        out.append(Finding("exception", "info", None, f"Eccezione su {len(dids)} macchine", msg,
                           {"devices": sorted(name(d) for d in dids)}))
    return out


def _group_widespread(found: list[Finding], min_devices: int = 3) -> list[Finding]:
    """Stesso problema con lo stesso dettaglio su molte macchine = un solo avviso di flotta."""
    groups = defaultdict(list)
    for f in found:
        if f.device_id and f.rule in GROUPABLE:
            groups[(f.rule, f.detail)].append(f)
    out = [f for f in found if not (f.device_id and f.rule in GROUPABLE
                                    and len(groups[(f.rule, f.detail)]) >= min_devices)]
    for (rule, detail), fs in groups.items():
        if len(fs) >= min_devices:
            names = sorted(f.title.split(":")[0] for f in fs)
            sev = min((f.severity for f in fs), key=SEVERITY_ORDER.get)
            out.append(Finding(rule, sev, None, f"{fs[0].title.split(': ', 1)[1]} su {len(fs)} macchine",
                               detail, {"devices": names}))
    return out


GROUPABLE = {"pos_error", "undervoltage_past", "gmi_flash_failed", "updater_failing", "app_down"}


def check_server() -> list[Finding]:
    """Salute del server di casa: Tailscale e' l'accesso da fuori (viaggi)."""
    try:
        out = subprocess.run(["tailscale", "status", "--json"], capture_output=True, text=True, timeout=15)
        st = json.loads(out.stdout or "{}").get("BackendState", "?")
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as e:
        st = f"errore: {e}"
    if st == "Running":
        return []
    return [Finding("server_tailscale", "crit", "server", "Server di casa: Tailscale non collegato",
                    f"stato {st}: da fuori casa il server non e' raggiungibile")]


def production_only(devices: list[dict], events: list[dict]) -> tuple[list[dict], list[dict]]:
    """Toglie le macchine di sviluppo/test e i loro eventi."""
    keep = [d for d in devices if not (d.get("mhd") or "").lstrip("0").startswith(cfg.EXCLUDED_MHD_PREFIXES)]
    ids = {d["device_id"] for d in keep}
    return keep, [e for e in events if e["device_id"] in ids]


def run_all(devices, events, window_h: float) -> list[Finding]:
    found = _group_widespread(check_devices(devices) + check_events(devices, events, window_h))
    # una sola Finding per chiave: tiene la piu' grave
    best: dict[str, Finding] = {}
    for f in found:
        if f.key not in best or SEVERITY_ORDER[f.severity] < SEVERITY_ORDER[best[f.key].severity]:
            best[f.key] = f
    return sorted(best.values(), key=lambda f: (SEVERITY_ORDER[f.severity], f.title))
