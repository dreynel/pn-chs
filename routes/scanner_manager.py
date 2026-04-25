import threading
import time
import base64
from pyzkfp import ZKFP2
from db import db_cursor

MATCH_THRESHOLD = 55

state_lock = threading.RLock()

ENROLLMENT_STATE = {
    'status': 'idle',        # idle, enrolling, success, error
    'step': 0,
    'message': '',
    'error': '',
    'employee_id': None,
    'finger_index': 1
}

KIOSK_STATE = {
    'status': 'stopped',     # stopped, running, error
    'last_scan': None,
    'last_error': None,
    'cooldowns': {}          # employee_id -> last_log_time
}

_thread_handle = None
_running = False


def get_all_fingerprints(cur):
    """Fetch all fingerprints to prevent duplicates."""
    cur.execute("SELECT id, user_name, fingerprint_template FROM fingerprints")
    rows = cur.fetchall()
    users = []
    for r in rows:
        try:
            template_bytes = base64.b64decode(r['fingerprint_template'])
            users.append((r['id'], r['user_name'], template_bytes))
        except Exception:
            pass
    return users


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

    # Load existing fingerprints from DB into the device
    id_map = {}
    try:
        with db_cursor() as (conn, cur):
            users = get_all_fingerprints(cur)
            cur.execute("SELECT employee_id, first_name, last_name FROM tblemployee")
            emps = {row['employee_id']: f"{row['first_name']} {row['last_name']}" for row in cur.fetchall()}

            for row_id, user_name, template in users:
                try:
                    zkfp.DBAdd(row_id, template)
                except Exception as ex:
                    print(f"Failed to DBAdd for row {row_id}: {ex}")

                cur.execute("SELECT employee_id FROM fingerprints WHERE id=%s", (row_id,))
                fr = cur.fetchone()
                if fr and fr['employee_id']:
                    id_map[row_id] = {
                        'employee_id': fr['employee_id'],
                        'name': emps.get(fr['employee_id'], user_name)
                    }
    except Exception as e:
        import traceback
        print(f"Scanner DB Error:\n{traceback.format_exc()}")

    with state_lock:
        KIOSK_STATE['status'] = 'running'

    print("Scanner active. Waiting for operations...")

    # Enrollment state tracking
    enroll_templates = []

    while _running:
        try:
            with state_lock:
                enrolling = (ENROLLMENT_STATE['status'] == 'enrolling')
                enroll_step = ENROLLMENT_STATE['step']
                enroll_emp_id = ENROLLMENT_STATE['employee_id']
                enroll_finger = ENROLLMENT_STATE.get('finger_index', 1)

            if enrolling:
                if enroll_step == 0:
                    with state_lock:
                        ENROLLMENT_STATE['step'] = 1
                        ENROLLMENT_STATE['message'] = "Scan 1/3: Please place your finger firmly on the scanner..."
                    enroll_templates = []
                    time.sleep(0.5)
                    continue

                if enroll_step <= 3:
                    res = zkfp.AcquireFingerprint()
                    if res:
                        tmp, img = res
                        if not tmp or len(tmp) == 0:
                            time.sleep(0.1)
                            continue

                        # Check for duplicates across the DB
                        if len(id_map) > 0:
                            fid, score = zkfp.DBIdentify(tmp)
                            if score >= MATCH_THRESHOLD:
                                matched_name = id_map.get(fid, {}).get('name', 'Unknown')
                                with state_lock:
                                    ENROLLMENT_STATE['status'] = 'error'
                                    ENROLLMENT_STATE['error'] = f"Fingerprint already enrolled for '{matched_name}' (score: {score})."
                                time.sleep(2)
                                continue

                        enroll_templates.append(tmp)
                        with state_lock:
                            ENROLLMENT_STATE['message'] = f"✅ Scan {enroll_step} successful. Please lift your finger."
                            ENROLLMENT_STATE['step'] = enroll_step + 1

                        time.sleep(1.5)  # Wait for finger lift
                else:
                    # Proceed to merge all 3 scans
                    with state_lock:
                        ENROLLMENT_STATE['message'] = "Merging fingerprint data..."

                    merged_template, merged_len = zkfp.DBMerge(*enroll_templates)
                    if merged_template is None or merged_len == 0:
                        with state_lock:
                            ENROLLMENT_STATE['status'] = 'error'
                            ENROLLMENT_STATE['error'] = "Failed to merge templates. Please try enrolling again."
                    else:
                        template_bytes = bytes(merged_template)
                        if 0 < merged_len < len(template_bytes):
                            template_bytes = template_bytes[:merged_len]

                        template_b64 = base64.b64encode(template_bytes).decode('utf-8')

                        try:
                            with db_cursor(commit=True) as (conn, cur):
                                cur.execute("SELECT first_name, last_name FROM tblemployee WHERE employee_id = %s", (enroll_emp_id,))
                                emp = cur.fetchone()
                                user_name = f"{emp['first_name']} {emp['last_name']}" if emp else str(enroll_emp_id)

                                cur.execute("""
                                    INSERT INTO fingerprints (employee_id, user_name, fingerprint_template, finger_index)
                                    VALUES (%s, %s, %s, %s)
                                    ON DUPLICATE KEY UPDATE 
                                        fingerprint_template = VALUES(fingerprint_template),
                                        user_name = VALUES(user_name)
                                """, (enroll_emp_id, user_name, template_b64, enroll_finger))
                                
                                # Since we might have updated an existing row, we fetch the ID
                                cur.execute("SELECT id FROM fingerprints WHERE employee_id=%s AND finger_index=%s", (enroll_emp_id, enroll_finger))
                                res_row = cur.fetchone()
                                new_id = res_row['id'] if res_row else cur.lastrowid


                            # Add to active array to avoid needing a reboot
                            zkfp.DBAdd(new_id, template_bytes)
                            id_map[new_id] = {
                                'employee_id': enroll_emp_id,
                                'name': user_name
                            }

                            with state_lock:
                                ENROLLMENT_STATE['status'] = 'success'
                                ENROLLMENT_STATE['message'] = f"Fingerprint enrolled successfully for {user_name}!"
                        except Exception as ex:
                            with state_lock:
                                ENROLLMENT_STATE['status'] = 'error'
                                ENROLLMENT_STATE['error'] = f"Database Error: {str(ex)}"

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
                                    if now - last_log < 10:  # 10 second cooldown per employee
                                        print(f"Cooldown active for {user_info['name']}")
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
                            print(f"Unknown finger (score: {score})")
                            with state_lock:
                                KIOSK_STATE['last_error'] = {
                                    'message': 'Fingerprint not recognized. Please try again.',
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
