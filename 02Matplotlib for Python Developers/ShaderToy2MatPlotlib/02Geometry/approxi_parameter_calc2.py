import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

## 这里重点在于如何找的合适的参数


# 初始化参数
t = np.linspace(0, 1, 1000, dtype=np.float32)
y_true = np.tan(t * np.pi/4, dtype=np.float32)

# 定义多项式形式
def polynomial(t, coeffs):
    """ 5次多项式结构 """
    return t * (coeffs[0] + t**2*(coeffs[1] + t**2*coeffs[2]))

# 重新构建设计矩阵（保持与shader相同结构）
X = np.column_stack([t, t**3, t**5]).astype(np.float32)

# 带权重的最小二乘法
weights = np.linspace(1, 3, len(t), dtype=np.float32)  # 强调后半段精度
coeffs_lsq = np.linalg.lstsq(X * weights[:, None], y_true * weights, rcond=None)[0].astype(np.float32)

def objective(coeffs):
    pred = polynomial(t, coeffs)
    mse = np.mean((pred - y_true)**2)
    max_err = np.max(np.abs(pred - y_true))
    return 0.2*mse + 0.8*max_err  # 更强调最大误差优化

# 原约束范围
bounds = [(0.78, 0.80), (0.12, 0.16), (0.06, 0.07)]  # 更宽松的范围


# 使用经验参数作为初始值
initial_guesses = [
    np.array([0.787756, 0.145251, 0.066993], dtype=np.float32),
    np.array([0.785, 0.15, 0.065],dtype=np.float32),            # 扰动初始值1
    np.array([0.79, 0.14, 0.07],dtype=np.float32),              # 扰动初始值2
]

result = minimize(objective, initial_guesses[1],
                bounds=bounds,
                method='SLSQP',
                options={'maxiter': 500,'ftol':1e-6})
coeffs_opt = result.x.astype(np.float32)


# 计算各方法的预测值
y_lsq = polynomial(t, coeffs_lsq)
y_manual = polynomial(t, [0.787756, 0.145251, 0.066993])
y_opt = polynomial(t, coeffs_opt)

# 误差计算函数
def calc_errors(y_pred):
    y_pred = y_pred.astype(np.float32)
    mse = np.mean((y_true - y_pred)**2)
    max_err = np.max(np.abs(y_true - y_pred))
    return mse, max_err

# 对比结果
methods = {
    "Weighted LSQ": coeffs_lsq,
    "Manual Params": [0.787756, 0.145251, 0.066993],
    "Optimized": coeffs_opt
}
print( coeffs_opt )
print("{:<15} | {:^15} | {:^15}".format("Method", "MSE (1e-6)", "Max Error (1e-4)"))
print("-"*50)
for name, coeffs in methods.items():
    y_pred = polynomial(t, coeffs)
    mse, max_err = calc_errors(y_pred)
    print("{:<15} | {:>12.4f} | {:>14.4f}".format(name, mse*1e6, max_err*1e4))

plt.figure(figsize=(10, 4))

# 误差分布直方图
plt.subplot(121)
plt.hist((y_manual - y_true)*1e4, bins=50, alpha=0.5, label='Manual')
plt.hist((y_opt - y_true)*1e4, bins=50, alpha=0.5, label='Optimized')
plt.xlabel('Error (×10⁻⁴)')
plt.ylabel('Count')
plt.legend()

# 累积误差分布
plt.subplot(122)
plt.plot(np.sort(np.abs(y_manual - y_true)*1e4),
        np.linspace(0,1,len(t)), label='Manual')
plt.plot(np.sort(np.abs(y_opt - y_true)*1e4),
        np.linspace(0,1,len(t)), label='Optimized')
plt.xlabel('Absolute Error (×10⁻⁴)')
plt.ylabel('CDF')
plt.legend()

plt.tight_layout()
plt.show()