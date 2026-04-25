import cv2
import numpy as np
import time
import sqlite3
import os
from pyzkfp import ZKFP2

DB_FILE = "biometric.db"
MATCH_THRESHOLD = 55

# ── SQLite ────────────────────────────────────────────────────────────────────

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            template BLOB NOT NULL,
            enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

def get_all_users(conn):
    c = conn.cursor()
    c.execute("SELECT id, name, template FROM users")
    return c.fetchall()

def save_user(conn, name, template):
    c = conn.cursor()
    c.execute("INSERT INTO users (name, template) VALUES (?, ?)", (name, sqlite3.Binary(bytes(template))))
    conn.commit()
    return c.lastrowid

# ── Engine ────────────────────────────────────────────────────────────────────

def load_templates_into_engine(zkfp, conn):
    users = get_all_users(conn)
    for user_id, name, template in users:
        zkfp.DBAdd(user_id, bytes(template))
    print(f"Loaded {len(users)} template(s) into ZKTeco engine.")
    return {row[0]: row[1] for row in users}

# ── Capture ───────────────────────────────────────────────────────────────────

def capture_with_quality_check(zkfp, label="Scan"):
    while True:
        res = zkfp.AcquireFingerprint()
        if res is None:
            continue

        # ✅ CORRECT ORDER: template is FIRST, image is SECOND
        template, img = res

        if template is None or len(template) == 0:
            print("  ⚠️  Poor quality — press finger more firmly...")
            continue

        # Display image
        width = zkfp.width
        height = zkfp.height
        fingerprint = np.frombuffer(bytes(img), dtype=np.uint8).reshape((height, width))
        cv2.imshow(label, fingerprint)
        cv2.waitKey(500)

        return template, img

# ── Enroll ────────────────────────────────────────────────────────────────────

def enroll_finger(zkfp, conn, id_map):
    name = input("Enter person's name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    print(f"\nEnrolling '{name}'. Scan 3 times for best accuracy...")
    templates = []

    for i in range(3):
        print(f"\n  [{i+1}/3] Place your finger firmly and flat...")
        template, img = capture_with_quality_check(zkfp, f"Enrolling [{i+1}/3]")

        # Duplicate check
        if len(id_map) > 0:
            fid, score = zkfp.DBIdentify(template)  # ✅ fid first, score second
            if score >= MATCH_THRESHOLD:
                matched_name = id_map.get(fid, "Unknown")
                print(f"\n  ⚠️  Already enrolled as '{matched_name}' (score: {score}). Aborting.")
                cv2.destroyAllWindows()
                return

        templates.append(template)
        print(f"  ✅ Sample {i+1} captured.")
        time.sleep(1.2)

    cv2.destroyAllWindows()

    # ✅ DBMerge returns (regTemp, regTempLen) tuple
    merged_template, merged_len = zkfp.DBMerge(*templates)
    if merged_template is None or merged_len == 0:
        print("❌ Merge failed — please re-enroll.")
        return

    user_id = save_user(conn, name, merged_template)
    zkfp.DBAdd(user_id, merged_template)
    id_map[user_id] = name
    print(f"\n✅ '{name}' enrolled successfully! (ID: {user_id})")

# ── Identify ──────────────────────────────────────────────────────────────────

def identify_finger(zkfp, id_map):
    print("\nPlace your finger to identify... (Ctrl+C to return to menu)")
    while True:
        template, img = capture_with_quality_check(zkfp, "Identifying")

        fid, score = zkfp.DBIdentify(template)  # ✅ fid first, score second

        print(f"\n{'─'*40}")
        if score >= MATCH_THRESHOLD:
            name = id_map.get(fid, "Unknown")
            print(f"  ✅ IDENTIFIED : {name}")
            print(f"  Match Score  : {score}/100")
            print(f"  User ID      : {fid}")
        else:
            print(f"  ❌ NOT RECOGNIZED")
            print(f"  Best Score   : {score}/100  (threshold: {MATCH_THRESHOLD})")
        print(f"{'─'*40}")

        time.sleep(2.5)
        cv2.destroyAllWindows()
        print("\nPlace finger again or Ctrl+C to return to menu...")

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    zkfp = ZKFP2()
    zkfp.Init()
    zkfp.OpenDevice(0)
    print(f"Device ready — {zkfp.width}x{zkfp.height}")

    conn = init_db()
    id_map = load_templates_into_engine(zkfp, conn)

    try:
        while True:
            print("\n┌──────────────────────────┐")
            print("│  [E] Enroll new finger    │")
            print("│  [I] Identify finger      │")
            print("│  [L] List enrolled users  │")
            print("│  [Q] Quit                 │")
            print("└──────────────────────────┘")
            choice = input("Choose: ").strip().upper()

            if choice == "E":
                enroll_finger(zkfp, conn, id_map)

            elif choice == "I":
                if not id_map:
                    print("⚠️  No enrolled users yet. Please enroll first.")
                else:
                    try:
                        identify_finger(zkfp, id_map)
                    except KeyboardInterrupt:
                        cv2.destroyAllWindows()
                        print("\nReturned to menu.")

            elif choice == "L":
                users = get_all_users(conn)
                if not users:
                    print("No enrolled users.")
                else:
                    print(f"\n{'ID':<6} {'Name':<20} Enrolled At")
                    print("─" * 50)
                    for uid, name, _, *_ in [(r[0], r[1], r[2]) for r in users]:
                        c2 = conn.cursor()
                        c2.execute("SELECT enrolled_at FROM users WHERE id=?", (uid,))
                        row = c2.fetchone()
                        print(f"{uid:<6} {name:<20} {row[0] if row else 'N/A'}")

            elif choice == "Q":
                break

    except KeyboardInterrupt:
        print("\nExiting...")

    finally:
        conn.close()
        zkfp.CloseDevice()
        zkfp.Terminate()
        cv2.destroyAllWindows()
        print("Device closed.")

if __name__ == "__main__":
    main()