import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

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
    return 0.4*mse + 0.6*max_err  # 可调权重

# 约束条件：系数非负
bounds = [(0.7, 0.8), (0.1, 0.2), (0.06, 0.07)]  # 基于经验参数的约束

# 使用经验参数作为初始值
initial_guess = np.array([0.787756, 0.145251, 0.066993], dtype=np.float32)

result = minimize(objective, initial_guess,
                bounds=bounds,
                method='SLSQP',
                options={'maxiter': 100})
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

print("{:<15} | {:^15} | {:^15}".format("Method", "MSE (1e-6)", "Max Error (1e-4)"))
print("-"*50)
for name, coeffs in methods.items():
    y_pred = polynomial(t, coeffs)
    mse, max_err = calc_errors(y_pred)
    print("{:<15} | {:>12.4f} | {:>14.4f}".format(name, mse*1e6, max_err*1e4))

plt.figure(figsize=(10, 6))

# 绘制误差曲线
plt.plot(t, (y_lsq - y_true)*1e4, label='Weighted LSQ')
plt.plot(t, (y_manual - y_true)*1e4, label='Manual Params')
plt.plot(t, (y_opt - y_true)*1e4, label='Optimized')

plt.title('Error Comparison (×10⁻⁴)')
plt.xlabel('t')
plt.ylabel('Error')
plt.legend()
plt.grid(True)
plt.show()