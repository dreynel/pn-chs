import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="007622",
        database="dbpnchs"
    )
    cur = conn.cursor()
    # Add category column
    cur.execute("ALTER TABLE tblpayhead ADD COLUMN category ENUM('Earning', 'Deduction') DEFAULT 'Earning' AFTER amount")
    
    # Set historical data based on sign
    cur.execute("UPDATE tblpayhead SET category = 'Deduction' WHERE amount < 0")
    
    conn.commit()
    print("Migration successful: added 'category' to tblpayhead")
    conn.close()
except Exception as e:
    print(e)
