import threading
import time
import base64
from flask import Blueprint, jsonify
from mysql.connector import Error
from db import db_cursor
from pyzkfp import ZKFP2

fingerprint_bp = Blueprint('fingerprints', __name__, url_prefix='/api/fingerprint')

MATCH_THRESHOLD = 55

from routes.scanner_manager import ENROLLMENT_STATE, state_lock, start_device_thread

# Helper functions get_all_fingerprints and the old run_enrollment have been migrated
# to scanner_manager.py to prevent singleton access conflicts.


@fingerprint_bp.route('/enroll/<emp_id>/<int:finger_index>', methods=['POST'])
def start_enrollment(emp_id, finger_index):
    with state_lock:
        if ENROLLMENT_STATE['status'] == 'enrolling':
            return jsonify({'error': 'Scanner is currently in use by another enrollment process.'}), 409
        
        ENROLLMENT_STATE['status'] = 'enrolling'
        ENROLLMENT_STATE['step'] = 0
        ENROLLMENT_STATE['message'] = 'Initializing scanner...'
        ENROLLMENT_STATE['error'] = ''
        ENROLLMENT_STATE['employee_id'] = emp_id
        ENROLLMENT_STATE['finger_index'] = finger_index

    # Make sure the global scanner engine is running so it can process the scans
    start_device_thread()

    return jsonify({'message': 'Enrollment started.'}), 200


@fingerprint_bp.route('/enroll_status', methods=['GET'])
def get_status():
    with state_lock:
        return jsonify({
            'status': ENROLLMENT_STATE['status'],
            'step': ENROLLMENT_STATE['step'],
            'message': ENROLLMENT_STATE['message'],
            'error': ENROLLMENT_STATE['error']
        })


@fingerprint_bp.route('/enroll_cancel', methods=['POST'])
def cancel_enrollment():
    with state_lock:
        if ENROLLMENT_STATE['status'] == 'enrolling':
            ENROLLMENT_STATE['status'] = 'error'
            ENROLLMENT_STATE['error'] = 'Enrollment cancelled by user.'
    return jsonify({'message': 'Cancelled'}), 200
