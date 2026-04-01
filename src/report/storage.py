import sqlite3
from pathlib import Path
from report.time_utils import now, parse_iso_datetime, today_timezone

DB_PATH = Path("data/report.db")


def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_storage():
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project TEXT NOT NULL,
                section TEXT NOT NULL,
                text TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def add_entry(entry):
    init_storage()
    created_at = now().isoformat()
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO entries (project, section, text, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (entry.project, entry.section, entry.text, created_at),
        )
        conn.commit()


def load_entries(from_dt: str | None = None, to_dt: str | None = None):
    init_storage()

    if bool(from_dt) != bool(to_dt):
        raise ValueError("from_dt and to_dt must be provided together")

    query = """
        SELECT project, section, text, created_at
        FROM entries
    """
    params = []

    if from_dt and to_dt:
        query += " WHERE created_at >= ? AND created_at <= ?"
        params.extend([from_dt, to_dt])

    query += " ORDER BY created_at ASC, id ASC"

    with _connect() as conn:
        rows = conn.execute(query, params).fetchall()

    report_date = today_timezone().isoformat()
    if from_dt:
        report_date = parse_iso_datetime(from_dt).date().isoformat()

    return {
        "date": report_date,
        "entries": [
            {
                "project": row["project"],
                "section": row["section"],
                "text": row["text"],
                "created_at": row["created_at"],
            }
            for row in rows
        ]
    }
