# save_fingerprint.py
import mysql.connector
# from pyzkfp.pyzkfp import PyZKFP
from pyzkfp import PyZKFP
# Connect to database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="007622",
    database="dbpnchs"
)
cursor = db.cursor()

# Initialize fingerprint scanner
zk = PyZKFP()
if not zk.Init():
    print("Failed to initialize fingerprint scanner")
    exit()

user_name = input("Enter user name: ")

print("Place your finger on the scanner...")

# Capture fingerprint
while True:
    if zk.IsFingerPressed():
        if zk.AcquireFingerprint():
            template = zk.BlobToBase64(zk.GetTemplate())
            # Save to database
            sql = "INSERT INTO fingerprints (user_name, fingerprint_template) VALUES (%s, %s)"
            cursor.execute(sql, (user_name, template))
            db.commit()
            print("Fingerprint saved successfully!")
            break

zk.Close()
cursor.close()
db.close()