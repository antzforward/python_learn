import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from math import pi

# 参数设置
NUMPOINTS = 16
FPS = 30
TOTAL_FRAMES = 200
DPI = 100

# 初始化图形
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5), facecolor='black')
fig.suptitle('Circle Parametrization Comparison', color='white', fontsize=16)
axes = [ax1, ax2, ax3]

for ax in axes:
    ax.set_facecolor('black')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect('equal')
    ax.invert_yaxis()  # 修复坐标系方向

# 初始化绘图元素
plots = []
colors = plt.cm.hsv(np.linspace(0, 1, NUMPOINTS))

for ax in axes:
    plot = [ax.plot([], [], '-', lw=1, alpha=0.3, color='white')[0]]
    for c in colors:
        plot.append(ax.plot([], [], 'o', markersize=6, color=c, alpha=0.8)[0])
    plots.append(plot)

titles = [
    "Method 1: Trigonometric\n(cosθ, sinθ)",
    "Method 2: Square Root\nParameterization",
    "Method 3: Rational Function\nParameterization"
]


# 参数化方法实现 ----------------------------------------------------------------

def method0(t):
    """ 传统三角函数方法 """
    angle = 2 * pi * t
    return np.column_stack([np.cos(angle),-np.sin(angle)])


def method1(t):
    """ 平方根参数化方法 """
    s = (t*4.0) % 1.0
    s = s ** 2 * (3 - 2 * s)  # Cubic smoothstep

    points = np.column_stack([np.sqrt(1 - s), np.sqrt(s)])

    # 精确象限处理
    quadrant = np.floor(t * 4).astype(int) % 4
    for i in range(len(points)):
        q = quadrant[i]
        x, y = points[i]
        if q == 1:
            points[i] = [x,-y]#[-y, x]
        elif q == 2:
            points[i] = [-y,-x]#[-x, -y]
        elif q == 3:
            points[i] = [-x,y]#[y, -x]
        else:#0象限 也要转换
            points[i] = [y, x]
    return points


def method2(t):
    """ 有理分式参数化方法 """
    s = (t*4.0) % 1.0
    s2 = s ** 2
    s = s * (0.787756 + s2 * (0.145251 + s2 * 0.066993))  # 多项式近似

    points = np.column_stack([(1 - s ** 2) / (1 + s ** 2), (2 * s) / (1 + s ** 2)])

    # 精确象限处理
    quadrant = np.floor(t * 4).astype(int) % 4
    for i in range(len(points)):
        q = quadrant[i]
        x, y = points[i]
        if q == 1:
            points[i] = [x, -y]  # [-y, x]
        elif q == 2:
            points[i] = [-y, -x]  # [-x, -y]
        elif q == 3:
            points[i] = [-x, y]  # [y, -x]
        else:  # 0 象限 也要转换
            points[i] = [y, x]
    return points


# 动画更新函数 ----------------------------------------------------------------
def animate(frame):
    time = frame / FPS

    for ax, plot, title in zip(axes, plots, titles):
        ax.set_title(title, color='white', fontsize=10)

        # 生成参数序列（修正时间范围）
        t = np.linspace(0, 1, NUMPOINTS, endpoint=False) + time / 4

        # 获取点位置
        if ax == ax1:
            points = method0(t)
        elif ax == ax2:
            points = method1(t)
        else:
            points = method2(t)

        # 更新线
        plot[0].set_data(points[:, 0], points[:, 1])

        # 更新点（修复警告）
        for i in range(NUMPOINTS):
            plot[i + 1].set_data([points[i, 0]], [points[i, 1]])

    return [elem for plot in plots for elem in plot]


# 创建动画 ---------------------------------------------------------------------
ani = FuncAnimation(
    fig,
    animate,
    frames=TOTAL_FRAMES,
    interval=1000 / FPS,
    blit=True
)

plt.show()