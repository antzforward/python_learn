import numpy as np
import matplotlib.pyplot as plt

# 设置支持中文的字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 设置抛物面参数
p = 1.0  # 焦距参数
x_min, x_max = -1, 5
y_min, y_max = -3, 3

# 创建抛物线 (y² = 4px)
x_parabola = np.linspace(0, x_max, 200)
y_parabola = 2 * np.sqrt(p * x_parabola)  # 上半部分
y_parabola_neg = -y_parabola  # 下半部分

# 创建图形
fig, ax = plt.subplots(figsize=(12, 8))

# 绘制抛物线
ax.plot(x_parabola, y_parabola, 'b-', linewidth=2, label='抛物面反射镜')
ax.plot(x_parabola, y_parabola_neg, 'b-', linewidth=2)

# 绘制焦点
focus_x, focus_y = p, 0
ax.scatter(focus_x, focus_y, color='red', s=100, label='点光源（焦点）')

# 生成从焦点发出的多角度光线
num_rays = 20
angles = np.linspace(-np.pi / 2.5, np.pi / 2.5, num_rays)


# 计算光线路径
def calculate_ray_path(angle):
    # 入射光线参数方程（从焦点发出）
    t_incident = np.linspace(0, 2, 50)
    incident_x = focus_x + t_incident * np.cos(angle)
    incident_y = focus_y + t_incident * np.sin(angle)

    # 找到与抛物线的交点
    intersection = None
    for i in range(len(incident_x)):
        x_val = incident_x[i]
        if x_val < 0:  # 只考虑x>0的部分
            continue

        # 抛物线方程 y² = 4px
        parabola_y = 2 * np.sqrt(p * x_val)

        # 检查是否接近抛物线
        if abs(incident_y[i]) <= abs(parabola_y) and abs(incident_y[i]) > 0.01:
            # 使用更精确的方法找到交点
            # 参数化抛物线: (t^2/(4p), t), t为参数
            # 我们需要解方程: 焦点到交点的直线与抛物线相交
            t_para = 2 * np.sqrt(p * x_val)
            if incident_y[i] > 0:
                t_para = abs(t_para)
            else:
                t_para = -abs(t_para)

            # 精确交点
            exact_x = t_para ** 2 / (4 * p)
            exact_y = t_para

            # 如果当前点接近精确交点
            if (abs(incident_x[i] - exact_x) < 0.1 and
                    abs(incident_y[i] - exact_y) < 0.1):
                intersection = (exact_x, exact_y)
                break

    # 如果没有找到精确交点，使用近似交点
    if intersection is None:
        for i in range(len(incident_x)):
            x_val = incident_x[i]
            if x_val < 0:
                continue

            parabola_y = 2 * np.sqrt(p * x_val)
            if abs(incident_y[i]) <= abs(parabola_y) + 0.1:
                intersection = (x_val, incident_y[i])
                break

    if intersection is None:
        return None, None, None, None

    # 反射光线（水平向右，平行于x轴）
    reflection_length = 2
    reflection_x = np.linspace(intersection[0], intersection[0] + reflection_length, 20)
    reflection_y = intersection[1] * np.ones_like(reflection_x)

    # 只保留入射光线到交点的部分
    incident_x_to_intersection = np.linspace(focus_x, intersection[0], 30)
    incident_y_to_intersection = np.linspace(focus_y, intersection[1], 30)

    return incident_x_to_intersection, incident_y_to_intersection, reflection_x, reflection_y


# 绘制光线
for angle in angles:
    if abs(angle) < 0.01:  # 跳过接近水平的光线，避免数值问题
        continue

    incident_x, incident_y, reflection_x, reflection_y = calculate_ray_path(angle)

    # 只绘制找到交点的光线
    if incident_x is not None:
        # 绘制入射光线（橙色）
        ax.plot(incident_x, incident_y, color='orange', alpha=0.8, linewidth=1.5)

        # 绘制反射光线（绿色）
        ax.plot(reflection_x, reflection_y, color='green', alpha=0.8, linewidth=1.5)

        # 标记交点
        ax.scatter(incident_x[-1], incident_y[-1], color='purple', s=20, alpha=0.7)

# 添加光轴
ax.axhline(0, color='black', linestyle='--', alpha=0.5, linewidth=1)

# 添加说明文本
ax.text(0.5, 2.5, '入射光线（橙色）', color='orange', fontsize=12, fontweight='bold')
ax.text(3.0, 2.5, '反射光线（绿色，平行）', color='green', fontsize=12, fontweight='bold')
ax.text(0.5, -2.5, '点光源位于抛物线焦点', color='red', fontsize=10)
ax.text(3.0, -2.5, '反射后形成平行光束', color='green', fontsize=10)

# 设置图形属性
ax.set_xlabel('X轴')
ax.set_ylabel('Y轴')
ax.set_title('抛物面反射镜：点光源发出的光线反射后形成平行光', fontsize=14, fontweight='bold')
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.grid(True, linestyle='--', alpha=0.3)
ax.legend(loc='upper right')

# 添加坐标箭头
ax.arrow(x_min, 0, x_max - x_min + 0.5, 0, head_width=0.1, head_length=0.1, fc='k', ec='k')
ax.arrow(0, y_min, 0, y_max - y_min + 0.5, head_width=0.1, head_length=0.1, fc='k', ec='k')

plt.tight_layout()
plt.show()