# 🚀 SAAS Pro: Intelligent Attendance & Data Analysis Platform
### 智能考勤与数据分析平台

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit)
![SQLite](https://img.shields.io/badge/Database-SQLite3-003B57?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 Project Description / 项目描述

**SAAS Pro** is an industrial-grade, cloud-ready SaaS application developed entirely in Python. It moves beyond traditional attendance logging by providing an active intelligence engine that manages the full data lifecycle—from multi-tenant secure login and anti-cheating check-in mechanisms to deep behavioral analytics.

**SAAS Pro** 是一款完全基于 Python 开发的工业级云端 SaaS 应用。它超越了传统的电子日志，提供了一个主动的智能引擎，管理从多租户安全登录、抗作弊签到机制到学生行为深度分析的完整数据生命周期。

---

## ✨ Key Features / 核心功能

*   **👥 Multi-tenant Architecture**: Secure portals for multiple professors with data isolation.
    *   *多租户架构：为多位教授提供安全门户及数据隔离。*
*   **📱 Dynamic QR Code Engine**: Real-time generated QR codes for secure, location-aware student check-ins.
    *   *动态二维码引擎：实时生成二维码，确保安全的学生签到。*
*   **📊 360° Analytics Dashboard**: Interactive visualizations for attendance trends and student risk detection.
    *   *360° 分析看板：交互式可视化出勤趋势与学生风险检测。*
*   **📂 Bulk Management**: High-performance Excel/CSV engine for student registration.
    *   *批量管理：高性能 Excel/CSV 学生注册引擎。*

---

## 🛠 Technologies Used / 使用技术

| Category | Technology |
| :--- | :--- |
| **Frontend** | Streamlit |
| **Logic & Data** | Pandas, NumPy |
| **Database** | SQLite3 |
| **Visuals** | Plotly |
| **Utilities** | qrcode, openpyxl, xlsxwriter |

---

## 🚀 Installation Instructions / 安装指南

To set up the environment locally, ensure you have **Python 3.10+** installed.
*如需在本地配置环境，请确保已安装 Python 3.10+。*

1. **Clone the repository / 克隆仓库**
   ```bash
   git clone <your-repository-url>
   cd 3320PROJECT
Create a virtual environment / 创建虚拟环境
code
Bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
Install dependencies / 安装依赖
code
Bash
pip install -r requirements.txt
💻 How to Run / 如何运行
Run the following command from the root directory:
请在根目录下运行以下命令：
code
Bash
streamlit run app.py
👨‍🏫 Professor Access: Login via http://localhost:8501 (Default PW: 123456).
🎓 Student Access: Access via generated QR code or append ?mode=student to the URL.
📂 Dataset Usage / 数据集说明
The system utilizes a relational database and supports external data imports.
系统使用关系型数据库并支持外部数据导入。
Internal Database (attendance.db): Automatically initialized on first run. Stores students, courses, attendance, and logs.
External Input (CSV/Excel): Supports bulk-upload in the "Management" tab.
Requirements: Must contain ID and Name. Supports fuzzy column matching.
📈 Output Explanation / 输出说明
Interactive Visualizations:
Trend Charts: Daily attendance fluctuations.
Activity Heatmaps: Identification of peak attendance periods.
Status Pie Charts: Proportions of Present, Absent, Late, and Excused.
Risk Alerts: Automated list of students with attendance < 75%.
Audit Logs: Timestamped records of all administrative actions.
👤 Contributors
Your Name - Lead Developer / Architect
Partner Name - UI/UX & Documentation
© 2024 SAAS Pro Team. Built for Python Course Project.
code
Code
### 为什么这个排版更好？
1.  **使用了徽章 (Badges)**：顶部显示 Python、Streamlit 等图标，一眼看上去就是专业开源项目的范儿。
2.  **模块化 (Sections)**：使用了 `---` 分割线，让内容层次分明。
3.  **图标 (Emojis)**：在标题前加入火箭、书本、齿轮等图标，增加视觉愉悦感。
4.  **代码块高亮**：正确使用了 Bash 代码块，GitHub 会提供一键复制功能。
5.  **表格 (Tables)**：技术栈使用表格排列，整齐清晰。
