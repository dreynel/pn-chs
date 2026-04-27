import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
from contextlib import contextmanager

DB_CONFIG = {
    "host":     "34.134.43.148",
    "database": "dbpnchs",
    "user":     "root",
    "password": "Mlfd5rGPn$Y|-2C0",
    "charset":  "utf8mb4",
    "autocommit": False,
}

# Create a connection pool to avoid extremely slow remote TCP/SSL handshakes on every payload
db_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="cloud_pool",
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