import mysql.connector
from mysql.connector import Error

def migrate():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="007622",
            database="dbpnchs"
        )
        cur = conn.cursor()

        # Update tblpayhead
        print("Migrating tblpayhead...")
        try:
            cur.execute("ALTER TABLE tblpayhead ADD COLUMN mode ENUM('Amount', 'Percentage') DEFAULT 'Amount' AFTER amount")
            cur.execute("ALTER TABLE tblpayhead ADD COLUMN percentage_value DECIMAL(10, 2) DEFAULT 0.00 AFTER mode")
            print("tblpayhead updated.")
        except Error as e:
            if 'duplicate column' in str(e).lower() or 'column already exists' in str(e).lower() or '1060' in str(e):
                print("tblpayhead columns already exist.")
            else:
                raise e

        # Update tblglobal_payheads
        print("\nMigrating tblglobal_payheads...")
        try:
            cur.execute("ALTER TABLE tblglobal_payheads ADD COLUMN mode ENUM('Amount', 'Percentage') DEFAULT 'Amount' AFTER amount")
            cur.execute("ALTER TABLE tblglobal_payheads ADD COLUMN percentage_value DECIMAL(10, 2) DEFAULT 0.00 AFTER mode")
            print("tblglobal_payheads updated.")
        except Error as e:
            if 'duplicate column' in str(e).lower() or 'column already exists' in str(e).lower() or '1060' in str(e):
                print("tblglobal_payheads columns already exist.")
            else:
                raise e

        conn.commit()
        print("\nMigration completed successfully.")
        conn.close()
    except Exception as e:
        print(f"\nMigration failed: {e}")

if __name__ == "__main__":
    migrate()
