import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# 设置中文字体（在绘图代码前添加）
plt.rcParams['font.sans-serif'] = ['SimHei']  # 根据系统可用字体选择
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示异常

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
R = 2

# 圆锥 z = sqrt(x² + y²)
theta = np.linspace(0, 2*np.pi, 100)
r = np.linspace(0, R, 100)
T, R_grid = np.meshgrid(theta, r)
X_cone = R_grid * np.cos(T)
Y_cone = R_grid * np.sin(T)
Z_cone = R_grid
ax.plot_surface(X_cone, Y_cone, Z_cone, alpha=0.5, color='orange')

# 球面 x² + y² + z² = R²
phi = np.linspace(0, np.pi, 50)
theta = np.linspace(0, 2*np.pi, 50)
PHI, THETA = np.meshgrid(phi, theta)
X_sphere = R * np.sin(PHI) * np.cos(THETA)
Y_sphere = R * np.sin(PHI) * np.sin(THETA)
Z_sphere = R * np.cos(PHI)
ax.plot_surface(X_sphere, Y_sphere, Z_sphere, alpha=0.3, color='blue')

ax.set_title("(3) 圆锥与球面的交（冰淇淋锥形）")
ax.set_box_aspect([1, 1, 1])  # 强制x/y/z轴单位长度相等
plt.show()