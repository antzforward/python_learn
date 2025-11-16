import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from itertools import combinations

from bidict import bidict


#绘制图1.2的Peterson的图
# 信息来自AI
def demonstrate_equivalence():
    """展示Petersen图的不同等价定义"""
    definitions = {
        "标准定义": "外五边形 + 内五角星",
        "Kneser图 KG₅,₂": "5元集的2元子集，不相交则相连",
        "Johnson图 J(5,2,0)": "5元集的2元子集，交集为空则相连",
        "奇图 O₃": "3元集的子集构图",
        "(3,5)-笼图": "度数为3，围长为5的最小图",
        "Kempe图": "历史名称，源于四色定理研究",
        "Peirce图": "历史名称，源于逻辑学研究"
    }

    for name, description in definitions.items():
        print(f"• {name}: {description}")


demonstrate_equivalence()

print("生成图1.2的Peterson图，Perterson图，Kempe图，Peice图，水平分布")

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

G = nx.petersen_graph()
print("图1 - 无向环状图:")
print("顶点:", list(G.nodes()))
print("边:", list(G.edges()))
print("是否有重边:", G.has_edge(1, 2) and G.has_edge(2, 1))  # 无向图不会重复计算
print()

# labels 互相查找的方式，方便我找位置，比如画弧线
info = bidict()
info[0] = 'y1'
info[1] = 'y3'
info[2] = 'y5'
info[3] = 'y2'
info[4] = 'y4'
info[5] = 'x1'
info[6] = 'x3'
info[7] = 'x5'
info[8] = 'x2'
info[9] = 'x4'


def draw_Peice(ax):
    '''
    绘制Peice图，就是最经典的外正五边形 内五角星的形式
    '''
    pos = {}
    indexs = range(5)
    r = 3
    plus_angle = 2 * np.pi / 5
    start_angle = np.pi / 2 + 2 * plus_angle
    for i in indexs:
        current_angle = start_angle + i * plus_angle
        pos[i] = (r * np.cos(current_angle), r * np.sin(current_angle))
    indexs = range(5, 10)
    r = 1.5
    for i in indexs:
        current_angle = start_angle + i * plus_angle
        pos[i] = (r * np.cos(current_angle), r * np.sin(current_angle))
    nx.draw(G, pos=pos, ax=ax)
    nx.draw_networkx_labels(G, pos=pos, ax=ax, labels=info)
    # 使用 pad 参数增加标题和子图之间的距离
    ax.set_title('Peice图', pad=20)
    ax.set_aspect('equal')  # 这将使得 x 轴和 y 轴具有相同的比例


def draw_Kempe(ax):
    '''
    绘制Kempe图
    :param ax:
    :return: void
    '''
    pos = {}
    pos[5] = (0, 0)
    indexs = range(6, 10)
    r = 3
    start_angle = np.pi / 2
    plus_angle = - 2 * np.pi / 9
    for i in indexs:
        label = f'x{i - 4}'
        current_angle = start_angle + (i - 6) * plus_angle
        pos[info.inv[label]] = (r * np.cos(current_angle), r * np.sin(current_angle))

    start_angle = np.pi / 2
    plus_angle = 2 * np.pi / 9
    start_angle += plus_angle
    for i, label in enumerate(['y2', 'y4', 'y1', 'y3', 'y5']):
        current_angle = start_angle + i * plus_angle
        pos[info.inv[label]] = (r * np.cos(current_angle), r * np.sin(current_angle))
    print(pos)
    nx.draw_networkx_nodes(G, pos=pos, ax=ax, nodelist=G.nodes())

    exclusive_edgeInfos = [(info.inv['y2'], info.inv['y5']), (info.inv['x3'], info.inv['y3'])]
    exclude_set = {tuple(sorted(edge)) for edge in exclusive_edgeInfos}
    exclude_edges = [edge for edge in G.edges if (tuple(sorted(edge)) in exclude_set)]
    kept_edges = [edge for edge in G.edges() if tuple(sorted(edge)) not in exclude_set]
    # 先绘制直线的部分
    nx.draw_networkx_edges(G, pos=pos, edgelist=kept_edges, ax=ax)
    nx.draw_networkx_edges(G, pos=pos, edgelist=exclude_edges[:1], ax=ax, arrows=True, connectionstyle='arc3,rad=0.3')
    nx.draw_networkx_edges(G, pos=pos, edgelist=exclude_edges[1:], ax=ax, arrows=True, connectionstyle='arc3,rad=-0.3')
    #绘制标签
    nx.draw_networkx_labels(G, pos=pos, ax=ax, labels=info)
    # 使用 pad 参数增加标题和子图之间的距离
    ax.set_title('Kempe图', pad=20)
    ax.set_aspect('equal')  # 这将使得 x 轴和 y 轴具有相同的比例


def draw_Petersen(ax):
    pos = {}
    plus_angle = 2 * np.pi / 5
    start_angle = 2 * plus_angle
    r = 1
    for i in range(5):
        label = f'x{i + 1}'
        current_angle = start_angle - i * plus_angle
        current_pos = (r * np.cos(current_angle) - 1.5, r * np.sin(current_angle))
        pos[info.inv[label]] = current_pos

    # y 标记的点只能逐步加了
    start_angle = np.pi
    for i, label in enumerate(['y1', 'y3', 'y5', 'y2', 'y4']):
        current_angle = start_angle + i * plus_angle
        current_pos = (r * np.cos(current_angle) + 1.5, r * np.sin(current_angle))
        pos[info.inv[label]] = current_pos
    nx.draw(G, pos=pos, ax=ax)
    nx.draw_networkx_labels(G, pos=pos, ax=ax, labels=info)
    # 使用 pad 参数增加标题和子图之间的距离
    ax.set_title('Petersen图', pad=10)
    ax.set_aspect('equal')  # 这将使得 x 轴和 y 轴具有相同的比例


#图1.2的绘图形式
if False:
    # 创建一个足够大的画布来容纳所有子图
    fig, axes = plt.subplots(1, 3, figsize=(3 * 6, 1 * 5))
    # 确保 axes 是二维数组
    axes = axes.flatten()
    draw_Petersen(ax=axes[0])
    draw_Kempe(ax=axes[1])
    draw_Peice(ax=axes[2])
    plt.tight_layout()
    plt.savefig('1-2-3-1.png', bbox_inches='tight')
    plt.show()


# 不绘制1.3图的Petersen图了，因为跟第一次画的两个相同，只是label不同，连position都一样
# 这里绘制1.2.3题的图
def draw_triangle_Petersen(ax):
    '''
    表现为正三角形占位的形式，有三条线是弧形的，但是曲率大致相同
    关键这个没有label标记node，难度变化了，给Petersen图顶点打标记都挺难的
    我用类似数独的方式把id号标记出来了。
    :param ax:
    :return:
    '''
    pos = {}
    pos[0] = (0, 0)
    # 外部三角形
    r = 3
    start_angle = np.pi / 2
    plus_angle = 2 * np.pi / 3
    nodeid_list = [2, 9, 8]
    for index, id in enumerate(nodeid_list):
        current_angle = start_angle + index * plus_angle
        pos[id] = (r * np.cos(current_angle), r * np.sin(current_angle))
    # 内部三角形
    r = 1.5
    start_angle = np.pi / 2
    plus_angle = 2 * np.pi / 3
    nodeid_list = [1, 4, 5]
    for index, id in enumerate(nodeid_list):
        current_angle = start_angle + index * plus_angle
        pos[id] = (r * np.cos(current_angle), r * np.sin(current_angle))
    # 外部三角形边的中点
    r = 3 * np.sin(np.pi / 6)
    start_angle = np.pi / 6
    plus_angle = 2 * np.pi / 3
    nodeid_list = [3, 7, 6]
    for index, id in enumerate(nodeid_list):
        current_angle = start_angle + index * plus_angle
        pos[id] = (r * np.cos(current_angle), r * np.sin(current_angle))
    #排除的边，要用圆弧线
    exclude_set = [(4, 3), (1, 6), (7, 5)]
    exclude_set = [tuple(sorted(edge)) for edge in exclude_set]
    print(exclude_set)
    kept_edges = [edge for edge in G.edges() if tuple(sorted(edge)) not in exclude_set]

    # 绘制顶点
    nx.draw_networkx_nodes(G, pos=pos, ax=ax, nodelist=G.nodes())
    # 绘制直线边
    nx.draw_networkx_edges(G, pos=pos, edgelist=kept_edges, ax=ax)
    # 绘制曲线边
    nx.draw_networkx_edges(G, pos=pos, edgelist=exclude_set[1:], ax=ax, arrows=True, connectionstyle='arc3,rad=0.5')
    nx.draw_networkx_edges(G, pos=pos, edgelist=exclude_set[:1], ax=ax, arrows=True, connectionstyle='arc3,rad=-0.5')
    # 绘制标签
    nx.draw_networkx_labels(G, pos=pos, ax=ax, labels=info)
    # 使用 pad 参数增加标题和子图之间的距离
    ax.set_title('正三角形Ketersen图', pad=20)
    ax.set_aspect('equal')  # 这将使得 x 轴和 y 轴具有相同的比例


def draw_circle_Petersen(ax):
    '''

    :param ax:
    :return:
    '''
    pos = {}
    indexs = range(5)
    r = 3
    plus_angle = 2 * np.pi / 5
    start_angle = -np.pi / 2
    for i in indexs:
        current_angle = start_angle + i * plus_angle
        pos[i] = (r * np.cos(current_angle), r * np.sin(current_angle))
    indexs = range(5, 10)
    r = 3
    start_angle = np.pi / 2
    for i in indexs:
        current_angle = start_angle + i * plus_angle
        pos[i] = (r * np.cos(current_angle), r * np.sin(current_angle))
    nx.draw(G, pos=pos, ax=ax)
    nx.draw_networkx_labels(G, pos=pos, ax=ax, labels=info)
    ax.set_title('圆周 Petersen图', pad=10)
    ax.set_aspect('equal')  # 这将使得 x 轴和 y 轴具有相同的比例


def draw_tower_Petersen(ax):
    '''
    绘制一个像塔一样的Petersen图
    我只能看出来是左右对称结构，全直线，可能有稳定性
    但是我不太清楚这个图咋来的，只能照着描绘一下。
    还是同构图
    这里换个思路来处理，先确定位置，然后设置连线，然后根据Info信息打标，反过来处理可能简单一点
    :param ax:
    :return:
    '''
    pos = {}
    pos[0] = (0, 0)
    # 第二列
    y = 2 * np.sin(np.pi / 6)
    pos[1] = (-2 * np.cos(np.pi / 6), -y)
    pos[2] = (0, -y)
    pos[3] = (2 * np.cos(np.pi / 6), -y)
    # 第三列
    y1 = y + 2.5 * np.cos(np.pi / 6)
    pos[4] = (-2.5 * np.cos(np.pi / 6), -y1)
    pos[5] = (2.5 * np.cos(np.pi / 6), -y1)
    # 第四列
    y2 = y + 1.5
    pos[6] = (-2 * np.sin(np.pi / 12), -y2)
    pos[7] = (2 * np.sin(np.pi / 12), -y2)
    # 第五列
    y3 = y + 2.5 * np.cos(np.pi / 12)
    pos[8] = (-2 * np.sin(np.pi / 12), -y3)
    pos[9] = (2 * np.sin(np.pi / 12), -y3)
    for i, p in pos.items():
        x, y = p
        pos[i] = (x, y + 2.5)  #上移
    g = nx.Graph()
    g.add_nodes_from([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    g.add_edges_from(
        [(0, 1), (0, 2), (0, 3), (1, 8), (1, 7), (2, 4), (2, 5), (3, 6), (3, 9), (4, 6), (4, 8), (5, 7), (5, 9), (6, 7),
         (8, 9)])
    nx.draw(g, pos=pos, ax=ax)
    nx.draw_networkx_labels(g, pos=pos, ax=ax, labels=info)
    # 使用 pad 参数增加标题和子图之间的距离
    ax.set_title('塔式Petersen图', pad=20)
    ax.set_aspect('equal')  # 这将使得 x 轴和 y 轴具有相同的比例

def draw_fan_Petersen(ax):
    pos = {}
    pos[0] = (0, 0)
    # 第二列
    r = 1.75
    pos[1] = (-r * np.sin(np.pi / 6), -r * np.cos(np.pi / 6))
    pos[2] = (0, -r)
    pos[3] = (r * np.sin(np.pi / 6), -r * np.cos(np.pi / 6))

    r2 = 1.25
    # 第三列 第一组
    pos[4] = ( pos[1][0] - r2* np.sin(np.pi / 6), pos[1][1] -  r2 * np.cos(np.pi / 6))
    pos[5] = ( pos[1][0], pos[1][1] - r2)
    # 第三列 第二组
    pos[6] = ( pos[2][0] - r2* np.sin(np.pi / 12), pos[2][1] -  r2 * np.cos(np.pi / 12) )
    pos[7] = ( pos[2][0] + r2* np.sin(np.pi / 12), pos[2][1] -  r2 * np.cos(np.pi / 12))
    # 第三列 第三组
    pos[8] = ( pos[3][0], pos[3][1] - r2)
    pos[9] = ( pos[3][0] + r2* np.sin(np.pi / 6), pos[3][1] -  r2 * np.cos(np.pi / 6))
    for i, p in pos.items():
        x, y = p
        pos[i] = (x, y + 1)  # 上移
    g = nx.Graph()
    g.add_nodes_from([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    g.add_edges_from(
        [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 6), (2, 7), (3, 8), (3, 9), (4, 6), (4, 9), (5, 7), (5, 8), (6, 8),
         (7, 9)])
    excluded_edges = [(4, 6), (4, 9), (5, 7), (5, 8), (6, 8),
         (7, 9)]
    mid_rad_edges = [(5,8)]
    big_rad_edges = [(4,9)]
    # 绘制顶点
    nx.draw_networkx_nodes(G, pos=pos, ax=ax, nodelist=g.nodes())
    # 绘制直线边
    nx.draw_networkx_edges(G, pos=pos, edgelist=[edge for edge in g.edges if edge not in excluded_edges ], ax=ax)
    # 绘制曲线边
    nx.draw_networkx_edges(G, pos=pos, edgelist=[edge for edge in excluded_edges if edge not in big_rad_edges and edge not in mid_rad_edges], ax=ax, arrows=True, connectionstyle='arc3,rad=0.55')
    nx.draw_networkx_edges(G, pos=pos, edgelist=[edge for edge in mid_rad_edges], ax=ax, arrows=True,
                           connectionstyle='arc3,rad=0.75')
    nx.draw_networkx_edges(G, pos=pos, edgelist=[edge for edge in big_rad_edges ], ax=ax, arrows=True, connectionstyle='arc3,rad=0.85')
    nx.draw_networkx_labels(g, pos=pos, ax=ax, labels=info)
    # 使用 pad 参数增加标题和子图之间的距离
    ax.set_title('扇子Petersen图', pad=20)
    ax.set_aspect('equal')  # 这将使得 x 轴和 y 轴具有相同的比例

if True:
    # 创建一个足够大的画布来容纳所有子图
    fig, axes = plt.subplots(1, 4, figsize=(4 * 6, 1 * 5))
    # 确保 axes 是二维数组
    axes = axes.flatten()
    draw_tower_Petersen(ax=axes[0])
    draw_triangle_Petersen(ax=axes[1])
    draw_circle_Petersen(ax=axes[2])
    draw_fan_Petersen(ax=axes[3])
    plt.savefig('1-2-3-2.png', bbox_inches='tight')
    plt.show()
