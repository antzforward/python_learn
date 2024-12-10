"""
这里还是基于一个想法，把Sequence的内容转换成有对应名字的属性
与之类似的是：Naming a Slice.py 这里是将Range 改成了Slice，避免了index，offset的数值设置
这里差不多。
tuple先定义格式，然后属性不可修改，这是比较重要的。
"""
from collections import namedtuple
Subscriber = namedtuple('Subscriber', ['addr', 'joined'])
sub = Subscriber('jonesy@example.com', '2012-10-19')#其实joined可以转换为Date，因为tuple不做这个事情。
print(sub, sub.addr, sub.joined)
print(len(sub))
addr, joined = sub # tuple 分解方式。

# 定义股票的tuple
Stock = namedtuple('Stock', ['name', 'shares', 'price'])
def compute_cost(records):
    total = 0.0
    for rec in records:
        s = Stock(*rec)
        total += s.shares * s.price
    return total
s = Stock('ACME', 100, 123.45)
print(s)
# s.shares = 75 #can't set attribute
t = s._replace(shares=75) # 产生新的instance
print( s, t,s == t )

#始终从default tuple构造instance的方式

Stock = namedtuple('Stock', ['name', 'shares', 'price', 'date', 'time'])
# Create a prototype instance
stock_prototype = Stock('', 0, 0.0, None, None) #type default 设置
# Function to convert a dictionary to a Stock
def dict_to_stock(s):
    return stock_prototype._replace(**s)
a = {'name': 'ACME', 'shares': 100, 'price': 123.45}
print( dict_to_stock( a ))
b = {'name': 'ACME', 'shares': 100, 'price': 123.45, 'date': '12/17/2012'}
print( dict_to_stock( b ))

"""
最后，但同样重要的是，如果你的目标是定义一个高效的数据结构，并且你将在这个结构中更改各种实例属性，那么使用命名元组（namedtuple）并不是最佳选择。
相反，考虑定义一个使用 __slots__ 的类。
下面的例子：

在这个例子中，Person 类使用 __slots__ 定义了三个属性：fname、lname 和 uid。使用 __slots__ 的好处是它可以帮助节省内存，因为 __slots__ 
限制了实例只能拥有指定的属性，而不是使用默认的字典来存储属性。这在创建大量实例时尤其有用，因为它减少了内存的开销。

请注意，使用 __slots__ 后，你不能添加 __slots__ 中未定义的属性，否则会引发 AttributeError。
同时，使用 __slots__ 的类也不再支持动态创建属性，因为它们没有 __dict__。
"""
class Person:
    __slots__ = ('fname', 'lname', 'uid')  # 定义允许的属性

    def __init__(self, fname, lname, uid):
        self.fname = fname
        self.lname = lname
        self.uid = uid

    def __repr__(self):
        return f"Person(fname={self.fname}, lname={self.lname}, uid={self.uid})"

# 创建Person实例
person = Person('John', 'Doe', 123)

# 打印实例
print(person)

# 修改属性
person.fname = 'Jane'

# 打印修改后的实例
print(person)

# 对namedtuple 和 slot 进行内存比较。 slot比较像c系列的class了。
"""
result: slot 确实在性能与内存占用上都胜出了。
Memory usage of one PersonNamedTuple instance: 80 bytes
Memory usage of one PersonWithSlots instance: 56 bytes
Time to create 100000 PersonNamedTuple instances: 0.052665399853140116 seconds
Time to create 100000 PersonWithSlots instances: 0.0280305000487715 seconds
"""
import sys
from collections import namedtuple
import timeit

# 定义一个使用 namedtuple 的类
class PersonNamedTuple(namedtuple('PersonNamedTuple', ['fname', 'lname', 'uid'])):
    def __new__(cls, fname, lname, uid):
        return super(PersonNamedTuple, cls).__new__(cls, fname, lname, uid)

# 定义一个使用 __slots__ 的类
class PersonWithSlots:
    __slots__ = ['fname', 'lname', 'uid']

    def __init__(self, fname, lname, uid):
        self.fname = fname
        self.lname = lname
        self.uid = uid

# 创建大量实例进行测试
num_instances = 100000

# 测试 namedtuple 的内存占用
namedtuple_memory_usage = sys.getsizeof(PersonNamedTuple('John', 'Doe', 1))
print(f"Memory usage of one PersonNamedTuple instance: {namedtuple_memory_usage} bytes")

# 测试 __slots__ 的内存占用
slots_memory_usage = sys.getsizeof(PersonWithSlots('John', 'Doe', 1))
print(f"Memory usage of one PersonWithSlots instance: {slots_memory_usage} bytes")

# 测试创建 namedtuple 实例的性能
namedtuple_creation_time = timeit.timeit(
    lambda: [PersonNamedTuple('John', 'Doe', i) for i in range(num_instances)],
    number=1
)
print(f"Time to create {num_instances} PersonNamedTuple instances: {namedtuple_creation_time} seconds")

# 测试创建 __slots__ 实例的性能
slots_creation_time = timeit.timeit(
    lambda: [PersonWithSlots('John', 'Doe', i) for i in range(num_instances)],
    number=1
)
print(f"Time to create {num_instances} PersonWithSlots instances: {slots_creation_time} seconds")