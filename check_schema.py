import sys
sys.path.append('e:\\proj\\pnchs\\Local')
from db import db_cursor

try:
    with db_cursor() as (conn, cur):
        cur.execute("DESCRIBE tblemployee")
        rows = cur.fetchall()
        print("tblemployee:")
        for row in rows:
            print(row)
except Exception as e:
    print(f"Error: {e}")
