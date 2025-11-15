import networkx as nx
import matplotlib.pyplot as plt

from graph_utils.graph_drawer import draw_arrow_on_edges

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

## 创建有向图
G = nx.Graph()

# 所有3位二进制数(顶点),只设置了ID
vertices = [i for i in range(8)]
# 添加顶点
G.add_nodes_from(vertices)

# 定义边的规则:i,j,且|j-i| = s (mod 8),s ={1,4}
s = {1, 4}
for x in vertices:
    for y in vertices:
        if abs((y-x)) % 8 in s:
            G.add_edge(x, y)
# 绘制图形
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G, seed=42)  #使用spring 布局

# 绘制节点和边
nx.draw_networkx_nodes(G, pos, node_size=1500, node_color='lightblue',alpha=0.7)
nx.draw_networkx_edges(G, pos, arrows=False, edge_color='b')
# 绘制箭头
#draw_arrow_on_edges(G, pos, position=0.5, arrowstyle='->', color='red', mutation_scale=15, lw=2, alpha=0.9)
# 标注顶点
nx.draw_networkx_labels(G, pos , font_size=14, font_color='black')

# 设置标题和调整布局
plt.title('无向图：绝对值取模(D3 mod 8)')
plt.axis('off')
plt.tight_layout(pad=3.0)  # 增加内边距
plt.tight_layout()
# 添加图例解释
plt.figtext(0.5, 0.01,
            "转换规则: 每个节点 i 指向 j,且 |j-i|=s (mod 8) s={1,4}",
            ha='center', fontsize=14)
#plt.show()
plt.savefig('1-1-1-e.png', bbox_inches='tight')
