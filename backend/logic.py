from .db_handler import DatabaseHandler
import datetime
import pandas as pd

class AttendanceManager:
    def __init__(self):
        self.db = DatabaseHandler()
        self.statuses = ["Present", "Absent", "Late", "Excused"]

    def mark_attendance(self, student_id, status, date=None):
        if date is None:
            date = datetime.date.today().strftime("%Y-%m-%d")
        self.db.save_attendance(date, student_id, status)

    def get_full_analytics(self):
        df = self.db.get_attendance_report()
        if df.empty: return df, None
        
        # 计算每个学生的出勤率
        stats = df.groupby(['id', 'name']).agg(
            Total_Days=('status', 'count'),
            Present_Days=('status', lambda x: (x == 'Present').sum())
        ).reset_index()
        stats['Attendance_Rate'] = (stats['Present_Days'] / stats['Total_Days'] * 100).round(1)
        return df, stats

    def get_alerts(self, threshold=75.0):
        _, stats = self.get_full_analytics()
        if stats is None: return []
        return stats[stats['Attendance_Rate'] < threshold]