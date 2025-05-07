import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 参数设置
a, b, c = 2, 3, 4
theta = np.linspace(0, 2*np.pi, 100)
z = np.linspace(-5, 5, 100)

# 准线：z = c平面上的椭圆
t = np.linspace(0, 2*np.pi, 100)
x_ellipse = a * np.cos(t)
y_ellipse = b * np.sin(t)
z_ellipse = c * np.ones_like(t)

# 锥面参数化
theta_grid, z_grid = np.meshgrid(theta, z)
x_cone = a * z_grid / c * np.cos(theta_grid)
y_cone = b * z_grid / c * np.sin(theta_grid)
z_cone = z_grid

# 绘制
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# 绘制锥面
ax.plot_surface(x_cone, y_cone, z_cone, alpha=0.5, color='blue', label='Cone')

# 绘制准线椭圆
ax.plot(x_ellipse, y_ellipse, z_ellipse, 'r-', lw=2, label='Directrix (Ellipse)')

# 绘制母线示例
num_lines = 8
for t in np.linspace(0, 2*np.pi, num_lines):
    x_line = [0, a * np.cos(t)]
    y_line = [0, b * np.sin(t)]
    z_line = [0, c]
    ax.plot(x_line, y_line, z_line, 'g--', lw=1, alpha=0.7, label='Generatrix' if t ==0 else "")

# 设置标签和图例
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Cone Surface Visualization')
ax.legend()

# 启用鼠标旋转交互
plt.tight_layout()
ax.set_box_aspect([1, 1, 1])  # 强制x/y/z轴单位长度相等
plt.show()