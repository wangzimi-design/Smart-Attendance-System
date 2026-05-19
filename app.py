import streamlit as st
import pandas as pd
from backend.logic import AttendanceManager
from utils.visualizer import create_trend_chart, create_status_pie

# --- 页面配置 ---
st.set_page_config(page_title="SAAS | Smart Attendance", layout="wide", page_icon="🚀")
manager = AttendanceManager()

# --- 侧边栏样式 ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3589/3589030.png", width=100)
    st.title("SAAS Control")
    menu = st.radio("Navigation", ["Dashboard", "Attendance", "Students Manager"])
    st.divider()
    st.info("System v2.0 - Stable")

# --- 1. Dashboard 仪表盘 ---
if menu == "Dashboard":
    st.title("📊 Analytics Dashboard")
    df, stats = manager.get_full_analytics()

    if not df.empty:
        # 核心指标卡片
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Students", len(manager.db.get_all_students()))
        col2.metric("Total Records", len(df))
        avg_rate = stats['Attendance_Rate'].mean()
        col3.metric("Avg Attendance", f"{avg_rate:.1f}%")
        col4.metric("Today's Presence", len(df[df['date'] == str(pd.Timestamp.now().date())]))

        st.divider()

        # 图表展示
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(create_trend_chart(df), use_container_width=True)
        with c2:
            st.plotly_chart(create_status_pie(df), use_container_width=True)

        # 预警系统
        st.subheader("⚠️ Attendance Alerts (< 75%)")
        alerts = manager.get_alerts()
        if not alerts.empty:
            st.warning(f"Found {len(alerts)} students with low attendance!")
            st.dataframe(alerts, use_container_width=True)
        else:
            st.success("All students are above the threshold.")
    else:
        st.info("No data available. Please mark attendance first.")

# --- 2. Attendance 考勤管理 ---
elif menu == "Attendance":
    st.title("📝 Attendance Marking")
    students = manager.db.get_all_students()
    
    if students.empty:
        st.error("No students found. Please add students first.")
    else:
        with st.expander("Batch Marking Form", expanded=True):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                selected_student = st.selectbox("Select Student", 
                    [f"{r['id']} - {r['name']} ({r['department']})" for _, r in students.iterrows()])
            with col2:
                status = st.select_slider("Status", options=manager.statuses)
            with col3:
                date = st.date_input("Date")

            if st.button("Submit Record", use_container_width=True, type="primary"):
                s_id = selected_student.split(" - ")[0]
                manager.mark_attendance(s_id, status, date.strftime("%Y-%m-%d"))
                st.toast(f"Recorded: {selected_student} as {status}", icon="✅")

        # 导出功能
        st.divider()
        raw_data = manager.db.get_attendance_report()
        st.download_button("📥 Export CSV Report", 
                          data=raw_data.to_csv(index=False), 
                          file_name="attendance_report.csv", 
                          mime="text/csv")
        st.dataframe(raw_data, use_container_width=True)

# --- 3. Students Manager 学生管理 ---
elif menu == "Students Manager":
    st.title("👥 Student Management")
    
    tab1, tab2 = st.tabs(["Add New Student", "Manage Existing"])
    
    with tab1:
        with st.form("add_student_form"):
            c1, c2, c3 = st.columns(3)
            new_id = c1.text_input("Student ID")
            new_name = c2.text_input("Full Name")
            new_dept = c3.selectbox("Department", ["CS", "Business", "Arts", "Engineering"])
            if st.form_submit_button("Add to Database"):
                if new_id and new_name:
                    if manager.db.add_student(new_id, new_name, new_dept):
                        st.success(f"Added {new_name} successfully!")
                    else:
                        st.error("ID already exists.")
                else:
                    st.warning("Please fill all fields.")

    with tab2:
        students = manager.db.get_all_students()
        st.table(students)
        del_id = st.text_input("Enter ID to Delete")
        if st.button("Delete Student", type="secondary"):
            manager.db.delete_student(del_id)
            st.rerun()