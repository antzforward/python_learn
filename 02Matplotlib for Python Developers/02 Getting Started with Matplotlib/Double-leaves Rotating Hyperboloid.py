import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 参数范围
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(-1, 1, 100)
U, V = np.meshgrid(u, v)

# 旋转双叶双曲面的参数方程
X = np.sqrt(1 + V**2) * np.cos(U)
Y = V * np.sin(U)
Z = np.sqrt(1 - V**2)

# 创建3D图形
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制旋转双叶双曲面
ax.plot_surface(X, Y, Z, cmap='viridis')

# 设置图形属性
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.set_title('Two-Sheet Hyperboloid')

# 显示图形
plt.show()