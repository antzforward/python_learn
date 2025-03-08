import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import rcParams

# 配置全局参数提升渲染质量
rcParams.update({
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'font.size': 8,
    'image.origin': 'upper'  # 确保坐标系方向正确
})


def create_diagonal_gradient(size=512, angle=45, cmap='viridis'):
    """
    创建对角线渐变图像
    参数：
    size: 图像尺寸（正方形）
    angle: 渐变角度（0-360度）
    cmap: 颜色映射名称或自定义对象
    """
    # 生成网格坐标
    x = np.linspace(-1, 1, size)
    y = np.linspace(-1, 1, size)
    X, Y = np.meshgrid(x, y)

    # 计算角度对应的方向向量
    rad = np.deg2rad(angle)
    u = np.cos(rad)
    v = np.sin(rad)

    # 生成渐变数据（GPU加速计算）
    gradient = (u * X + v * Y).astype(np.float32)
    gradient = (gradient - gradient.min()) / (gradient.max() - gradient.min())

    # 创建自定义颜色映射
    if isinstance(cmap, str):
        try:
            cmap = plt.get_cmap(cmap)
        except Exception as ex:
            print(f"Wrong Color Map Name:{0} Except:{1}",cmap,str(ex))
            colors = [(0.8, 0.2, 0.2), (0.2, 0.4, 0.8)]  # 红蓝渐变
            cmap = LinearSegmentedColormap.from_list('custom', colors)
    return gradient, cmap


# 生成渐变数据
data, cmap = create_diagonal_gradient(size=1024, angle=45, cmap='hsv')

# 创建图像并优化性能
fig, ax = plt.subplots(figsize=(6, 6), tight_layout=True)
img = ax.imshow(
    data,
    cmap=cmap,
    interpolation='bicubic',  # 双三次插值提升平滑度
    aspect='auto'
)

# 添加专业级色标
cbar = fig.colorbar(img, ax=ax, shrink=0.8)
cbar.set_label('Normalized Gradient Value', rotation=270, labelpad=15)

# 添加网格线（半透明）
ax.grid(True, color='white', linestyle='--', linewidth=0.5, alpha=0.3)

# 设置坐标轴
ax.set_xticks(np.linspace(0, 1024, 5))
ax.set_xticklabels(np.linspace(-1, 1, 5, dtype=np.float32))
ax.set_yticks(np.linspace(0, 1024, 5))
ax.set_yticklabels(np.linspace(1, -1, 5, dtype=np.float32))
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')

# 导出为多种格式
plt.savefig('gradient.png', bbox_inches='tight', pad_inches=0.1)
#plt.savefig('gradient.pdf', bbox_inches='tight', pad_inches=0.1)

plt.show()