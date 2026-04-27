from flask import Blueprint, jsonify, request
from mysql.connector import Error
from db import db_cursor

employee_bp = Blueprint('employees', __name__, url_prefix='/api/employees')


# ── Helpers ────────────────────────────────────────────────────────────────────

def _next_employee_id(cur):
    """Generate the next EMP-XXX id based on the highest existing one."""
    cur.execute("SELECT employee_id FROM tblemployee ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    if not row:
        return "EMP-001"
    last = row["employee_id"]
    try:
        num = int(last.split("-")[1]) + 1
    except (IndexError, ValueError):
        num = 1
    return f"EMP-{num:03d}"


def _get_payheads(cur, employee_id):
    cur.execute(
        "SELECT id, pay_head, description, amount, category, mode, percentage_value FROM tblpayhead WHERE employee_id = %s ORDER BY id",
        (employee_id,)
    )
    rows = cur.fetchall()
    return [{
        "id": r["id"], 
        "pay_head": r["pay_head"], 
        "description": r["description"],
        "amount": float(r["amount"]), 
        "category": r["category"],
        "mode": r["mode"],
        "percentage_value": float(r["percentage_value"])
    } for r in rows]


def _get_enrolled_fingers(cur, employee_id):
    cur.execute("SELECT finger_index FROM fingerprints WHERE employee_id = %s ORDER BY finger_index", (employee_id,))
    rows = cur.fetchall()
    return [int(r["finger_index"]) for r in rows]


def _row_to_dict(row, pay_heads, enrolled_fingers=None):
    return {
        "id":          row["employee_id"],
        "first_name":  row["first_name"],
        "last_name":   row["last_name"],
        "designation": row["designation"],
        "birthday":    str(row["birthday"]) if row["birthday"] else "",
        "email":       row["email"],
        "contact":     row["contact"],
        "address":     row["address"],
        "pay_heads":   pay_heads,
        "enrolled_fingers": enrolled_fingers or []
    }


# ── LIST ───────────────────────────────────────────────────────────────────────
@employee_bp.route('/', methods=['GET'])
def list_employees():
    q = request.args.get('q', '').strip()
    try:
        with db_cursor() as (conn, cur):
            if q:
                like = f"%{q}%"
                cur.execute("""
                    SELECT employee_id, first_name, last_name, designation
                    FROM tblemployee
                    WHERE first_name  LIKE %s
                       OR last_name   LIKE %s
                       OR employee_id LIKE %s
                       OR designation LIKE %s
                    ORDER BY id
                """, (like, like, like, like))
            else:
                cur.execute("""
                    SELECT employee_id, first_name, last_name, designation
                    FROM tblemployee ORDER BY id
                """)
            rows = cur.fetchall()
        return jsonify([{
            "id":          r["employee_id"],
            "first_name":  r["first_name"],
            "last_name":   r["last_name"],
            "designation": r["designation"],
        } for r in rows])
    except Error as e:
        return jsonify({"error": str(e)}), 500


# ── GET ONE ────────────────────────────────────────────────────────────────────
@employee_bp.route('/<emp_id>', methods=['GET'])
def get_employee(emp_id):
    try:
        with db_cursor() as (conn, cur):
            cur.execute("SELECT * FROM tblemployee WHERE employee_id = %s", (emp_id,))
            row = cur.fetchone()
            if not row:
                return jsonify({"error": "Employee not found"}), 404
            pay_heads = _get_payheads(cur, emp_id)
            enrolled_fingers = _get_enrolled_fingers(cur, emp_id)
        return jsonify(_row_to_dict(row, pay_heads, enrolled_fingers))
    except Error as e:
        return jsonify({"error": str(e)}), 500


# ── CREATE ─────────────────────────────────────────────────────────────────────
@employee_bp.route('/', methods=['POST'])
def create_employee():
    data = request.get_json(force=True)
    required = ['first_name', 'last_name', 'designation', 'birthday', 'email', 'contact', 'address']
    for field in required:
        if not str(data.get(field, '')).strip():
            return jsonify({"error": f"'{field}' is required"}), 400
    try:
        with db_cursor(commit=True) as (conn, cur):
            new_id = _next_employee_id(cur)
            cur.execute("""
                INSERT INTO tblemployee
                    (employee_id, first_name, last_name, designation, birthday, email, contact, address)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                new_id,
                data['first_name'].strip(),
                data['last_name'].strip(),
                data['designation'].strip(),
                data['birthday'] or None,
                data['email'].strip(),
                data['contact'].strip(),
                data['address'].strip(),
            ))
            for ph in data.get('pay_heads', []):
                if str(ph.get('pay_head', '')).strip():
                    cur.execute(
                        "INSERT INTO tblpayhead (employee_id, pay_head, description, amount, category, mode, percentage_value) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (new_id, ph['pay_head'].strip(), ph.get('description', '').strip(), float(ph.get('amount', 0)), ph.get('category', 'Earning'), ph.get('mode', 'Amount'), float(ph.get('percentage_value', 0)))
                    )
            
            # --- CREATE USER LOGIN ---
            # Username/Password = last_name (lowercase, stripped)
            username = data['last_name'].strip().lower()
            password = username
            fullname = f"{data['first_name'].strip()} {data['last_name'].strip()}"
            
            # Check for username collision (tblusers.username is UNIQUE)
            cur.execute("SELECT id FROM tblusers WHERE username = %s", (username,))
            if cur.fetchone():
                # If collision, append employee ID suffix (e.g., smith005)
                username = f"{username}{new_id.split('-')[1]}"
                password = username # Keep password same as username for initial setup
                
            cur.execute(
                "INSERT INTO tblusers (username, password, name, role, employee_id) VALUES (%s, %s, %s, %s, %s)",
                (username, password, fullname, 'Employee', new_id)
            )
            cur.execute("SELECT * FROM tblemployee WHERE employee_id = %s", (new_id,))
            row = cur.fetchone()
            ph_saved = _get_payheads(cur, new_id)
            enrolled_fingers = _get_enrolled_fingers(cur, new_id)
        return jsonify(_row_to_dict(row, ph_saved, enrolled_fingers)), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500


# ── UPDATE ─────────────────────────────────────────────────────────────────────
@employee_bp.route('/<emp_id>', methods=['PUT'])
def update_employee(emp_id):
    data = request.get_json(force=True)
    try:
        with db_cursor(commit=True) as (conn, cur):
            cur.execute("SELECT id FROM tblemployee WHERE employee_id = %s", (emp_id,))
            if not cur.fetchone():
                return jsonify({"error": "Employee not found"}), 404
            cur.execute("""
                UPDATE tblemployee
                SET first_name=%s, last_name=%s, designation=%s,
                    birthday=%s, email=%s, contact=%s, address=%s
                WHERE employee_id=%s
            """, (
                data.get('first_name','').strip(),
                data.get('last_name','').strip(),
                data.get('designation','').strip(),
                data.get('birthday') or None,
                data.get('email','').strip(),
                data.get('contact','').strip(),
                data.get('address','').strip(),
                emp_id,
            ))
            cur.execute("DELETE FROM tblpayhead WHERE employee_id=%s", (emp_id,))
            for ph in data.get('pay_heads', []):
                if str(ph.get('pay_head', '')).strip():
                    cur.execute(
                        "INSERT INTO tblpayhead (employee_id, pay_head, description, amount, category, mode, percentage_value) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (emp_id, ph['pay_head'].strip(), ph.get('description', '').strip(), float(ph.get('amount', 0)), ph.get('category', 'Earning'), ph.get('mode', 'Amount'), float(ph.get('percentage_value', 0)))
                    )
            cur.execute("SELECT * FROM tblemployee WHERE employee_id=%s", (emp_id,))
            row = cur.fetchone()
            ph_saved = _get_payheads(cur, emp_id)
            enrolled_fingers = _get_enrolled_fingers(cur, emp_id)
        return jsonify(_row_to_dict(row, ph_saved, enrolled_fingers))
    except Error as e:
        return jsonify({"error": str(e)}), 500


# ── DELETE ─────────────────────────────────────────────────────────────────────
@employee_bp.route('/<emp_id>', methods=['DELETE'])
def delete_employee(emp_id):
    try:
        with db_cursor(commit=True) as (conn, cur):
            cur.execute("SELECT id FROM tblemployee WHERE employee_id=%s", (emp_id,))
            if not cur.fetchone():
                return jsonify({"error": "Employee not found"}), 404
            
            # Cascade delete to all foreign tables
            cur.execute("DELETE FROM tblpayhead WHERE employee_id=%s", (emp_id,))
            cur.execute("DELETE FROM tblpayroll_details WHERE employee_id=%s", (emp_id,))
            cur.execute("DELETE FROM fingerprints WHERE employee_id=%s", (emp_id,))
            cur.execute("DELETE FROM tblbiometric_logs WHERE employee_id=%s", (emp_id,))
            cur.execute("DELETE FROM tbltime_logs WHERE employee_id=%s", (emp_id,))
            cur.execute("DELETE FROM tblleaves WHERE employee_id=%s", (emp_id,))
            cur.execute("DELETE FROM tblenrollment_tasks WHERE employee_id=%s", (emp_id,))
            cur.execute("DELETE FROM tblusers WHERE employee_id=%s", (emp_id,))
            
            cur.execute("DELETE FROM tblemployee WHERE employee_id=%s", (emp_id,))
        return jsonify({"message": f"Employee {emp_id} deleted successfully."})
    except Error as e:
        return jsonify({"error": str(e)}), 500