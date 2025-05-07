import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建单叶双曲面
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# 参数化曲面 (u: 双曲角，v: 圆周角)
u = np.linspace(-2, 2, 50)
v = np.linspace(0, 2*np.pi, 50)
U, V = np.meshgrid(u, v)

# 单叶双曲面参数方程
X = 3 * np.cosh(U) * np.cos(V)
Y = 5 * np.sinh(U)
Z = 2 * np.cosh(U) * np.sin(V)

# 绘制曲面
ax.plot_surface(X, Y, Z, alpha=0.4, color='blue', label='曲面')
ax.plot_surface(X, -Y, Z, alpha=0.4, color='blue')  # 对称部分

# 绘制截口曲线
# 1. 平面 x=2 的双曲线
y_x2 = np.linspace(-10, 10, 100)
z_x2_pos = np.sqrt(4*(5/9 + y_x2**2/25))
z_x2_neg = -z_x2_pos
ax.plot(2*np.ones_like(y_x2), y_x2, z_x2_pos, 'r-', lw=2, label='x=2 (双曲线)')
ax.plot(2*np.ones_like(y_x2), y_x2, z_x2_neg, 'r-')

# 2. 平面 y=0 的椭圆
theta = np.linspace(0, 2*np.pi, 100)
x_y0 = 3 * np.cos(theta)
z_y0 = 2 * np.sin(theta)
ax.plot(x_y0, np.zeros_like(theta), z_y0, 'g--', label='y=0 (椭圆)')

# 3. 平面 y=5 的椭圆
x_y5 = 3 * np.sqrt(2) * np.cos(theta)
z_y5 = 2 * np.sqrt(2) * np.sin(theta)
ax.plot(x_y5, 5*np.ones_like(theta), z_y5, 'm-', label='y=5 (椭圆)')

# 4. 平面 z=1 的双曲线
# 平面 z=1 的双曲线
x_min = np.sqrt(9 * (3/4))  # 计算x的最小绝对值 x_min ≈ 2.598
x_z1 = np.linspace(-5, 5, 100)
x_z1 = x_z1[(x_z1 <= -x_min) | (x_z1 >= x_min)]  # 仅保留 |x| ≥ 2.598 的区域

y_z1_pos = 5 * np.sqrt((x_z1**2)/9 - 3/4)  # 此时根号内非负
y_z1_neg = -y_z1_pos

ax.plot(x_z1, y_z1_pos, np.ones_like(x_z1), 'c-', label='z=1 (双曲线)')
ax.plot(x_z1, y_z1_neg, np.ones_like(x_z1), 'c-')

# 5. 平面 z=2 的直线
z_min = 2 * np.sqrt(5/9)  # ≈1.491
z_x2 = np.linspace(-6, 6, 100)
z_x2 = z_x2[(z_x2 <= -z_min) | (z_x2 >= z_min)]  # 仅保留 |z| ≥1.491

y_x2 = 5 * np.sqrt((z_x2**2)/4 - 5/9)
ax.plot(2*np.ones_like(z_x2), y_x2, z_x2, 'r-', lw=2, label='x=2 (双曲线)')

# 设置坐标轴比例（基于分母系数的实际几何比例）
ax.set_box_aspect([3, 5, 2])  # 对应分母系数 (9,25,4)

# 手动限制坐标范围（确保图形对称）
#ax.set_xlim(-6, 6)   # x轴范围 ±6（2倍半轴长度）
#ax.set_ylim(-10, 10) # y轴范围 ±10（2倍虚半轴长度）
#ax.set_zlim(-4, 4)   # z轴范围 ±4（2倍半轴长度）

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()
ax.set_title("单叶双曲面及其截口曲线")

plt.show()