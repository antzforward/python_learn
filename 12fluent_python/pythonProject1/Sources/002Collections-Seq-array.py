'''
替代List的理由
1、效率高
2、内存占用少，这里用memoryview，我也用过sys.getsizeof的形式
基本上跟程序设计的性能测试的两个方面是相同的。
'''

'''
使用NumPy和SciPy是必须的
用array就用他们吧，可以方便改维度的。
'''
'''
数据结构中的各种队列
deque 双向队列
queue 队列
multiprocessing下的Queue，任务管理下的队列
asyncio下的Queue、LifoQueue、PriorityQueue和JoinableQueue
heapq：堆队列
'''