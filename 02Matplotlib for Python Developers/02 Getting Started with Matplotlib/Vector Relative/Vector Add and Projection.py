import matplotlib.pyplot as plt
import numpy as np

# 定义向量
v = np.array([2, 3])
u = np.array([-1, 1])

# 向量加法
w = v + u

# 绘制向量
plt.arrow(0, 0, v[0], v[1], head_width=0.1, head_length=0.2, fc='blue', ec='blue', length_includes_head=True, label="v")
plt.arrow(v[0], v[1], u[0], u[1], head_width=0.1, head_length=0.2, fc='red', ec='red', length_includes_head=True, label="u at v")
plt.arrow(0, 0, w[0], w[1], head_width=0.1, head_length=0.2, fc='green', ec='green', length_includes_head=True, label="v + u")

# 投影
# 计算 u 在 v 上的投影
proj_uv = np.dot(u, v) / np.dot(v, v) * v
plt.arrow(0, 0, proj_uv[0], proj_uv[1], head_width=0.1, head_length=0.2, color='purple', linestyle='--', length_includes_head=True, label="proj of u on v")

# 设置图形属性
plt.axis('equal')
plt.xlim(-3, 5)
plt.ylim(-1, 4)
plt.grid(True)
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.title("Vector Operations: Addition and Projection")
plt.legend(["v", "u", "v+u", "projection of u on v"])

# 显示图形
plt.show()