import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建双叶双曲面
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# 参数化双曲面 (z >= 0 和 z <= 0 两叶)
theta = np.linspace(0, 2*np.pi, 100)
z_upper = np.linspace(0, 6, 100)
z_lower = np.linspace(-6, 0, 100)
T, Z_upper = np.meshgrid(theta, z_upper)
T, Z_lower = np.meshgrid(theta, z_lower)

# 计算x,y坐标
X_upper = np.sqrt(Z_upper**2/9) * np.cos(T)
Y_upper = np.sqrt(Z_upper**2/9) * np.sin(T)
X_lower = np.sqrt(Z_lower**2/9) * np.cos(T)
Y_lower = np.sqrt(Z_lower**2/9) * np.sin(T)

# 绘制双曲面
ax.plot_surface(X_upper, Y_upper, Z_upper, alpha=0.4, color='blue')
ax.plot_surface(X_lower, Y_lower, Z_lower, alpha=0.4, color='blue')

# 绘制截口曲线
# 1. z=3平面上的圆
z3_theta = np.linspace(0, 2*np.pi, 100)
x_z3 = np.cos(z3_theta)
y_z3 = np.sin(z3_theta)
ax.plot(x_z3, y_z3, 3*np.ones_like(z3_theta), 'r-', lw=2, label='z=3 (圆)')

# 2. x=0平面上的直线
z_line = np.linspace(-6, 6, 100)
y_z0 = z_line/3
ax.plot(np.zeros_like(z_line), y_z0, z_line, 'g--', label='x=0 (直线)')
ax.plot(np.zeros_like(z_line), -y_z0, z_line, 'g--')

# 平面 y=1/3 的截口双曲线
z_hyper = np.linspace(-6, 6, 100)
z_hyper = z_hyper[(z_hyper <= -1) | (z_hyper >= 1)]  # 排除 |z| < 1
x_hyper = np.sqrt((z_hyper**2)/9 - (1/3)**2)

ax.plot(x_hyper, (1/3)*np.ones_like(z_hyper), z_hyper, 'c-', label='y=1/3 (双曲线)')
ax.plot(-x_hyper, (1/3)*np.ones_like(z_hyper), z_hyper, 'c-')

# 设置坐标比例和标签
ax.set_box_aspect([6, 6, 6])  # 确保比例一致
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()
ax.set_title("双叶双曲面及其截口曲线")

plt.show()