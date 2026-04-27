import mysql.connector

DB_CONFIG = {
    "host":     "34.134.43.148",
    "database": "dbpnchs",
    "user":     "root",
    "password": "Mlfd5rGPn$Y|-2C0",
    "charset":  "utf8mb4",
    "autocommit": True,
}

conn = mysql.connector.connect(**DB_CONFIG)
cur = conn.cursor()
cur.execute("UPDATE tblenrollment_tasks SET status='cancelled' WHERE status='pending'")
print(f"Cleared {cur.rowcount} pending tasks.")
