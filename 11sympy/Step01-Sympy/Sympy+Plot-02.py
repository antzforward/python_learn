import sympy as sp
import plotly.graph_objects as go
import numpy as np

x, y = sp.symbols('x y')
f = sp.sin(x**2 + y**2)*sp.exp(-0.1*(x**2+y**2)) # 定义二元微分函数
print( sp.latex(f)) #

# 符号微分
df_dx = sp.diff(f, x)
df_dy = sp.diff(f, y)

# 生成网格数据
X, Y = np.mgrid[-3:3:100j, -3:3:100j]
f_numeric = sp.lambdify((x,y), f)(X,Y)  # 数值化函数

# 绘制梯度场与曲面
fig = go.Figure(data=[
    go.Surface(z=f_numeric, x=X, y=Y, colorscale='viridis'),
    go.Cone(x=X.flatten(), y=Y.flatten(), z=f_numeric.flatten(),
            u=sp.lambdify((x,y), df_dx)(X,Y).flatten(),  # 梯度X分量
            v=sp.lambdify((x,y), df_dy)(X,Y).flatten(),  # 梯度Y分量
            w=np.zeros_like(X.flatten()),
            sizemode='absolute', sizeref=0.3)
])
fig.show()

