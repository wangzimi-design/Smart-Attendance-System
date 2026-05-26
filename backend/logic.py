from .db_handler import DatabaseHandler
import pandas as pd
import datetime
import os

class AttendanceManager:
    def __init__(self):
        self.db = DatabaseHandler()
        # 定义核心四种状态
        self.statuses = ["Present", "Absent", "Late", "Excused"]

    def import_students_from_df(self, df, professor_name):
        """
        从文件批量导入学生。支持模糊匹配列名，确保录入成功。
        """
        success_count = 0
        df.columns = [str(c).lower().strip() for c in df.columns]
        
        for _, row in df.iterrows():
            # 智能识别 ID、姓名、部门
            sid = str(row.get('id', row.get('student_id', row.get('学号', row.iloc[0]))))
            name = str(row.get('name', row.get('student_name', row.get('姓名', row.iloc[1]))))
            dept = str(row.get('department', row.get('dept', 'General')))
            
            if sid and name and sid != 'nan' and name != 'nan':
                if self.db.add_student(sid, name, dept):
                    success_count += 1
        
        self.db.add_log(professor_name, f"Bulk imported {success_count} students via file.")
        return success_count

    def submit_batch_attendance(self, df_edited, date, course_id, professor_name):
        """
        提交批量考勤记录。支持 Present, Absent, Late, Excused 四种状态。
        """
        if df_edited.empty:
            return
            
        batch_data = []
        for _, row in df_edited.iterrows():
            # 检查 ID 列是否存在（根据 app.py 的 data_editor 列名匹配）
            s_id = str(row.get('id', row.get('student_id', '')))
            status = row.get('status', 'Present')
            if s_id:
                batch_data.append((date, s_id, course_id, status))
        
        self.db.save_batch_attendance(batch_data)
        self.db.add_log(professor_name, f"Recorded attendance for {course_id} on {date}")

    def get_full_analytics(self, course_id):
        """
        全量数据分析：计算出席率、缺勤率、迟到率等。
        """
        df = self.db.get_attendance_report(course_id)
        if df.empty:
            return df, None
        
        # 1. 基础汇总
        stats = df.groupby(['student_id', 'student_name']).agg(
            Total_Sessions=('status', 'count'),
            Present_Count=('status', lambda x: (x == 'Present').sum()),
            Absent_Count=('status', lambda x: (x == 'Absent').sum()),
            Late_Count=('status', lambda x: (x == 'Late').sum()),
            Excused_Count=('status', lambda x: (x == 'Excused').sum())
        ).reset_index()
        
        # 2. 计算加权出勤率 (出席=100%, 迟到=50%, 其他=0%)
        stats['Attendance_Rate'] = (
            (stats['Present_Count'] * 1.0 + stats['Late_Count'] * 0.5) / stats['Total_Sessions'] * 100
        ).round(1)
        
        return df, stats

    def get_student_personal_report(self, student_id, course_id):
        """
        专门为“学生画像”准备：获取单个学生在特定课程的所有考勤细节。
        """
        df = self.db.get_attendance_report(course_id)
        if df.empty:
            return pd.DataFrame()
        
        personal_df = df[df['student_id'] == student_id].sort_values('date')
        return personal_df

    def get_alerts(self, course_id, threshold=75.0):
        """
        自动筛选风险学生 (出勤率低于预设阈值)。
        """
        _, stats = self.get_full_analytics(course_id)
        if stats is None or stats.empty:
            return pd.DataFrame()
        
        return stats[stats['Attendance_Rate'] < threshold].sort_values('Attendance_Rate')