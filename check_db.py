from db import db_cursor
try:
    with db_cursor() as (conn, cur):
        cur.execute("SELECT * FROM tblbiometric_logs ORDER BY log_time DESC LIMIT 10")
        logs = cur.fetchall()
        print(f"DEBUG: Found {len(logs)} logs")
        for l in logs:
            print(l)
        
        cur.execute("SELECT employee_id, first_name FROM tblemployee")
        emps = cur.fetchall()
        print(f"DEBUG: Found {len(emps)} employees")
except Exception as e:
    print(e)
