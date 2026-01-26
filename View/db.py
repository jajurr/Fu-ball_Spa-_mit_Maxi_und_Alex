import sqlite3
from pathlib import Path
from typing import Iterable, Any, Optional

import pandas as pd
import streamlit as st

# Pfad zu SQLite:
DEFAULT_DB_PATH = Path("C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Fussball.db")

@st.cache_resource
def get_connection(db_path: str) -> sqlite3.Connection:
    """
    Verbindung zu SQLite
    """
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def get_db_path() -> str:
    """
    Gibt den Pfad zur SQLite Datenbank zurück
    """
    return str(DEFAULT_DB_PATH)

def query_df(sql: str, params: Optional[Iterable[Any]] = None, db_path: Optional[str] = None) -> pd.DataFrame:
    """
    Führt eine SELECT-Abfrage aus und gibt ein DataFrame zurück
    """
    if params is None:
        params = ()
    if db_path is None:
        db_path = get_db_path()

    conn = get_connection(db_path)
    return pd.read_sql_query(sql, conn, params=params)

def query_value(sql: str, params: Optional[Iterable[Any]] = None, db_path: Optional[str] = None):
    """
    Abfrage für einen Wert
    """
    if params is None:
        params = ()
    if db_path is None:
        db_path = get_db_path()

    conn = get_connection(db_path)
    cur = conn.execute(sql, params)
    row = cur.fetchone()
    return row[0] if row else None

def blob_to_bytes(value):
    """
    Macht aus einem Blob in der DB bytes
    """
    if value is None:
        return None
    if isinstance(value, memoryview):
        return value.tobytes()
    return value