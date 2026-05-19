import plotly.express as px
import plotly.graph_objects as go

def create_trend_chart(df):
    if df.empty: return None
    count_df = df[df['status'] == 'Present'].groupby('date').size().reset_index(name='Count')
    fig = px.area(count_df, x='date', y='Count', title="Daily Attendance Trend",
                  line_shape='spline', color_discrete_sequence=['#00CC96'])
    fig.update_layout(template="plotly_dark", hovermode="x unified")
    return fig

def create_status_pie(df):
    if df.empty: return None
    status_counts = df['status'].value_counts().reset_index()
    fig = px.pie(status_counts, values='count', names='status', title="Overall Status Distribution",
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(template="plotly_dark")
    return fig