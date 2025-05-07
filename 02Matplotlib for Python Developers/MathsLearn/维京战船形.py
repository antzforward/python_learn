import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
R = 2

# 球面1：x² + y² + z² = R²
phi = np.linspace(0, np.pi, 50)
theta = np.linspace(0, 2*np.pi, 50)
PHI, THETA = np.meshgrid(phi, theta)
X1 = R * np.sin(PHI) * np.cos(THETA)
Y1 = R * np.sin(PHI) * np.sin(THETA)
Z1 = R * np.cos(PHI)
ax.plot_surface(X1, Y1, Z1, alpha=0.3, color='blue')

# 球面2：x² + y² + (z-R)^2 = R²（修正方程，原输入疑似有误）
Z2 = Z1 + R  # 正确平移后的球面方程应为 (z-R)^2
ax.plot_surface(X1, Y1, Z2, alpha=0.3, color='red')

# 关键修正：统一坐标轴范围
max_range = 3 * R  # 确保所有轴范围差相等
ax.set_xlim(-max_range/2, max_range/2)
ax.set_ylim(-max_range/2, max_range/2)
ax.set_zlim(-R, 2*R)  # 覆盖两球面的最低点(-R)和最高点(2R)

# 强制三维坐标系等比例
ax.set_box_aspect([max_range, max_range, 3*R])  # 轴长度比例 = [x_range, y_range, z_range]

ax.set_title("(4) 两球面相交的维京战船形（修正比例）")
plt.show()