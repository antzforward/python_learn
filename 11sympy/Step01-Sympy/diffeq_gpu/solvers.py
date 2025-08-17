import torch
import time
from typing import Callable, Tuple, List, Optional, Union
from .monitor import GPUMonitor


class PDESolver:
    """偏微分方程求解器基类"""

    def __init__(self, grid_size: int, device: str = "cuda"):
        """
        初始化求解器

        参数:
            grid_size: 网格大小
            device: 计算设备 ('cuda' 或 'cpu')
        """
        self.grid_size = grid_size
        self.device = torch.device(device if torch.cuda.is_available() and device == "cuda" else "cpu")
        self.u = torch.zeros(grid_size, grid_size, device=self.device, dtype=torch.float32)
        self.border_mask = torch.ones_like(self.u, device=self.device)
        self.border_mask[1:-1, 1:-1] = 0.0

    def set_initial_condition(self, initial_func: Callable = None):
        """
        设置初始条件

        参数:
            initial_func: 初始条件函数，接受坐标(x,y)返回温度值
        """
        if initial_func is None:
            # 默认中心热源
            source_x, source_y = self.grid_size // 2, self.grid_size // 4
            self.u[source_x - 50:source_x + 50, source_y - 50:source_y + 50] = 10.0
        else:
            # 使用自定义初始条件
            x = torch.arange(self.grid_size, device=self.device)
            y = torch.arange(self.grid_size, device=self.device)
            X, Y = torch.meshgrid(x, y, indexing='ij')
            self.u = initial_func(X, Y).to(self.device)

    def set_boundary_conditions(self, boundary_func: Callable = None):
        """
        设置边界条件

        参数:
            boundary_func: 边界条件函数，接受坐标(x,y)返回边界值
        """
        if boundary_func is None:
            # 默认边界为0
            self.border_mask = torch.ones_like(self.u, device=self.device)
            self.border_mask[1:-1, 1:-1] = 0.0
        else:
            # 使用自定义边界条件
            x = torch.arange(self.grid_size, device=self.device)
            y = torch.arange(self.grid_size, device=self.device)
            X, Y = torch.meshgrid(x, y, indexing='ij')
            boundary_values = boundary_func(X, Y).to(self.device)
            self.u[self.border_mask == 1] = boundary_values[self.border_mask == 1]

    def solve(
            self,
            steps: int = 500,
            record_interval: int = 10,
            gpu_monitor: Optional[GPUMonitor] = None,
            progress_callback: Optional[Callable] = None
    ) -> Tuple[torch.Tensor, List[torch.Tensor]]:
        """
        求解微分方程

        参数:
            steps: 时间步数
            record_interval: 记录中间结果的间隔
            gpu_monitor: GPU监控器
            progress_callback: 进度回调函数

        返回:
            final_state: 最终状态
            history: 历史状态列表
        """
        history = [self.u.cpu().clone()]

        start_time = time.time()
        for step in range(1, steps + 1):
            # 核心计算步骤
            self._step()

            # 记录状态
            if step % record_interval == 0 or step == steps:
                history.append(self.u.cpu().clone())

            # GPU监控
            if gpu_monitor and step % record_interval == 0:
                gpu_monitor.record(step)

            # 进度回调
            if progress_callback:
                progress_callback(step, steps)

        total_time = time.time() - start_time
        print(f"求解完成! 总时间: {total_time:.2f}秒, 平均每步: {total_time / steps * 1000:.2f}ms")
        return self.u, history

    def _step(self):
        """单个时间步的计算（由子类实现）"""
        raise NotImplementedError("子类必须实现 _step 方法")


class HeatEquationSolver(PDESolver):
    """热传导方程求解器"""

    def __init__(self, grid_size: int, alpha: float = 0.25, dt: float = 0.01, **kwargs):
        """
        初始化热传导求解器

        参数:
            grid_size: 网格大小
            alpha: 热扩散系数
            dt: 时间步长
        """
        super().__init__(grid_size, **kwargs)
        self.alpha = alpha
        self.dt = dt

    def _step(self):
        """执行单个时间步的计算"""
        # 计算拉普拉斯算子
        laplacian = (self.u[2:, 1:-1] + self.u[:-2, 1:-1] +
                     self.u[1:-1, 2:] + self.u[1:-1, :-2] -
                     4 * self.u[1:-1, 1:-1])

        # 更新温度
        self.u[1:-1, 1:-1] += self.alpha * laplacian * self.dt

        # 应用边界条件
        self.u[self.border_mask == 1] = 0.0


class WaveEquationSolver(PDESolver):
    """波动方程求解器"""

    def __init__(self, grid_size: int, c: float = 0.5, dt: float = 0.01, **kwargs):
        """
        初始化波动方程求解器

        参数:
            grid_size: 网格大小
            c: 波速
            dt: 时间步长
        """
        super().__init__(grid_size, **kwargs)
        self.c = c
        self.dt = dt
        self.v = torch.zeros_like(self.u)  # 速度场

    def _step(self):
        """执行单个时间步的计算"""
        # 计算拉普拉斯算子
        laplacian = (self.u[2:, 1:-1] + self.u[:-2, 1:-1] +
                     self.u[1:-1, 2:] + self.u[1:-1, :-2] -
                     4 * self.u[1:-1, 1:-1])

        # 更新速度
        self.v[1:-1, 1:-1] += self.c ** 2 * laplacian * self.dt

        # 更新位移
        self.u[1:-1, 1:-1] += self.v[1:-1, 1:-1] * self.dt

        # 应用边界条件
        self.u[self.border_mask == 1] = 0.0