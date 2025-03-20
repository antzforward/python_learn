import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from matplotlib.patches import RegularPolygon
from matplotlib.collections import PatchCollection


# 创建一个色相环
def create_hue_circle(ax, num_colors=6, shape='triangle'):
    # 定义色相环上的颜色
    hues = np.linspace(0, 1, num_colors, endpoint=False)
    colors = [mcolors.hsv_to_rgb([hue, 1, 1]) for hue in hues]

    # 绘制色相环
    circle = plt.Circle((0.5, 0.5), 0.4, fill=False, color='black', lw=2)
    ax.add_patch(circle)

    # 绘制颜色点
    angles = np.linspace(0, 2 * np.pi, num_colors, endpoint=False)
    for angle, color in zip(angles, colors):
        x = 0.5 + 0.4 * np.cos(angle)
        y = 0.5 + 0.4 * np.sin(angle)
        ax.plot(x, y, 'o', color=color, markersize=10)

    # 绘制形状（三角形、正方形、五角形等）
    if shape == 'triangle':
        num_sides = 3
    elif shape == 'square':
        num_sides = 4
    elif shape == 'pentagon':
        num_sides = 5
    else:
        raise ValueError("Unsupported shape")

    # 计算多边形的顶点颜色
    polygon_angles = np.linspace(0, 2 * np.pi, num_sides, endpoint=False)
    polygon_colors = [mcolors.hsv_to_rgb([(hue + 0.5) % 1, 1, 1]) for hue in hues[:num_sides]]

    # 创建多边形并填充颜色
    polygon = RegularPolygon((0.5, 0.5), num_sides, radius=0.4, edgecolor='black', lw=2)
    ax.add_patch(polygon)

    # 创建渐变填充
    patch_collection = PatchCollection([polygon], cmap='viridis')
    patch_collection.set_array(np.linspace(0, 1, len(polygon_colors)))
    ax.add_collection(patch_collection)

    # 显示中间色
    mid_angle = (angles[0] + angles[1]) / 2
    mid_x = 0.5 + 0.4 * np.cos(mid_angle)
    mid_y = 0.5 + 0.4 * np.sin(mid_angle)
    mid_color = mcolors.hsv_to_rgb([(hues[0] + hues[1]) / 2, 1, 1])
    ax.plot(mid_x, mid_y, 'o', color=mid_color, markersize=10)

    # 显示互补色
    comp_angle = angles[0] + np.pi
    comp_x = 0.5 + 0.4 * np.cos(comp_angle)
    comp_y = 0.5 + 0.4 * np.sin(comp_angle)
    comp_color = mcolors.hsv_to_rgb([(hues[0] + 0.5) % 1, 1, 1])
    ax.plot(comp_x, comp_y, marker='x', color=comp_color, markersize=10)


# 创建图形
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')
ax.axis('off')

# 绘制色相环和颜色组合
create_hue_circle(ax, num_colors=6, shape='triangle')

plt.show()