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
        # 学生表：增加专业信息
        cursor.execute('''CREATE TABLE IF NOT EXISTS students (id TEXT PRIMARY KEY, name TEXT, department TEXT)''')
        # 考勤表：保持结构
        cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (date TEXT, student_id TEXT, status TEXT)''')
        self.conn.commit()

    def add_student(self, s_id, name, dept="General"):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO students VALUES (?, ?, ?)", (s_id, name, dept))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def delete_student(self, s_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (s_id,))
        cursor.execute("DELETE FROM attendance WHERE student_id = ?", (s_id,))
        self.conn.commit()

    def get_all_students(self):
        return pd.read_sql("SELECT * FROM students", self.conn)

    def save_attendance(self, date, s_id, status):
        cursor = self.conn.cursor()
        # 如果同一天已存在记录则更新，否则插入 (Upsert 逻辑)
        cursor.execute("""
            INSERT INTO attendance (date, student_id, status) VALUES (?, ?, ?)
            ON CONFLICT DO UPDATE SET status=excluded.status
        """, (date, s_id, status)) # 注意：SQLite 3.24+ 支持此语法
        # 如果版本低，简单处理：
        cursor.execute("DELETE FROM attendance WHERE date=? AND student_id=?", (date, s_id))
        cursor.execute("INSERT INTO attendance VALUES (?, ?, ?)", (date, s_id, status))
        self.conn.commit()

    def get_attendance_report(self):
        query = """
        SELECT a.date, s.id, s.name, s.department, a.status 
        FROM attendance a 
        JOIN students s ON a.student_id = s.id
        ORDER BY a.date DESC
        """
        return pd.read_sql(query, self.conn)