import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, diff, solve, limit, oo, exp, ln, atan, sin, sqrt, pi
from sympy.calculus.util import continuous_domain
from sympy.solvers.inequalities import solve_univariate_inequality

# 设置绘图样式
plt.style.use('seaborn-whitegrid')
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'SimHei', 'Microsoft YaHei']  # 常用支持中文的字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 正确显示负号


def analyze_and_plot_function(f, x, x_range=(-5, 5), y_range=(-5, 5),
                              title="Function Plot", special_points=None):
    """
    分析函数性质并绘制图形

    参数:
    f: SymPy 表达式，要分析的函数
    x: SymPy 符号，自变量
    x_range: x轴范围
    y_range: y轴范围
    title: 图表标题
    special_points: 需要特别标注的点
    """
    # 计算一阶和二阶导数
    f_prime = diff(f, x)
    f_double_prime = diff(f_prime, x)

    # 寻找临界点（一阶导数为零或不存在的点）
    critical_points = solve(f_prime, x, domain=sp.Reals)

    # 寻找拐点（二阶导数为零或不存在的点）
    inflection_points = solve(f_double_prime, x, domain=sp.Reals)

    # 寻找渐近线
    asymptotes = find_asymptotes(f, x)

    # 确定凹凸区间
    concavity = determine_concavity(f_double_prime, x)

    # 打印分析结果
    print(f"分析函数: {f}")
    print(f"一阶导数: {f_prime}")
    print(f"二阶导数: {f_double_prime}")
    print(f"临界点: {critical_points}")
    print(f"拐点: {inflection_points}")
    print(f"渐近线: {asymptotes}")
    print(f"凹凸性: {concavity}")
    print("-" * 50)

    # 绘制函数图形
    plot_function(f, x, x_range, y_range, title,
                  critical_points, inflection_points, asymptotes, special_points)


def find_asymptotes(f, x):
    """寻找函数的渐近线"""
    asymptotes = []

    # 水平渐近线
    lim_pos = limit(f, x, oo)
    lim_neg = limit(f, x, -oo)

    if lim_pos.is_real:
        asymptotes.append(f"y = {lim_pos} (x→∞)")
    if lim_neg.is_real and lim_neg != lim_pos:
        asymptotes.append(f"y = {lim_neg} (x→-∞)")

    # 垂直渐近线（寻找函数不连续点）
    domain = continuous_domain(f, x, sp.Reals)
    if isinstance(domain, sp.Union):
        # 找到不连续点
        discontinuities = []
        for interval in domain.args:
            if isinstance(interval, sp.Interval):
                # 检查区间端点
                if interval.left_open and interval.left.is_real:
                    discontinuities.append(interval.left)
                if interval.right_open and interval.right.is_real:
                    discontinuities.append(interval.right)

        for point in discontinuities:
            if limit(f, x, point, dir='+') in [oo, -oo] or limit(f, x, point, dir='-') in [oo, -oo]:
                asymptotes.append(f"x = {point}")

    return asymptotes


def determine_concavity(f_double_prime, x):
    """确定函数的凹凸性"""
    # 找到二阶导数为零的点
    zeros = solve(f_double_prime, x, domain=sp.Reals)

    # 创建测试区间
    test_points = []
    if zeros:
        zeros_sorted = sorted([z.evalf() for z in zeros if z.is_real])
        test_points = [-oo] + zeros_sorted + [oo]
    else:
        test_points = [-oo, oo]

    # 在每个区间测试二阶导数的符号
    concavity = []
    for i in range(len(test_points) - 1):
        test_val = (test_points[i] + test_points[i + 1]) / 2
        if test_val == -oo:
            test_val = -1000
        elif test_val == oo:
            test_val = 1000

        sign = f_double_prime.subs(x, test_val)
        if sign > 0:
            concavity.append(f"({test_points[i]}, {test_points[i + 1]}): 凹向上")
        elif sign < 0:
            concavity.append(f"({test_points[i]}, {test_points[i + 1]}): 凹向下")

    return concavity


def plot_function(f, x, x_range, y_range, title,
                  critical_points, inflection_points, asymptotes, special_points=None):
    """绘制函数图形并标注特殊点"""
    # 创建数值函数用于绘图
    f_numeric = sp.lambdify(x, f, 'numpy')

    # 生成x值
    x_vals = np.linspace(x_range[0], x_range[1], 1000)

    # 计算y值
    y_vals = f_numeric(x_vals)

    # 创建图形
    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, y_vals, label=f'${sp.latex(f)}$')

    # 标注临界点
    for point in critical_points:
        if point.is_real and x_range[0] <= point <= x_range[1]:
            y_point = f.subs(x, point)
            plt.plot(point, y_point, 'ro', label=f'临界点 ({point:.2f}, {y_point:.2f})')

    # 标注拐点
    for point in inflection_points:
        if point.is_real and x_range[0] <= point <= x_range[1]:
            y_point = f.subs(x, point)
            plt.plot(point, y_point, 'go', label=f'拐点 ({point:.2f}, {y_point:.2f})')

    # 标注特殊点
    if special_points:
        for point in special_points:
            if point.is_real and x_range[0] <= point <= x_range[1]:
                y_point = f.subs(x, point)
                plt.plot(point, y_point, 'mo', label=f'特殊点 ({point:.2f}, {y_point:.2f})')

    # 绘制渐近线
    for asymptote in asymptotes:
        if asymptote.startswith('x ='):
            # 垂直渐近线
            x_val = float(asymptote.split('=')[1].strip())
            plt.axvline(x=x_val, color='r', linestyle='--', alpha=0.5, label=f'渐近线: {asymptote}')
        elif asymptote.startswith('y ='):
            # 水平渐近线
            y_val = float(asymptote.split('=')[1].split()[0].strip())
            plt.axhline(y=y_val, color='g', linestyle='--', alpha=0.5, label=f'渐近线: {asymptote}')

    plt.xlim(x_range)
    plt.ylim(y_range)
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


