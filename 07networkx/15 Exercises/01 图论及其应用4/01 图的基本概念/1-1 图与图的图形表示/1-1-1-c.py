import networkx as nx
import matplotlib.pyplot as plt

from graph_utils.graph_drawer import draw_arrow_on_edges

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

## 创建无向图
G = nx.Graph()

# 所有3位二进制数(顶点),只设置了ID
vertices = [i for i in range(8)]
# 添加顶点
G.add_nodes_from(vertices)

# 定义边的规则:x=x1x2x3,y=y1y2y3,且|x1-y1|+|x2-y2|+|x3-y3|=1->x与y只有1bit翻转
for x in vertices:
    for k in range(3):
        y = x ^ (1 << k)  # 第k位反转
        G.add_edge(x, y)
# 绘制图形
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G, seed=42)  #使用spring 布局

# 绘制节点和边
nx.draw_networkx_nodes(G, pos, node_size=1500, node_color='lightblue')
nx.draw_networkx_edges(G, pos, arrows=False, edge_color='b')
# 绘制箭头
#draw_arrow_on_edges(G, pos, position=0.5, arrowstyle='->', color='red', mutation_scale=15, lw=2, alpha=0.9)
# 标注顶点,默认用id，这里转一下
labels = {i: f"{i:03b}" for i in range(8)}#ID:label 这种map形式
nx.draw_networkx_labels(G, pos, labels=labels , font_size=14, font_color='black')
#设置标题和调整布局
plt.title('无向图：二进制转化规则(D3 Base-2)')
plt.axis('off')
plt.tight_layout(pad=3.0)  # 增加内边距
plt.tight_layout()
# 添加图例解释
plt.figtext(0.5, 0.01,
            "转换规则: 每个节点 'abc' 指向 '!abc'或'a!bc'或'ab!c'",
            ha='center', fontsize=14)
#plt.show()
plt.savefig('1-1-1-c.png', bbox_inches='tight')
