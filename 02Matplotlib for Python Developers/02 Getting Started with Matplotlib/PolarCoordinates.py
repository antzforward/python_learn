import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

## 2024年12月26日， 修正，绘制图像不对。
# 定义极坐标方程
def polar_equation(a):
    p = 10**2 * np.cos(2 * a)
    return np.sqrt(p)

# 创建角度数组
a = np.linspace(-np.pi*0.25,  np.pi*0.25, 1000)

# 初始化图形和轴
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
line, = ax.plot([], [], 'b-')  # 初始化一个空的线对象

# 初始化函数，设置图形的初始状态
def init():
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_theta_zero_location('N')  # 设置极轴的起始位置
    ax.set_theta_direction(1)  # 设置极轴的方向为顺时针
    return line,

# 更新函数，用于动画的每一帧
def update(frame):
    x = a[:frame+1]  # 角度
    y = polar_equation(x)  # 极径
    line.set_data(x, y)  # 更新线的数据
    return line,

# 创建动画
ani = FuncAnimation(fig, update, frames=len(a), init_func=init, blit=True, interval=10)

# 显示动画
plt.show()