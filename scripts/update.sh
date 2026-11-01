#!/usr/bin/env bash
# Aggiornamento del server da GitHub (in tirata, come il gitpuller dei Pi).
# Il codice si modifica solo sul Mac e arriva con un push; questo script, ogni
# 10 minuti (cgslim-agent-update.timer):
#   1. se origin/main ha commit nuovi, li prende (rebase dei commit di dati del server)
#   2. aggiorna librerie e unit systemd se sono cambiate
#   3. prova: `agent.cli status` deve leggere il DB e far girare le regole
#   4. esito su Telegram; se la prova fallisce torna al commit di prima
# E' in bash e non in Python apposta: un commit che rompe il Python non deve
# poter rompere anche il ritorno indietro.
set -uo pipefail

ROOT=/opt/cgslim-agent
BAD_FILE=$ROOT/state/update_bad_commit
cd "$ROOT" || exit 1

tg() {  # messaggio Telegram con le credenziali del .env, senza passare dal Python
  local tok chat
  tok=$(grep -m1 '^TELEGRAM_BOT_TOKEN=' .env | cut -d= -f2- | tr -d '"')
  chat=$(grep -m1 '^TELEGRAM_CHAT_ID=' .env | cut -d= -f2- | tr -d '"')
  curl -s -m 20 "https://api.telegram.org/bot$tok/sendMessage" \
    --data-urlencode "chat_id=$chat" --data-urlencode "text=$1" >/dev/null
}

git fetch -q origin main || exit 0          # niente rete: si riprova al prossimo giro
remote=$(git rev-parse origin/main)
git merge-base --is-ancestor "$remote" HEAD && exit 0   # gia' aggiornato
[ "$(cat "$BAD_FILE" 2>/dev/null)" = "$remote" ] && exit 0  # gia' scartato: si aspetta un fix

old=$(git rev-parse HEAD)
if ! git pull -q --rebase --autostash origin main; then
  git rebase --abort 2>/dev/null
  tg "⚠️ cgslim-agent: aggiornamento a ${remote:0:7} non applicabile (conflitto git), resto su ${old:0:7}"
  echo "$remote" > "$BAD_FILE"
  exit 1
fi
changed=$(git diff --name-only "$old" HEAD)

if grep -q '^requirements.txt$' <<<"$changed"; then
  venv/bin/pip -q install -r requirements.txt || { pip_failed=1; }
fi

if [ -z "${pip_failed:-}" ] && venv/bin/python -m agent.cli status >/tmp/cgslim-agent-update.log 2>&1; then
  if grep -q '^systemd/' <<<"$changed"; then
    sudo install -m 644 systemd/*.service systemd/*.timer /etc/systemd/system/
    sudo systemctl daemon-reload
  fi
  rm -f "$BAD_FILE"
  tg "✅ cgslim-agent aggiornato a ${remote:0:7}: $(git log -1 --format=%s "$remote" | cut -c1-120)"
else
  err=$(tail -3 /tmp/cgslim-agent-update.log | cut -c1-300)
  git reset -q --hard "$old"
  [ -n "${pip_failed:-}" ] && venv/bin/pip -q install -r requirements.txt
  echo "$remote" > "$BAD_FILE"
  tg "❌ cgslim-agent: ${remote:0:7} non supera la prova, tornato a ${old:0:7}. Errore: $err"
  exit 1
fi
