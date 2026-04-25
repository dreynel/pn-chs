import mysql.connector
from db import DB_CONFIG

def test_connection():
    try:
        print(f"Attempting to connect to {DB_CONFIG['database']} on {DB_CONFIG['host']}...")
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print("Successfully connected to MySQL!")
            conn.close()
        return True
    except Exception as e:
        print(f"Failed to connect to MySQL: {e}")
        return False

if __name__ == "__main__":
    test_connection()
