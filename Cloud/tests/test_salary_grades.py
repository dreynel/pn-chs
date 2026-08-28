import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import db_cursor
from init_db import init

class TestSalaryGradeManagement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init()

    def test_salary_grades_seeded(self):
        with db_cursor() as (conn, cur):
            cur.execute("SELECT COUNT(*) AS cnt FROM tblsalary_grades")
            row = cur.fetchone()
            cnt = row['cnt'] if isinstance(row, dict) else row[0]
            self.assertEqual(cnt, 33, "Should have 33 salary grade records in database")

    def test_teacher_positions(self):
        with db_cursor() as (conn, cur):
            cur.execute("SELECT salary_grade, position_title, step_1 FROM tblsalary_grades WHERE salary_grade = 11")
            row = cur.fetchone()
            self.assertEqual(row['position_title'], 'Teacher I')
            self.assertEqual(float(row['step_1']), 31705.00)

            cur.execute("SELECT salary_grade, position_title, step_1 FROM tblsalary_grades WHERE salary_grade = 18")
            row = cur.fetchone()
            self.assertEqual(row['position_title'], 'Master Teacher I')
            self.assertEqual(float(row['step_1']), 53818.00)

if __name__ == '__main__':
    unittest.main()
