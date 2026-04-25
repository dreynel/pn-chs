from db import db_cursor
import mysql.connector

def check_schema():
    tables = ['tblemployee', 'tblpayhead', 'tblglobal_payheads', 'tblstatutory_registry']
    for table in tables:
        print(f"\n--- {table} ---")
        try:
            with db_cursor() as (conn, cur):
                cur.execute(f"DESCRIBE {table}")
                cols = cur.fetchall()
                for col in cols:
                    print(f"{col['Field']}: {col['Type']}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    check_schema()
