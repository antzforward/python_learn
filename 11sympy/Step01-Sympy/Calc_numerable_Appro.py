import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from scipy.special import roots_legendre


def trapezoidal_rule(f, a, b, n):
    """梯形法数值积分"""
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return h * (0.5 * y[0] + np.sum(y[1:-1]) + 0.5 * y[-1])


def adaptive_trapezoidal(f, a, b, tol=1e-6, max_iter=20):
    """
    自适应梯形法
    根据精度要求自动选择分割数n
    """
    n = 1
    prev_result = trapezoidal_rule(f, a, b, n)
    errors = []
    n_values = [n]

    for i in range(1, max_iter):
        n *= 2  # 加倍分割数
        result = trapezoidal_rule(f, a, b, n)
        error = abs(result - prev_result)
        errors.append(error)
        n_values.append(n)

        if error < tol:
            return result, n, errors, n_values

        prev_result = result

    return result, n, errors, n_values


def simpson_rule(f, a, b, n):
    """辛普森法数值积分"""
    if n % 2 != 0:
        n += 1  # 确保n为偶数
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return h / 3 * (y[0] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-2:2]) + y[-1])


def adaptive_simpson(f, a, b, tol=1e-6, max_iter=20):
    """
    自适应辛普森法
    根据精度要求自动选择分割数n
    """
    n = 2
    prev_result = simpson_rule(f, a, b, n)
    errors = []
    n_values = [n]

    for i in range(1, max_iter):
        n *= 2  # 加倍分割数
        result = simpson_rule(f, a, b, n)
        error = abs(result - prev_result)
        errors.append(error)
        n_values.append(n)

        if error < tol:
            return result, n, errors, n_values

        prev_result = result

    return result, n, errors, n_values


def romberg_integration(f, a, b, tol=1e-6, max_iter=20):
    """
    龙贝格积分法（自动满足精度要求）
    """
    R = np.zeros((max_iter, max_iter))
    n = 1
    h = b - a
    R[0, 0] = 0.5 * h * (f(a) + f(b))
    errors = []
    n_values = [1]

    for i in range(1, max_iter):
        h /= 2
        total = 0
        for k in range(1, 2 ** i, 2):
            total += f(a + k * h)

        R[i, 0] = 0.5 * R[i - 1, 0] + h * total

        for j in range(1, i + 1):
            R[i, j] = R[i, j - 1] + (R[i, j - 1] - R[i - 1, j - 1]) / (4 ** j - 1)

        error = abs(R[i, i] - R[i, i - 1])
        errors.append(error)
        n_values.append(2 ** i)

        if error < tol:
            return R[i, i], 2 ** i, errors, n_values

    return R[-1, -1], 2 ** (max_iter - 1), errors, n_values


def gaussian_quadrature(f, a, b, n):
    """高斯积分法"""
    x, w = roots_legendre(n)
    t = 0.5 * (b - a) * x + 0.5 * (a + b)
    return 0.5 * (b - a) * np.sum(w * f(t))


def adaptive_gaussian(f, a, b, tol=1e-6, max_iter=20):
    """
    自适应高斯积分法
    根据精度要求自动选择高斯点数
    """
    n = 2
    prev_result = gaussian_quadrature(f, a, b, n)
    errors = []
    n_values = [n]

    for i in range(1, max_iter):
        n += 2  # 增加高斯点数
        result = gaussian_quadrature(f, a, b, n)
        error = abs(result - prev_result)
        errors.append(error)
        n_values.append(n)

        if error < tol:
            return result, n, errors, n_values

        prev_result = result

    return result, n, errors, n_values


def calculate_with_sympy(f_expr, a, b):
    """使用 Sympy 计算精确积分值"""
    x = sp.symbols('x')
    integral = sp.integrate(f_expr, (x, a, b))
    if integral.has(sp.Integral):
        return integral.evalf()
    return integral.evalf()


def calculate_error(approx, exact):
    """计算相对误差"""
    return abs((approx - exact) / exact) * 100


def plot_convergence(methods_results, exact):
    """绘制收敛图"""
    plt.figure(figsize=(12, 8))

    for method_name, results in methods_results.items():
        n_values = results['n_values']
        errors = results['errors']

        # 确保n_values和errors长度一致
        min_len = min(len(n_values), len(errors))
        n_values = n_values[:min_len]
        errors = errors[:min_len]

        plt.loglog(n_values, errors, 'o-', label=method_name)

    plt.xlabel('Number of intervals/points')
    plt.ylabel('Absolute Error')
    plt.title('Convergence of Numerical Integration Methods')
    plt.legend()
    plt.grid(True, which="both", ls="-")
    plt.show()


def plot_error_reduction(methods_results, exact):
    """绘制误差减少图"""
    plt.figure(figsize=(12, 8))

    for method_name, results in methods_results.items():
        n_values = results['n_values']
        errors = results['errors']

        # 确保n_values和errors长度一致
        min_len = min(len(n_values), len(errors))
        n_values = n_values[:min_len]
        errors = errors[:min_len]

        # 计算相对误差
        relative_errors = [abs(err / exact) for err in errors]
        plt.loglog(n_values, relative_errors, 'o-', label=method_name)

    plt.xlabel('Number of intervals/points')
    plt.ylabel('Relative Error')
    plt.title('Error Reduction of Numerical Integration Methods')
    plt.legend()
    plt.grid(True, which="both", ls="-")
    plt.show()


# 测试函数
def test_function(x):
    """测试函数：sin(x^2)，在[0, 1]上无初等原函数"""
    return np.sin(x ** 2)


# 主程序
if __name__ == "__main__":
    # 定义积分区间
    a, b = 0, 1
    tol = 1e-6

    # 使用 Sympy 计算精确值
    x_sym = sp.symbols('x')
    f_expr = sp.sin(x_sym ** 2)
    exact_value = calculate_with_sympy(f_expr, a, b)
    print(f"Exact value (Sympy): {exact_value:.10f}")

    # 设置各种自适应数值积分方法
    methods = {
        "Adaptive Trapezoidal": adaptive_trapezoidal,
        "Adaptive Simpson": adaptive_simpson,
        "Romberg": romberg_integration,
        "Adaptive Gaussian": adaptive_gaussian
    }

    # 计算结果并收集数据
    results = {}
    print("\nAdaptive Numerical Integration Results:")
    for name, method in methods.items():
        result, n, errors, n_values = method(test_function, a, b, tol)
        rel_error = calculate_error(result, exact_value)

        print(f"{name}:")
        print(f"  Result: {result:.10f}")
        print(f"  Required n: {n}")
        print(f"  Relative error: {rel_error:.4e}%")

        # 收集数据用于绘图
        results[name] = {
            'result': result,
            'n': n,
            'errors': errors,
            'n_values': n_values
        }

    # 绘制收敛图
    plot_convergence(results, exact_value)
    plot_error_reduction(results, exact_value)

    # 分析不同精度要求下的表现
    print("\nPerformance at different tolerance levels:")
    tolerances = [1e-3, 1e-5, 1e-7, 1e-9]
    for tol in tolerances:
        print(f"\nTolerance: {tol:.1e}")
        for name, method in methods.items():
            result, n, _, _ = method(test_function, a, b, tol)
            rel_error = calculate_error(result, exact_value)
            print(f"  {name}: n={n}, error={rel_error:.2e}%")