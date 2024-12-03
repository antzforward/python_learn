import heapq

class PriorityQueue:#-priority,将默认最小堆改成最大堆。pyt
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        # 元组的第一个元素是优先级，用于堆排序
        # 第二个元素是索引，确保相同优先级的元素按照添加顺序排序
        # 第三个元素是实际的元素
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        # 弹出并返回优先级最高的元素
        return heapq.heappop(self._queue)[-1]

    def peek(self):
        # 返回优先级最高的元素，但不从队列中移除
        if self.is_empty():
            return None
        return self._queue[0][-1]

    def is_empty(self):
        # 检查队列是否为空
        return len(self._queue) == 0

    def change_priority(self, item, new_priority):
        # 找到第一个匹配的项目并更新其优先级
        found = False
        for i in range(len(self._queue)):
            if self._queue[i][2] == item:
                self._queue[i] = (-new_priority, self._queue[i][1], item)
                found = True
                break
        if found:
            heapq.heapify(self._queue)

# 使用 PriorityQueue
pq = PriorityQueue()
pq.push('task1', priority=3)
pq.push('task2', priority=1)
pq.push('task3', priority=2)

print(pq.pop())  # 输出: task1
print(pq.peek())  # 输出: task3
print(pq.pop())  # 输出: task3
pq.change_priority('task2', new_priority=4)
print(pq.pop())  # 输出: task2

'''
Dijkstra算法是一种广泛使用的最短路径查找算法，适用于带权重的有向图或无向图。这里提供一个简单的实现步骤，并附上相应的Python代码示例。

Dijkstra 算法基本概念：
目标：从图中的一个顶点到其他所有顶点找到最短路径。
输入：图以邻接表表示，每个节点存储其邻居和到邻居的边的权重。
Python 实现步骤：
初始化距离表，记录起点到每个顶点的距离。
使用优先队列（小根堆）来维护未访问顶点集合，以当前最小估计距离排序。
从起点开始，将顶点依次从优先队列中取出，更新其邻居的距离。
重复以上步骤，直到所有的顶点都被处理过。

关键点：
优先队列：我们使用了 heapq 模块，它可以将列表转换成堆结构（默认为最小堆），这样可以始终以最小代价从堆中取出节点。每当发现一条更短的路线到某个节点时，就更新这个节点的距离并重新加入堆中。
性能：如果不使用优先队列，算法的效率明显下降。利用优先队列（最小堆），确保总是处理当前距离最小的节点，从而减少不必要的重复处理。
此代码提供了一个基本框架，对于更复杂的图（如包含周期或特别大的数据集）可能需要进一步优化或修改。
'''
def dijkstra(graph, start):
    # graph 的形式是字典：{node: [(cost, neighbour), ...]}
    # 距离表，存储从 start 到该节点的最短路径长度，初始化为无穷大
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    # 优先队列，保存 (当前最短距离, 对应节点)
    priority_queue = [(0, start)]

    while priority_queue:
        # 弹出当前距离最小的节点
        current_distance, current_node = heapq.heappop(priority_queue)

        # 节点的最短路径已经确定时，跳过处理
        if current_distance > distances[current_node]:
            continue

        # 遍历每个邻接点并更新距离
        for weight, neighbor in graph[current_node]:
            distance = current_distance + weight

            # 只有在找到更短的路径时才进行更新
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances


# 示例图
graph = {
    'A': [(1, 'B'), (4, 'C')],
    'B': [(2, 'C'), (2, 'D')],
    'C': [(3, 'D')],
    'D': []
}

# 执行 Dijkstra 算法
start_node = 'A'
shortest_paths = dijkstra(graph, start_node)
print(shortest_paths)  # 输出从起点 A 到所有节点的最短路径长度


"""
使用优先队列实现任务调度。
更符合调度，最小堆。
"""

def schedule_tasks(tasks):
    pq = [(task['deadline'], task['duration'], task['name']) for task in tasks]
    heapq.heapify(pq)
    current_time = 0
    scheduled_tasks = []

    while tasks or pq:
        while tasks and tasks[0]['deadline'] <= current_time:
            task = tasks.pop(0)
            heapq.heappush(pq, (task['deadline'] + task['duration'], task['duration'], task['name']))
        current_task = heapq.heappop(pq)
        current_time += current_task[1]
        scheduled_tasks.append(current_task[2])

    return scheduled_tasks

# 示例任务
tasks = [
    {'name': 'task1', 'deadline': 4, 'duration': 2},
    {'name': 'task2', 'deadline': 1, 'duration': 3},
    {'name': 'task3', 'deadline': 3, 'duration': 1},
]

print(schedule_tasks(tasks))