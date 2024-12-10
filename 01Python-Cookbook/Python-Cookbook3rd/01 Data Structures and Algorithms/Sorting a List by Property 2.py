"""
前面介绍了在sorted里面使用lambda的方式进行比较的方式
sorted(people, key=lambda x:x.fname)
rows_by_fname = sorted(rows, key=itemgetter('fname'))
这两种方法，是否还有其他的方法，如果是自己定义的class 当然可以定义比较函数了
不过缺点就是只给了一个默认的比较函数，要想字定义 还是要设置自己的key
用例太简单了 ：1.14. Sorting Objects Without Native Comparison Support
我用1.13的结构来说明吧。
注意一下这里的装饰器的作用，感觉应该在其他语言中也要找到对应物，因为重复性很大
在Python中，这些方法（被称为丰富比较方法）是可选的，您可以根据需要实现它们。通常，如果您实现了__eq__（等于）方法，它就足以支持基本的成员测试。
如果您需要排序功能，至少应该实现__lt__（小于）方法，因为排序算法通常基于“小于”的概念来工作。
如果您只实现__lt__方法，Python的functools模块提供了一个total_ordering装饰器，它可以自动为您生成其他比较方法。
这里是如何使用total_ordering装饰器的示例：
我搜索了一下 并没找到c#对应的东西。
"""
from functools import total_ordering


@total_ordering
class Person:
    def __init__(self, fname:str, lname:str, uid:int):
        self.fname:str = fname
        self.lname:str = lname
        self.uid = uid

    def __repr__(self):
        return f"{self.__class__.__name__}(fname={self.fname}, lname={self.lname}, uid={self.uid})"

    def __le__(self, other: object) -> NotImplemented:
        if not isinstance(other, Person):
            return NotImplemented
        return self.fname < other.fname

    def __eq__(self, other: object) -> NotImplemented:
        if not isinstance(other, Person):
            return NotImplemented
        return self.fname == other.fname


people = [
    Person('Brian', 'Jones', 1003),
    Person('David', 'Beazley', 1002),
    Person('John', 'Cleese', 1001),
    Person('Big', 'Jones', 1004)
]
print('*' * 20)
rows_by_fname = sorted(people)
rows_by_uid = sorted(people, key=lambda x: x.uid)
print(rows_by_fname)
print(rows_by_uid)
rows_by_lfname = sorted(people, key=lambda x: (x.lname, x.fname))
print(rows_by_lfname)

from  operator import attrgetter

rows_by_lfname = sorted(people, key=attrgetter('lname','fname'))
print(rows_by_lfname)

## 性能测试。
import  timeit
# 创建Person实例列表
people = [
    Person('Brian', 'Jones', 1003),
    Person('David', 'Beazley', 1002),
    Person('John', 'Cleese', 1001),
    Person('Big', 'Jones', 1004)
] * 100  # 增加列表长度以提高测试准确性

# 使用__le__方法排序的测试用例
def sort_with_le():
    sorted(people, key=lambda x: (x.lname, x.fname))

# 使用lambda函数排序的测试用例
def sort_with_lambda():
    sorted(people, key=lambda x: x.fname)

# 使用attrgetter排序的测试用例
def sort_with_attrgetter():
    sorted(people, key=attrgetter('fname'))

# 测试排序时间
time_le = timeit.timeit(sort_with_le, number=100)
time_lambda = timeit.timeit(sort_with_lambda, number=100)
time_attrgetter = timeit.timeit(sort_with_attrgetter, number=100)

print(f"Sort with __le__: {time_le:.6f} seconds")
print(f"Sort with lambda: {time_lambda:.6f} seconds")
print(f"Sort with attrgetter: {time_attrgetter:.6f} seconds")

