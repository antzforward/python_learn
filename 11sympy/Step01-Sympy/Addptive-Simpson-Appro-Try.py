import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

# 在导入matplotlib前设置环境变量
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'SimHei', 'Microsoft YaHei']  # 常用支持中文的字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 正确显示负号
# 定义被积函数
def f(x):
    return np.exp(-x ** 2)


# 辛普森积分基础函数
def simpson(f, a, b):
    """计算区间[a, b]上的辛普森积分"""
    c = (a + b) / 2
    h = (b - a) / 6  # 辛普森公式中的h/3因子
    return h * (f(a) + 4 * f(c) + f(b))


# 自适应辛普森法
def adaptive_simpson(f, a, b, tol=1e-6, depth=0, max_depth=20, points=None):
    """
    自适应辛普森法递归实现
    :param f: 被积函数
    :param a: 区间左端点
    :param b: 区间右端点
    :param tol: 容差
    :param depth: 当前递归深度
    :param max_depth: 最大递归深度
    :param points: 用于记录划分点
    :return: 积分近似值
    """
    if points is None:
        points = []

    # 计算整个区间的辛普森积分
    S1 = simpson(f, a, b)

    # 计算二等分后的积分
    m = (a + b) / 2
    S2_left = simpson(f, a, m)
    S2_right = simpson(f, m, b)
    S2 = S2_left + S2_right

    # 记录划分点
    points.append((a, b, depth))

    # 误差估计
    error = abs(S1 - S2) / 15

    # 递归终止条件
    if depth >= max_depth:
        return S2, points

    if error < tol:
        return S2, points
    else:
        # 递归处理两个子区间
        left_result, left_points = adaptive_simpson(
            f, a, m, tol / 2, depth + 1, max_depth, points
        )
        right_result, right_points = adaptive_simpson(
            f, m, b, tol / 2, depth + 1, max_depth, points
        )
        return left_result + right_result, points


# 可视化自适应划分过程
def visualize_adaptive_partition(f, a, b, points):
    """可视化自适应划分过程"""
    plt.figure(figsize=(12, 8))

    # 绘制函数曲线
    x = np.linspace(a, b, 500)
    y = f(x)
    plt.plot(x, y, 'b-', linewidth=2, label=r'$f(x)=e^{-x^2}$')

    # 绘制划分区间
    colors = plt.cm.viridis(np.linspace(0, 1, max_depth + 1))
    for (start, end, depth) in points:
        depth_color = colors[depth]
        plt.axvline(x=start, color=depth_color, linestyle='--', alpha=0.7)
        plt.axvline(x=end, color=depth_color, linestyle='--', alpha=0.7)

        # 标记深度
        mid = (start + end) / 2
        plt.text(mid, f(mid) * 0.8, f'depth={depth}',
                 ha='center', fontsize=9, color=depth_color)

    # 标记最后一个点
    plt.axvline(x=b, color='red', linestyle='-', linewidth=1.5)

    # 添加图例和标题
    plt.title('自适应辛普森法区间划分', fontsize=14)
    plt.xlabel('x', fontsize=12)
    plt.ylabel('f(x)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()

    return plt


# 主程序
if __name__ == "__main__":
    # 积分区间
    a, b = 0, 1

    # 计算精确值
    exact_value, _ = integrate.quad(f, a, b)

    # 使用自适应辛普森法
    tol = 1e-6
    max_depth = 10
    approx, points = adaptive_simpson(f, a, b, tol, max_depth=max_depth)

    # 输出结果
    print(f"精确值: {exact_value:.10f}")
    print(f"自适应辛普森法近似值: {approx:.10f}")
    print(f"绝对误差: {abs(approx - exact_value):.4e}")
    print(f"相对误差: {abs(approx - exact_value) / exact_value:.4e}")
    print(f"递归深度: {max(p[2] for p in points)}")
    print(f"总区间数: {len(points)}")

    # 可视化
    plt = visualize_adaptive_partition(f, a, b, points)
    plt.savefig('adaptive_simpson.png', dpi=300)
    plt.show()