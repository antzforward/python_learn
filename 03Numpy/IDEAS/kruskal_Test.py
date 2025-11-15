class UnionFind:
    """并查集数据结构，用于检测环"""

    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:
            return False  # 已在同一集合，会形成环

        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        return True


def kruskal_algorithm(vertices, edges):
    """
    Kruskal算法求最小生成树

    Parameters:
    vertices: 顶点列表
    edges: 边列表 [(u, v, weight)]

    Returns:
    mst_edges: 最小生成树的边列表
    total_weight: 总权重
    """
    # 创建顶点到索引的映射
    vertex_to_index = {v: i for i, v in enumerate(vertices)}

    # 按权重排序边
    edges.sort(key=lambda x: x[2])

    uf = UnionFind(len(vertices))
    mst_edges = []
    total_weight = 0

    for u, v, weight in edges:
        u_idx, v_idx = vertex_to_index[u], vertex_to_index[v]
        if uf.union(u_idx, v_idx):
            mst_edges.append((u, v, weight))
            total_weight += weight

    return mst_edges, total_weight


# 示例使用
vertices = ['A', 'B', 'C', 'D']
edges = [
    ('A', 'B', 2), ('A', 'C', 3),
    ('B', 'C', 1), ('B', 'D', 1),
    ('C', 'D', 4)
]

mst_edges, total_weight = kruskal_algorithm(vertices, edges)
print("最小生成树边:", mst_edges)
print("总权重:", total_weight)