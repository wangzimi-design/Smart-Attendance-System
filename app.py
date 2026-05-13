import streamlit as st
from backend.logic import AttendanceManager
from utils.visualizer import create_trend_chart

st.set_page_config(page_title="Smart Attendance System", layout="wide")
manager = AttendanceManager()

# 初始化一些测试数据（第一次运行有用）
if manager.db.get_all_students().empty:
    manager.db.add_student("101", "Alice")
    manager.db.add_student("102", "Bob")

st.title("🚀 Smart Attendance & Analytics")

# 侧边栏导航
menu = st.sidebar.selectbox("Menu", ["Mark Attendance", "Dashboard"])

if menu == "Mark Attendance":
    st.header("📝 Mark Daily Attendance")
    students = manager.db.get_all_students()
    
    # 创建下拉框
    student_list = [f"{row['id']} - {row['name']}" for _, row in students.iterrows()]
    selected = st.selectbox("Select Student", student_list)
    
    if st.button("Mark as Present"):
        s_id = selected.split(" - ")[0]
        manager.mark_attendance(s_id)
        st.success(f"Attendance recorded for {selected}!")

elif menu == "Dashboard":
    st.header("📊 Data Analytics Dashboard")
    df = manager.get_stats()
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Raw Data")
        st.dataframe(df, use_container_width=True)
    
    with col2:
        st.subheader("Visual Analysis")
        fig = create_trend_chart(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available yet.")