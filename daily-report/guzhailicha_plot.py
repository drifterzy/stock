import akshare as ak
import plotly.graph_objects as go
df = ak.stock_ebs_lg()
# 创建图表
fig = go.Figure()

# 添加股债利差曲线
fig.add_trace(go.Scatter(x=df['日期'], y=df['股债利差'], mode='lines+markers', name='股债利差'))

# 添加股债利差均线曲线
fig.add_trace(go.Scatter(x=df['日期'], y=df['股债利差均线'], mode='lines+markers', name='股债利差均线'))

# 设置图表布局和标题
fig.update_layout(title='股债利差与股债利差均线变化趋势', xaxis_title='日期', yaxis_title='值')

# 显示图表
fig.show()