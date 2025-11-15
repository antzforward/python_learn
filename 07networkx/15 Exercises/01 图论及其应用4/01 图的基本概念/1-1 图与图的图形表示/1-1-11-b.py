import networkx as nx
import matplotlib.pyplot as plt

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# 创建完全图 K5
G = nx.complete_graph(5)


# 定义染色规则
def color_edge(i, j):
    diff = abs(i - j)
    min_diff = min(diff, 5 - diff)
    if min_diff == 1:  # 距离为1或4，染红色
        return 'red'
    else:  # 距离为2或3，染蓝色
        return 'blue'


# 为每条边染色
edge_colors = {}
for i, j in G.edges():
    edge_colors[(i, j)] = color_edge(i, j)


# 验证是否存在同色三角形
def check_monochromatic_triangles():
    triangles = []
    # 获取所有三角形
    for i in range(5):
        for j in range(i + 1, 5):
            for k in range(j + 1, 5):
                triangles.append((i, j, k))

    red_triangles = []
    blue_triangles = []

    for triangle in triangles:
        i, j, k = triangle
        edges = [(i, j), (i, k), (j, k)]
        colors = [edge_colors[edge] for edge in edges]

        if all(color == 'red' for color in colors):
            red_triangles.append(triangle)
        elif all(color == 'blue' for color in colors):
            blue_triangles.append(triangle)

    return red_triangles, blue_triangles


# 检查结果
red_tri, blue_tri = check_monochromatic_triangles()

print("红色三角形（三人互相认识）:", red_tri)
print("蓝色三角形（三人互不认识）:", blue_tri)
print(f"是否存在同色三角形: {len(red_tri) > 0 or len(blue_tri) > 0}")

# 可视化图
pos = nx.circular_layout(G)  # 将顶点排列在圆上

plt.figure(figsize=(8, 8))
nx.draw_networkx_nodes(G, pos, node_color='lightgray', node_size=500)
nx.draw_networkx_labels(G, pos, font_size=16, font_weight='bold')

# 绘制边
red_edges = [edge for edge, color in edge_colors.items() if color == 'red']
blue_edges = [edge for edge, color in edge_colors.items() if color == 'blue']

nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='red', width=2)
nx.draw_networkx_edges(G, pos, edgelist=blue_edges, edge_color='blue', width=2)

plt.title("K5的染色方案（无同色三角形）")
plt.axis('off')
#plt.show()
plt.savefig('1-1-11-b.png', bbox_inches='tight')

# 打印边的颜色
print("\n边的颜色:")
for edge, color in edge_colors.items():
    print(f"边 {edge}: {color}")