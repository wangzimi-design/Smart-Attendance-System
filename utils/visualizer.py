import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# 定义全局色彩方案，确保四种状态在所有图表中颜色一致
COLOR_MAP = {
    'Present': '#2ecc71',  # 绿色
    'Absent': '#e74c3c',   # 红色
    'Late': '#f1c40f',     # 黄色
    'Excused': '#3498db'   # 蓝色
}

def create_trend_chart(df):
    """
    趋势图：展示每日出勤人数的波动。
    """
    if df.empty: return None
    
    # 统计每天每种状态的人数
    trend_df = df.groupby(['date', 'status']).size().reset_index(name='count')
    
    fig = px.line(trend_df, x='date', y='count', color='status',
                  title="Daily Attendance Trend by Status",
                  markers=True,
                  color_discrete_map=COLOR_MAP)
    
    fig.update_layout(template="plotly_dark", hovermode="x unified",
                      xaxis_title="Date", yaxis_title="Number of Students")
    return fig

def create_status_pie(df):
    """
    饼图：直观展示 Present/Absent/Late/Excused 的占比。
    """
    if df.empty: return None
    
    status_counts = df['status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    
    fig = px.pie(status_counts, values='Count', names='Status',
                 title="Overall Status Proportions",
                 color='Status',
                 color_discrete_map=COLOR_MAP,
                 hole=0.4) # 使用环形图更现代
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(template="plotly_dark")
    return fig

def create_attendance_heatmap(df):
    """
    热力图：展示课程的活跃度（哪天签到最密集）。
    """
    if df.empty: return None
    
    # 数据转换
    df['date'] = pd.to_datetime(df['date'])
    df['Day'] = df['date'].dt.day_name()
    df['Week'] = df['date'].dt.isocalendar().week
    
    # 统计每天的总签到数（活跃度）
    heat_df = df.groupby(['Week', 'Day']).size().reset_index(name='Activity')
    
    # 定义星期顺序
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    fig = px.density_heatmap(heat_df, x="Week", y="Day", z="Activity",
                             category_orders={"Day": days_order},
                             title="Class Activity Intensity (Heatmap)",
                             color_continuous_scale="Viridis")
    
    fig.update_layout(template="plotly_dark")
    return fig

def create_personal_bar(df):
    """
    个人画像专用：展示单个学生考勤状态的柱状统计。
    """
    if df.empty: return None
    counts = df['status'].value_counts().reset_index()
    counts.columns = ['Status', 'Count']
    
    fig = px.bar(counts, x='Status', y='Count', color='Status',
                 title="Personal Attendance Summary",
                 color_discrete_map=COLOR_MAP)
    fig.update_layout(template="plotly_dark", showlegend=False)
    return fig