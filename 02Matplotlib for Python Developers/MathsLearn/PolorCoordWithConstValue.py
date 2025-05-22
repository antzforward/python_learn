import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ---------- 新增：修复中文显示问题 ----------
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'WenQuanYi Zen Hei']  # 指定中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示异常
# ------------------------------------------

# 创建画布和子图
fig = plt.figure(figsize=(18, 6))

# 1. 球面族：ρ = 常数
ax1 = fig.add_subplot(131, projection='3d')
rho_values = [1, 2, 3]
theta = np.linspace(0, np.pi, 50)
phi = np.linspace(0, 2*np.pi, 50)
Theta, Phi = np.meshgrid(theta, phi)
for rho in rho_values:
    X = rho * np.sin(Theta) * np.cos(Phi)
    Y = rho * np.sin(Theta) * np.sin(Phi)
    Z = rho * np.cos(Theta)
    ax1.plot_surface(X, Y, Z, alpha=0.3, edgecolor='none')
ax1.set_title('ρ = 常数 (同心球面)', fontsize=12)

# 2. 锥面族：θ = 常数
ax2 = fig.add_subplot(132, projection='3d')
theta_values = [np.pi/6, np.pi/4, np.pi/3]
rho = np.linspace(0, 3, 50)
phi = np.linspace(0, 2*np.pi, 50)
Rho, Phi = np.meshgrid(rho, phi)
for theta in theta_values:
    X = Rho * np.sin(theta) * np.cos(Phi)
    Y = Rho * np.sin(theta) * np.sin(Phi)
    Z = Rho * np.cos(theta)
    ax2.plot_surface(X, Y, Z, alpha=0.3, linewidth=0.1)
ax2.set_title('θ = 常数 (锥面)', fontsize=12)

# 3. 半平面族：φ = 常数
ax3 = fig.add_subplot(133, projection='3d')
phi_values = [0, np.pi/2, np.pi]
rho = np.linspace(0, 3, 50)
theta = np.linspace(0, np.pi, 50)
Rho, Theta = np.meshgrid(rho, theta)
for phi in phi_values:
    X = Rho * np.sin(Theta) * np.cos(phi)
    Y = Rho * np.sin(Theta) * np.sin(phi)
    Z = Rho * np.cos(Theta)
    ax3.plot_surface(X, Y, Z, alpha=0.3, linewidth=0.1)
ax3.set_title('φ = 常数 (半平面)', fontsize=12)

# 调整视角和坐标轴范围
for ax in [ax1, ax2, ax3]:
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_zlim(-3, 3)
    ax.view_init(elev=20, azim=30)

plt.tight_layout()
plt.show()