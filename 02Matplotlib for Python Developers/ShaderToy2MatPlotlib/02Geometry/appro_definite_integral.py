import numpy as np

def trapezoidal(f, a, b, n):
    h = (b - a) / n
    x = np.linspace(a, b, n+1)
    y = f(x)
    return h/2 * (y[0] + 2*np.sum(y[1:-1]) + y[-1])

def simpson(f, a, b, n):
    if n % 2 != 0:
        n += 1  # 确保n为偶数
    h = (b - a) / n
    x = np.linspace(a, b, n+1)
    y = f(x)
    return h/3 * (y[0] + 4*np.sum(y[1:-1:2]) + 2*np.sum(y[2:-2:2]) + y[-1])

# 测试积分x【0，pi/2】 f = sin(x)sin(2x)sin(3x) 的情况
f = lambda  x: np.sin(x)*np.sin(2*x)*np.sin(3*x)
exact = 1/6
print("梯形法结果:", trapezoidal(f, 0, np.pi*0.5, 6))
print("辛普森法结果:", simpson(f, 0, np.pi*0.5, 6))
print("精确值:", exact)