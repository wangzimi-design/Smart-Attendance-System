import pandas as pd
import os

# 确保文件夹存在
if not os.path.exists('data'):
    os.makedirs('data')

def load_students():
    """读取学生名单"""
    try:
        return pd.read_csv('data/students.csv')
    except FileNotFoundError:
        return pd.DataFrame(columns=['ID', 'Name'])

def save_attendance(date, student_id, status):
    """保存一条考勤记录"""
    file_path = 'data/attendance.csv'
    new_data = pd.DataFrame([[date, student_id, status]], columns=['Date', 'ID', 'Status'])
    
    # 如果文件不存在则创建，存在则追加(append)
    if not os.path.exists(file_path):
        new_data.to_csv(file_path, index=False)
    else:
        new_data.to_csv(file_path, mode='a', header=False, index=False)
    print(f"Record saved: {student_id} is {status} on {date}")