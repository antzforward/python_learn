import matplotlib.pyplot as plt
import numpy as np

# 定义网格
x, y = np.meshgrid(np.linspace(-2, 2, 10), np.linspace(-2, 2, 10))

# 定义向量场函数
u = -y
v = x

# 绘制向量场
plt.quiver(x, y, u, v, color='r')

# 设置图形属性
plt.axis('equal')
plt.xlim(-2.5, 2.5)
plt.ylim(-2.5, 2.5)
plt.grid(True)
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.title("Vector Field")

# 显示图形
plt.show()