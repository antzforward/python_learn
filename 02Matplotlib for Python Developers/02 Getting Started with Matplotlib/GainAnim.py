import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 定义摆线的参数方程
def gain(t,k):
    x = t
    v = 0.5 * pow(abs(2.0 * ( x if x < 0.5 else 1.0 - x) ), k)
    y = v if x < 0.5 else 1.0 - v
    return x, y

# 创建图形和轴
fig, ax = plt.subplots()
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')

# 初始化摆线的点
x_data, y_data = [], []
ln, = plt.plot([], [], 'o-', animated=True)
# 初始化函数，设置图形的初始状态
def init():
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    # 设置 x 轴和 y 轴的刻度位置为 0.1 的间隔
    ax.set_xticks(np.arange(0, 1.1, 0.1))
    ax.set_yticks(np.arange(0, 1.1, 0.1))
    ax.grid( True )
    return ln,

a = 0.2
# 更新函数，用于动画的每一帧
def update(frame):
    x, y = gain(frame,a )
    x_data.append(x)
    y_data.append(y)
    ln.set_data(x_data, y_data)
    ln.set_linewidth(2)
    ln.set_markersize(1)
    return ln,

# 创建动画
ani = FuncAnimation(fig, update, frames=np.linspace(0.0, 1.0, 1000),
                    init_func=init, blit=True, interval=10)

# 显示动画
plt.show()