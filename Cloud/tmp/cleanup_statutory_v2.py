import sys
import os
sys.path.append(os.getcwd())
from db import db_cursor

def cleanup():
    try:
        with db_cursor() as (conn, cur):
            cur.execute("DELETE FROM tblstatutory_registry WHERE config_key IN ('GSIS_ENABLED', 'BIR_ENABLED', 'SSS_ENABLED')")
            conn.commit()
            print("Successfully removed legacy statutory toggles.")
    except Exception as e:
        print(f"Error during cleanup: {e}")

if __name__ == '__main__':
    cleanup()
