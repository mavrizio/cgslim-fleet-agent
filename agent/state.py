"""Memoria degli avvisi tra un giro e l'altro (state/alerts.json).

Decide cosa mandare: nuovo problema, critico ancora aperto da ripetere,
problema risolto. Gli eventi puntuali (flash fallito, eccezione...) non
"si risolvono": escono dalla finestra e basta, senza messaggio di chiusura.
"""
import json
import os
from datetime import datetime, timedelta, timezone

from . import config as cfg
from .checks import EVENT_RULES, Finding

STATE_FILE = cfg.STATE_DIR / "alerts.json"
POINT_EVENTS = set(EVENT_RULES) | {"exception"}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def load() -> dict:
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {"open": {}, "history": []}


def save(state: dict) -> None:
    cfg.STATE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    os.replace(tmp, STATE_FILE)


def diff(state: dict, findings: list[Finding]) -> tuple[list[Finding], list[Finding], list[dict]]:
    """Ritorna (nuovi da avvisare, critici da ripetere, risolti) e aggiorna state."""
    now = _now()
    open_ = state.setdefault("open", {})
    history = state.setdefault("history", [])
    current = {f.key: f for f in findings}

    new, repeat = [], []
    for key, f in current.items():
        rec = open_.get(key)
        if rec is None:
            open_[key] = {"rule": f.rule, "severity": f.severity, "device_id": f.device_id,
                          "title": f.title, "detail": f.detail, "first_seen": now.isoformat(),
                          "last_seen": now.isoformat(), "last_sent": None}
            if f.severity in ("crit", "warn"):
                new.append(f)
                open_[key]["last_sent"] = now.isoformat()
            continue
        rec.update(last_seen=now.isoformat(), title=f.title, detail=f.detail)
        escalated = f.severity == "crit" and rec["severity"] != "crit"
        rec["severity"] = f.severity
        last_sent = datetime.fromisoformat(rec["last_sent"]) if rec.get("last_sent") else None
        if escalated or (f.severity == "crit" and
                         (last_sent is None or now - last_sent > timedelta(hours=cfg.RENOTIFY_HOURS))):
            repeat.append(f)
            rec["last_sent"] = now.isoformat()

    resolved = []
    for key in list(open_):
        if key in current:
            continue
        rec = open_.pop(key)
        rec["resolved_at"] = now.isoformat()
        history.append(rec)
        if rec["rule"] not in POINT_EVENTS and rec.get("last_sent"):
            resolved.append(rec)
    # storico per il report giornaliero: ultimi 14 giorni
    cutoff = (now - timedelta(days=14)).isoformat()
    state["history"] = [h for h in history if h.get("resolved_at", "") > cutoff]
    return new, repeat, resolved
