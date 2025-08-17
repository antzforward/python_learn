import torch
import time
from typing import Tuple, List, Optional


class GPUMonitor:
    """GPU性能监控工具"""

    def __init__(self):
        self.use_nvml = False
        self.gpu_count = torch.cuda.device_count()
        self.utilizations: List[float] = []
        self.memory_usages: List[float] = []  # 单位MB
        self.timestamps: List[float] = []  # 记录时间戳（从开始监控的时间）
        self.start_time = time.time()

        try:
            if hasattr(torch.cuda, 'utilization'):
                self.utilization = self._get_utilization_torch
                print("使用 PyTorch 内置 GPU 监控")
            else:
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

    def _get_utilization_torch(self) -> List[int]:
        """使用PyTorch内置API获取GPU利用率"""
        return [torch.cuda.utilization(i) for i in range(self.gpu_count)]

    def _get_utilization_nvml(self) -> List[int]:
        """使用NVML库获取GPU利用率"""
        utils = []
        for handle in self.handles:
            util = self.pynvml.nvmlDeviceGetUtilizationRates(handle)
            utils.append(util.gpu)
        return utils

    def memory_usage(self) -> List[float]:
        """获取当前显存使用量（单位：MB）"""
        return [torch.cuda.memory_allocated(i) / (1024 ** 2) for i in range(self.gpu_count)]

    def record(self, step: int = None):
        """记录当前GPU状态"""
        # 记录时间（从开始监控以来的秒数）
        elapsed = time.time() - self.start_time
        self.timestamps.append(elapsed)
        # 记录GPU利用率和显存
        utils = self.utilization()
        self.utilizations.append(utils[0] if self.gpu_count > 0 else 0)
        mem_usage = self.memory_usage()
        self.memory_usages.append(mem_usage[0] if self.gpu_count > 0 else 0)

    def get_performance_data(self) -> Tuple[List[float], List[float], List[float]]:
        """获取监控数据：时间戳、GPU利用率、显存使用(MB)"""
        return self.timestamps, self.utilizations, self.memory_usages

    def close(self):
        """关闭监控器并释放资源"""
        if self.use_nvml:
            self.pynvml.nvmlShutdown()

    def __enter__(self):
        """上下文管理器入口"""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """上下文管理器出口"""
        self.close()