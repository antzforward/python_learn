from sympy import symbols, Function, Eq, dsolve, solve
# 在导入matplotlib前设置环境变量
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'SimHei', 'Microsoft YaHei']  # 常用支持中文的字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 正确显示负号

def solve_bacteria_growth():
    """解决细菌增长问题"""
    # 定义符号变量
    t = symbols('t')  # 时间变量
    k = symbols('k')  # 增长比例常数
    y = Function('y')(t)  # 细菌数量函数
    C1 = symbols('C1')  # 积分常数

    # 问题1的解答
    print("===== 问题(1)解答 =====")
    # 建立微分方程
    eq = Eq(y.diff(t), k * y)
    print(f"微分方程: {eq}")

    # 求解通解
    general_solution = dsolve(eq, y)
    print(f"通解: {general_solution}")

    # 设初始条件: t=0时细菌数为y0
    # 条件1: t=4时，y=2*y0
    solution_1 = general_solution

    # 替换初始条件
    y0_1 = symbols('y0_1')  # 初始细菌数
    cond_equation_1 = Eq(solution_1.rhs.subs(t, 4), 2 * y0_1)
    cond_equation_1 = cond_equation_1.subs(general_solution.lhs, solution_1.rhs)

    # 求解常数关系
    k_value = solve(cond_equation_1, k)[0]
    print(f"比例常数k: {k_value}")

    # 计算12小时后的细菌数
    solution_at_12h = solution_1.rhs.subs(k, k_value).subs(C1, y0_1).simplify()
    solution_at_12h = solution_at_12h.subs(t, 12)

    # 表达为初始数量的倍数
    multiple = solution_at_12h / y0_1
    print(f"12小时后细菌数是初始的 {multiple} 倍")

    # 问题2的解答
    print("\n===== 问题(2)解答 =====")
    # 建立相同的微分方程
    # 使用相同的通解

    # 设定边界条件
    y3 = 10 ** 4  # 3小时时的细菌数
    y5 = 4 * 10 ** 4  # 5小时时的细菌数

    # 使用两个时间点的值求解
    # 时间点1: t=3, y=y3
    eq3 = Eq(general_solution.rhs.subs(t, 3), y3)
    # 时间点2: t=5, y=y5
    eq5 = Eq(general_solution.rhs.subs(t, 5), y5)

    # 求解常数
    constants = solve([eq3, eq5], (k, C1))
    print(f"常数解: k = {constants[0]}, C1 = {constants[1]}")

    # 计算初始值(t=0)
    initial_value = general_solution.rhs.subs(t, 0).subs(constants)
    print(f"初始细菌数: {initial_value}")


# 执行解答
solve_bacteria_growth()