"""Accesso in sola lettura al DB del fleet monitor (ruolo fleet_agent, migrazione 0010)."""
import psycopg
from psycopg.rows import dict_row

from .config import env


def connect() -> psycopg.Connection:
    return psycopg.connect(
        host=env("FLEET_DB_HOST"),
        port=int(env("FLEET_DB_PORT", "5432")),
        dbname=env("FLEET_DB_NAME", "postgres"),
        user=env("FLEET_DB_USER"),
        password=env("FLEET_DB_PASSWORD"),
        sslmode="require",
        connect_timeout=15,
        row_factory=dict_row,
        autocommit=True,
    )


def devices(conn) -> list[dict]:
    return conn.execute(
        """
        select d.device_id, d.mhd, d.hostname, d.label, d.location, d.app_version,
               d.fw_version, d.git_branch, d.git_commit, d.app_running, d.last_seen, d.last_reason,
               d.status, d.device_key_status, d.config_key_status,
               extract(epoch from now() - d.last_seen)::int as age_s,
               r.center, r.battery
          from devices d
          left join machine_registry r on ltrim(r.mhd, '0') = ltrim(d.mhd, '0')
         order by d.mhd
        """
    ).fetchall()


def events(conn, hours: float) -> list[dict]:
    return conn.execute(
        """
        select id, device_id, received_at, event_at, kind, data
          from device_events
         where received_at > now() - make_interval(secs => %s)
         order by received_at
        """,
        (hours * 3600,),
    ).fetchall()


def transactions(conn, hours: float) -> list[dict]:
    return conn.execute(
        """
        select device_id, mhd, ts, mode, method, item, amount_req, amount, outcome, reason
          from transactions
         where ts > now() - make_interval(secs => %s)
         order by ts
        """,
        (hours * 3600,),
    ).fetchall()


def config_changes(conn, hours: float) -> list[dict]:
    return conn.execute(
        """
        select device_id, kind, key, state, created_at, result_at, error
          from config_changes
         where created_at > now() - make_interval(secs => %s)
        """,
        (hours * 3600,),
    ).fetchall()
