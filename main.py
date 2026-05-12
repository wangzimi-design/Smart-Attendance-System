import tkinter as tk
from tkinter import messagebox
from backend.database_logic import load_students, save_attendance
from datetime import datetime

def submit_attendance():
    # 简单的逻辑：给 Alice 记一个 Present
    date_str = datetime.now().strftime("%Y-%m-%d")
    save_attendance(date_str, 101, "Present")
    messagebox.showinfo("Success", "Attendance marked for Alice!")

# 创建窗口
root = tk.Tk()
root.title("Smart Attendance System")
root.geometry("300x200")

label = tk.Label(root, text="Click to mark Alice as Present")
label.pack(pady=20)

btn = tk.Button(root, text="Mark Attendance", command=submit_attendance)
btn.pack(pady=10)

root.mainloop()