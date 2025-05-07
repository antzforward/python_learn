import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# 设置中文字体（在绘图代码前添加）
plt.rcParams['font.sans-serif'] = ['SimHei']  # 根据系统可用字体选择
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示异常

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 圆柱1：x² + y² = 1
theta = np.linspace(0, 2*np.pi, 100)
z = np.linspace(-1, 1, 50)
T, Z = np.meshgrid(theta, z)
X_cyl1 = np.cos(T)
Y_cyl1 = np.sin(T)
ax.plot_surface(X_cyl1, Y_cyl1, Z, alpha=0.5, color='green')

# 圆柱2：y² + z² = 1
Y_cyl2 = np.cos(T)
Z_cyl2 = np.sin(T)
ax.plot_surface(Z, Y_cyl2, Z_cyl2, alpha=0.5, color='purple')

ax.set_title("(5) 两垂直圆柱的交（Steinmetz 固体）")
ax.set_box_aspect([1, 1, 1])  # 强制x/y/z轴单位长度相等
plt.show()