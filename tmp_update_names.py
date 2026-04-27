import sys
sys.path.append('e:/proj/pnchs/Local')
from db import db_cursor

try:
    with db_cursor() as (conn, cur):
        cur.execute("UPDATE tblemployee SET first_name='System', last_name='Administrator' WHERE employee_id='EMP-901'")
        cur.execute("UPDATE tblemployee SET first_name='Human', last_name='Resources' WHERE employee_id='EMP-902'")
        cur.execute("UPDATE tblemployee SET first_name='Financial', last_name='Controller' WHERE employee_id='EMP-903'")

        cur.execute("UPDATE tblusers SET name='System Administrator', employee_id='EMP-901' WHERE role='Admin'")
        cur.execute("UPDATE tblusers SET name='Human Resources', employee_id='EMP-902' WHERE role='HR'")
        cur.execute("UPDATE tblusers SET name='Financial Controller', employee_id='EMP-903' WHERE role='Finance'")
        
        conn.commit()
    print("Database names synced successfully with commit!")
except Exception as e:
    print("Error:", e)
