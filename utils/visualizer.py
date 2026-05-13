import plotly.express as px

def create_trend_chart(df):
    if df.empty: return None
    # 按日期统计人数
    count_df = df.groupby('date').size().reset_index(name='Attendance Count')
    fig = px.line(count_df, x='date', y='Attendance Count', title="Daily Attendance Trend",
                  markers=True, template="plotly_dark")
    return fig