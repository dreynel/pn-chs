import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager

DB_CONFIG = {
    "host":     "localhost",
    "database": "dbpnchs",
    "user":     "root",
    "password": "007622",
    "charset":  "utf8mb4",
    "autocommit": False,
}


def get_connection():
    """Open and return a new MySQL connection."""
    return mysql.connector.connect(**DB_CONFIG)


@contextmanager
def db_cursor(commit=False):
    """
    Context manager that yields (conn, cursor).
    Automatically commits or rolls back, then closes.

    Usage:
        with db_cursor(commit=True) as (conn, cur):
            cur.execute("INSERT ...")
    """
    conn = None
    cur  = None
    try:
        conn = get_connection()
        cur  = conn.cursor(dictionary=True)
        yield conn, cur
        if commit:
            conn.commit()
    except Error as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if cur:
            cur.close()
        if conn and conn.is_connected():
            conn.close()