import torch
import time


def warmup_gpu(iterations: int = 10, grid_size: int = 100):
    """
    预热GPU以提高后续计算性能

    参数:
        iterations: 预热迭代次数
        grid_size: 测试网格大小
    """
    if not torch.cuda.is_available():
        return

    print("预热GPU...")
    device = torch.device("cuda")
    u = torch.zeros(grid_size, grid_size, device=device)

    start_time = time.time()
    for _ in range(iterations):
        laplacian = (u[2:, 1:-1] + u[:-2, 1:-1] + u[1:-1, 2:] + u[1:-1, :-2] - 4 * u[1:-1, 1:-1])

    warmup_time = time.time() - start_time
    print(f"GPU预热完成, 耗时: {warmup_time:.4f}秒")
    torch.cuda.empty_cache()


def print_system_info():
    """打印系统信息和GPU状态"""
    import platform
    import psutil

    print("=" * 50)
    print("系统信息:")
    print(f"操作系统: {platform.system()} {platform.release()}")
    print(f"处理器: {platform.processor()}")
    print(f"物理核心数: {psutil.cpu_count(logical=False)}")
    print(f"逻辑核心数: {psutil.cpu_count(logical=True)}")
    print(f"总内存: {psutil.virtual_memory().total / (1024 ** 3):.2f} GB")

    if torch.cuda.is_available():
        print("\nGPU信息:")
        print(f"设备数量: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")
            print(f"    计算能力: {torch.cuda.get_device_capability(i)}")
            print(f"    显存: {torch.cuda.get_device_properties(i).total_memory / (1024 ** 3):.2f} GB")
    else:
        print("\n未检测到可用的CUDA设备")

    print("=" * 50)