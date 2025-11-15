import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

def draw_arrow_on_edges(
    G, pos,
    position=0.5,          # 箭头在边上的位置：0~1，0是起点，1是终点，默认0.5是中点
    arrowstyle='->',       # 箭头样式
    color='red',           # 箭头颜色
    mutation_scale=15,     # 箭头头部大小
    lw=2,                  # 线宽
    alpha=0.9,             # 透明度
    ax=None,               # Matplotlib Axes，一般不用传
):
    """
    在有向图的每条边上，指定位置绘制一个箭头。

    参数:
        G (nx.DiGraph): 有向图
        pos (dict): 节点位置字典，如 {'A':(x,y), ...}
        position (float): 箭头在边上的位置，范围 [0,1]，0=起点，1=终点，默认 0.5（中点）
        arrowstyle (str): Matplotlib 箭头样式，如 '->', '-|>', 'fancy' 等
        color (str): 箭头颜色，如 'red', 'blue', '#FF0000'
        mutation_scale (int): 箭头头部大小
        lw (float): 线宽
        alpha (float): 透明度
        ax: Matplotlib Axes 对象，一般无需传递
    """
    if ax is None:
        ax = plt.gca()

    for src, tgt in G.edges():
        x1, y1 = pos[src]
        x2, y2 = pos[tgt]

        # 计算边的向量
        dx = x2 - x1
        dy = y2 - y1

        # 边长
        norm = (dx**2 + dy**2) ** 0.5
        if norm == 0:
            continue  # 跳过重合节点

        # 单位方向向量
        ux = dx / norm
        uy = dy / norm

        # 计算箭头所在的位置：沿着边的 direction 走 position * 边长
        mx = x1 + position * dx
        my = y1 + position * dy

        # 箭头终点：再往前走一小段（比如 0.1倍边长，可调整）
        arrow_offset = 0.1
        ex = mx + arrow_offset * ux
        ey = my + arrow_offset * uy

        # 绘制箭头
        arrow = FancyArrowPatch(
            (mx, my), (ex, ey),
            arrowstyle=arrowstyle,
            color=color,
            mutation_scale=mutation_scale,
            lw=lw,
            alpha=alpha,
        )
        ax.add_patch(arrow)