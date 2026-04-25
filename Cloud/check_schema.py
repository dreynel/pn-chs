import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="007622",
        database="dbpnchs"
    )
    cur = conn.cursor(dictionary=True)
    
    print("--- tblpayhead ---")
    cur.execute("DESCRIBE tblpayhead")
    for col in cur.fetchall():
        print(f"Col: {col['Field']}, Type: {col['Type']}")
        
    print("\n--- tblstatutory_registry ---")
    cur.execute("DESCRIBE tblstatutory_registry")
    for col in cur.fetchall():
        print(f"Col: {col['Field']}, Type: {col['Type']}")
    
    print("\n--- DATA ---")
    cur.execute("SELECT * FROM tblstatutory_registry")
    for row in cur.fetchall():
        print(row)
    conn.close()
except Exception as e:
    print(e)
