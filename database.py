"""database.py — SQLite persistence for the Multi-Agent Research System.
Author: Avatar Putra Sigit | GitHub: qurrrrsebastian-prog
"""
import os
import sqlite3
from datetime import datetime
from typing import List, Optional

import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "app.db")


def get_connection() -> sqlite3.Connection:
    """Return a SQLite connection with row access by name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create tables. Call once at app start."""
    conn = get_connection()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS research_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, session_token TEXT UNIQUE,
            timestamp TEXT, topic TEXT, final_output TEXT,
            total_time_seconds REAL, status TEXT DEFAULT 'in_progress');
        CREATE TABLE IF NOT EXISTS agent_steps (
            id INTEGER PRIMARY KEY AUTOINCREMENT, session_id INTEGER,
            agent_name TEXT, step_order INTEGER, input_data TEXT,
            output_data TEXT, execution_time_ms REAL, status TEXT);
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, user TEXT,
            action TEXT, details TEXT);
        """
    )
    conn.commit()
    conn.close()


def add_log(action: str, details: str = "", user: str = "anonymous") -> None:
    """Append an entry to the audit log."""
    conn = get_connection()
    conn.execute(
        "INSERT INTO audit_log (timestamp, user, action, details) VALUES (?, ?, ?, ?)",
        (datetime.now().isoformat(timespec="seconds"), user, action, details),
    )
    conn.commit()
    conn.close()


# --------------------------------------------------------------------------- #
# Sessions & steps
# --------------------------------------------------------------------------- #
def create_session(session_token: str, topic: str) -> int:
    """Create a research session and return its id."""
    conn = get_connection()
    cur = conn.execute(
        """INSERT INTO research_sessions (session_token, timestamp, topic, status)
           VALUES (?, ?, ?, 'in_progress')""",
        (session_token, datetime.now().isoformat(timespec="seconds"), topic),
    )
    conn.commit()
    rid = cur.lastrowid
    conn.close()
    return rid


def add_step(session_id: int, agent_name: str, step_order: int, input_data: str,
             output_data: str, execution_time_ms: float, status: str) -> None:
    """Persist a completed agent step."""
    conn = get_connection()
    conn.execute(
        """INSERT INTO agent_steps
           (session_id, agent_name, step_order, input_data, output_data,
            execution_time_ms, status)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (session_id, agent_name, step_order, input_data, output_data,
         execution_time_ms, status),
    )
    conn.commit()
    conn.close()


def finalize_session(session_id: int, final_output: str, total_time_seconds: float,
                     status: str = "completed") -> None:
    """Mark a session complete with its final output and total time."""
    conn = get_connection()
    conn.execute(
        """UPDATE research_sessions
           SET final_output=?, total_time_seconds=?, status=? WHERE id=?""",
        (final_output, total_time_seconds, status, session_id),
    )
    conn.commit()
    conn.close()


def get_sessions(limit: int = 100) -> pd.DataFrame:
    """Return research sessions, newest first."""
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM research_sessions ORDER BY id DESC LIMIT ?", conn,
        params=[limit])
    conn.close()
    return df


def get_session(session_id: int):
    """Return a single session as a dict, or None."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM research_sessions WHERE id = ?",
                       (session_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_steps(session_id: int) -> pd.DataFrame:
    """Return the agent steps for a session in order."""
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM agent_steps WHERE session_id = ? ORDER BY step_order",
        conn, params=[session_id])
    conn.close()
    return df


def clear_sessions() -> None:
    """Delete all sessions and steps."""
    conn = get_connection()
    conn.execute("DELETE FROM agent_steps")
    conn.execute("DELETE FROM research_sessions")
    conn.commit()
    conn.close()
