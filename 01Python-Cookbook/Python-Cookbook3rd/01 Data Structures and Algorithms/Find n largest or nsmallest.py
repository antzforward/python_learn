"""
在headpq里面去最大，或最小的n个元素
最小堆结构，这个常规的用法有
实现优先队列、合并有序序列，最大最小的N个元素，霍夫曼编码
"""

import heapq
nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
print(heapq.nlargest(3, nums)) # Prints [42, 37, 23]
print(heapq.nsmallest(3, nums)) # Prints [-4, 1, 2]

# 直接把nums 装进headqp 再说
hpq = []
for num in nums:
    heapq.heappush( hpq, num )
print( hpq ) #[-4, 2, 1, 23, 7, 2, 18, 23, 42, 37, 8] 最小堆的形式。
#或者这样,直接讲nums 转换成headpq
heapq.heapify( nums )
print( nums )
print( heapq.nlargest(3, hpq ))

# 添加了compare的heap的形式，
portfolio = [
 {'name': 'IBM', 'shares': 100, 'price': 91.1},
 {'name': 'AAPL', 'shares': 50, 'price': 543.22},
 {'name': 'FB', 'shares': 200, 'price': 21.09},
 {'name': 'HPQ', 'shares': 35, 'price': 31.75},
 {'name': 'YHOO', 'shares': 45, 'price': 16.35},
 {'name': 'ACME', 'shares': 75, 'price': 115.65}
]
cheap = heapq.nsmallest(3, portfolio, key=lambda s: s['price'])
expensive = heapq.nlargest(3, portfolio, key=lambda s: s['price'])
print( cheap )
print( expensive )


## 优先队列
import  heapq
class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0 # 增加计数器，让每次增加的相同Item和priority 组成的Element不同。
    def push(self, item, priority):
        heapq.heappush(self._queue,(-priority, self._index, item))#元组比较顺序从左到右进行。默认用的是元组比较逻辑
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]

# 使用优先队列
pq = PriorityQueue()
pq.push('task1', priority=3)
pq.push('task2', priority=1)
pq.push('task3', priority=2)

print(pq.pop())  # 输出: task1
print(pq.pop())  # 输出: task3
print(pq.pop())  # 输出: task2

## 合并多个有序序列，而无需一次性加载所有数据。
sorted_arrays = [
    [1, 3, 5],
    [2, 4, 6],
    [0, 9]
]
merged_array = list(heapq.merge(*sorted_arrays))
print(merged_array)  # 输出: [0, 1, 2, 3, 4, 5, 6, 9]

## 最大，最小堆，在上面。 pass

## 霍夫曼编码
#霍夫曼编码是一种被广泛使用于数据压缩的算法，它使用不同长度的编码代表不同频率的字符。
# 使用 heapq 可以有效地建立霍夫曼编码所需的优先队列。

from collections import defaultdict, Counter
import heapq


def huffman_encode(s):
    if not s:#字符串是否为空。
        return []
    # 计算每个字符的频率并创建一个堆
    frequency = Counter(s)
    heap = [[wt, [sym, ""]] for sym, wt in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)

        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]

        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))


# 示例
ss =[
    "this is an example for huffman encoding",
    "aaabbb",
    'ac ab ab',
    "the quick brown fox jumps over the lazy dog",
    "Moonshot AI, 2024!",
    ""
]
for s in ss:
    huffman_code = huffman_encode(s)
    print(s)
    print('*'*50)
    for char, code in huffman_code:
        print(f"{char}: {code}")
    print('*' * 50)
