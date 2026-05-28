# 🚀 SAAS Pro: Intelligent Attendance & Data Analysis Platform
### 智能考勤与数据分析平台

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit)
![SQLite](https://img.shields.io/badge/Database-SQLite3-003B57?logo=sqlite)

---

## 📖 Project Description / 项目描述

**SAAS Pro** is an industrial-grade, cloud-ready SaaS application developed entirely in Python. It manages the full data lifecycle—from multi-tenant secure login to deep behavioral analytics.

**SAAS Pro** 是一款完全基于 Python 开发的工业级云端 SaaS 应用。它管理从多租户安全登录、抗作弊签到机制到学生行为深度分析的完整数据生命周期。

---

## ✨ Key Features / 核心功能

*   **👥 Multi-tenant Architecture**: Secure portals for multiple professors with data isolation.
*   **📱 Dynamic QR Code Engine**: Real-time generated QR codes for student check-ins.
*   **📊 360° Analytics Dashboard**: Interactive visualizations for attendance trends.
*   **📂 Bulk Management**: High-performance Excel/CSV engine for student registration.

---

## 🛠 Technologies Used / 使用技术

| Category | Technology |
| :--- | :--- |
| **Frontend** | Streamlit |
| **Logic & Data** | Pandas, NumPy |
| **Database** | SQLite3 |
| **Visuals** | Plotly |

---

## 🚀 Installation Instructions / 安装指南

> **Note**: Ensure you have **Python 3.10+** installed.

### 1. Clone the repository / 克隆仓库
```bash
git clone <your-repository-url>
cd 3320PROJECT

---

### 2. Create a virtual environment / 创建虚拟环境

**On Windows:**
python -m venv venv
.\venv\Scripts\activate

**On macOS/Linux:**
python3 -m venv venv
source venv/bin/activate

---

### 3. Install dependencies / 安装依赖
pip install -r requirements.txt

---

## 🧩 Technical Implementation / 技术实现与课程关联

*本项目展示了 Python 课程核心概念的实际应用：*

*   **Chapter 10 & 11 (OOP)**: Utilized Classes for `DatabaseHandler` and `AttendanceManager` to ensure modular code.
*   **Chapter 14 (Database)**: Relational storage using SQLite3 with JOIN queries and composite keys.
*   **Chapter 5 & 6 (Logic & Errors)**: Robust function modularization and `try-except` blocks for safe parsing.
*   **Data Analysis**: Use of **Pandas** for weighted rate calculation and **Plotly** for rendering.

---

## 💻 How to Run / 如何运行

Execute the following command in your terminal:
streamlit run app.py

*   **👨‍🏫 Professor Access**: Login via `http://localhost:8501` (Default PW: `123456`).
*   **🎓 Student Access**: Access via QR code or append `?mode=student` to the URL.

---

## 📂 Dataset Usage / 数据集说明

*   **Internal Database**: `attendance.db` is auto-initialized on first run. Stores students, courses, and logs.
*   **External Input**: Supports bulk-upload in the **"Management"** tab.
*   **Requirements**: Files must contain `ID` and `Name` columns. Supports fuzzy column matching.

---

## 📈 Output Explanation / 输出说明

*   **Interactive Visualizations**: Includes Daily Trend Charts, Class Activity Heatmaps, and Status Pie Charts.
*   **Risk Alerts**: An automated list of students with attendance **< 75%**.
*   **Audit Logs**: A timestamped record of all administrative actions.

---

## 👤 Contributors / 贡献者
*   **Your Name** - Lead Developer / Architect (全栈开发与架构)
*   **Partner Name** - UI/UX & Documentation (界面设计与文档)

---
© 2026 SAAS Pro Team. Built for Python Course Project.

