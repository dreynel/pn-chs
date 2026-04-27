import mysql.connector
from mysql.connector import Error, pooling
from contextlib import contextmanager

# DB_CONFIG = {
#     "host":     "localhost",
#     "database": "dbpnchs",
#     "user":     "root",
#     "password": "007622",
#     "charset":  "utf8mb4",
#     "autocommit": False,
# }

DB_CONFIG = {
    "host":     "34.134.43.148",
    "database": "dbpnchs",
    "user":     "root",
    "password": "Mlfd5rGPn$Y|-2C0",
    "charset":  "utf8mb4",
    "autocommit": False,
}

# Create a connection pool to drastically reduce TCP handshake latency on every ping
try:
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="cloud_pool",
        pool_size=15,  # Match the Local configuration
        pool_reset_session=True,
        **DB_CONFIG
    )
except Error as e:
    print(f"Error initializing connection pool: {e}")
    connection_pool = None

def get_connection():
    """Open and return a new MySQL connection from the pool."""
    if connection_pool:
        return connection_pool.get_connection()
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