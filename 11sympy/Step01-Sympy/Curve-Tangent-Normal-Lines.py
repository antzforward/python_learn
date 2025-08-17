import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
from sympy import symbols, cos, sin, diff, lambdify
from matplotlib.patches import FancyArrowPatch
from matplotlib.text import Text

# 定义符号变量
t, a = symbols('t a')
# 参数方程（摆线）
x_expr = a * (t - sin(t))
y_expr = a * (1 - cos(t))

# 计算切向量（一阶导数）
dx_dt = diff(x_expr, t)
dy_dt = diff(y_expr, t)

# 计算法向量 - 通过旋转切向量90度
nx_expr = -dy_dt
ny_expr = dx_dt

# 转换为数值函数
t_val = symbols('t')
a_val = 1.0  # 设置常数a的值

# 创建数值函数
x_func = lambdify(t_val, x_expr.subs({a: a_val, t: t_val}), 'numpy')
y_func = lambdify(t_val, y_expr.subs({a: a_val, t: t_val}), 'numpy')
dx_func = lambdify(t_val, dx_dt.subs({a: a_val, t: t_val}), 'numpy')
dy_func = lambdify(t_val, dy_dt.subs({a: a_val, t: t_val}), 'numpy')
nx_func = lambdify(t_val, nx_expr.subs({a: a_val, t: t_val}), 'numpy')
ny_func = lambdify(t_val, ny_expr.subs({a: a_val, t: t_val}), 'numpy')

# 生成曲线数据
t_points = np.linspace(0.01, 4 * np.pi, 1000)
x_points = x_func(t_points)
y_points = y_func(t_points)

# 创建图形和事件处理
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x_points, y_points, 'b-', label='Cycloid')
ax.set_title('Click on the curve to show tangent and normal')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.grid(True)
ax.axis('equal')  # 保持比例一致
ax.legend()

# 存储当前绘制的对象
current_tangent = None
current_normal = None
current_point = None
current_tangent_text = None
current_normal_text = None


def find_closest_t(x_click, y_click):
    """查找曲线上距离点击位置最近的t值"""

    def distance_squared(t_val):
        x_curve = x_func(t_val)
        y_curve = y_func(t_val)
        return (x_curve - x_click) ** 2 + (y_curve - y_click) ** 2

    # 在t范围内搜索最小距离
    result = minimize_scalar(distance_squared, bounds=(0.01, 4 * np.pi), method='bounded')
    return result.x


def onclick(event):
    global current_tangent, current_normal, current_point, current_tangent_text, current_normal_text

    # 只处理主鼠标按钮点击
    if event.button != 1 or not event.inaxes:
        return

    # 查找最近点对应的t值
    t_closest = find_closest_t(event.xdata, event.ydata)

    # 计算曲线上的点
    x0 = float(x_func(t_closest))
    y0 = float(y_func(t_closest))

    # 计算切向量和法向量
    dx = float(dx_func(t_closest))
    dy = float(dy_func(t_closest))
    nx = float(nx_func(t_closest))
    ny = float(ny_func(t_closest))

    # 归一化向量（保持方向，固定长度）
    tangent_length = 0.8 * a_val
    normal_length = 0.8 * a_val

    # 计算向量长度
    tangent_mag = np.sqrt(dx ** 2 + dy ** 2)
    normal_mag = np.sqrt(nx ** 2 + ny ** 2)

    # 避免除以零
    if tangent_mag > 1e-10:
        scale_t = tangent_length / tangent_mag
    else:
        scale_t = 0

    if normal_mag > 1e-10:
        scale_n = normal_length / normal_mag
    else:
        scale_n = 0

    # 清除之前的对象
    if current_tangent:
        current_tangent.remove()
    if current_normal:
        current_normal.remove()
    if current_point:
        current_point.remove()
    if current_tangent_text:
        current_tangent_text.remove()
    if current_normal_text:
        current_normal_text.remove()

    # 创建新的点标记
    current_point = ax.plot([x0], [y0], 'ko', markersize=6, label='Point')[0]

    # 创建带箭头的切线
    current_tangent = FancyArrowPatch(
        (x0, y0),
        (x0 + dx * scale_t, y0 + dy * scale_t),
        arrowstyle='->', mutation_scale=15,
        color='red', linewidth=2
    )
    ax.add_patch(current_tangent)

    # 创建带箭头的法线
    current_normal = FancyArrowPatch(
        (x0, y0),
        (x0 + nx * scale_n, y0 + ny * scale_n),
        arrowstyle='->', mutation_scale=15,
        color='green', linewidth=2
    )
    ax.add_patch(current_normal)

    # 添加向量标注（放在箭头中间位置）
    t_mid_x = x0 + dx * scale_t * 0.5
    t_mid_y = y0 + dy * scale_t * 0.5
    n_mid_x = x0 + nx * scale_n * 0.5
    n_mid_y = y0 + ny * scale_n * 0.5

    current_tangent_text = ax.text(t_mid_x, t_mid_y, 'T', color='red',
                                   fontsize=12, ha='center', va='center',
                                   bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2'))

    current_normal_text = ax.text(n_mid_x, n_mid_y, 'N', color='green',
                                  fontsize=12, ha='center', va='center',
                                  bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2'))

    # 更新图例
    handles, labels = ax.get_legend_handles_labels()
    # 只保留曲线和点的图例
    filtered_handles = [h for h, l in zip(handles, labels) if l in ['Cycloid', 'Point']]
    filtered_labels = [l for l in labels if l in ['Cycloid', 'Point']]

    # 添加切线和法线的图例
    filtered_handles.append(plt.Line2D([0], [0], color='red', linewidth=2))
    filtered_labels.append('Tangent')
    filtered_handles.append(plt.Line2D([0], [0], color='green', linewidth=2))
    filtered_labels.append('Normal')

    ax.legend(filtered_handles, filtered_labels)

    # 打印点信息
    print(f"Clicked at t={t_closest:.4f}, point=({x0:.4f}, {y0:.4f})")
    print(f"Tangent vector: ({dx:.4f}, {dy:.4f})")
    print(f"Normal vector: ({nx:.4f}, {ny:.4f})")

    fig.canvas.draw()


# 连接点击事件
fig.canvas.mpl_connect('button_press_event', onclick)
plt.tight_layout()
plt.show()