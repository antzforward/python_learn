import networkx as nx
import matplotlib.pyplot as plt
# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# 1. 创建具有4个顶点的无向图（环状）
G1 = nx.Graph()
G1.add_nodes_from([1, 2, 3, 4])
G1.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1)])

print("图1 - 无向环状图:")
print("顶点:", list(G1.nodes()))
print("边:", list(G1.edges()))
print("是否有重边:", G1.has_edge(1, 2) and G1.has_edge(2, 1))  # 无向图不会重复计算
print()

# 可视化图1
plt.figure(figsize=(8, 6))
plt.subplot(2, 2, 1)
pos1 = nx.circular_layout(G1)
nx.draw(G1, pos1, with_labels=True, node_color='lightblue',
        node_size=500, font_size=16, font_weight='bold')
plt.title("无向环状图")

# 2. 创建具有3个顶点的有向图（环状）
G2 = nx.DiGraph()
G2.add_nodes_from(['A', 'B', 'C'])
G2.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'A')])

print("图2 - 有向环状图:")
print("顶点:", list(G2.nodes()))
print("边:", list(G2.edges()))
print()

# 可视化图2
plt.subplot(2, 2, 2)
pos2 = nx.circular_layout(G2)
nx.draw(G2, pos2, with_labels=True, node_color='lightgreen',
        node_size=500, font_size=16, font_weight='bold',
        arrows=True, arrowsize=20)
plt.title("有向环状图")

# 3. 在图2基础上添加一条从'A'指向'C'的边
G3 = G2.copy()  # 复制图2
G3.add_edge('A', 'C')  # 添加边 A->C

print("图3 - 添加边A->C后的有向图:")
print("顶点:", list(G3.nodes()))
print("边:", list(G3.edges()))

# 检查是否有重边
# 有向图中，重边是指相同的顶点对和方向
has_duplicate = G3.has_edge('A', 'C') and ('A', 'C') in [('A', 'C')]  # 实际上我们刚刚添加了一条
# 更准确地说，检查是否有多条从A到C的边
# NetworkX的DiGraph不允许重边，所以添加已存在的边不会有影响
print("是否有重边:", len([e for e in G3.edges() if e == ('A', 'C')]) > 1)

# 检查是否有对称边
# 对称边是指一对方向相反的边，如(A,C)和(C,A)
has_symmetric = G3.has_edge('A', 'C') and G3.has_edge('C', 'A')
print("是否有对称边:", has_symmetric)
print()

# 可视化图3
plt.subplot(2, 2, 3)
pos3 = nx.circular_layout(G3)
nx.draw(G3, pos3, with_labels=True, node_color='lightcoral',
        node_size=500, font_size=16, font_weight='bold',
        arrows=True, arrowsize=20)
plt.title("添加边A->C后的有向图")

plt.tight_layout()
#plt.show()
plt.savefig('1-1-12.png', bbox_inches='tight')

# 更详细地分析图3
print("图3的详细分析:")
print("所有边:", list(G3.edges()))
print("从A出发的边:", list(G3.out_edges('A')))
print("指向A的边:", list(G3.in_edges('A')))
print("从C出发的边:", list(G3.out_edges('C')))
print("指向C的边:", list(G3.in_edges('C')))