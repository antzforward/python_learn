from sympy import *


def curvature_center(xt, yt, zt, t_val):
    """计算空间曲线在给定点处的外切球（密切球）的球心和半径"""
    r = Matrix([xt, yt, zt])  # 曲线参数方程

    # 一阶导数（切向量）
    T_t = r.diff(t)
    T = T_t.subs(t, t_val)  # t_val 处的切向量
    T_mag = T.norm()  # 切向量模长

    # 二阶导数（加速度）
    A_t = T_t.diff(t)
    A = A_t.subs(t, t_val)  # t_val 处的加速度

    # 计算叉积 T × A
    cross_TA = T.cross(A)
    cross_TA_mag = cross_TA.norm()

    # 计算曲率 κ
    kappa = cross_TA_mag / (T_mag ** 3) if T_mag != 0 else 0

    # 计算单位切向量
    unit_T = T / T_mag

    # 计算单位切向量的导数（T'）
    unit_T_prime = diff(unit_T, t).subs(t, t_val)

    # 计算单位主法向量 N
    N_prime = unit_T_prime
    N_prime_mag = N_prime.norm()
    unit_N = N_prime / N_prime_mag if N_prime_mag != 0 else Matrix([0, 0, 0])

    # 计算曲率中心 C = r(t0) + (1/κ) * N
    r_t0 = r.subs(t, t_val)
    R = 1 / kappa if kappa != 0 else oo  # 曲率半径
    center = r_t0 + unit_N * R

    return center, R, kappa

t = symbols('t')
# 示例：螺旋线 r(t) = (cos(t), sin(t), t)
xt, yt, zt = cos(t), sin(t), t
t_val = pi  # 在 t=π 处计算

# 计算密切球球心和半径
center, radius, kappa = curvature_center(xt, yt, zt, t_val)

print(f"在 t={t_val} 处：")
print(f"位置：({center[0].evalf():.4f}, {center[1].evalf():.4f}, {center[2].evalf():.4f})")
print(f"曲率：κ = {kappa.evalf():.6f}")
print(f"曲率半径：R = {radius.evalf():.6f}")
print(f"密切球球心：({center[0].evalf():.6f}, {center[1].evalf():.6f}, {center[2].evalf():.6f})")