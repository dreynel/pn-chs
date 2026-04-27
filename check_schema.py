import mysql.connector

DB_CONFIG = {
    "host":     "34.134.43.148",
    "database": "dbpnchs",
    "user":     "root",
    "password": "Mlfd5rGPn$Y|-2C0",
    "charset":  "utf8mb4",
    "autocommit": False,
}

conn = mysql.connector.connect(**DB_CONFIG)
cur = conn.cursor()
cur.execute("""
SELECT TABLE_NAME, COLUMN_NAME 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'dbpnchs' 
AND COLUMN_NAME = 'employee_id'
""")
for row in cur.fetchall():
    print(row)
