import networkx as nx
import matplotlib.pyplot as plt

from graph_utils.graph_drawer import draw_arrow_on_edges
# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False    # 正常显示负号

## 创建有向图
G = nx.DiGraph()

# 所有3位二进制数(顶点)
vertices = [f"{i:03b}" for i in range(8)]

# 添加顶点
G.add_nodes_from( vertices )

# 定义边的规则:x=x1x2x3->y=x2x30或x2x31
for x in vertices:
    x1,x2,x3 = x[0],x[1],x[2]
    y1 = x2+x3+'0'
    y2 = x2+x3+'1'
    G.add_edge(x, y1)
    G.add_edge(x, y2)

# 绘制图形
plt.figure(figsize=(10,8))
pos = nx.spring_layout(G,seed=42) #使用spring 布局

# 绘制节点和边
nx.draw_networkx_nodes(G, pos,node_size=1500,node_color='lightblue')
nx.draw_networkx_edges(G, pos, arrows=False,edge_color='b' )
# 绘制箭头
draw_arrow_on_edges(G, pos, position=0.5, arrowstyle='->', color='red', mutation_scale=15, lw=2, alpha=0.9)
# 标注顶点
nx.draw_networkx_labels(G, pos, font_size=14, font_color='black')
#设置标题和调整布局
plt.title('有向图：二进制转化规则(D3 Base-2)')
plt.axis('off')
plt.tight_layout(pad=3.0)  # 增加内边距
plt.tight_layout()
# 添加图例解释
plt.figtext(0.5, 0.01,
            "转换规则: 每个节点 'abc' 指向 'bcd' (d={0,1})",
            ha='center', fontsize=14)
#plt.show()
plt.savefig('1-1-1-a.png', bbox_inches='tight')