"""cgslim-agent: controllo della flotta CGSLIM.

  python -m agent.cli check [--dry-run]   livello 1, ogni 15 min (timer systemd)
  python -m agent.cli status              stampa i problemi aperti adesso, senza inviare
  python -m agent.cli telegram-chat-id    legge il chat_id dopo /start al bot
  python -m agent.cli daily [--no-send] [--force]  livello 2, report giornaliero con Claude (timer 10:00)
"""
import argparse
import json
import subprocess
import sys
import urllib.request

from . import checks, db, notify, state
from .config import env

ICON = {"crit": "🔴", "warn": "🟠", "info": "⚪"}
CHECK_WINDOW_H = 0.5  # eventi puntuali: un po' piu' del passo del timer, il doppione lo toglie state


def _fmt(f: checks.Finding) -> str:
    line = f"{ICON[f.severity]} <b>{notify.esc(f.title)}</b>"
    if f.detail:
        line += f"\n    {notify.esc(f.detail)}"
    if f.data.get("devices"):
        line += f"\n    <i>{notify.esc(', '.join(f.data['devices']))}</i>"
    return line


def cmd_check(args) -> int:
    with db.connect() as conn:
        devices = db.devices(conn)
        events = db.events(conn, hours=6)
    devices, events = checks.production_only(devices, events)
    findings = checks.run_all(devices, events, CHECK_WINDOW_H)
    st = state.load()
    new, repeat, resolved = state.diff(st, findings)

    parts = []
    if new:
        parts.append("<b>Nuovi problemi</b>\n" + "\n".join(_fmt(f) for f in new))
    if repeat:
        parts.append("<b>Ancora aperti</b>\n" + "\n".join(_fmt(f) for f in repeat))
    if resolved:
        parts.append("<b>Risolti</b>\n" + "\n".join(f"✅ {notify.esc(r['title'])}" for r in resolved))
    online = sum(1 for d in devices if d["age_s"] < 35 * 60)
    msg = f"🛠 <b>Flotta CGSLIM</b> · {online}/{len(devices)} online\n\n" + "\n\n".join(parts) if parts else ""

    if args.dry_run:
        print(msg or "(niente da inviare)")
        print(f"\n[dry-run] aperti: {len(findings)}, nuovi {len(new)}, ripetuti {len(repeat)}, risolti {len(resolved)}")
        return 0
    if msg:
        notify.telegram(msg)
    state.save(st)  # dopo l'invio: se Telegram fallisce, il prossimo giro ritenta
    return 0


def cmd_status(args) -> int:
    with db.connect() as conn:
        devices = db.devices(conn)
        events = db.events(conn, hours=24)
    devices, events = checks.production_only(devices, events)
    findings = checks.run_all(devices, events, 24)
    online = sum(1 for d in devices if d["age_s"] < 35 * 60)
    print(f"Macchine {len(devices)}, online {online}, problemi {len(findings)}\n")
    for f in findings:
        print(f"{ICON[f.severity]} {f.title}" + (f"\n     {f.detail}" if f.detail else "")
              + (f"\n     {', '.join(f.data['devices'])}" if f.data.get("devices") else ""))
    return 0


def cmd_chat_id(args) -> int:
    url = f"https://api.telegram.org/bot{env('TELEGRAM_BOT_TOKEN')}/getUpdates"
    with urllib.request.urlopen(url, timeout=20) as r:
        updates = json.load(r).get("result", [])
    chats = {(u.get("message") or {}).get("chat", {}).get("id"): (u.get("message") or {}).get("chat", {})
             for u in updates if u.get("message")}
    if not chats:
        print("Nessun messaggio: scrivi /start al bot e riprova")
        return 1
    for cid, chat in chats.items():
        print(cid, chat.get("username") or chat.get("title") or chat.get("first_name"))
    return 0


def cmd_daily(args) -> int:
    from . import daily
    from .config import ROOT

    usage = daily.run(send=not args.no_send, force=args.force)
    print(f"report fatto: {usage}")
    # il registro va nel repo: e' cosi' che arriva allo sviluppo
    git = ["git", "-C", str(ROOT)]
    subprocess.run(git + ["add", "ISSUES.md", "reports"], check=True)
    if subprocess.run(git + ["diff", "--cached", "--quiet"]).returncode:
        subprocess.run(git + ["commit", "-q", "-m", "Report giornaliero e registro problemi"], check=True)
        subprocess.run(git + ["push", "-q", "origin", "main"], check=True)
    return 0


def main() -> int:
    p = argparse.ArgumentParser(prog="cgslim-agent")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("--dry-run", action="store_true")
    c.set_defaults(fn=cmd_check)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    sub.add_parser("telegram-chat-id").set_defaults(fn=cmd_chat_id)
    d = sub.add_parser("daily")
    d.add_argument("--no-send", action="store_true", help="scrive report e registro senza inviarli")
    d.add_argument("--force", action="store_true", help="analisi con Claude anche senza novita'")
    d.set_defaults(fn=cmd_daily)
    args = p.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
