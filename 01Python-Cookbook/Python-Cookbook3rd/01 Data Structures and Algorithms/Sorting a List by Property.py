'''
用例中原来表示为，List中每个都有一个Dictionary，
他们都有共同的key，然后根据共同的key来排序，获取key对应的属性就用itemgetter 方式
我觉得比较常见的还是，List里面放的是class的实例，根据class的属性来排序
或者List里面放着tuple，这里使用namedTuple来定义属性名字，然后排序
'''
import future.builtins.disabled

#dictionary的形式
rows = [
 {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
 {'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
 {'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
 {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
]

from operator import itemgetter
print('*'*20)
rows_by_fname = sorted(rows, key=itemgetter('fname'))
rows_by_uid = sorted(rows, key=itemgetter('uid'))
print(rows_by_fname)
print(rows_by_uid)
rows_by_lfname = sorted(rows, key=itemgetter('lname','fname'))
print(rows_by_lfname)

# class 定义以及data 表现为class 实例的情况
class Person:
    def __init__(self, fname, lname, uid):
        self.fname = fname
        self.lname = lname
        self.uid = uid

    def __repr__(self):
        return f"{self.__class__.__name__}(fname={self.fname}, lname={self.lname}, uid={self.uid})"

people = [
    Person('Brian', 'Jones', 1003),
    Person('David', 'Beazley', 1002),
    Person('John', 'Cleese', 1001),
    Person('Big', 'Jones', 1004)
]
print('*'*20)
rows_by_fname = sorted(people, key=lambda x:x.fname)
rows_by_uid = sorted(people, key=lambda x:x.uid)
print(rows_by_fname)
print(rows_by_uid)
rows_by_lfname = sorted(people, key=lambda x:(x.lname,x.fname))
print(rows_by_lfname)

## 使用namedtuple，不用namedtuple就只能用序号了，不喜欢用数字方式。
from  collections import  namedtuple
# 定义一个命名元组
Person = namedtuple('Person', ['fname', 'lname', 'uid'])

# 创建命名元组的实例
rows = [
    Person('Brian', 'Jones', 1003),
    Person('David', 'Beazley', 1002),
    Person('John', 'Cleese', 1001),
    Person('Big', 'Jones', 1004)
]

#于class定义的方式完全相同的写法，tuple比class 轻量一点。
"""
使用元组的好处是它们是不可变的，这可以防止数据被意外更改。此外，元组比列表更节省内存，因为它们是不可变的。
如果你的数据不需要修改，或者你想要确保数据不被更改，那么元组是一个不错的选择。
不过，如果你需要更复杂的数据结构和操作，那么使用类可能更合适。
"""
print('*'*20)
rows_by_fname = sorted(people, key=lambda x:x.fname)
rows_by_uid = sorted(people, key=lambda x:x.uid)
print(rows_by_fname)
print(rows_by_uid)
rows_by_lfname = sorted(people, key=lambda x:(x.lname,x.fname))
print(rows_by_lfname)

#如果来自json，按照下面的方式来解析。注意json的loads就默认解析了一些结构，但是结构本身还是字符串。
import json
from collections import namedtuple

# 定义命名元组
Person = namedtuple('Person', ['fname', 'lname', 'uid'])

# 自定义object_hook函数，将字典转换为命名元组
def person_object_hook(dct):
    return Person(**dct)

# JSON字符串
json_string = '''
[
    {"fname": "Brian", "lname": "Jones", "uid": 1003},
    {"fname": "David", "lname": "Beazley", "uid": 1002},
    {"fname": "John", "lname": "Cleese", "uid": 1001},
    {"fname": "Big", "lname": "Jones", "uid": 1004}
]
'''

# 使用json.loads函数解析JSON字符串，并使用person_object_hook作为object_hook参数
people = json.loads(json_string, object_hook=person_object_hook)

print('*'*20)
#打印的时候，字符串的引号去不掉。
rows_by_fname = sorted(people, key=lambda x:x.fname)
rows_by_uid = sorted(people, key=lambda x:x.uid)
print(rows_by_fname)
print(rows_by_uid)
rows_by_lfname = sorted(people, key=lambda x:(x.lname,x.fname))
print(rows_by_lfname)