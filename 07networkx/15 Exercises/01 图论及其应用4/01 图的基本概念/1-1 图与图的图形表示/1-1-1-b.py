import networkx as nx
import matplotlib.pyplot as plt
import itertools
from graph_utils.graph_drawer import draw_arrow_on_edges

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False    # 正常显示负号

## 创建有向图
G = nx.DiGraph()

# 所有3位三进制数(顶点)
base = [f'{i}'for i in range(3)]
vertices = [''.join(t) for t in itertools.product(base, repeat=3)]

# 添加顶点
G.add_nodes_from(vertices)

# 定义边的规则:x=x1x2x3->y=x2x3a或x2x3a,且a!=x3
for x in vertices:
    x1, x2, x3 = x[0], x[1], x[2]
    successors = [x2 + x3 + d for d in base if d != x3]
    for y in successors:
        G.add_edge( x,y)

# 绘制图形
plt.figure(figsize=(10, 10))
pos = nx.circular_layout(G)  #换其他的布局

# 绘制节点和边
nx.draw_networkx_nodes(G, pos, node_size=1500, node_color='lightblue',alpha=0.7)
# 绘制带箭头的边
nx.draw_networkx_edges(G, pos, arrows=False, edge_color='gray', width=1.5, alpha=0.6)
# 绘制箭头
draw_arrow_on_edges(G, pos, position=0.5, arrowstyle='->', color='red', mutation_scale=15, lw=2, alpha=0.9)
# 标注顶点
nx.draw_networkx_labels(G, pos, font_size=14, font_color='black')
#设置标题和调整布局
plt.title('有向图 - 3位三进制数字转换规则 (D3 Base-3)', fontsize=14)
plt.axis('off')
# 添加图例解释
plt.figtext(0.5, 0.01,
            "转换规则: 每个节点 'abc' 指向 'bcd' (d ≠ c)",
            ha='center', fontsize=14)
plt.tight_layout(pad=3.0)
#plt.show()
plt.savefig('1-1-1-b.png', bbox_inches='tight')
