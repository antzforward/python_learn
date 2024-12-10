"""
原名教：Extracting a subset of a Dictionary
看起来就是根据Dictionary的items进行filter操作
可以对比 Filtering Sequence Elements 里面的代码
注意[] 为list，set
() 为tuple或者对象
{} 为字典
其中很多的例子我都用Linq表现了，不重复了。
"""
prices = {
 'ACME': 45.23,
 'AAPL': 612.78,
 'IBM': 205.55,
 'HPQ': 37.20,
 'FB': 10.75
}
# Make a dictionary of all prices over 200
p1 = { key:value for key, value in prices.items() if value > 200 }
print( p1 ) #{'AAPL': 612.78, 'IBM': 205.55}
# Make a dictionary of tech stocks
tech_names = { 'AAPL', 'IBM', 'HPQ', 'MSFT' }
p2 = { key:value for key,value in prices.items() if key in tech_names }
print( p2 ) #{'AAPL': 612.78, 'IBM': 205.55, 'HPQ': 37.2}
#p2 其实不太好的,这么用可能好一点，一般db数据要大一点,但是，这种写法改变了dict的order，没有特别的意思 不要这么写。
p2 = {key:prices[key] for key in tech_names if key in prices.keys() }
print( p2 ) #{'IBM': 205.55, 'AAPL': 612.78, 'HPQ': 37.2}

# 性能测试，创建大的字典
import numpy as np

# 设置随机种子以获得可重复的结果
np.random.seed(0)

# 生成一个大字典，包含1000000个随机键值对
num_entries = 1000000
tech_names = np.random.randint(0, 10000, num_entries)
prices = {key: np.random.randint(1, 100) for key in tech_names}
#缩减tech_names 符合日常查询匹配的习惯，这里选20个
tech_names = tech_names[:20]

# 现在你可以使用这个大字典来测试上面两种写法的性能和内存占用
from memory_profiler import profile
import time

# 测试第一种写法的性能和内存占用
start_time = time.time()
p2 = {key: prices[key] for key in tech_names if key in prices.keys()}
print(f"第一种写法耗时：{time.time() - start_time}秒")
# 使用memory_profiler测量内存占用
# profile装饰器可以测量函数级别的内存占用
@profile
def test_dict_comprehension():
    p2 = {key: prices[key] for key in tech_names if key in prices.keys()}
test_dict_comprehension()

# 测试第二种写法的性能和内存占用
start_time = time.time()
p2 = {key: value for key, value in prices.items() if key in tech_names}
print(f"第二种写法耗时：{time.time() - start_time}秒")
# 使用memory_profiler测量内存占用
@profile
def test_dict_items():
    p2 = {key: value for key, value in prices.items() if key in tech_names}
test_dict_items()

