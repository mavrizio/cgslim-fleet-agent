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


# Stato ridotto ai campi letti da checks.check_devices: i controlli girano ogni
# 15 min e il free di Supabase conta il traffico in uscita (5 GB/mese). Lo stato
# completo (~4 KB a macchina) serve solo al report giornaliero (daily.py).
# Se check_devices legge un campo nuovo, aggiungerlo QUI.
SLIM_STATUS = """
        jsonb_strip_nulls(jsonb_build_object(
          'runtime', jsonb_build_object(
            'age_s', d.status #> '{runtime,age_s}',
            'serial_missing', d.status #> '{runtime,serial_missing}',
            'gmi_blocked', d.status #> '{runtime,gmi_blocked}',
            'cashless', jsonb_build_object(
              'chl_mode', d.status #> '{runtime,cashless,chl_mode}',
              'p95_error', d.status #> '{runtime,cashless,p95_error}')),
          'host', jsonb_build_object(
            'throttled', d.status #> '{host,throttled}',
            'cpu_temp_c', d.status #> '{host,cpu_temp_c}',
            'disk_free_mb', d.status #> '{host,disk_free_mb}',
            'clock_skew_s', d.status #> '{host,clock_skew_s}'),
          'app', jsonb_build_object('updater', jsonb_build_object(
            'ok', d.status #> '{app,updater,ok}',
            'failures', d.status #> '{app,updater,failures}',
            'error', d.status #> '{app,updater,error}'))
        ))"""


def devices(conn, slim: bool = False) -> list[dict]:
    """slim=True: solo i campi di stato usati dai controlli periodici (vedi SLIM_STATUS)."""
    status = SLIM_STATUS if slim else "d.status"
    return conn.execute(
        f"""
        select d.device_id, d.mhd, d.hostname, d.label, d.location, d.app_version,
               d.fw_version, d.git_branch, d.git_commit, d.app_running, d.last_seen, d.last_reason,
               {status} as status, d.device_key_status, d.config_key_status,
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
