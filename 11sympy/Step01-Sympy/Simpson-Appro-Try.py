import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
import matplotlib.patches as patches

# 在导入matplotlib前设置环境变量
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'SimHei', 'Microsoft YaHei']  # 常用支持中文的字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 正确显示负号
# 定义被积函数
def f(x):
    return np.exp(-x ** 2)


# 精确解 (通过scipy获取)
exact_value, _ = integrate.quad(f, 0, 1)


# 辛普森法数值积分
def simpson_integral(a, b, n):
    """
    辛普森法数值积分
    :param a: 积分下限
    :param b: 积分上限
    :param n: 区间数（偶数）
    :return: 积分近似值
    """
    if n % 2 != 0:
        raise ValueError("区间数n必须是偶数")

    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)

    # 辛普森公式：首尾系数1，奇数索引系数4，偶数索引系数2
    coeffs = 4 * np.ones(n + 1)
    coeffs[0] = 1
    coeffs[n] = 1
    coeffs[2:n - 1:2] = 2  # 设置偶数索引点系数为2

    return (h / 3) * np.dot(coeffs, y)


# 可视化辛普森法近似的积分区域
def visualize_simpson(a, b, n):
    """
    可视化辛普森法近似的积分区域
    :param a: 积分下限
    :param b: 积分上限
    :param n: 区间数（偶数）
    """
    # 计算辛普森积分
    approx = simpson_integral(a, b, n)

    # 创建图形
    fig, ax = plt.subplots(figsize=(12, 8))

    # 绘制原函数曲线
    x_curve = np.linspace(a, b, 500)
    y_curve = f(x_curve)
    ax.plot(x_curve, y_curve, 'b-', linewidth=2, label=r'$f(x)=e^{-x^2}$')

    # 绘制分割点和抛物线
    h = (b - a) / n
    x_points = np.linspace(a, b, n + 1)
    y_points = f(x_points)
    ax.plot(x_points, y_points, 'ro', markersize=8, label='划分点')

    # 标注辛普森法信息
    ax.set_title(
        f'辛普森法数值积分 (n={n})：近似值={approx:.6f}, 精确值={exact_value:.6f}\n误差={abs(approx - exact_value):.6f}',
        fontsize=14)

    # 不同区间使用不同颜色填充
    colors = ['#FFDDDD', '#DDFFDD', '#DDDDFF', '#FFFFDD', '#FFDDFF']

    # 每组两个区间（即每三个点）填充一个抛物线区域
    for i in range(0, n, 2):  # 每次处理两个区间
        # 每组的三个点
        x0, x1, x2 = x_points[i], x_points[i + 1], x_points[i + 2]
        y0, y1, y2 = y_points[i], y_points[i + 1], y_points[i + 2]

        # 创建二次函数 p(x) = Ax² + Bx + C
        # 通过三点确定二次函数系数
        A = (y2 - 2 * y1 + y0) / (2 * h ** 2)
        B = (y2 - y0) / (2 * h)
        C = y1

        # 细分区间的点（用于绘制抛物线）
        x_parabola = np.linspace(x0, x2, 50)
        # 局部坐标：以x1为中心
        u = x_parabola - x1
        y_parabola = A * u ** 2 + B * u + C

        # 绘制抛物线
        ax.plot(x_parabola, y_parabola, 'm--', linewidth=1.5)

        # 填充抛物线下的面积
        ax.fill_between(x_parabola, y_parabola, alpha=0.2, color=colors[i // 2 % len(colors)])

        # 标记分区点
        ax.text((x0 + x1) / 2, min(y0, y1) * 0.9, f'区间 {i + 1}', ha='center', fontsize=10)
        ax.text((x1 + x2) / 2, min(y1, y2) * 0.9, f'区间 {i + 2}', ha='center', fontsize=10)

    # 设置图形属性
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('f(x)', fontsize=12)
    ax.legend(loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    return fig, ax


# 主程序
if __name__ == "__main__":
    # 积分区间
    a, b = 0, 1

    # 计算精确值
    exact_value, _ = integrate.quad(f, a, b)
    print(f"精确值: {exact_value:.8f}")

    # 不同区间数的结果比较
    n_values = [2, 4, 6, 8, 10]
    print("不同区间数的辛普森法结果:")
    for n in n_values:
        approx = simpson_integral(a, b, n)
        error = abs(approx - exact_value)
        print(f"n={n}: {approx:.8f} | 误差={error:.8f}")

    # 可视化展示 (以n=6为例)
    visualize_simpson(a, b, n=6)
    plt.savefig('simpson_integration.png', dpi=300)
    plt.show()