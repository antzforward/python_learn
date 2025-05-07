import plotly.graph_objects as go
import numpy as np

# 参数设置
a = 2  # 控制悬链线的开口宽度（a > 0）
x_range = np.linspace(-5, 5, 500)  # x轴范围

# 悬链线方程
y = a * (np.exp(x_range / a) + np.exp(-x_range / a)) / 2

# 创建图形
fig = go.Figure()

# 绘制悬链线
fig.add_trace(go.Scatter(
    x=x_range,
    y=y,
    mode='lines',
    name='悬链线',
    line=dict(color='blue')
))

# 图形布局
fig.update_layout(
    title=f'悬链线 (a={a})',
    xaxis_title='x',
    yaxis_title='y',
    template='plotly_white',
    width=800,
    height=400
)

# 显示图形
fig.show()