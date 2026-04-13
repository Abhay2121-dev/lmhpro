"""
database.py  –  Gentle Reflection Prototype
SQLite persistence. Single table, clean helpers.
"""
import json
import sqlite3
from datetime import date, datetime
from pathlib import Path
from typing import Optional

DB = Path(__file__).parent / "journal.db"


def _conn() -> sqlite3.Connection:
    c = sqlite3.connect(str(DB), check_same_thread=False)
    c.row_factory = sqlite3.Row
    return c


def init():
    with _conn() as c:
        c.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            ts            TEXT NOT NULL,
            entry_date    TEXT NOT NULL,
            mode          TEXT NOT NULL,
            prompt        TEXT NOT NULL,
            body          TEXT NOT NULL,
            reflection    TEXT,
            questions     TEXT,
            starters      TEXT,
            reminiscence  TEXT,
            reframe       TEXT,
            tags          TEXT,
            summary       TEXT,
            risk          TEXT DEFAULT 'low',
            word_count    INTEGER DEFAULT 0
        )""")
        c.commit()


def save(
    mode: str, prompt: str, body: str,
    reflection: Optional[str] = None,
    questions: Optional[list] = None,
    starters: Optional[list] = None,
    reminiscence: Optional[str] = None,
    reframe: Optional[str] = None,
    tags: Optional[list] = None,
    summary: Optional[str] = None,
    risk: str = "low",
) -> int:
    with _conn() as c:
        cur = c.execute(
            """INSERT INTO entries
               (ts, entry_date, mode, prompt, body, reflection, questions,
                starters, reminiscence, reframe, tags, summary, risk, word_count)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                datetime.utcnow().isoformat(),
                date.today().isoformat(),
                mode, prompt, body, reflection,
                json.dumps(questions) if questions else None,
                json.dumps(starters)  if starters  else None,
                reminiscence, reframe,
                json.dumps(tags)      if tags       else None,
                summary, risk,
                len(body.split()),
            ),
        )
        c.commit()
        return cur.lastrowid


def all_entries() -> list[dict]:
    with _conn() as c:
        rows = c.execute("SELECT * FROM entries ORDER BY ts DESC").fetchall()
    return [_d(r) for r in rows]


def entries_for_date(d: str) -> list[dict]:
    with _conn() as c:
        rows = c.execute(
            "SELECT * FROM entries WHERE entry_date=? ORDER BY ts", (d,)
        ).fetchall()
    return [_d(r) for r in rows]


def distinct_dates() -> list[str]:
    with _conn() as c:
        rows = c.execute(
            "SELECT DISTINCT entry_date FROM entries ORDER BY entry_date DESC"
        ).fetchall()
    return [r["entry_date"] for r in rows]


def _d(row: sqlite3.Row) -> dict:
    d = dict(row)
    for f in ("questions", "starters", "tags"):
        if d.get(f):
            try:
                d[f] = json.loads(d[f])
            except Exception:
                d[f] = []
    return d
