import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 创建一个新的图形
fig = plt.figure()
# 添加一个3D子图
ax = fig.add_subplot(111, projection='3d')

# 定义x和y的范围
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)

# 绘制平面
surf = ax.plot_surface(X, Y, 1.5 + 2.5*X - 2 * Y,label='5x-4y-2z+3=0')
# X,Y = np.meshgrid( x, (20 -2*x)/3)
# Z = np.zeros_like(X)
# surf = ax.plot_surface(X, Y, Z,label='2x+3y-20=0')
# Y,Z = np.meshgrid(y,4*y/7)
# X = np.zeros_like( y )
# surf = ax.plot_surface(X, Y, Z ,label='4y-7z = 0')
# Y,Z = np.meshgrid(y,y)
# X = 2/3 * np.ones_like( Y )
# surf = ax.plot_surface(X, Y, Z ,label='3x - 2 = 0')
Y,Z = np.meshgrid(y,-y)
X = np.zeros_like( y )
surf = ax.plot_surface(X, Y, Z ,label='y - z = 0')

# 添加颜色条
#fig.colorbar(surf, shrink=0.5, aspect=5)

# 设置坐标轴标签
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# 设置坐标轴的显示范围
ax.set_xlim([-5, 5])
ax.set_ylim([-5, 5])
ax.set_zlim([-5, 5])
ax.legend()
# 显示图形
plt.show()