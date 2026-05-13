import sqlite3
import pandas as pd
import os

class DatabaseHandler:
    def __init__(self, db_path="backend/data/attendance.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()
        # 创建学生表
        cursor.execute('''CREATE TABLE IF NOT EXISTS students (id TEXT PRIMARY KEY, name TEXT)''')
        # 创建考勤表
        cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (date TEXT, student_id TEXT, status TEXT)''')
        self.conn.commit()

    def add_student(self, s_id, name):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO students VALUES (?, ?)", (s_id, name))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass # 学生已存在

    def get_all_students(self):
        return pd.read_sql("SELECT * FROM students", self.conn)

    def save_attendance(self, date, s_id, status):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO attendance VALUES (?, ?, ?)", (date, s_id, status))
        self.conn.commit()

    def get_attendance_report(self):
        query = """
        SELECT a.date, s.id, s.name, a.status 
        FROM attendance a 
        JOIN students s ON a.student_id = s.id
        """
        return pd.read_sql(query, self.conn)