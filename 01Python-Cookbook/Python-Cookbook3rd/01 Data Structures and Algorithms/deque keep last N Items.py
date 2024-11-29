# 这个感觉满足FIFO的最多N个Items的情况。
# 当然如果是对于大的List每次只显示最后的N Items也一种view的思路
# deque double-ended queue 双端队列是有索引的序列容器，允许在它的首尾两端快速查入和删除。

from collections import deque

def search( lines, pattern, history=5):
    """
    您希望保留在迭代期间或其他某种处理过程中看到的最后几个项目的有限历史记录。
    :param lines:当前的记录。
    :param pattern: 需要报错历史记录的模式
    :param history: 保存多长历史 5 表示最后
    :return:line:当前记录 ,之前的5个记录，最多history个记录 满足Pattern。
    """
    previous_lines = deque( maxlen= history )
    for line in lines:
        if pattern in line:
            yield line, previous_lines
            previous_lines.append(line)


with open('Unpack Iterables to More 1 Elements.py') as f:
    """
    每次触发到pattern的时候，返回现在的记录，以及之前的5个记录
    """
    for line, prevlines in search( f, '#', 5):
        for pline in prevlines:
            print( pline,end='')
        print(line,end='')
        print('-'*20)

# 以下介绍deque的常规用法，deque设置最大长度 maxlen来定义。
# 最简单的用法 说明,当append* 超过最大数量时，自动pop 一个，始终是右边pop出来。
q = deque(maxlen=3)
q.append(1)
q.append(2)
q.append(3)
q.append(4)
print(q) #deque([2, 3, 4], maxlen=3)
q.appendleft(1)
print(q) #deque([1, 2, 3], maxlen=3)
q.pop()
print(q) #deque([1, 2], maxlen=3)
q.append(1)
print(q) #deque([1, 2, 1], maxlen=3)
q.popleft()
print(q) #deque([2, 1], maxlen=3)
print(q[0],q[-1]) #2 1
q.extend([4,5,6,7])
print(q) #deque([5, 6, 7], maxlen=3)
q.rotate(1) #右转一个位置，7，6，5
print(q) #deque([7, 5, 6], maxlen=3)
q.rotate(-1)#左转一个位置
print(q) #deque([5, 6, 7], maxlen=3)

# 一些依赖deque的经典用法咯：：Custom Usage for stl
#1 实现滑动窗口，如计算所有k大小的连续子数组的最大最小值，可以通过保持deque中存储当前窗口的最大最小的索引，从而高效更新窗口
#2 快速方问两端元素，这个已经在前面API介绍差不多了
#3 旋转元素，这在处理循环数组的问题时非常有用
#4 最大长度，只处理最新数据的场合，如实时数据流分析。当然可以appendleft，从尾部开始处理，这个方便中途启动的方式。


