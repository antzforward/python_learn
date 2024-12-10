"""
取除冗余，并且保证顺序
核心是一个generator（生成器）的设计模式，它允许你以惰性（lazy，也就是用yield ）的方式生成一系列值。
以下是一个惰性求值的类型 Lazy Evaluation Generator
Lazy Evaluation Generator 是产生一个IEnumerable 不会占用大量内存。
注意这个yield关键字的使用，恩，不需要写成yield return的模式。
另外这里声明的dedupe的优点是去重复但是不改变顺序。

这个似乎对应的是Linq的Distinct
"""
import numpy as np


def dedupe(items) :
    seen = set()
    for item in items:
        if item not in seen:
            yield item
        seen.add(item)


a = [1, 5, 2, 1, 9, 1, 5, 10]
print(list(dedupe(a)))  #[1, 5, 2, 9, 10]
print(set(a))  #{1, 2, 5, 9, 10}
import numpy
print(np.unique(np.array(a))) #等同于C#里面的Distinct的用法

# 比如用惰性计算的生成器的写法
# 写个简单的，从1到N个的fibonacci的数列生成器,序号从0 开始，第一个数字为0
def fibonacci(count):
    a, b = 0, 1
    for i in range(count):
        yield a
        a, b = b, a + b


print(list(fibonacci(10)))  #[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


def fibonacci(start, count):
    end = start + count
    a, b = 0, 1
    for i in range(end):
        if i >= start:
            yield a
        a, b = b, a + b


print(list(fibonacci(1, 9)))  #[1, 1, 2, 3, 5, 8, 13, 21, 34]


#for dicts
def dedupe(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
        seen.add(val)


a = [{'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 1, 'y': 2}, {'x': 2, 'y': 4}]
print(list(dedupe(a, key=lambda d: (d['x'], d['y']))))  #[{'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 2, 'y': 4}]
print(list(dedupe(a, key=lambda d: d['x'])))  #[{'x': 1, 'y': 2}, {'x': 2, 'y': 4}]

## 这里用来说以下dedupe的用法 比如读本文件
with open('Remove Duplicates from a Sequence while Ordered.py', 'r') as f:
    for line in dedupe(f):
        print(line, end='')  #自带了\n
