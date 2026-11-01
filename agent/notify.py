"""Uscite: Telegram (bot dedicato alla flotta) ed email (SMTP di memo_ingest)."""
import html
import json
import smtplib
import urllib.parse
import urllib.request
from email.message import EmailMessage

from .config import env

TELEGRAM_MAX = 4000  # il limite e' 4096: margine per i tag HTML


def telegram(text_html: str) -> None:
    token, chat = env("TELEGRAM_BOT_TOKEN"), env("TELEGRAM_CHAT_ID")
    if not token or not chat:
        raise RuntimeError("TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID mancanti in .env")
    # spezza per righe: un taglio a meta' di un tag HTML farebbe rifiutare il messaggio
    chunks, cur = [], ""
    for line in text_html.splitlines(keepends=True):
        if len(cur) + len(line) > TELEGRAM_MAX and cur:
            chunks.append(cur)
            cur = ""
        cur += line
    chunks.append(cur)
    for chunk in chunks:
        body = urllib.parse.urlencode({"chat_id": chat, "text": chunk, "parse_mode": "HTML",
                                       "disable_web_page_preview": "true"}).encode()
        req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage", data=body)
        with urllib.request.urlopen(req, timeout=20) as r:
            if not json.load(r).get("ok"):
                raise RuntimeError("Telegram ha rifiutato il messaggio")


def email(subject: str, text: str, html_body: str | None = None) -> None:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = env("SMTP_FROM") or env("SMTP_USER")
    msg["To"] = env("REPORT_EMAIL_TO")
    msg.set_content(text)
    if html_body:
        msg.add_alternative(html_body, subtype="html")
    host, port = env("SMTP_HOST", "smtp.gmail.com"), int(env("SMTP_PORT", "465"))
    smtp = smtplib.SMTP_SSL(host, port, timeout=30) if port == 465 else smtplib.SMTP(host, port, timeout=30)
    with smtp as s:
        if port != 465:
            s.starttls()
        s.login(env("SMTP_USER"), env("SMTP_PASSWORD"))
        s.send_message(msg)


def esc(s) -> str:
    return html.escape(str(s), quote=False)
