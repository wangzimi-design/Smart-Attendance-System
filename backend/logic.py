from .db_handler import DatabaseHandler
import datetime

class AttendanceManager:
    def __init__(self):
        self.db = DatabaseHandler()

    def mark_attendance(self, student_id, status="Present"):
        today = datetime.date.today().strftime("%Y-%m-%d")
        self.db.save_attendance(today, student_id, status)

    def get_stats(self):
        df = self.db.get_attendance_report()
        return df