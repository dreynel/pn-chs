"""
Clean database script: Retains ONLY John Lenard Bocal as user/employee,
and populates sample time logs for 1st Half of August 2026 (Aug 1-15).
"""
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))

from db import db_cursor
from services.policy_engine import LeavePolicyService, AttendancePolicyService

def clean_and_seed():
    print("[INIT] Cleaning database...")
    with db_cursor(commit=True) as (conn, cur):
        # 1. Clean transactions, logs, payroll, leaves
        cur.execute("DELETE FROM tbltime_logs")
        cur.execute("DELETE FROM tblleave_transactions")
        cur.execute("DELETE FROM tblleaves")
        cur.execute("DELETE FROM tblaudit_logs")
        cur.execute("DELETE FROM tblpayroll_details")
        cur.execute("DELETE FROM tblpayroll")
        cur.execute("DELETE FROM tblenrollment_tasks")
        cur.execute("DELETE FROM fingerprints")
        cur.execute("DELETE FROM tblpayhead WHERE employee_id != 'EMP-001'")
        cur.execute("DELETE FROM tblleave_balances WHERE employee_id != 'EMP-001'")
        cur.execute("DELETE FROM tblemployee WHERE employee_id != 'EMP-001'")
        cur.execute("DELETE FROM tblusers")

        # 2. Ensure John Lenard Bocal exists in tblemployee
        cur.execute("SELECT id FROM tblemployee WHERE employee_id = 'EMP-001'")
        emp_exists = cur.fetchone()
        if not emp_exists:
            cur.execute("""
                INSERT INTO tblemployee (employee_id, first_name, last_name, designation, employee_type, birthday, email, contact, address)
                VALUES ('EMP-001', 'John Lenard', 'Bocal', 'Teacher I', 'TEACHING', '1995-05-15', 'john.lenard@school.edu.ph', '+63 917 123 4567', 'Puerto Princesa City, Palawan')
            """)
        else:
            cur.execute("""
                UPDATE tblemployee
                SET first_name='John Lenard', last_name='Bocal', designation='Teacher I', employee_type='TEACHING',
                    email='john.lenard@school.edu.ph', contact='+63 917 123 4567', address='Puerto Princesa City, Palawan'
                WHERE employee_id='EMP-001'
            """)

        # 3. Ensure User Login Credentials in tblusers
        cur.execute("DELETE FROM tblusers")
        cur.execute("""
            INSERT INTO tblusers (username, password, name, role, employee_id)
            VALUES 
            ('admin', 'admin123', 'John Lenard Bocal', 'Admin', 'EMP-001'),
            ('hr', 'hr1234', 'John Lenard Bocal (HR)', 'HR', 'EMP-001'),
            ('finance', 'finance123', 'John Lenard Bocal (Finance)', 'Finance', 'EMP-001'),
            ('john.lenard@school.edu.ph', 'user123', 'John Lenard Bocal', 'Employee', 'EMP-001')
        """)

        # 4. Pay heads for John Lenard Bocal (Basic Salary Grade 11 Step 1 = ₱27,000, PERA = ₱2,000)
        cur.execute("DELETE FROM tblpayhead WHERE employee_id = 'EMP-001'")
        cur.execute("""
            INSERT INTO tblpayhead (employee_id, pay_head, amount, mode)
            VALUES 
            ('EMP-001', 'Basic Salary', 27000.00, 'Amount'),
            ('EMP-001', 'PERA', 2000.00, 'Amount')
        """)

        # 5. Initialize Leave Balances (0 mins VL, 0 mins SL - No credits available)
        cur.execute("DELETE FROM tblleave_balances WHERE employee_id = 'EMP-001'")
        cur.execute("""
            INSERT INTO tblleave_balances (employee_id, vl_minutes, sl_minutes)
            VALUES ('EMP-001', 0, 0)
        """)

        print("[SEED] Seeding sample time logs for 1st Half of August 2026 (Aug 1 - Aug 15)...")

        # Schedule for TEACHING: AM 07:30-11:30, PM 13:00-17:00
        sample_logs = [
            # (day, am_in, am_out, pm_in, pm_out, actual_class, teach_rel, approved, remarks)
            (1, None, None, None, None, 0, 0, True, 'Weekend'),
            (2, None, None, None, None, 0, 0, True, 'Weekend'),
            (3, '07:25:00', '11:30:00', '12:55:00', '17:01:00', 360, 120, True, 'On time'),
            (4, '07:40:00', '11:30:00', '12:58:00', '17:00:00', 360, 120, True, '10m Tardy - AM Traffic'),
            (5, '07:28:00', '11:30:00', '12:59:00', '17:00:00', 360, 120, True, 'On time'),
            (6, '07:30:00', '11:30:00', '13:00:00', '16:45:00', 360, 120, True, '15m Undertime - Official Meeting'),
            (7, '07:26:00', '11:30:00', '12:58:00', '17:02:00', 360, 120, True, 'On time'),
            (8, None, None, None, None, 0, 0, True, 'Weekend'),
            (9, None, None, None, None, 0, 0, True, 'Weekend'),
            (10, '07:27:00', '11:30:00', '12:57:00', '17:00:00', 360, 120, True, 'On time'),
            (11, '07:42:00', '11:30:00', '13:00:00', '17:00:00', 360, 120, True, '12m Tardy - Rain'),
            (12, '07:29:00', '11:30:00', '12:58:00', '17:00:00', 360, 120, True, 'On time'),
            (13, '07:30:00', '11:30:00', '12:59:00', '17:05:00', 360, 120, True, 'On time'),
            (14, '07:24:00', '11:30:00', '12:55:00', '17:00:00', 360, 120, True, 'On time'),
            (15, None, None, None, None, 0, 0, True, 'Weekend'),
        ]

        for item in sample_logs:
            day, am_in, am_out, pm_in, pm_out, actual_class, teach_rel, approved, remarks = item
            if am_in is None:
                continue # Skip weekend logs

            w_date = date(2026, 8, day)
            
            calc = AttendancePolicyService.calculate_tardiness_and_undertime(
                'TEACHING', 'Teacher I', am_in, am_out, pm_in, pm_out,
                actual_classroom_minutes=actual_class,
                teaching_related_minutes=teach_rel,
                teaching_related_approved=approved
            )
            late = calc['tardiness_minutes']
            under = calc['undertime_minutes']

            # Process leave deduction
            proc = LeavePolicyService.process_tardiness_and_undertime(
                cur, 'EMP-001', w_date, late, under, reference_id=f"LOG-202608{day:02d}", user_name='System'
            )

            cur.execute("""
                INSERT INTO tbltime_logs (
                    employee_id, work_date, am_time_in, am_time_out, pm_time_in, pm_time_out,
                    actual_classroom_teaching_minutes, teaching_related_minutes, teaching_related_approved,
                    tardiness_minutes, undertime_minutes, vl_minutes_charged, unpaid_minutes, remarks
                ) VALUES (
                    'EMP-001', %s, %s, %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s, %s, %s
                )
            """, (
                w_date, am_in, am_out, pm_in, pm_out,
                actual_class, teach_rel, 1 if approved else 0,
                late, under, proc['total_vl_charged'], proc['total_lwop_minutes'], remarks
            ))

    print("[SUCCESS] Database cleaned and populated cleanly! Only John Lenard Bocal (EMP-001) remains with sample August 1-15 DTR logs.")

if __name__ == '__main__':
    clean_and_seed()
