import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 设置中文字体（在绘图代码前添加）
plt.rcParams['font.sans-serif'] = ['SimHei']  # 根据系统可用字体选择
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示异常

# 参数设置
a, b = 2, 1
u = np.linspace(-5, 5, 100)
v = np.linspace(-5, 5, 100)
U, V = np.meshgrid(u, v)

# 参数化双曲抛物面
X = a * U
Y = b * V
Z = (X**2 / a**2 - Y**2 / b**2) / 2

# 绘制图形
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# 绘制曲面（颜色映射表示高度）
surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8, linewidth=0, antialiased=True)

# 标注鞍点
ax.scatter(0, 0, 0, c='red', s=100, label='鞍点 (0,0,0)')

# 设置坐标轴
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title("双曲抛物面 x^2 - y^2 = 2z")
ax.legend()

# 添加颜色条
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)

# 设置视角和比例（确保鞍形清晰）
ax.view_init(elev=30, azim=-60)
ax.set_box_aspect([5, 5, 5])  # 单位长度一致

plt.show()