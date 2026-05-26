import streamlit as st
import pandas as pd
import datetime
import io
import qrcode
import socket
import time
from backend.logic import AttendanceManager
from utils.visualizer import (
    create_trend_chart, 
    create_status_pie, 
    create_attendance_heatmap,
    create_personal_bar
)

# --- 1. 语言包定义 ---
LANG = {
    "CN": {
        "login_title": "🔐 SAAS 教授门户登录",
        "user_label": "用户名",
        "pw_label": "密码",
        "login_btn": "登录",
        "nav_title": "导航菜单",
        "nav_options": ["📊 数据看板", "📝 考勤控制", "👤 学生画像", "⚙️ 管理中心"],
        "logout_btn": "登出系统",
        "active_course": "当前选择班级",
        "no_course": "暂无班级，请先去管理中心添加",
        "dash_title": "数据分析看板",
        "m_std": "学生总数",
        "m_rate": "平均出勤率",
        "m_late": "迟到总数",
        "m_abs": "缺勤总数",
        "m_alert": "出勤预警 (< 75%)",
        "att_manual": "手动点名",
        "att_qr": "扫码模式",
        "att_date": "考勤日期",
        "att_save": "保存手动记录",
        "att_qr_sub": "展示给全班同学扫描",
        "att_qr_tip": "动态签到二维码",
        "profile_title": "学生个人出勤画像",
        "profile_search": "搜索学生 (姓名/ID)",
        "profile_history": "历史记录",
        "mgmt_title": "系统管理中心",
        "mgmt_tabs": ["班级管理", "批量导入学生", "网络设置"],
        "mgmt_add_c": "添加新班级",
        "mgmt_c_id": "课程 ID",
        "mgmt_c_name": "课程名称",
        "mgmt_import_btn": "开始批量导入",
        "std_checkin_title": "📱 学生自主签到",
        "std_id_label": "请输入学号",
        "std_confirm": "确认签到",
        "std_success": "✅ 签到成功！"
    },
    "EN": {
        "login_title": "🔐 SAAS Professor Portal",
        "user_label": "Username",
        "pw_label": "Password",
        "login_btn": "Login",
        "nav_title": "Navigation",
        "nav_options": ["📊 Dashboard", "📝 Attendance", "👤 Student Profiles", "⚙️ Management"],
        "logout_btn": "Logout",
        "active_course": "Active Class",
        "no_course": "No classes found. Add one in Management.",
        "dash_title": "Analytics Dashboard",
        "m_std": "Total Students",
        "m_rate": "Avg Rate",
        "m_late": "Total Lates",
        "m_abs": "Total Absents",
        "m_alert": "Attendance Alerts (< 75%)",
        "att_manual": "Manual List",
        "att_qr": "QR Code Mode",
        "att_date": "Attendance Date",
        "att_save": "Submit Manual Records",
        "att_qr_sub": "Show to Classroom",
        "att_qr_tip": "Dynamic Check-in QR",
        "profile_title": "Student Performance Profiles",
        "profile_search": "Select Student",
        "profile_history": "History History",
        "mgmt_title": "System Management",
        "mgmt_tabs": ["Classes", "Import List", "Network"],
        "mgmt_add_c": "Add New Course",
        "mgmt_c_id": "Course ID",
        "mgmt_c_name": "Course Name",
        "mgmt_import_btn": "Confirm Bulk Import",
        "std_checkin_title": "📱 Student Self Check-in",
        "std_id_label": "Enter Student ID",
        "std_confirm": "Confirm Attendance",
        "std_success": "✅ Success! Recorded."
    }
}

# --- 2. 基础函数 ---
def get_system_url():
    if "custom_url" in st.session_state and st.session_state.custom_url:
        return st.session_state.custom_url
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return f"http://{ip}:8501"
    except:
        return "http://localhost:8501"

st.set_page_config(page_title="SAAS AI Pro", layout="wide", page_icon="👨‍🏫")
manager = AttendanceManager()

# --- 3. 处理学生签到 (双语自适应) ---
params = st.query_params
if params.get("mode") == "student":
    # 学生端简单显示双语，无需切换
    st.title("📱 Student Check-in / 学生签到")
    cid = params.get("cid")
    cname = params.get("cname", "Class")
    st.info(f"Class: **{cname}**")
    with st.form("st_form"):
        s_id = st.text_input("Student ID / 学号")
        if st.form_submit_button("Check-in / 确认签到", type="primary"):
            if s_id:
                today = datetime.date.today().strftime("%Y-%m-%d")
                temp_df = pd.DataFrame([{'id': s_id, 'status': 'Present'}])
                manager.submit_batch_attendance(temp_df, today, cid, f"Student:{s_id}")
                st.success("Success! / 签到成功！")
                st.balloons()
    st.stop()

# --- 4. 教授端侧边栏 (语言选择在此) ---
with st.sidebar:
    st.title("🚀 SAAS Control")
    # 核心：选择语言
    lang_choice = st.selectbox("Language / 语言切换", ["CN", "EN"])
    T = LANG[lang_choice] # 获取对应语言包
    
    st.divider()
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        st.write(f"Logged in: **{st.session_state.user}**")
        menu = st.radio(T["nav_title"], T["nav_options"])
        
        # 课程选择
        my_courses = manager.db.get_courses_by_professor(st.session_state.user)
        curr_course_id = None
        if not my_courses.empty:
            sel_c = st.selectbox(T["active_course"], my_courses['name'].tolist())
            curr_course_id = my_courses[my_courses['name'] == sel_c]['id'].values[0]
        else:
            st.warning(T["no_course"])
            sel_c = "None"
            
        if st.button(T["logout_btn"], use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
    else:
        st.info("Please Login First")

# --- 5. 登录逻辑 (双语) ---
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.title(T["login_title"])
    col1, _ = st.columns([1, 2])
    user = col1.text_input(T["user_label"])
    pw = col1.text_input(T["pw_label"], type="password")
    if col1.button(T["login_btn"], type="primary"):
        if pw == "123456":
            st.session_state.logged_in = True
            st.session_state.user = user
            st.rerun()
    st.stop()

# --- 6. 功能模块路由 ---

# A. Dashboard
if menu == T["nav_options"][0]:
    st.title(f"{T['dash_title']}: {sel_c}")
    if curr_course_id:
        df, stats = manager.get_full_analytics(curr_course_id)
        if not df.empty:
            m1, m2, m3, m4 = st.columns(4)
            m1.metric(T["m_std"], len(stats))
            m2.metric(T["m_rate"], f"{stats['Attendance_Rate'].mean():.1f}%")
            m3.metric(T["m_late"], (df['status'] == 'Late').sum())
            m4.metric(T["m_abs"], (df['status'] == 'Absent').sum())
            
            st.divider()
            c1, c2 = st.columns(2)
            with c1: st.plotly_chart(create_trend_chart(df), use_container_width=True)
            with c2: st.plotly_chart(create_status_pie(df), use_container_width=True)
            st.plotly_chart(create_attendance_heatmap(df), use_container_width=True)
            
            st.subheader(T["m_alert"])
            st.dataframe(manager.get_alerts(curr_course_id), use_container_width=True, hide_index=True)
        else: st.info("No data available.")

# B. Attendance
elif menu == T["nav_options"][1]:
    st.title(f"{T['att_manual']}/{T['att_qr']}: {sel_c}")
    if curr_course_id:
        mode = st.tabs([T["att_manual"], T["att_qr"]])
        
        with mode[0]:
            date = st.date_input(T["att_date"], datetime.date.today())
            std_df = manager.db.get_all_students()
            if not std_df.empty:
                std_df['status'] = "Present"
                edited = st.data_editor(std_df, use_container_width=True, hide_index=True,
                    column_config={
                        "status": st.column_config.SelectboxColumn("Status", options=manager.statuses, required=True),
                        "id": st.column_config.Column(disabled=True),
                        "name": st.column_config.Column(disabled=True)
                    })
                if st.button(T["att_save"], type="primary"):
                    manager.submit_batch_attendance(edited, date.strftime("%Y-%m-%d"), curr_course_id, st.session_state.user)
                    st.success("✅ Saved!")

        with mode[1]:
            st.subheader(T["att_qr_sub"])
            system_url = get_system_url()
            checkin_url = f"{system_url}/?mode=student&cid={curr_course_id}&cname={sel_c}"
            qr_img = qrcode.make(checkin_url)
            buf = io.BytesIO(); qr_img.save(buf, format="PNG")
            st.image(buf.getvalue(), width=350, caption=T["att_qr_tip"])

# C. Student Profiles
elif menu == T["nav_options"][2]:
    st.title(T["profile_title"])
    all_std = manager.db.get_all_students()
    if not all_std.empty:
        choice = st.selectbox(T["profile_search"], [f"{r['id']} - {r['name']}" for _, r in all_std.iterrows()])
        sid = choice.split(" - ")[0]
        report = manager.db.get_attendance_report(curr_course_id)
        p_df = report[report['student_id'] == sid]
        if not p_df.empty:
            c1, c2 = st.columns([1, 2])
            with c1: st.plotly_chart(create_status_pie(p_df), use_container_width=True)
            with c2: 
                st.subheader(T["profile_history"])
                st.dataframe(p_df[['date', 'status']].sort_values('date', ascending=False), use_container_width=True)
        else: st.warning("No data for this student.")

# D. Management
elif menu == T["nav_options"][3]:
    st.title(T["mgmt_title"])
    tab1, tab2, tab3 = st.tabs(T["mgmt_tabs"])
    
    with tab1: # Classes
        st.subheader(T["mgmt_add_c"])
        with st.form("c_f"):
            c1, c2 = st.columns(2)
            cid = c1.text_input(T["mgmt_c_id"])
            cn = c2.text_input(T["mgmt_c_name"])
            if st.form_submit_button("OK"):
                if cid and cn: manager.db.add_course(cid, cn, st.session_state.user); st.rerun()
        st.dataframe(manager.db.get_courses_by_professor(st.session_state.user), use_container_width=True)

    with tab2: # Import
        st.subheader("Bulk Import Students (Excel/CSV)")
        up = st.file_uploader("Upload", type=['csv', 'xlsx'])
        if up:
            df_up = pd.read_csv(up) if up.name.endswith('csv') else pd.read_excel(up)
            if st.button(T["mgmt_import_btn"]):
                cnt = manager.import_students_from_df(df_up, st.session_state.user)
                st.success(f"Imported {cnt}!")

    with tab3: # Network
        st.subheader("🌐 Network Configuration")
        cl_url = st.text_input("Public App URL (for Cloud deployment)", placeholder="https://xxx.streamlit.app")
        if st.button("Update URL"):
            st.session_state.custom_url = cl_url
            st.success("Updated!")