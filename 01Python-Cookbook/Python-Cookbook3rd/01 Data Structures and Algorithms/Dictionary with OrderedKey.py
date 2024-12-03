import json
from collections import  OrderedDict
d = OrderedDict() #查入顺序的dict，这里的Ordered 按查入时间来定
d['foo'] = 1
d['bar'] = 2
d['spam'] = 3
d['grok'] = 4
# Outputs "foo 1", "bar 2", "spam 3", "grok 4"
for key in d:
    print(key, d[key],end=',')
print()
#调整顺序,特殊操作。
d.move_to_end('foo')
print(json.dumps(d))

#对比一下普通的
from collections import  defaultdict
d = {} #没啥区别，Python 3.7中普通的字典已经保证了插入顺序。
d['foo'] = 1
d['bar'] = 2
d['spam'] = 3
d['grok'] = 4
for key in d:
    print(key, d[key],end=';')
print()
print( json.dumps(d) )

'''
何时一定要用OrderedDict（就是依赖查入时序的字典情况）
严格的元素顺序：

1.当需要频繁地添加或删除键值对，并重新排序这些键值对时（例如将最近使用的项目移动到末端或开始位置）。这在实现某些缓存策略如 LRU (Least Recently Used) 缓存时非常有用。
当输出顺序必须与输入顺序完全一致，即使在进行了一些操作如更新或查询后。
比较依赖于插入顺序：

2.如果你需要比较两个集合，不仅需要它们包含相同的元素，而且元素的添加顺序也必须相同，那么 OrderedDict 将非常适用。例如，在测试环境中，保持元素顺序可以帮助确保重现性和一致的结果。
数据记录与分析：

3.在需要按顺序记录条目的时间序列数据处理中，OrderedDict 可以确保数据的顺序性和快速访问。比如，你可能需要保持日志文件的条目顺序，或者在金融应用中按交易时间排序记录。
维护历史记录：

4.当你处理需要维护编辑或操作历史的系统时（如撤销/重做功能的实现），OrderedDict 可以有效管理这些历史记录的顺序。
'''

# LRU缓存的用法
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return -1
        else:
            # 这个操作会把元素移到字典的末尾表示最近使用过
            self.cache.move_to_end(key)
            return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            # 更新键值对，并移到末尾表示最近使用
            self.cache.move_to_end(key)
        elif len(self.cache) == self.capacity:
            # 缓存已满，移除第一个键值对（最久未使用）
            self.cache.popitem(last=False)
        self.cache[key] = value

# 使用演示
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))       # 返回 1
cache.put(3, 3)           # 移除 key 2
print(cache.get(2))       # 返回 -1 (未找到)
