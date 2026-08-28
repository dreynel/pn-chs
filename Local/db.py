import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
from contextlib import contextmanager

import os

DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "dbpnchs"),
    "user":     os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "007622"),
    "charset":  "utf8mb4",
    "autocommit": False,
}

# Create a connection pool to avoid slow handshakes on every payload
db_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="local_scanner_pool",
    pool_size=15,
    pool_reset_session=True,
    **DB_CONFIG
)

def get_connection():
    """Returns a connection from the connection pool instantly."""
    return db_pool.get_connection()


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