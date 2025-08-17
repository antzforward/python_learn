from diffeq_gpu import WaveEquationSolver, create_wave_animation, create_3d_surface_plot
import matplotlib.pyplot as plt
import torch
import numpy as np

# 自定义初始条件 - 中心扰动
def wave_initial(x, y):
    center_x, center_y = x.shape[0] // 2, x.shape[1] // 2
    r = torch.sqrt((x - center_x)**2 + (y - center_y)**2)
    return torch.exp(-r**2 / 500) * torch.sin(r / 5)

# 初始化求解器
solver = WaveEquationSolver(grid_size=500, c=0.5, dt=0.01)
solver.set_initial_condition(initial_func=wave_initial)

# 求解方程
final_u, history = solver.solve(steps=300, record_interval=5)

# 创建波动动画
history_np = [h.numpy() for h in history]
animation = create_wave_animation(history_np, steps=300)
animation.save('wave_propagation.gif', writer='pillow', fps=15)

# 创建3D表面图
final_fig = create_3d_surface_plot(final_u.cpu().numpy(), title='Wave Final State')
final_fig.savefig('wave_final_3d.png', dpi=150)

plt.show()