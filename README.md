SAAS Pro: Intelligent Attendance & Data Analysis Platform
SAAS Pro: 智能考勤与数据分析平台
1. Project Description / 项目描述
SAAS Pro is an industrial-grade, cloud-ready SaaS application developed entirely in Python. It moves beyond traditional attendance logging by providing an active intelligence engine that manages the full data lifecycle—from multi-tenant secure login and anti-cheating check-in mechanisms to deep behavioral analytics.
SAAS Pro 是一款完全基于 Python 开发的工业级云端 SaaS 应用。它超越了传统的电子日志，提供了一个主动的智能引擎，管理从多租户安全登录、抗作弊签到机制到学生行为深度分析的完整数据生命周期。
Key Features / 核心功能:
Multi-tenant Architecture: Secure portals for multiple professors with data isolation. (多租户架构：为多位教授提供安全门户及数据隔离)
Dynamic QR Code Engine: Real-time generated QR codes for secure, location-aware student check-ins. (动态二维码引擎：实时生成二维码，确保安全的学生签到)
360° Analytics Dashboard: Interactive visualizations for attendance trends and student risk detection. (360° 分析看板：交互式可视化出勤趋势与学生风险检测)
Bulk Management: High-performance Excel/CSV engine for student registration. (批量管理：高性能 Excel/CSV 学生注册引擎)

2. Installation Instructions / 安装指南
To set up the environment locally, ensure you have Python 3.10+ installed.
如需在本地配置环境，请确保已安装 Python 3.10+。
Clone the repository / 克隆仓库:
code
Bash
git clone <your-repository-url>
cd 3320PROJECT
Create a virtual environment (Optional but recommended) / 创建虚拟环境 (可选但推荐):
code
Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies / 安装依赖:
code
Bash
pip install -r requirements.txt

3. How to Run the Code / 如何运行代码
The application is built using Streamlit. Run the following command from the root directory:
本应用基于 Streamlit 构建。请在根目录下运行以下命令：
code
Bash
streamlit run app.py
Professor Access: Open the local URL (usually http://localhost:8501) and login with credentials (Default PW: 123456).
(教授端访问：打开本地 URL 并使用凭据登录，默认密码：123456)
Student Access: Students access the system via the generated QR code or by appending ?mode=student to the URL.
(学生端访问：学生通过生成的二维码或在 URL 后添加 ?mode=student 进入)

4. Dataset Usage Explained / 数据集使用说明
The system utilizes a relational database (SQLite) and supports external data imports.
系统使用关系型数据库 (SQLite) 并支持外部数据导入。
Internal Database (attendance.db): Automatically created upon first run. It stores 4 primary tables: students, courses, attendance, and logs.
(内部数据库：首次运行时自动创建。存储 4 张主表：学生表、课程表、考勤表和日志表)
External Input (CSV/Excel): Professors can bulk-upload student lists via the "Management" tab.
(外部输入：教授可通过“管理中心”标签页批量上传学生名单)
Requirements: The file should contain columns such as ID (Student ID) and Name. The system uses fuzzy matching to identify columns.
(要求：文件应包含 ID 和 Name 列。系统采用模糊匹配技术识别列名)

5. Output Explanation / 输出说明
The system generates three types of outputs to assist in educational decision-making:
系统生成三类输出，以辅助教学决策：
Interactive Visualizations (UI):
Trend Charts: Daily attendance fluctuations. (趋势图：每日出勤波动)
Activity Heatmaps: Identification of peak attendance periods. (活跃热力图：识别出勤高峰时段)
Status Pie Charts: Proportions of "Present", "Absent", "Late", and "Excused". (状态饼图：各项状态占比)
Risk Alerts: An automated list of students whose attendance rate falls below the 75% threshold.
(风险预警：自动筛选出勤率低于 75% 阈值的学生名单)
Audit Logs: A timestamped record of all administrative actions (e.g., course creation, manual record overrides).
(审计日志：所有行政操作的带时间戳记录，如创建课程、手动修改记录等)
Technologies Used / 使用技术
Frontend: Streamlit
Logic & Data: Pandas, NumPy
Database: SQLite3
Visuals: Plotly
Utilities: qrcode, openpyxl
