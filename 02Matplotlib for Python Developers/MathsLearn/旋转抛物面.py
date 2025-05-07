import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 定义抛物面方程：z = 2 - (x² + y²)/8
x = np.linspace(-10, 10, 100)
y = np.linspace(-10, 10, 100)
X, Y = np.meshgrid(x, y)
Z = 2 - (X**2 + Y**2)/8

# 绘制抛物面
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 绘制上半部分抛物面（限制 Z <= 2）
mask = Z <= 2
ax.plot_surface(X, Y, Z, facecolors=plt.cm.viridis(Z), alpha=0.8, rstride=1, cstride=1)

# 标注顶点和平面 z=4
ax.scatter(0, 0, 2, c='red', s=100, label='顶点 (0,0,2)')
ax.plot([-10,10], [0,0], [4,4], 'r--', lw=2, label='平面 z=4')

# 设置坐标轴比例和标签
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_zlim(-50, 5)
ax.set_box_aspect([10, 10, 10])  # 增强三维比例感
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()
ax.set_title("轨迹曲面：旋转抛物面 $x^2 + y^2 = -8(z-2)$")

plt.show()