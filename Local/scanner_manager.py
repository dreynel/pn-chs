import threading
import time
import base64
import requests
import os
from pyzkfp import ZKFP2

CLOUD_API_URL = os.environ.get('CLOUD_API_URL', 'https://pn-chs.onrender.com')

MATCH_THRESHOLD = 55

state_lock = threading.RLock()

KIOSK_STATE = {
    'status': 'stopped',     # stopped, running, error
    'last_scan': None,
    'last_error': None,
    'cooldowns': {}          # employee_id -> last_log_time
}

_thread_handle = None
_running = False

def sync_fingerprints_from_cloud():
    """Fetch all fingerprints directly from the live database."""
    try:
        from db import db_cursor
        with db_cursor() as (conn, cur):
            cur.execute("SELECT id, employee_id, user_name, fingerprint_template FROM fingerprints")
            data = cur.fetchall()
            users = []
            for r in data:
                try:
                    template_bytes = base64.b64decode(r['fingerprint_template'])
                    users.append((r['id'], r['employee_id'], r['user_name'], template_bytes))
                except Exception:
                    pass
            return users
    except Exception as e:
        print(f"Failed to sync fingerprints: {e}")
    return []

def _scanner_loop():
    global _running

    zkfp = ZKFP2()

    try:
        zkfp.Init()
        zkfp.OpenDevice(0)
    except Exception as e:
        import traceback
        print(f"Scanner Thread Error initializing device:\n{traceback.format_exc()}")
        with state_lock:
            KIOSK_STATE['status'] = 'error'
            _running = False
        return

    # Load existing fingerprints from Database into the device
    id_map = {}
    print("Syncing fingerprints from Database...")
    users = sync_fingerprints_from_cloud()
    for row_id, emp_id, user_name, template in users:
        try:
            zkfp.DBAdd(row_id, template)
            id_map[row_id] = {
                'employee_id': emp_id,
                'name': user_name
            }
        except Exception as ex:
            print(f"Failed to DBAdd for row {row_id}: {ex}")

    with state_lock:
        KIOSK_STATE['status'] = 'running'

    print("Scanner active. Waiting for operations...")

    # Enrollment tracking state specifically for the background thread process
    enroll_task = None
    enroll_templates = []
    enroll_step = 0

    while _running:
        try:
            # Poll for tasks every iteration if not currently enrolling
            if not enroll_task:
                try:
                    from db import db_cursor
                    with db_cursor() as (conn, cur):
                        cur.execute("SELECT id, employee_id, finger_index FROM tblenrollment_tasks WHERE status='pending' ORDER BY id ASC LIMIT 1")
                        task = cur.fetchone()
                        if task:
                            enroll_task = task
                            enroll_templates = []
                            enroll_step = 1
                            print(f"Discovered new enrollment task: {enroll_task}")
                except Exception:
                    pass

            if enroll_task:
                if enroll_step <= 3:
                    print(f"Enroll step {enroll_step}/3... Please scan finger.")
                    res = zkfp.AcquireFingerprint()
                    if res:
                        tmp, img = res
                        if not tmp or len(tmp) == 0:
                            time.sleep(0.1)
                            continue

                        # Check for duplicates
                        if len(id_map) > 0:
                            fid, score = zkfp.DBIdentify(tmp)
                            if score >= MATCH_THRESHOLD:
                                matched_name = id_map.get(fid, {}).get('name', 'Unknown')
                                print(f"Error: Fingerprint already enrolled for '{matched_name}' (score: {score}).")
                                try:
                                    with db_cursor(commit=True) as (conn, cur):
                                        cur.execute("UPDATE tblenrollment_tasks SET status='error' WHERE id=%s", (enroll_task['id'],))
                                except Exception: pass
                                enroll_task = None
                                time.sleep(2)
                                continue

                        enroll_templates.append(tmp)
                        enroll_step += 1
                        print(f"Scan {enroll_step - 1} successful. Please lift finger.")
                        time.sleep(1.5)  # Wait for finger lift
                else:
                    # Proceed to merge all 3 scans
                    print("Merging fingerprint data...")
                    merged_template, merged_len = zkfp.DBMerge(*enroll_templates)
                    if merged_template is None or merged_len == 0:
                        print("Failed to merge templates.")
                        try:
                            from db import db_cursor
                            with db_cursor(commit=True) as (conn, cur):
                                cur.execute("UPDATE tblenrollment_tasks SET status='error' WHERE id=%s", (enroll_task['id'],))
                        except Exception: pass
                    else:
                        template_bytes = bytes(merged_template)
                        if 0 < merged_len < len(template_bytes):
                            template_bytes = template_bytes[:merged_len]

                        template_b64 = base64.b64encode(template_bytes).decode('utf-8')
                        
                        try:
                            # Send to Database directly
                            from db import db_cursor
                            with db_cursor(commit=True) as (conn, cur):
                                cur.execute("SELECT first_name, last_name FROM tblemployee WHERE employee_id=%s", (enroll_task['employee_id'],))
                                emp = cur.fetchone()
                                user_name = f"{emp['first_name']} {emp['last_name']}" if emp else str(enroll_task['employee_id'])

                                cur.execute("""
                                    INSERT INTO fingerprints (employee_id, user_name, fingerprint_template, finger_index)
                                    VALUES (%s, %s, %s, %s)
                                    ON DUPLICATE KEY UPDATE 
                                        fingerprint_template = VALUES(fingerprint_template),
                                        user_name = VALUES(user_name)
                                """, (enroll_task['employee_id'], user_name, template_b64, enroll_task['finger_index']))

                                # Mark task success
                                cur.execute("UPDATE tblenrollment_tasks SET status='success' WHERE id=%s", (enroll_task['id'],))
                            
                            print("Successfully stored enrollment to Database.")
                            
                            # Add to active array to avoid needing a reboot
                            new_local_id = max(list(id_map.keys()) + [0]) + 1
                            zkfp.DBAdd(new_local_id, template_bytes)
                            id_map[new_local_id] = {
                                'employee_id': enroll_task['employee_id'],
                                'name': user_name
                            }
                        except Exception as e:
                            print(f"Error completing enrollment: {e}")
                    
                    # Clear task
                    enroll_task = None

            else:
                # Normal Kiosk Scanning Mode
                res = zkfp.AcquireFingerprint()
                if res:
                    tmp, img = res
                    if len(id_map) > 0:
                        fid, score = zkfp.DBIdentify(tmp)
                        if score >= MATCH_THRESHOLD:
                            user_info = id_map.get(fid)
                            if user_info:
                                emp_id = user_info['employee_id']
                                now = time.time()
                                
                                with state_lock:
                                    last_log = KIOSK_STATE['cooldowns'].get(emp_id, 0)
                                    if now - last_log < 10:  # 10 second cooldown
                                        time.sleep(1)
                                        continue
                                        
                                    print(f"Identified: {user_info['name']} (score: {score})")
                                    KIOSK_STATE['last_scan'] = {
                                        'employee_id': emp_id,
                                        'name': user_info['name'],
                                        'timestamp': now
                                    }
                                    KIOSK_STATE['cooldowns'][emp_id] = now
                                time.sleep(2)
                        else:
                            with state_lock:
                                KIOSK_STATE['last_error'] = {
                                    'message': 'Fingerprint not recognized.',
                                    'timestamp': time.time()
                                }
                            time.sleep(1.5)

            time.sleep(0.1)

        except Exception as e:
            import traceback
            print(f"Scanner loop exception:\n{traceback.format_exc()}")
            time.sleep(1)

    try:
        zkfp.CloseDevice()
        zkfp.Terminate()
    except:
        pass

    with state_lock:
        KIOSK_STATE['status'] = 'stopped'
    print("Scanner thread permanently stopped.")


def start_device_thread():
    """Starts the scanner thread if not running."""
    global _running, _thread_handle
    with state_lock:
        if _running:
            return
        _running = True
    _thread_handle = threading.Thread(target=_scanner_loop)
    _thread_handle.daemon = True
    _thread_handle.start()

def stop_device_thread():
    """Signals the scanner thread to shut down."""
    global _running
    with state_lock:
        _running = False
