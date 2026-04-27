import sys
sys.path.append('e:/proj/pnchs/Local')
from db import db_cursor

try:
    with db_cursor() as (conn, cur):
        cur.execute("SELECT id, username, name, role, employee_id FROM tblusers")
        for row in cur.fetchall():
            print(row)
        
        cur.execute("SELECT * FROM tblemployee")
        print("\nEmployees:")
        for row in cur.fetchall():
            print((row['employee_id'], row['first_name'], row['last_name']))
except Exception as e:
    print("Error:", e)
