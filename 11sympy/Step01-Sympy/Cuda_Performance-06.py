from diffeq_gpu import HeatEquationSolver, GPUMonitor, warmup_gpu
import time
import matplotlib.pyplot as plt
import torch
# 预热GPU
warmup_gpu()

# 测试不同网格大小
sizes = [256, 512, 1024, 2048]
times = []
mem_usages = []

for size in sizes:
    print(f"\n测试网格大小: {size}x{size}")

    # 初始化求解器
    solver = HeatEquationSolver(grid_size=size)
    solver.set_initial_condition()

    # 使用GPU监控器
    with GPUMonitor() as monitor:
        start = time.time()
        _, _ = solver.solve(steps=100, gpu_monitor=monitor)
        end = time.time()

    # 记录性能
    times.append(end - start)
    mem_usages.append(max(monitor.memory_usages))

    # 清理内存
    del solver
    torch.cuda.empty_cache()

# 在导入matplotlib前设置环境变量
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'SimHei', 'Microsoft YaHei']  # 常用支持中文的字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 正确显示负号

# 绘制性能曲线
plt.figure(figsize=(10, 6))
plt.plot(sizes, times, 'o-', label='计算时间 (s)')
plt.plot(sizes, mem_usages, 's-', label='峰值显存 (MB)')
plt.xlabel('网格大小')
plt.ylabel('性能指标')
plt.title('热传导方程性能分析')
plt.legend()
plt.grid(True)
plt.savefig('performance_comparison.png', dpi=150)
plt.show()