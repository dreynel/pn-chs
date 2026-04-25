import os
import requests
from flask import Flask, render_template, jsonify, request
from scanner_manager import KIOSK_STATE, start_device_thread

app = Flask(__name__)

CLOUD_API_URL = os.environ.get('CLOUD_API_URL', 'http://127.0.0.1:5000')

@app.route('/')
def redirect_to_kiosk():
    return render_template('kiosk.html')

@app.route('/kiosk')
def kiosk():
    return render_template('kiosk.html')

@app.route('/api/attendance/start', methods=['POST'])
def start_kiosk():
    KIOSK_STATE['last_scan'] = None
    KIOSK_STATE['last_error'] = None
    start_device_thread()
    return jsonify({'message': 'Scanner started'})

@app.route('/api/attendance/stop', methods=['POST'])
def stop_kiosk():
    # Keep it running usually, but satisfy the Kiosk JS if it calls it
    return jsonify({'message': 'Stopping...'})

@app.route('/api/attendance/poll', methods=['GET'])
def poll_kiosk():
    import time
    return jsonify({
        'status': KIOSK_STATE['status'],
        'last_scan': KIOSK_STATE['last_scan'],
        'last_error': KIOSK_STATE['last_error'],
        'server_time': time.time()
    })

@app.route('/api/attendance/log', methods=['POST'])
def log_attendance():
    # Forward the log to the Cloud API
    data = request.json
    try:
        resp = requests.post(f"{CLOUD_API_URL}/api/attendance/log", json=data)
        if resp.ok:
            return jsonify({'message': 'Forwarded successfully'}), 200
        else:
            return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({'error': f"Failed to reach Cloud API: {e}"}), 500

if __name__ == '__main__':
    # Local runs on port 5001 so it doesn't conflict with Cloud on 5000 during dev
    app.run(host='0.0.0.0', port=5001, debug=True)
