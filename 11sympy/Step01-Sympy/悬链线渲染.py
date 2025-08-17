import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'SimHei', 'Microsoft YaHei']  # 常用支持中文的字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 正确显示负号

# 设置悬链线参数
a = 1.0
x = np.linspace(-3, 3, 400)
y = a * np.cosh(x / a)  # 悬链线方程

# 选择一个点P
x0 = 1.5
y0 = a * np.cosh(x0 / a)

# 计算曲率半径R
kappa = 1 / (a * np.cosh(x0 / a)**2)
R = 1 / kappa

# 计算法线长度L
dy_dx = np.sinh(x0 / a)  # 一阶导数
m_normal = -1 / dy_dx  # 法线斜率
x_intercept = x0 + a * np.cosh(x0 / a) * np.sinh(x0 / a)  # 法线与x轴交点
L = np.sqrt((x_intercept - x0)**2 + (0 - y0)**2)  # 法线长度

# 创建绘图
fig, ax = plt.subplots(figsize=(12, 8))

# 绘制悬链线
ax.plot(x, y, 'b-', linewidth=2, label=f'悬链线 $y = {a}\\cosh(x/{a})$')

# 绘制点P
ax.plot(x0, y0, 'ro', markersize=8, label=f'点 P(${x0:.1f}$, ${y0:.2f}$)')

# 绘制法线
x_normal = np.array([x0 - 2, x0, x_intercept])
y_normal = m_normal * (x_normal - x0) + y0
ax.plot(x_normal, y_normal, 'g--', linewidth=1.5, label='法线')

# 标记法线长度
mid_x = (x0 + x_intercept) / 2
mid_y = y0 / 2
ax.annotate(f'$L = {L:.4f}$', xy=(mid_x, mid_y),
            xytext=(mid_x+0.2, mid_y+0.2), fontsize=12,
            arrowprops=dict(arrowstyle='->', color='g'))

# 绘制曲率圆
# 计算曲率中心（沿法线方向偏移R）
normal_vector = np.array([1, m_normal]) / np.sqrt(1 + m_normal**2)
curvature_center = np.array([x0, y0]) - normal_vector * R * np.sign(dy_dx)

# 绘制曲率圆
circle = plt.Circle((curvature_center[0], curvature_center[1]), R,
                    color='r', fill=False, alpha=0.7, linewidth=2)
ax.add_patch(circle)
ax.plot(curvature_center[0], curvature_center[1], 'ro', markersize=6,
        label=f'曲率中心 ($R={R:.4f}$)')

# 添加标注
ax.annotate(f'$R = {R:.4f}$', xy=(curvature_center[0], curvature_center[1]),
            xytext=(curvature_center[0]+0.5, curvature_center[1]-0.3), fontsize=12,
            arrowprops=dict(arrowstyle='->', color='r'))

# 添加图例和标题
ax.legend(loc='upper center')
ax.set_title(f'悬链线曲率半径与法线长度关系 (a={a})')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.7)
ax.axhline(0, color='k', linewidth=0.5)
ax.axvline(0, color='k', linewidth=0.5)

# 显示结果
plt.show()

# 打印数值比较
print(f"计算值验证 (x0 = {x0}):")
print(f"曲率半径 R = {R:.6f}")
print(f"法线长度 L = {L:.6f}")
print(f"差值 |R - L| = {abs(R - L):.6e}")