import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb


def phyllotaxis_pattern(n_points=200, angle=137.508, c=1.5, size=20):
    """
    生成叶序分形图案
    参数:
        n_points: 总点数 (默认200)
        angle: 发散角度 (默认137.508度)
        c: 缩放因子 (默认1.5)
        size: 点的大小 (默认20)
    """
    # 黄金角转换为弧度 (0-2π)
    golden_angle = np.deg2rad(angle)

    # 生成索引序列
    n = np.arange(n_points)

    # 计算点的极坐标
    r = c * np.sqrt(n)  # 径向坐标
    theta = n * golden_angle  # 角度坐标

    # 转换为直角坐标
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    # 创建颜色映射 (HSV色调随角度变化)
    hue = (theta % (2 * np.pi)) / (2 * np.pi)
    colors = hsv_to_rgb(np.column_stack([hue, np.ones_like(hue), np.ones_like(hue)]))

    # 创建图形
    plt.figure(figsize=(10, 10), facecolor='black')
    ax = plt.subplot(111, aspect='equal')

    # 绘制点
    plt.scatter(x, y, s=size, c=colors, alpha=0.9, edgecolors='none')

    # 美化设置
    plt.title(f"Phyllotaxis Fractal\nAngle: {angle}°, Points: {n_points}",
              color='white', fontsize=16)
    plt.axis('off')
    plt.xlim(-c * np.sqrt(n_points) - 1, c * np.sqrt(n_points) + 1)
    plt.ylim(-c * np.sqrt(n_points) - 1, c * np.sqrt(n_points) + 1)
    plt.tight_layout()
    plt.savefig(f'phyllotaxis_fractal_{angle}_{c}.png', dpi=150, facecolor='white')
    plt.show()


def draw_psPhyllotaxys_equivalent():
    """
    完全复现LaTeX PSTricks中的 psPhyllotaxis 效果
    """
    import matplotlib.patches as patches
    # PSTricks默认参数
    n_points = 1000
    angle = 137.508  # PSTricks使用的黄金角
    c = 0.5  # 半径缩放因子

    # 创建图形并设置坐标轴范围(-3, -3)到(3,3)
    fig, ax = plt.subplots(figsize=(6, 6), facecolor='white')
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')
    ax.axis('off')  # 隐藏坐标轴

    # 生成点序列
    n = np.arange(1, n_points + 1)
    golden_angle = np.deg2rad(angle)

    # 计算坐标
    r = c * np.sqrt(n)
    theta = n * golden_angle
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    # 创建彩虹色映射 (匹配PSTricks的颜色方案)
    hue = (theta % (2 * np.pi)) / (2 * np.pi)
    saturation = 1 - (r / np.max(r)) * 0.8  # 外圈饱和度降低
    lightness = 0.7 - 0.4 * (r / np.max(r))  # 内圈亮度略低
    colors = hsv_to_rgb(np.column_stack([hue, saturation, lightness]))

    # 创建点对象 - 使用椭圆创建更好的视觉重叠效果
    for i in range(len(x)):
        ellipse = patches.Ellipse(
            (x[i], y[i]),
            width=0.15,
            height=0.15,
            angle=np.rad2deg(theta[i]) % 360,
            facecolor=colors[i],
            edgecolor='none'
        )
        ax.add_patch(ellipse)

    # 添加标题框以完全匹配 \psframebox 效果
    rect = patches.Rectangle(
        (-3, -3),
        6,
        6,
        linewidth=0.5,
        edgecolor='black',
        facecolor='none'
    )
    ax.add_patch(rect)

    plt.tight_layout()
    plt.savefig('psPhyllotaxis_equivalent.png', dpi=300, bbox_inches='tight')
    plt.show()
# 绘制等效效果
draw_psPhyllotaxys_equivalent()
# 生成三种不同的叶序分形图案
phyllotaxis_pattern(n_points=300, angle=137.508)  # 经典向日葵模式
phyllotaxis_pattern(n_points=500, angle=144.0)  # 替代黄金角模式
phyllotaxis_pattern(n_points=1000, angle=137.508, c=0.8)  # 高密度模式