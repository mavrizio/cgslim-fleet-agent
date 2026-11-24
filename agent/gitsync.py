"""Commit dei dati del server (registro, report, note) e push su GitHub.

Lo usano il report giornaliero e la lettura delle note da Telegram; anche
scripts/update.sh prende lo stesso lock (state/git.lock), cosi' due giri
non lavorano sul repo nello stesso momento.
Se il rebase non riesce si torna indietro e il commit resta in locale: il
prossimo giro ritenta. Un repo lasciato a meta' rebase bloccherebbe anche
gli aggiornamenti del codice.
"""
import fcntl
import subprocess
from contextlib import contextmanager

from . import config as cfg

LOCK_FILE = cfg.STATE_DIR / "git.lock"
LOCK_WAIT_S = 300


@contextmanager
def repo_lock():
    cfg.STATE_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOCK_FILE, "w") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)


def _git(*args, check=True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(cfg.ROOT), *args], check=check,
                          capture_output=True, text=True, timeout=LOCK_WAIT_S)


def commit_and_push(paths: list[str], message: str) -> str:
    """Ritorna 'nothing', 'pushed' o 'local' (commit fatto, push al prossimo giro)."""
    with repo_lock():
        existing = [p for p in paths if (cfg.ROOT / p).exists()]
        if existing:
            _git("add", "-A", "--", *existing)
        if _git("diff", "--cached", "--quiet", check=False).returncode:
            _git("commit", "-q", "-m", message)
        elif not _git("log", "-1", "origin/main..HEAD", "--format=%h", check=False).stdout.strip():
            return "nothing"
        if _git("pull", "-q", "--rebase", "origin", "main", check=False).returncode:
            _git("rebase", "--abort", check=False)
            print("git: rebase non riuscito, commit tenuto in locale")
            return "local"
        if _git("push", "-q", "origin", "main", check=False).returncode:
            print("git: push non riuscito, ritento al prossimo giro")
            return "local"
        return "pushed"
