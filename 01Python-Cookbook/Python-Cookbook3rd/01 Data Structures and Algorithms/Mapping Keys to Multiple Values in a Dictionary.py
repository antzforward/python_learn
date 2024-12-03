"""
You want to make a dictionary that maps keys to more than one value (a so-called
“multidict”).
"""
from collections import defaultdict

# 创建一个multidict，其中每个键映射到一个列表
multidict = defaultdict(list) #value是list

# 添加键值对
multidict['key1'].append('value1')
multidict['key1'].append('value2')
multidict['key2'].append('value3')

# 访问键对应的值列表
print(multidict['key1'])  # 输出: ['value1', 'value2']
print(multidict['key2'])  # 输出: ['value3']

# 检查键是否存在
if 'key3' in multidict:
    print(multidict['key3'])  # 如果键不存在，这里会打印出一个空列表
else:
    print("Key does not exist")

# 获取所有键
print(multidict.keys())

# 获取所有值
for key, values in multidict.items():
    print(f"Key: {key}, Values: {values}")


"""
value 设计为集合
"""
# 创建一个multidict，其中每个键映射到一个集合
multidict = defaultdict(set)

# 添加键值对
multidict['key1'].add('value1')
multidict['key1'].add('value2')
multidict['key2'].add('value3')

# 访问键对应的值集合
print(multidict['key1'])  # 输出: {'value1', 'value2'}
print(multidict['key2'])  # 输出: {'value3'}

#用defaultdict 代码比较清楚一点
d = defaultdict(list)
d['A'] =['1','3','5']
d['B'] =[1,2,3,4]
print(d)

# 这里主要是对应的multidict，满足一对多的情况
# 对应C#中默认的本来是两个类型，只是value类型可以是另外一个容器而已。

#还有一种更常见的情况，单射且满射的两个数值进行map，这里有
# bidict
from bidict import  bidict
from bidict import bidict

# 创建并初始化bidict
immutable_bidict = bidict({'a': 1, 'b': 2, 'c': 3})

# 访问操作
print(immutable_bidict['a'])  # 输出: 1
print(immutable_bidict.inverse[1])  # 输出: 'a'

# 尝试修改操作将抛出错误
# immutable_bidict['d'] = 4  # TypeError: 'bidict' object does not support item assignment


from bidict import MutableBidict

# 创建一个可变的双向字典
mutable_bidict = MutableBidict({'x': 10, 'y': 20})

# 添加新的键值对
mutable_bidict['z'] = 30

# 删除键值对
del mutable_bidict['x']

# 访问和反向访问
print(mutable_bidict['y'])  # 输出: 20
print(mutable_bidict.inverse[20])  # 输出: 'y'

# 反向添加 (直接在inverse属性上操作)
mutable_bidict.inverse[40] = 'w'
print(mutable_bidict['w'])  # 输出: 40