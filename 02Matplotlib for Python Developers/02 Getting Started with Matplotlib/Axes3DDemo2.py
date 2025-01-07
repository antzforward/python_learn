import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制抛物面
X, Y = np.meshgrid(np.linspace(-1, 1, 100), np.linspace(-1, 1, 100))
Z = X**2 + Y**2

# 绘制坐标面
ax.plot_surface(X, Y, Z, alpha=0.5)

# 绘制平面 x+y-1=0
x = np.linspace(-1, 2, 100)
y = 1 - x
z = x**2 + (1-x)**2
ax.plot(x, y, z, label='Plane x+y-1=0')

ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.set_title('Paraboloid and Plane Intersection')
ax.legend()

plt.show()

# 圆锥与球的交集
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

R = 1
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, 1, 100)
U, V = np.meshgrid(u, v)

# 圆锥
X_cone = R * V * np.cos(U)
Y_cone = R * V * np.sin(U)
Z_cone = np.sqrt(X_cone**2 + Y_cone**2)

# 球
X_sphere = R * np.sin(V) * np.cos(U)
Y_sphere = R * np.sin(V) * np.sin(U)
Z_sphere = R * np.cos(V)

ax.plot_surface(X_cone, Y_cone, Z_cone, alpha=0.5, label='Cone')
ax.plot_surface(X_sphere, Y_sphere, Z_sphere, alpha=0.5, label='Sphere')

ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.set_title('Cone and Sphere Intersection')
ax.legend()

plt.show()