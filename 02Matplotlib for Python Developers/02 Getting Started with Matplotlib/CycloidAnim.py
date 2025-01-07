import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 定义摆线的参数方程
def cycloid(t, a):
    x = a * (t - np.sin(t))
    y = a * (1 - np.cos(t))
    return x, y

# 创建图形和轴
fig, ax = plt.subplots()
ax.set_xlim(-1, 10)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')

# 初始化摆线的点
x_data, y_data = [], []
ln, = plt.plot([], [], 'o-', animated=True)

# 初始化函数，设置图形的初始状态
def init():
    ax.set_xlim(-1, 10)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
    ax.grid( True )
    return ln,

a = 1
# 更新函数，用于动画的每一帧
def update(frame):
    x, y = cycloid(frame, a)  # 假设半径a为1
    x_data.append(x)
    y_data.append(y)
    ln.set_data(x_data, y_data)
    return ln,

# 创建动画
ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 1000),
                    init_func=init, blit=True, interval=10)

# 显示动画
plt.show()