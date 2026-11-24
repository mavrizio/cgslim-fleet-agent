"""Note di Maurizio per l'agente: spiegazioni, giustificazioni, correzioni.

Una nota = un file notes/N<numero>.json nel repo, cosi' si scrivono sia dal
server (messaggi Telegram al bot) sia dal Mac (commit e push) senza conflitti.
Il report giornaliero passa a Claude le note attive: valgono piu' delle sue
ipotesi. Claude risponde a ogni nota nuova e la archivia quando non serve piu'.

Da Telegram (solo dalla chat in TELEGRAM_CHAT_ID):
  testo libero              nota; CG-NNN e MHD nel testo la collegano
  rispondere a un messaggio del bot   nota collegata alla voce/macchina di quel messaggio
  /nota testo               come il testo libero
  /note [CG-NNN|MHD]        note attive
  /togli N                  archivia la nota N
  /aiuto                    i comandi

Dal Mac, senza .env ne' librerie:
  python3 -m agent.notes add "testo" [--issue CG-003] [--mhd 24350]
  python3 -m agent.notes list [--all]
  python3 -m agent.notes done N12
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

from . import config as cfg

ROME = ZoneInfo("Europe/Rome")
NOTES_DIR = cfg.ROOT / "notes"
OFFSET_FILE = cfg.STATE_DIR / "telegram_offset"
ISSUE_RE = re.compile(r"\bCG-\d{3}\b", re.IGNORECASE)
# MHD: 5-8 cifre isolate (gli zeri iniziali si tolgono); non prende versioni, orari, importi
MHD_RE = re.compile(r"(?<![\w.,/-])0*(\d{5,8})(?!\w|[.,:/-]\w)")

HELP = ("Scrivimi una nota e la uso nel prossimo report.\n"
        "• testo libero: nota; se dentro c'e' CG-003 o un MHD (24350) la collego\n"
        "• rispondi a un mio messaggio: la collego a quella voce o macchina\n"
        "• /note: note attive · /note CG-003 · /note 24350\n"
        "• /togli 12: archivia la nota N12\n"
        "Esempi: «CG-005 24254: cambiato alimentatore il 25/11» · "
        "«37008 e' in officina fino al 1/12, non segnalarla» · «chiudi CG-014, risolto col fw 4.20.98»")


def _now() -> datetime:
    return datetime.now(ROME)


# --- archivio -------------------------------------------------------------------

def _path(note_id: str):
    return NOTES_DIR / f"{note_id}.json"


def load_all() -> list[dict]:
    out = []
    for p in NOTES_DIR.glob("N*.json"):
        try:
            out.append(json.loads(p.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            print(f"nota illeggibile: {p.name}", file=sys.stderr)
    return sorted(out, key=lambda n: int(n["id"][1:]))


def active() -> list[dict]:
    return [n for n in load_all() if n.get("status") == "active"]


def save(note: dict) -> None:
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    p = _path(note["id"])
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(note, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    os.replace(tmp, p)


def get(note_id: str) -> dict | None:
    try:
        return json.loads(_path(note_id).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None


def normalize_id(raw: str) -> str | None:
    m = re.fullmatch(r"[Nn]?(\d+)", raw.strip())
    return f"N{int(m.group(1))}" if m else None


def links(text: str) -> tuple[list[str], list[str]]:
    issues = sorted({m.upper() for m in ISSUE_RE.findall(text)})
    mhds = sorted({m for m in MHD_RE.findall(ISSUE_RE.sub(" ", text))}, key=int)
    return issues, mhds


def add(text: str, source: str, issues=(), machines=()) -> dict:
    nums = [int(n["id"][1:]) for n in load_all()]
    note = {"id": f"N{max(nums, default=0) + 1}", "created": _now().isoformat(timespec="minutes"),
            "source": source, "issues": list(issues), "machines": list(machines),
            "text": text.strip(), "status": "active",
            "reply": None, "reply_date": None, "closed": None, "closed_by": None}
    save(note)
    return note


def close(note_id: str, by: str) -> dict | None:
    note = get(note_id)
    if note and note["status"] == "active":
        note.update(status="done", closed=_now().isoformat(timespec="minutes"), closed_by=by)
        save(note)
    return note


def label(n: dict) -> str:
    tags = n["issues"] + n["machines"]
    return f"{n['id']} ({n['created'][:10]}{', ' + ', '.join(tags) if tags else ''})"


# --- per il report giornaliero ------------------------------------------------------

def for_prompt(notes: list[dict]) -> list[dict]:
    return [{k: n[k] for k in ("id", "created", "issues", "machines", "text", "reply")} for n in notes]


def apply_replies(replies: list[dict]) -> list[dict]:
    """Risposte di Claude: le salva sulle note; keep=false archivia. Ritorna quelle applicate."""
    done, today = [], _now().strftime("%Y-%m-%d")
    for r in replies:
        note = get(r["id"])
        if not note or note["status"] != "active":
            continue
        note.update(reply=r["reply"].strip(), reply_date=today)
        if not r["keep"]:
            note.update(status="done", closed=_now().isoformat(timespec="minutes"), closed_by="agente")
        save(note)
        done.append(note)
    return done


# --- Telegram ---------------------------------------------------------------------

def _tg(method: str, **params) -> dict:
    url = f"https://api.telegram.org/bot{cfg.env('TELEGRAM_BOT_TOKEN')}/{method}"
    body = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None}).encode()
    with urllib.request.urlopen(urllib.request.Request(url, data=body), timeout=30) as r:
        return json.load(r)


def _reply(chat_id, text: str, to_msg=None) -> None:
    _tg("sendMessage", chat_id=chat_id, text=text[:4000], reply_to_message_id=to_msg,
        allow_sending_without_reply="true", disable_web_page_preview="true")


def _list_text(filter_: str | None) -> str:
    notes = active()
    if filter_:
        key = filter_.upper().lstrip("0") if not filter_.upper().startswith("CG-") else filter_.upper()
        notes = [n for n in notes if key in n["issues"] or key in n["machines"]]
    if not notes:
        return "Nessuna nota attiva" + (f" su {filter_}" if filter_ else "") + "."
    lines = []
    for n in notes:
        lines.append(f"• {label(n)}: {n['text']}")
        if n.get("reply"):
            lines.append(f"   ↳ agente {n['reply_date']}: {n['reply']}")
    return "\n".join(lines)


def handle_message(msg: dict) -> str | None:
    """Un messaggio dalla chat autorizzata -> testo della risposta del bot."""
    text = (msg.get("text") or "").strip()
    if not text:
        return "Leggo solo testo: scrivimi la nota a parole."
    cmd, _, rest = text.partition(" ")
    cmd = cmd.split("@")[0].lower()
    if cmd.startswith("/"):
        if cmd in ("/start", "/aiuto", "/help"):
            return HELP
        if cmd == "/note":
            return _list_text(rest.strip() or None)
        if cmd == "/togli":
            nid = normalize_id(rest)
            if not nid:
                return "Scrivi il numero: /togli 12"
            note = get(nid)
            if not note:
                return f"{nid} non esiste."
            if note["status"] != "active":
                return f"{nid} era gia' archiviata."
            close(nid, "maurizio")
            return f"🗑 {nid} archiviata: dal prossimo report non la uso piu'."
        if cmd != "/nota":
            return "Comando sconosciuto.\n\n" + HELP
        text = rest.strip()
        if not text:
            return "Scrivi il testo dopo /nota."

    issues, machines = links(text)
    replied = (msg.get("reply_to_message") or {})
    if replied and not (issues or machines):
        # risposta a un messaggio del bot: lo collego solo se li' c'e' una voce o una macchina sola
        r_text = replied.get("text") or ""
        r_issues, r_machines = links(r_text)
        if len(r_issues) == 1:
            issues = r_issues
        if len(r_machines) == 1:
            machines = r_machines
    note = add(text, "telegram", issues, machines)
    where = ", ".join(issues + machines) or "nessuna voce o macchina (nota generale)"
    return (f"📝 {note['id']} salvata · {where}\n"
            f"La uso nel prossimo report (alle 10:00) e ti rispondo li'. Per toglierla: /togli {note['id'][1:]}")


def poll_telegram() -> int:
    """Legge i messaggi nuovi al bot. Ritorna quante note sono cambiate."""
    chat = str(cfg.env("TELEGRAM_CHAT_ID"))
    if not cfg.env("TELEGRAM_BOT_TOKEN") or not chat:
        raise RuntimeError("TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID mancanti in .env")
    try:
        offset = int(OFFSET_FILE.read_text().strip())
    except (FileNotFoundError, ValueError):
        offset = None
    res = _tg("getUpdates", offset=offset, timeout=0, allowed_updates='["message"]')
    changed = 0
    for u in res.get("result", []):
        msg = u.get("message") or {}
        # avanzo prima di rispondere: un messaggio che fa fallire il giro non deve ripetersi all'infinito
        cfg.STATE_DIR.mkdir(parents=True, exist_ok=True)
        OFFSET_FILE.write_text(str(u["update_id"] + 1))
        if str((msg.get("chat") or {}).get("id")) != chat:
            continue  # solo la chat della flotta
        try:
            answer = handle_message(msg)
            changed += 1
        except Exception as e:  # la nota non deve far saltare le altre
            answer = f"⚠️ Nota non salvata: {e}"
        if answer:
            _reply(chat, answer, msg.get("message_id"))
    return changed


# --- uso dal Mac ------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(prog="agent.notes", description="Note per l'agente della flotta")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("text")
    a.add_argument("--issue", action="append", default=[])
    a.add_argument("--mhd", action="append", default=[])
    ls = sub.add_parser("list")
    ls.add_argument("--all", action="store_true")
    d = sub.add_parser("done")
    d.add_argument("id")
    args = p.parse_args()

    if args.cmd == "add":
        issues, machines = links(args.text)
        issues = sorted(set(issues) | {i.upper() for i in args.issue})
        machines = sorted(set(machines) | {m.lstrip("0") for m in args.mhd}, key=int)
        n = add(args.text, "mac", issues, machines)
        print(f"{label(n)} salvata in notes/{n['id']}.json: commit e push per mandarla al server")
    elif args.cmd == "list":
        for n in (load_all() if args.all else active()):
            print(f"{label(n)} [{n['status']}] {n['text']}" + (f"\n    ↳ {n['reply']}" if n.get("reply") else ""))
    else:
        nid = normalize_id(args.id)
        n = close(nid, "maurizio") if nid else None
        print(f"{nid} archiviata" if n else f"{args.id}: non trovata")
    return 0


if __name__ == "__main__":
    sys.exit(main())
