"""Configurazione: legge /opt/cgslim-agent/.env senza dipendenze esterne."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = ROOT / "state"
REPORTS_DIR = ROOT / "reports"
KNOWLEDGE_DIR = ROOT / "knowledge"


def _load_env(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env(ROOT / ".env")


def env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)


# Macchine di sviluppo/test: fuori dai controlli (decisione utente 2026-11-01)
EXCLUDED_MHD_PREFIXES = ("7788", "7777")

# Soglie del livello 1 (regole). Valori tarati sui dati di novembre 2026.
OFFLINE_WARN_MIN = 35        # il reporter manda ogni 15 min: 35 = due giri persi
OFFLINE_CRIT_HOURS = 6
RUNTIME_STALE_S = 300        # heartbeat di main.py vecchio con Pi online
REBOOT_STORM = (3, 6)        # >= 3 reboot in 6 ore
RESTART_STORM = (5, 6)       # >= 5 app_restart in 6 ore
CPU_TEMP_WARN = 75.0
DISK_FREE_WARN_MB = 1000
CLOCK_SKEW_WARN_S = 120
RENOTIFY_HOURS = 12          # un problema critico ancora aperto si ripete ogni 12 h
# Minuti di persistenza prima del primo avviso, per gli stati che vanno e vengono
DEBOUNCE_MIN = {"pos_error": 30, "runtime_stale": 15, "app_not_running": 15}
