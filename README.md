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

## Dove si lavora e come arriva al server
- **Codice**: si modifica solo sul Mac (`~/Documents/GitHub/cgslim-fleet-agent`), commit e push su GitHub.
- **Server**: `cgslim-agent-update.timer` ogni 10 min esegue `scripts/update.sh`: prende i commit nuovi,
  aggiorna librerie e unit systemd, prova `agent.cli status`; se la prova fallisce torna al commit di
  prima e lo scarta finche' non ne arriva uno nuovo. Esito su Telegram. Non serve raggiungere il server
  (funziona anche senza Tailscale).
- **Dati**: il server committa solo `ISSUES.md`, `reports/` e `data/issues.json` (registro), con rebase
  sui commit del Mac. Prima di modificare il codice sul Mac: `git pull`.
- `state/` (avvisi aperti, log dei report) resta solo sul server, fuori da git.

## Server di casa (viaggi)
- `mac-mini-autopoweron.service`: riaccensione automatica dopo un blackout.
- I controlli ogni 15 min avvisano su Telegram se Tailscale si scollega.
- Upgrade di versione di Ubuntu disattivati (`Prompt=never`): stamattina del 1/11 il passaggio a 26.04
  aveva rotto i venv Python di 4 servizi.

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
