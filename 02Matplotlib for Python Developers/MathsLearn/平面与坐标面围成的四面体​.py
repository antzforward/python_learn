import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# 设置中文字体（在绘图代码前添加）
plt.rcParams['font.sans-serif'] = ['SimHei']  # 根据系统可用字体选择
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示异常

# 创建数据
x = np.linspace(0, 3, 100)
y = np.linspace(0, 2, 100)
X, Y = np.meshgrid(x, y)
Z = 1 - X/3 - Y/2

# 绘制
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, alpha=0.5, color='blue')  # 平面
ax.plot_surface(np.zeros_like(X), Y, Z, alpha=0.3, color='gray')  # y-z平面
ax.plot_surface(X, np.zeros_like(Y), Z, alpha=0.3, color='gray')  # x-z平面
ax.plot_surface(X, Y, np.zeros_like(Z), alpha=0.3, color='gray')  # x-y平面
ax.set_title("(1) 平面与坐标面围成的四面体")
ax.set_box_aspect([1, 1, 1])  # 强制x/y/z轴单位长度相等
plt.show()