from db import db_cursor

def cleanup():
    with db_cursor() as (conn, cur):
        # Delete legacy toggle keys
        cur.execute("DELETE FROM tblstatutory_registry WHERE config_key IN ('GSIS_ENABLED', 'BIR_ENABLED', 'SSS_ENABLED')")
        conn.commit()
        print("Legacy statutory toggles removed.")

if __name__ == '__main__':
    cleanup()
