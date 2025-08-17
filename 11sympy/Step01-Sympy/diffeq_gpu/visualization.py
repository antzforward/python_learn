import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from typing import List, Tuple, Union
from matplotlib.colors import LinearSegmentedColormap


def create_performance_plot(
        timestamps: List[float],
        utilizations: List[float],
        memory_usages: List[float]
) -> Tuple[plt.Figure, plt.Axes]:
    """
    创建性能图表

    参数:
        timestamps: 时间戳列表
        utilizations: GPU利用率列表
        memory_usages: 显存使用列表

    返回:
        fig: 图表对象
        axs: 坐标轴对象列表
    """
    fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # GPU利用率图表
    axs[0].plot(timestamps, utilizations, 'b-')
    axs[0].set_title('GPU Utilization (%)')
    axs[0].set_ylabel('Utilization (%)')
    axs[0].grid(True)
    axs[0].set_ylim(0, 100)

    # 显存使用图表
    axs[1].plot(timestamps, memory_usages, 'r-')
    axs[1].set_title('GPU Memory Usage')
    axs[1].set_xlabel('Time (s)')
    axs[1].set_ylabel('Memory (MB)')
    axs[1].grid(True)

    plt.tight_layout()
    return fig, axs


def create_temperature_animation(
        history: List[np.ndarray],
        steps: int,
        interval: int = 200,
        cmap: Union[str, LinearSegmentedColormap] = 'inferno'
) -> FuncAnimation:
    """
    创建温度分布动画

    参数:
        history: 历史状态列表
        steps: 总步数
        interval: 动画帧间隔(毫秒)
        cmap: 颜色映射

    返回:
        animation: 动画对象
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.suptitle("Heat Distribution Evolution")

    # 初始帧
    img = ax.imshow(history[0], cmap=cmap, animated=True)
    plt.colorbar(img, ax=ax, label='Temperature')

    # 更新函数
    def update(frame):
        img.set_array(history[frame])
        ax.set_title(f"Step: {frame * steps // len(history)} / {steps}")
        return img,

    # 创建动画
    animation = FuncAnimation(fig, update, frames=len(history), interval=interval, blit=True)
    return animation


def create_wave_animation(
        history: List[np.ndarray],
        steps: int,
        interval: int = 200,
        cmap: Union[str, LinearSegmentedColormap] = 'coolwarm'
) -> FuncAnimation:
    """
    创建波动动画

    参数:
        history: 历史状态列表
        steps: 总步数
        interval: 动画帧间隔(毫秒)
        cmap: 颜色映射

    返回:
        animation: 动画对象
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.suptitle("Wave Propagation")

    # 初始帧
    img = ax.imshow(history[0], cmap=cmap, animated=True, vmin=-1, vmax=1)
    plt.colorbar(img, ax=ax, label='Displacement')

    # 更新函数
    def update(frame):
        img.set_array(history[frame])
        ax.set_title(f"Step: {frame * steps // len(history)} / {steps}")
        return img,

    # 创建动画
    animation = FuncAnimation(fig, update, frames=len(history), interval=interval, blit=True)
    return animation


def create_final_state_plot(
        final_state: np.ndarray,
        title: str = 'Final State',
        cmap: Union[str, LinearSegmentedColormap] = 'viridis'
) -> plt.Figure:
    """
    创建最终状态的热图

    参数:
        final_state: 最终状态数组
        title: 图表标题
        cmap: 颜色映射

    返回:
        fig: 图表对象
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    img = ax.imshow(final_state, cmap=cmap)
    plt.colorbar(img, label='Value')
    ax.set_title(title)
    return fig


def create_3d_surface_plot(
        state: np.ndarray,
        title: str = '3D Surface',
        cmap: Union[str, LinearSegmentedColormap] = 'viridis'
) -> plt.Figure:
    """
    创建3D表面图

    参数:
        state: 状态数组
        title: 图表标题
        cmap: 颜色映射

    返回:
        fig: 图表对象
    """
    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    x = np.arange(state.shape[0])
    y = np.arange(state.shape[1])
    X, Y = np.meshgrid(x, y)

    surf = ax.plot_surface(X, Y, state, cmap=cmap, linewidth=0, antialiased=True)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    ax.set_title(title)

    return fig