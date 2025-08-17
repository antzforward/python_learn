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


# 基础梯形法
def trapezoid(f, a, b):
    """计算区间[a, b]上的梯形积分"""
    return (b - a) * (f(a) + f(b)) / 2


# 自适应梯形法
def adaptive_trapezoid(f, a, b, tol=1e-6, depth=0, max_depth=20, points=None):
    """
    自适应梯形法递归实现
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

    # 计算整个区间的梯形积分
    T1 = trapezoid(f, a, b)

    # 计算二等分后的积分
    m = (a + b) / 2
    T2_left = trapezoid(f, a, m)
    T2_right = trapezoid(f, m, b)
    T2 = T2_left + T2_right

    # 记录划分点
    points.append((a, b, depth))

    # 误差估计
    error = abs(T1 - T2) / 3

    # 递归终止条件
    if depth >= max_depth:
        return T2, points

    if error < tol:
        return T2, points
    else:
        # 递归处理两个子区间
        left_result, left_points = adaptive_trapezoid(
            f, a, m, tol / 2, depth + 1, max_depth, points
        )
        right_result, right_points = adaptive_trapezoid(
            f, m, b, tol / 2, depth + 1, max_depth, points
        )
        return left_result + right_result, points


# 可视化自适应划分过程
def visualize_adaptive_partition(f, a, b, points, method_name):
    """可视化自适应划分过程"""
    plt.figure(figsize=(12, 8))

    # 绘制函数曲线
    x = np.linspace(a, b, 500)
    y = f(x)
    plt.plot(x, y, 'b-', linewidth=2, label=r'$f(x)=e^{-x^2}$')

    # 绘制划分区间
    max_depth = max(p[2] for p in points) if points else 0
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
    plt.title(f'自适应{method_name}法区间划分', fontsize=14)
    plt.xlabel('x', fontsize=12)
    plt.ylabel('f(x)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()

    return plt


# 主程序：对比梯形法与辛普森法
if __name__ == "__main__":
    # 积分区间
    a, b = 0, 1

    # 计算精确值
    exact_value, _ = integrate.quad(f, a, b)

    # 设置参数
    tol = 1e-6
    max_depth = 15

    # 自适应梯形法
    trap_approx, trap_points = adaptive_trapezoid(f, a, b, tol, max_depth=max_depth)
    trap_error = abs(trap_approx - exact_value)


    # 自适应辛普森法（复用之前的实现）
    def simpson(f, a, b):
        c = (a + b) / 2
        h = (b - a) / 6
        return h * (f(a) + 4 * f(c) + f(b))


    def adaptive_simpson(f, a, b, tol=1e-6, depth=0, max_depth=20, points=None):
        if points is None:
            points = []
        S1 = simpson(f, a, b)
        m = (a + b) / 2
        S2_left = simpson(f, a, m)
        S2_right = simpson(f, m, b)
        S2 = S2_left + S2_right
        points.append((a, b, depth))
        error = abs(S1 - S2) / 15
        if depth >= max_depth:
            return S2, points
        if error < tol:
            return S2, points
        else:
            left_result, left_points = adaptive_simpson(
                f, a, m, tol / 2, depth + 1, max_depth, points
            )
            right_result, right_points = adaptive_simpson(
                f, m, b, tol / 2, depth + 1, max_depth, points
            )
            return left_result + right_result, points


    simp_approx, simp_points = adaptive_simpson(f, a, b, tol, max_depth=max_depth)
    simp_error = abs(simp_approx - exact_value)

    # 输出结果对比
    print(f"精确值: {exact_value:.10f}")
    print("\n自适应梯形法结果:")
    print(f"近似值: {trap_approx:.10f}")
    print(f"绝对误差: {trap_error:.4e}")
    print(f"递归深度: {max(p[2] for p in trap_points)}")
    print(f"总区间数: {len(trap_points)}")

    print("\n自适应辛普森法结果:")
    print(f"近似值: {simp_approx:.10f}")
    print(f"绝对误差: {simp_error:.4e}")
    print(f"递归深度: {max(p[2] for p in simp_points)}")
    print(f"总区间数: {len(simp_points)}")

    # 可视化
    plt_trap = visualize_adaptive_partition(f, a, b, trap_points, "梯形")
    plt_trap.savefig('adaptive_trapezoid.png', dpi=300)

    plt_simp = visualize_adaptive_partition(f, a, b, simp_points, "辛普森")
    plt_simp.savefig('adaptive_simpson.png', dpi=300)

    plt_trap.show()
    plt_simp.show()