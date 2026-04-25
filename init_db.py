"""
Run this once to create the database tables:
    python init_db.py
"""
from db import get_connection
from mysql.connector import Error

DDL_USERS = """
CREATE TABLE IF NOT EXISTS tblusers (
    id            INT          NOT NULL AUTO_INCREMENT,
    username      VARCHAR(100) NOT NULL UNIQUE,
    password      VARCHAR(255) NOT NULL,
    name          VARCHAR(150) NOT NULL,
    role          VARCHAR(50)  NOT NULL,
    employee_id   VARCHAR(20)  NULL,
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
                               ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

DDL_PAYROLL = """
CREATE TABLE IF NOT EXISTS tblpayroll (
    id            INT          NOT NULL AUTO_INCREMENT,
    period_key    VARCHAR(20)  NOT NULL UNIQUE,
    year          INT          NOT NULL,
    month         INT          NOT NULL,
    half          INT          NOT NULL,
    status        VARCHAR(30)  NOT NULL DEFAULT 'Draft',
    remarks       TEXT         NULL,
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
                               ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

DDL_PAYROLL_DETAILS = """
CREATE TABLE IF NOT EXISTS tblpayroll_details (
    id            INT          NOT NULL AUTO_INCREMENT,
    period_key    VARCHAR(20)  NOT NULL,
    employee_id   VARCHAR(20)  NOT NULL,
    basic_salary  DECIMAL(10,2) DEFAULT 0,
    half_basic    DECIMAL(10,2) DEFAULT 0,
    other_earnings DECIMAL(10,2) DEFAULT 0,
    other_deductions DECIMAL(10,2) DEFAULT 0,
    daily_rate    DECIMAL(10,2) DEFAULT 0,
    absent_days   INT          DEFAULT 0,
    absent_deduction DECIMAL(10,2) DEFAULT 0,
    late_minutes  INT          DEFAULT 0,
    tardiness_deduction DECIMAL(10,2) DEFAULT 0,
    undertime_minutes INT          DEFAULT 0,
    undertime_deduction DECIMAL(10,2) DEFAULT 0,
    holiday_pay   DECIMAL(10,2) DEFAULT 0,
    leave_deduction DECIMAL(10,2) DEFAULT 0,
    total_gross   DECIMAL(10,2) DEFAULT 0,
    total_deduct  DECIMAL(10,2) DEFAULT 0,
    net_pay       DECIMAL(10,2) DEFAULT 0,
    is_negative   TINYINT(1)   DEFAULT 0,
    dtr_filed     TINYINT(1)   DEFAULT 0,
    payheads_json JSON         NULL,
    statutory_json JSON        NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_pd_payroll FOREIGN KEY (period_key) REFERENCES tblpayroll(period_key) ON DELETE CASCADE,
    CONSTRAINT fk_pd_emp FOREIGN KEY (employee_id) REFERENCES tblemployee(employee_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

DDL = """
CREATE TABLE IF NOT EXISTS tblemployee (
    id            INT          NOT NULL AUTO_INCREMENT,
    employee_id   VARCHAR(20)  NOT NULL UNIQUE,
    first_name    VARCHAR(80)  NOT NULL,
    last_name     VARCHAR(80)  NOT NULL,
    designation   VARCHAR(120) NOT NULL,
    birthday      DATE         NULL,
    email         VARCHAR(150) NOT NULL,
    contact       VARCHAR(30)  NOT NULL,
    address       TEXT         NOT NULL,
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
                               ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

DDL_FINGERPRINTS = """
CREATE TABLE IF NOT EXISTS fingerprints (
    id                   INT          NOT NULL AUTO_INCREMENT,
    employee_id          VARCHAR(20)  NULL,
    user_name            VARCHAR(150) NOT NULL,
    fingerprint_template TEXT         NOT NULL,
    created_at           DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    CONSTRAINT fk_fingerprint_employee
        FOREIGN KEY (employee_id)
        REFERENCES tblemployee (employee_id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

DDL2 = """
CREATE TABLE IF NOT EXISTS tblpayhead (
    id            INT            NOT NULL AUTO_INCREMENT,
    employee_id   VARCHAR(20)    NOT NULL,
    pay_head      VARCHAR(120)   NOT NULL,
    description   TEXT,
    amount        DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    mode          ENUM('Amount', 'Percentage') DEFAULT 'Amount',
    percentage_value DECIMAL(10, 2) DEFAULT 0.00,
    created_at    DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP
                                 ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    CONSTRAINT fk_payhead_employee
        FOREIGN KEY (employee_id)
        REFERENCES tblemployee (employee_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

DDL_BIO = """
CREATE TABLE IF NOT EXISTS tblbiometric_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(20) NOT NULL,
    log_type VARCHAR(20) NOT NULL,
    log_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_bio_emp FOREIGN KEY (employee_id) REFERENCES tblemployee(employee_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

DDL_HOLIDAYS = """
CREATE TABLE IF NOT EXISTS tblholidays (
    id INT AUTO_INCREMENT PRIMARY KEY,
    holiday_date DATE NOT NULL,
    holiday_name VARCHAR(150) NOT NULL,
    holiday_type VARCHAR(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

DDL_LEAVES = """
CREATE TABLE IF NOT EXISTS tblleaves (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(20) NOT NULL,
    leave_date DATE NOT NULL,
    leave_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending',
    CONSTRAINT fk_leave_emp FOREIGN KEY (employee_id) REFERENCES tblemployee(employee_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

DDL_GLOBAL_PAYHEADS = """
CREATE TABLE IF NOT EXISTS tblglobal_payheads (
    id            INT            NOT NULL AUTO_INCREMENT,
    name          VARCHAR(120)   NOT NULL,
    description   TEXT,
    amount        DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    type          VARCHAR(20)    NOT NULL, -- 'Earning' or 'Deduction'
    mode          ENUM('Amount', 'Percentage') DEFAULT 'Amount',
    percentage_value DECIMAL(10, 2) DEFAULT 0.00,
    created_at    DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

DDL_STATUTORY_REGISTRY = """
CREATE TABLE IF NOT EXISTS tblstatutory_registry (
    id            INT            NOT NULL AUTO_INCREMENT,
    config_key    VARCHAR(100)   NOT NULL UNIQUE,
    config_value  VARCHAR(255)   NOT NULL,
    config_mode   ENUM('Amount', 'Percentage') DEFAULT 'Percentage',
    description   TEXT           NULL,
    updated_at    DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

def _add_column_if_missing(cur, table, column, alter_sql):
    """Add a column only if it doesn't already exist (compatible with all MySQL versions)."""
    cur.execute(
        "SELECT COUNT(*) as cnt FROM INFORMATION_SCHEMA.COLUMNS "
        "WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME=%s AND COLUMN_NAME=%s",
        (table, column)
    )
    row = cur.fetchone()
    cnt = row['cnt'] if isinstance(row, dict) else row[0]
    if cnt == 0:
        cur.execute(alter_sql)


def init():
    try:
        conn = get_connection()
        cur  = conn.cursor(dictionary=True)
        cur.execute(DDL)
        cur.execute(DDL2)
        cur.execute(DDL_FINGERPRINTS)
        cur.execute(DDL_BIO)
        cur.execute(DDL_USERS)
        cur.execute(DDL_PAYROLL)
        cur.execute(DDL_PAYROLL_DETAILS)
        cur.execute(DDL_HOLIDAYS)
        cur.execute(DDL_LEAVES)
        cur.execute(DDL_GLOBAL_PAYHEADS)
        cur.execute(DDL_STATUTORY_REGISTRY)

        # ── Safe column migrations (works on all MySQL versions) ───────────────
        migrations = [
            ('tblpayroll',         'approved_by',     'ALTER TABLE tblpayroll ADD COLUMN approved_by VARCHAR(150) NULL AFTER remarks'),
            ('tblpayroll',         'approved_at',     'ALTER TABLE tblpayroll ADD COLUMN approved_at DATETIME NULL AFTER approved_by'),
            ('tblpayroll_details', 'holiday_pay',     'ALTER TABLE tblpayroll_details ADD COLUMN holiday_pay DECIMAL(10,2) DEFAULT 0 AFTER other_earnings'),
            ('tblpayroll_details', 'undertime_minutes', 'ALTER TABLE tblpayroll_details ADD COLUMN undertime_minutes INT DEFAULT 0 AFTER tardiness_deduction'),
            ('tblpayroll_details', 'undertime_deduction', 'ALTER TABLE tblpayroll_details ADD COLUMN undertime_deduction DECIMAL(10,2) DEFAULT 0 AFTER undertime_minutes'),
            ('tblpayroll_details', 'sss_ee',          'ALTER TABLE tblpayroll_details ADD COLUMN sss_ee DECIMAL(10,2) DEFAULT 0 AFTER undertime_deduction'),
            ('tblpayroll_details', 'philhealth_ee',   'ALTER TABLE tblpayroll_details ADD COLUMN philhealth_ee DECIMAL(10,2) DEFAULT 0 AFTER sss_ee'),
            ('tblpayroll_details', 'pagibig_ee',      'ALTER TABLE tblpayroll_details ADD COLUMN pagibig_ee DECIMAL(10,2) DEFAULT 0 AFTER philhealth_ee'),
            ('tblpayroll_details', 'withholding_tax', 'ALTER TABLE tblpayroll_details ADD COLUMN withholding_tax DECIMAL(10,2) DEFAULT 0 AFTER pagibig_ee'),
            ('tblpayroll_details', 'is_negative',     'ALTER TABLE tblpayroll_details ADD COLUMN is_negative TINYINT(1) DEFAULT 0 AFTER net_pay'),
            ('tblpayroll_details', 'payheads_json',   'ALTER TABLE tblpayroll_details ADD COLUMN payheads_json JSON NULL AFTER dtr_filed'),
            ('tblpayroll_details', 'statutory_json',  'ALTER TABLE tblpayroll_details ADD COLUMN statutory_json JSON NULL AFTER payheads_json'),
            ('tblpayhead',         'mode',            "ALTER TABLE tblpayhead ADD COLUMN mode ENUM('Amount', 'Percentage') DEFAULT 'Amount' AFTER amount"),
            ('tblpayhead',         'percentage_value', "ALTER TABLE tblpayhead ADD COLUMN percentage_value DECIMAL(10, 2) DEFAULT 0.00 AFTER mode"),
            ('tblpayhead',         'description',      "ALTER TABLE tblpayhead ADD COLUMN description TEXT AFTER pay_head"),
            ('tblglobal_payheads', 'mode',            "ALTER TABLE tblglobal_payheads ADD COLUMN mode ENUM('Amount', 'Percentage') DEFAULT 'Amount' AFTER amount"),
            ('tblglobal_payheads', 'percentage_value', "ALTER TABLE tblglobal_payheads ADD COLUMN percentage_value DECIMAL(10, 2) DEFAULT 0.00 AFTER mode"),
            ('tblglobal_payheads', 'description',      "ALTER TABLE tblglobal_payheads ADD COLUMN description TEXT AFTER name"),
            ('tblstatutory_registry', 'config_mode',  "ALTER TABLE tblstatutory_registry ADD COLUMN config_mode ENUM('Amount', 'Percentage') DEFAULT 'Percentage' AFTER config_value"),
        ]
        for table, col, sql in migrations:
            _add_column_if_missing(cur, table, col, sql)

        # Ensure finger_index exists on fingerprints
        _add_column_if_missing(cur, 'fingerprints', 'finger_index', "ALTER TABLE fingerprints ADD COLUMN finger_index INT DEFAULT 1")
        
        # Try adding unique constraint for (employee_id, finger_index) if not exist
        try:
            cur.execute("ALTER TABLE fingerprints ADD UNIQUE KEY idx_emp_finger (employee_id, finger_index)")
        except Exception:
            pass # Probably already exists
        
        # Seed users
        users = [
            ('admin', 'admin123', 'Overall Admin', 'Admin', None),
            ('finance', 'finance123', 'Finance Dept', 'Finance', None),
            ('hr', 'hr1234', 'HR Dept', 'HR', None),
            ('bjohnlenard@gmail.com', 'EMP-001', 'John Lenard Bocal', 'Employee', 'EMP-001')
        ]
        for u in users:
            cur.execute("SELECT id FROM tblusers WHERE username=%s", (u[0],))
            if not cur.fetchone():
                cur.execute("INSERT INTO tblusers (username, password, name, role, employee_id) VALUES (%s, %s, %s, %s, %s)", u)

        # Seed 2026 PH Holidays
        holidays = [
            ('2026-01-01', 'New Year\'s Day', 'Regular'),
            ('2026-02-25', 'EDSA People Power Revolution', 'Special'),
            ('2026-04-02', 'Maundy Thursday', 'Regular'),
            ('2026-04-03', 'Good Friday', 'Regular'),
            ('2026-04-09', 'Araw ng Kagitingan', 'Regular'),
            ('2026-05-01', 'Labor Day', 'Regular'),
            ('2026-06-12', 'Independence Day', 'Regular'),
            ('2026-08-21', 'Ninoy Aquino Day', 'Special'),
            ('2026-08-31', 'National Heroes Day', 'Regular'),
            ('2026-11-01', 'All Saints\' Day', 'Special'),
            ('2026-11-30', 'Bonifacio Day', 'Regular'),
            ('2026-12-25', 'Christmas Day', 'Regular'),
            ('2026-12-30', 'Rizal Day', 'Regular')
        ]
        for h in holidays:
            cur.execute("SELECT id FROM tblholidays WHERE holiday_date=%s", (h[0],))
            if not cur.fetchone():
                cur.execute("INSERT INTO tblholidays (holiday_date, holiday_name, holiday_type) VALUES (%s, %s, %s)", h)

        # Seed Statutory Config
        stat_configs = [
            ('PHIC_RATE', '0.05', 'Percentage', 'PhilHealth employee+employer combined rate'),
            ('PHIC_CAP',  '5000.00', 'Amount', 'Maximum monthly PhilHealth total contribution'),
            ('PHIC_FLOOR', '500.00', 'Amount', 'Minimum monthly PhilHealth total contribution'),
            ('PAGIBIG_EE_RATE', '0.02', 'Percentage', 'Pag-IBIG employee rate'),
            ('PAGIBIG_EE_CAP', '100.00', 'Amount', 'Maximum semi-monthly Pag-IBIG employee share'),
            ('SSS_ENABLED', '1', 'Amount', 'Enable SSS calculations (1=Yes, 0=No)'),
            ('BIR_ENABLED', '1', 'Amount', 'Enable Withholding Tax (1=Yes, 0=No)')
        ]
        for k, v, m, d in stat_configs:
            cur.execute("SELECT id FROM tblstatutory_registry WHERE config_key=%s", (k,))
            if not cur.fetchone():
                cur.execute("INSERT INTO tblstatutory_registry (config_key, config_value, config_mode, description) VALUES (%s, %s, %s, %s)", (k, v, m, d))

        conn.commit()
        cur.close()
        conn.close()
        print("[OK] Tables created/migrated: tblemployee, tblpayhead, fingerprints, tblusers, tblpayroll, tblpayroll_details, tblholidays, tblleaves")
    except Error as e:
        print(f"[ERROR] Database error: {e}")

if __name__ == '__main__':
    init()