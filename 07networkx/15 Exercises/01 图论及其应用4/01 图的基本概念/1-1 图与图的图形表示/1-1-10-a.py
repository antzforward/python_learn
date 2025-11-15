import networkx as nx
import matplotlib.pyplot as plt

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

plt.figure(figsize=(15, 4))

# 类型1：三角形+孤立点
G1 = nx.Graph()
G1.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'A')])
G1.add_node('D')  # 孤立点
plt.subplot(131)
pos1 = nx.circular_layout(G1)
nx.draw(G1, pos1, with_labels=True, node_size=800, node_color='lightblue', font_size=12)
plt.title(r'三角形（$K_3+K_1$）')

# 类型2：星形图
G2 = nx.Graph()
G2.add_edges_from([('A', 'B'), ('A', 'C'), ('A', 'D')])
plt.subplot(132)
nx.draw(G2, with_labels=True, node_size=800, node_color='salmon', font_size=12)
plt.title("星形图 （$K_{1,3}$)")

# 类型3：路径图
G3 = nx.Graph()
G3.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'D')])
plt.subplot(133)
nx.draw(G3, with_labels=True, node_size=800, node_color='lightgreen', font_size=12)
plt.title("路径图 ($P_4$)")

plt.tight_layout()
plt.savefig('1-1-10-a.png', dpi=300)
#plt.show()