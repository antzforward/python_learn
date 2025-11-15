import heapq


def prim_algorithm(graph, start_vertex):
    """
    Prim算法求加权连通图的最小生成树

    Parameters:
    graph: 邻接表表示的图，{vertex: [(neighbor, weight), ...]}
    start_vertex: 起始顶点

    Returns:
    mst_edges: 最小生成树的边列表 [(u, v, weight)]
    total_weight: 总权重
    """
    mst_edges = []
    visited = set([start_vertex])
    edges = [
        (weight, start_vertex, neighbor)
        for neighbor, weight in graph[start_vertex]
    ]
    heapq.heapify(edges)
    total_weight = 0

    while edges:
        weight, u, v = heapq.heappop(edges)
        if v not in visited:
            visited.add(v)
            mst_edges.append((u, v, weight))
            total_weight += weight

            for neighbor, w in graph[v]:
                if neighbor not in visited:
                    heapq.heappush(edges, (w, v, neighbor))

    return mst_edges, total_weight


# 示例使用
graph = {
    'A': [('B', 2), ('C', 3)],
    'B': [('A', 2), ('C', 1), ('D', 1)],
    'C': [('A', 3), ('B', 1), ('D', 4)],
    'D': [('B', 1), ('C', 4)]
}

mst_edges, total_weight = prim_algorithm(graph, 'A')
print("最小生成树边:", mst_edges)
print("总权重:", total_weight)