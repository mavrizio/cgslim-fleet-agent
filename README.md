# cgslim-agent

Agente di controllo della flotta CGSLIM. Gira sul server di casa
(`openclaw@openclaw-macmini6-2`, `/opt/cgslim-agent`) e legge il DB del fleet
monitor (progetto Supabase `cgslim-fleet`) con il ruolo `fleet_agent`, in sola
lettura (migrazione `0010_fleet_agent_readonly.sql` del repo cgslim-fleet).

## Livelli
- **Livello 1 – regole** (`agent/checks.py`), ogni 15 min (`cgslim-agent-check.timer`):
  offline, app ferma, seriale assente, GMI bloccata, POS in errore, tempeste di
  riavvii, sottotensione, disco, temperatura, updater. Avvisi Telegram con
  memoria in `state/alerts.json`: nuovo / critico ripetuto ogni 12 h / risolto.
- **Livello 2 – analisi con Claude**, giornaliero: report email + Telegram e
  registro dei problemi `ISSUES.md` per lo sviluppo. *(in costruzione)*

Le macchine con MHD `7788…` e `7777…` (sviluppo/test) sono escluse.

## Comandi
```bash
cd /opt/cgslim-agent
venv/bin/python -m agent.cli status            # problemi aperti, non invia niente
venv/bin/python -m agent.cli check --dry-run   # cosa invierebbe il prossimo giro
venv/bin/python -m agent.cli telegram-chat-id  # chat_id dopo /start al bot
```

## Segreti
Solo in `.env` (chmod 600, fuori da git): DB `fleet_agent`, `ANTHROPIC_API_KEY`,
bot Telegram, SMTP (stesso account di memo_ingest).
