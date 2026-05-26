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
        # 1. 学生库 (全局)
        cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                            id TEXT PRIMARY KEY, 
                            name TEXT, 
                            department TEXT)''')
        # 2. 课程库 (增加 professor 字段实现多租户隔离)
        cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
                            id TEXT PRIMARY KEY, 
                            name TEXT, 
                            professor TEXT)''')
        # 3. 考勤库 (复合主键防止重复)
        cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                            date TEXT, 
                            student_id TEXT, 
                            course_id TEXT, 
                            status TEXT,
                            PRIMARY KEY (date, student_id, course_id))''')
        # 4. 系统日志库
        cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
                            user TEXT, 
                            action TEXT)''')
        self.conn.commit()

    # --- 课程管理 (带教授身份验证) ---
    def add_course(self, c_id, name, professor):
        try:
            self.conn.cursor().execute("INSERT INTO courses VALUES (?, ?, ?)", (c_id, name, professor))
            self.conn.commit()
            self.add_log(professor, f"Created course: {name} ({c_id})")
            return True
        except: return False

    def delete_course(self, c_id, professor):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM courses WHERE id = ? AND professor = ?", (c_id, professor))
        cursor.execute("DELETE FROM attendance WHERE course_id = ?", (c_id,))
        self.conn.commit()
        self.add_log(professor, f"Deleted course: {c_id}")

    def get_courses_by_professor(self, professor):
        return pd.read_sql(f"SELECT * FROM courses WHERE professor = '{professor}'", self.conn)

    # --- 学生管理 ---
    def add_student(self, s_id, name, dept="General"):
        try:
            self.conn.cursor().execute("INSERT OR IGNORE INTO students VALUES (?, ?, ?)", (s_id, name, dept))
            self.conn.commit()
            return True
        except: return False

    def get_all_students(self):
        return pd.read_sql("SELECT * FROM students", self.conn)

    # --- 考勤核心逻辑 ---
    def save_batch_attendance(self, attendance_list):
        cursor = self.conn.cursor()
        cursor.executemany("INSERT OR REPLACE INTO attendance VALUES (?, ?, ?, ?)", attendance_list)
        self.conn.commit()

    def get_attendance_report(self, course_id):
        query = f"""
        SELECT a.date, s.id as student_id, s.name as student_name, s.department, a.status 
        FROM attendance a 
        JOIN students s ON a.student_id = s.id
        WHERE a.course_id = '{course_id}'
        ORDER BY a.date DESC
        """
        return pd.read_sql(query, self.conn)

    # --- 日志系统 ---
    def add_log(self, user, action):
        self.conn.cursor().execute("INSERT INTO logs (user, action) VALUES (?, ?)", (user, action))
        self.conn.commit()