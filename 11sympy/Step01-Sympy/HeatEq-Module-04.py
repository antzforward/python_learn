from diffeq_gpu import GPUMonitor, HeatEquationSolver
from diffeq_gpu import create_performance_plot, create_temperature_animation
import matplotlib.pyplot as plt

# 初始化求解器
solver = HeatEquationSolver(grid_size=1000, alpha=0.25, dt=0.01)
solver.set_initial_condition()

# 使用GPU监控器
with GPUMonitor() as monitor:
    # 求解方程
    final_u, history = solver.solve(
        steps=500,
        record_interval=10,
        gpu_monitor=monitor
    )

# 获取性能数据
timestamps, utilizations, memory_usages = monitor.get_performance_data()

# 创建性能图表
perf_fig, _ = create_performance_plot(timestamps, utilizations, memory_usages)
perf_fig.savefig('heat_performance.png', dpi=150)

# 创建温度动画
history_np = [h.numpy() for h in history]
animation = create_temperature_animation(history_np, steps=500)
animation.save('heat_evolution.gif', writer='pillow', fps=10)

plt.show()