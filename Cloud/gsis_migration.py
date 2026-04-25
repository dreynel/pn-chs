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

        print("Updating tblstatutory_registry schema...")
        try:
            cur.execute("ALTER TABLE tblstatutory_registry ADD COLUMN config_mode ENUM('Amount', 'Percentage') DEFAULT 'Percentage' AFTER config_value")
            print("config_mode column added.")
        except Error as e:
            if '1060' in str(e):
                print("config_mode column already exists.")
            else:
                raise e

        print("\nRebranding SSS to GSIS...")
        # Update SSS_ENABLED to GSIS_ENABLED
        cur.execute("UPDATE tblstatutory_registry SET config_key = 'GSIS_ENABLED', description = 'Enable/Disable GSIS Deductions' WHERE config_key = 'SSS_ENABLED'")
        
        # Add GSIS_RATE if it doesn't exist
        cur.execute("SELECT id FROM tblstatutory_registry WHERE config_key = 'GSIS_RATE'")
        if not cur.fetchone():
            cur.execute("INSERT INTO tblstatutory_registry (config_key, config_value, config_mode, description) VALUES ('GSIS_RATE', '9.00', 'Percentage', 'GSIS Employee Contribution Rate')")
            print("GSIS_RATE added.")

        # Add GSIS_FIXED_AMOUNT if it doesn't exist (for Amount mode)
        cur.execute("SELECT id FROM tblstatutory_registry WHERE config_key = 'GSIS_FIXED_AMOUNT'")
        if not cur.fetchone():
            cur.execute("INSERT INTO tblstatutory_registry (config_key, config_value, config_mode, description) VALUES ('GSIS_FIXED_AMOUNT', '0.00', 'Amount', 'GSIS Fixed Deduction Amount')")
            print("GSIS_FIXED_AMOUNT added.")

        # Update other common ones to have modes
        cur.execute("UPDATE tblstatutory_registry SET config_mode = 'Percentage' WHERE config_key LIKE '%_RATE%'")
        cur.execute("UPDATE tblstatutory_registry SET config_mode = 'Amount' WHERE config_key LIKE '%_CAP%' OR config_key LIKE '%_FLOOR%' OR config_key LIKE '%_FIXED%'")

        conn.commit()
        print("\nMigration completed successfully.")
        conn.close()
    except Exception as e:
        print(f"\nMigration failed: {e}")

if __name__ == "__main__":
    migrate()
