"""
这里是指，在数据转换同时使用数据规约。
"Data reduce"操作，通常称为数据规约或数据减少，是指在数据挖掘和数据处理中减少数据集规模的过程，同时尽量保留重要信息。这个操作包括数据压缩和数据立方体聚集等技术，目的是从大型数据库中提取关键数据，减少数据集的大小，优化存储，并提高处理能力
。
在函数式编程中，"reduce"函数通常接受一个初始值和一个累加器函数，然后遍历集合中的每个元素，逐步应用累加器函数，最终将所有元素缩减为一个单一的值。
例如，Python中的functools.reduce函数就是这种操作的实现。
因此，任何将多个输入值通过某种规则或函数合并为单个输出值的操作都可以被认为是"reduce"操作。这类操作在数据处理和分析中非常常见，
因为它们可以帮助简化数据，提取有用的信息，或者为进一步的分析做准备。
Python下面的例子有，默认的有一下的
求和（Sum）：将一系列数字相加得到总和。
求积（Product）：将一系列数字相乘得到乘积。
最小值（Min）：从一系列值中找出最小值。
最大值（Max）：从一系列值中找出最大值。
平均值（Average）：计算一系列数字的平均值。
逻辑与（All）：检查一系列布尔值是否全部为真。
逻辑或（Any）：检查一系列布尔值中是否有任意一个为真。
以及functools.reduce函数
对于c# 下面的用aggregate 来对应reduce方法。要同时做就必须Select+Aggregate一起才可以。
"""
from collections import namedtuple

nums = [1, 2, 3, 4, 5]
s = sum(x * x for x in nums)
print(s) #55
s = sum( x**2 for x in range(1,101))
print(s)

import  os
files = os.listdir( os.curdir )
if any( name.endswith('.py') for name in files ):
    print('There be python!')
else:
    print('Sorry, no python.')

# Output a tuple as CSV
s = ('ACME', 50, 123.45)
print(','.join(str(x) for x in s))

# Data reduction across fields of a data structure
portfolio = [
 {'name':'GOOG', 'shares': 50},
 {'name':'YHOO', 'shares': 75},
 {'name':'AOL', 'shares': 20},
 {'name':'SCOX', 'shares': 65}
]
min_shares = min(s['shares'] for s in portfolio)
print( min_shares )
# Alternative: Returns {'name': 'AOL', 'shares': 20}
min_shares = min(portfolio, key=lambda s: s['shares'])
print( min_shares )

## 下面定义常规的数据规约的用法，自己定义一个操作，体现数据从多变少的过程。
### 首先import reduce
from functools import reduce
words = ['Hello', 'world', 'this', 'is', 'Python']
sentence = reduce(lambda x, y: x + ' ' + y, words)
print(sentence)  # 输出 "Hello world this is Python"
#### 添加一个需求，希望在头尾都加上特殊字符，比如"🐉" 只是尾部显得多余又合理啊
sentence = reduce(lambda x, y: x + ' ' + y, words,"🐉")+"🐉"
print(sentence)  # 输出 "🐉 Hello world this is Python🐉"
sentence = "🐉" + reduce(lambda x, y: x + ' ' + y, words)+"🐉"
print(sentence)  # 输出 "🐉 Hello world this is Python🐉"

#### 转换成用list显示的效果
sentence = '['+reduce(lambda x,y:x+','+y, words )+']'
print( sentence )

## 一个计算Fibonacci 数的总和的过程
### 写个iterator 返回fibonacci
def fibonacci(n):
    a,b = 0,1
    for _ in range( n ):
        yield  a
        a, b = b, a+b
#### 计算整体和
result = reduce( lambda  x,y:x+y, fibonacci(5))
print(result )#7

## 用reduce的方式来做
# 定义一个斐波那契元组，包含两个元素：a和b
def fibonacci(n):
    return reduce(
        lambda ab, _: (ab[1], ab[0] + ab[1]),
        range(n),
        (0, 1)
    )[0]

# 计算第5个斐波那契数
fibonacci_5th = fibonacci(5)
print(f"The 5th Fibonacci number is: {fibonacci_5th}")  # 输出 5


# 测试一下 这两句代码的性能情况，个人认为方法1 效率 比方法2要差
# 方法1：sentence = reduce(lambda x, y: x + ' ' + y, words,"🐉")+"🐉"
# 方法2：sentence = "🐉" + reduce(lambda x, y: x + ' ' + y, words)+"🐉"
from memory_profiler import profile
import time
import numpy as np

np.random.seed(0)
num_entries = 10000
words = [str(x) for x in np.random.randint(0, 10000, num_entries)]

# 测试第一种写法的性能和内存占用
start_time = time.time()
sentence = reduce(lambda x, y: x + ' ' + y, words,"🐉")+"🐉"
print(f"第一种写法耗时：{time.time() - start_time}秒")
# 使用memory_profiler测量内存占用
# profile装饰器可以测量函数级别的内存占用
@profile
def test_sequence_aggregate():
    sentence = reduce(lambda x, y: x + ' ' + y, words,"🐉")+"🐉"
test_sequence_aggregate()

# 测试第二种写法的性能和内存占用
start_time = time.time()
sentence = "🐉" + reduce(lambda x, y: x + ' ' + y, words)+"🐉"
print(f"第二种写法耗时：{time.time() - start_time}秒")
# 使用memory_profiler测量内存占用
@profile
def test_sequence_reduce():
    sentence = "🐉" + reduce(lambda x, y: x + ' ' + y, words)+"🐉"
test_sequence_reduce()

