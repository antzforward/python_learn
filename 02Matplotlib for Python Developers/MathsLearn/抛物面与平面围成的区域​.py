import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# 设置中文字体（在绘图代码前添加）
plt.rcParams['font.sans-serif'] = ['SimHei']  # 根据系统可用字体选择
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示异常

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 抛物面 z = x² + y²
x = np.linspace(0, 1, 50)
y = np.linspace(0, 1, 50)
X, Y = np.meshgrid(x, y)
Z = X**2 + Y**2
ax.plot_surface(X, Y, Z, alpha=0.6, cmap='viridis')

# 平面 x+y=1
x_line = np.linspace(0,1,50)
y_line = 1 - x_line
z_line = x_line**2 + y_line**2
ax.plot(x_line, y_line, z_line, 'r-', lw=3)

ax.set_title("(2) 抛物面与平面围成的区域")
ax.set_box_aspect([1, 1, 1])  # 强制x/y/z轴单位长度相等
plt.show()