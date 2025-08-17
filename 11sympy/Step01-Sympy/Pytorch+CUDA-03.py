import torch
import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib.animation import FuncAnimation
import sys

# 在导入matplotlib前设置环境变量
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'SimHei', 'Microsoft YaHei']  # 常用支持中文的字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 正确显示负号

# 导入NVML监控模块
def init_gpu_monitoring():
    """GPU监控的跨版本实现"""

    class GPUMonitor:
        def __init__(self):
            self.use_nvml = False
            self.gpu_count = torch.cuda.device_count()

            try:
                # 尝试使用PyTorch内置API (v1.10+)
                if hasattr(torch.cuda, 'utilization'):
                    self.utilization = self._get_utilization_torch
                    print("使用 PyTorch 内置 GPU 监控")
                else:
                    # 使用NVML库
                    import pynvml
                    pynvml.nvmlInit()
                    self.use_nvml = True
                    self.pynvml = pynvml
                    self.handles = [pynvml.nvmlDeviceGetHandleByIndex(i) for i in range(self.gpu_count)]
                    self.utilization = self._get_utilization_nvml
                    print("使用 NVML GPU 监控")
            except ImportError:
                self.utilization = lambda: [-1]
                print("无法初始化 GPU 监控")

        def _get_utilization_torch(self):
            return [torch.cuda.utilization(i) for i in range(self.gpu_count)]

        def _get_utilization_nvml(self):
            utils = []
            for handle in self.handles:
                util = self.pynvml.nvmlDeviceGetUtilizationRates(handle)
                utils.append(util.gpu)
            return utils

        def memory_usage(self):
            return [torch.cuda.memory_allocated(i) for i in range(self.gpu_count)]

        def close(self):
            if self.use_nvml:
                self.pynvml.nvmlShutdown()

    return GPUMonitor()


# 初始化GPU监控
gpu_monitor = init_gpu_monitoring()

# 热传导模拟参数
grid_size = 1000
alpha = 0.25
dt = 0.01
steps = 500
snapshot_interval = 50

# 在GPU上初始化张量
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"\n使用设备: {device}")
if device.type == 'cuda':
    print(f"检测到 {torch.cuda.device_count()} 个GPU设备")
    print(f"设备名称: {torch.cuda.get_device_name(0)}")
    print(f"计算能力: {torch.cuda.get_device_capability(0)}")
    print(f"总显存: {torch.cuda.get_device_properties(0).total_memory / 1024 ** 3:.2f} GB\n")

# 创建温度场和边界掩码
u = torch.zeros(grid_size, grid_size, device=device, dtype=torch.float32)
border_mask = torch.ones_like(u, device=device)
border_mask[1:-1, 1:-1] = 0.0

# 设置热源
source_x, source_y = grid_size // 2, grid_size // 4
u[source_x - 50:source_x + 50, source_y - 50:source_y + 50] = 10.0

# 预热GPU
print("预热CUDA内核...")
start_time = time.time()
for _ in range(10):
    laplacian = (u[2:, 1:-1] + u[:-2, 1:-1] + u[1:-1, 2:] + u[1:-1, :-2] - 4 * u[1:-1, 1:-1])
warmup_time = time.time() - start_time
print(f"预热完成, 耗时: {warmup_time:.4f} 秒")

# 性能监控数据结构
timestamps = []
utilizations = []
temperatures = []
memory_usages = []

# 主模拟循环
print(f"\n开始进行 {steps} 步模拟 (网格: {grid_size}x{grid_size} = {grid_size ** 2 / 1e6:.1f} 百万点)")
start_time = time.time()

for step in range(1, steps + 1):
    # 监控点开始
    if step % 10 == 0:
        timestamps.append(step)
        utilizations.append(gpu_monitor.utilization()[0])
        memory_usages.append(gpu_monitor.memory_usage()[0] / (1024 ** 2))

    # 核心计算：热传导方程
    laplacian = (u[2:, 1:-1] + u[:-2, 1:-1] +
                 u[1:-1, 2:] + u[1:-1, :-2] -
                 4 * u[1:-1, 1:-1])
    u[1:-1, 1:-1] += alpha * laplacian * dt

    # 边界条件
    u[border_mask == 1] = 0.0
    u[source_x - 50:source_x + 50, source_y - 50:source_y + 50] = 10.0

# 性能统计
total_time = time.time() - start_time
print(f"\n模拟完成! 总时间: {total_time:.2f} 秒")
print(f"平均每步时间: {total_time / steps * 1000:.2f} 毫秒")
print(f"计算吞吐量: {steps * grid_size ** 2 / total_time / 1e9:.2f} GFLOP/s")
print(f"峰值显存使用: {max(memory_usages) if memory_usages else 'N/A':.2f} MB")

# 生成性能图表
if utilizations:
    fig, axs = plt.subplots(3, 1, figsize=(10, 12))

    # GPU利用率图表
    axs[0].plot(timestamps, utilizations, 'b-')
    axs[0].set_title('GPU 利用率 (%)')
    axs[0].set_ylim(0, 100)
    axs[0].grid(True)

    # 显存使用图表
    axs[1].plot(timestamps, memory_usages, 'r-')
    axs[1].set_title('显存使用 (MB)')
    axs[1].grid(True)

    # 温度场快照
    final_temp = u.cpu().numpy()
    im = axs[2].imshow(final_temp, cmap='inferno', interpolation='bilinear')
    plt.colorbar(im, ax=axs[2], label='温度')
    axs[2].set_title(f'最终温度分布 (模拟步数: {steps})')

    plt.tight_layout()
    plt.savefig('gpu_performance.png', dpi=150)
    plt.show()
    print("\n性能图表已保存为 'gpu_performance.png'")

# 清理资源
try:
    gpu_monitor.close()
except:
    pass