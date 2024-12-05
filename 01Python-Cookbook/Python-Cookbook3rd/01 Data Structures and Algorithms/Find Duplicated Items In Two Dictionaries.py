'''
两个字典中相同的元素查找。
如果我来说，从Items里面注意去查 一个一个比较太慢，应该用set，然后塞Items，
从这个set，逐个读出来，然后在两个dict里面 再比较一次？

唉，Python直接支持set的 &，- 操作
补充dict的操作，含义如下。把Item作为整个set的元素。
求与， 用A&B
求并， 用A+B 同A|B
求差   用A-B 或者B-A
'''

a = {
 'x' : 1,
 'y' : 2,
 'z' : 3
}

b = {
 'w' : 10,
 'x' : 11,
 'y' : 2
}
# 老的部分，主要针对set 容器操作
print( a.keys() & b.keys() )
print( a.keys() - b.keys() )

# 自己定义一个Dict 支持这些操作吧
# 为了表示基本类型的和差操作，打印一下测试

class MyDict(dict):
    def __add__(self, other):
        '''
        集合操作：和，等于A+B，注意这里的结果是Item的和，两个层面
        如果key不同，直接添加，如果key相同，Value不同，根据Value的类型来处理
        比如"A":3 对于"A":1 结果是"A":{1，3}：list or set 就是元素的add了。
        比如"A":1 对于"A":1 结果是"A":1,
        比如"A":[1,2,3] 对于"A":[1,2,4] 结果是""
        比如"A":(1,3) 对于"A":(1) 结果就是"A":{(1,3),{1}} =>tuple形式要检查格式
        :param other:
        :return: A+B
        '''
        if not isinstance(other, dict):
            return NotImplemented

        new_dict = self.copy()  # 复制当前字典

        for key, value in other.items():
            if key in new_dict:
                existing_value = new_dict[key]
                if isinstance(existing_value, set) and isinstance(value, set):
                    # 如果两个值都是集合类型，合并它们
                    new_dict[key] = existing_value | value
                elif isinstance(existing_value, list) and isinstance(value, list):
                    # 如果两个值都是列表，合并它们
                    new_dict[key] = existing_value + value
                elif isinstance(existing_value, tuple) and isinstance(value, tuple):
                    # 如果两个值都是元组，将它们转换为列表然后合并，最后转回元组
                    new_dict[key] = tuple(list(existing_value) + list(value))
                else:
                    # 对于其他不同或不可合并的类型，放入集合中
                    new_dict[key] = {existing_value, value}
            else:
                # 如果键不存在，直接添加
                new_dict[key] = value

        return MyDict(new_dict)
    def __sub__(self, other):
        '''
        集合的差操作：A-B指存在A，不在B中的元素,注意这里是检查Item 不单以Key作为判断
        比如"A":{1,3} 对于"A":1 结果是"A":3：list or set 就是元素的remove了。
        比如"A":1 对于"A":2 结果是"A":1,不匹配
        比如"A":(1,3) 对于"A":(1) 结果就是"A":(1,3) =>tuple形式要检查格式
        :param other:
        :return:
        '''
        if not isinstance(other, dict):
            return NotImplemented

        new_dict = self.copy()

        for key, value in other.items():
            if key in new_dict:
                existing_value = new_dict[key]
                if isinstance(existing_value, set) :
                    # 如果两个值都是集合，则进行集合差操作
                    if isinstance(value, set):
                        new_dict[key] = existing_value - value
                    else:
                        new_dict[key] = existing_value - {value}
                    if not new_dict[key] :  # 如果结果为空集合，删除该键
                        del new_dict[key]
                    elif len(new_dict[key]) == 1:
                        new_dict[key] = list(new_dict[key])[0] #退化成基本形式
                elif isinstance(existing_value, list) and isinstance(value, list):
                    # 如果两个值都是列表，进行元素差操作
                    # 只删除第二个列表中出现的第一个列表的元素
                    new_list = existing_value[:]
                    for item in value:
                        if item in new_list:
                            new_list.remove(item)
                    new_dict[key] = new_list
                    if not new_dict[key]:
                        del new_dict[key]
                elif isinstance(existing_value, tuple) and isinstance(value, tuple):
                    # 元组不支持原位修改，转换为列表处理后再转回元组
                    new_list = list(existing_value)
                    for item in value:
                        if item in new_list:
                            new_list.remove(item)
                    new_dict[key] = tuple(new_list)
                    if not new_dict[key]:
                        del new_dict[key]
                elif existing_value == value:
                    del new_dict[key]
                else:
                    # 对于其他不同或不能直接比较的情况，保留原始键值对
                    continue

        return MyDict(new_dict)

    def __or__(self, other):
        '''
        集合操作：和，等于A+B
        :param other:
        :return: A|B
        '''
        return self + other
    def __and__(self, other):
        '''
        集合操作，A与B的共同元素 A&B
        :param other:
        :return: A&B
        '''
        if not isinstance(other, dict):
            return NotImplemented
        common_keys = self.keys() & other.keys()
        new_dict = {}
        for key in common_keys:
            existing_value = self[ key ]
            value = other[key]
            # 底层进行& 操作
            if isinstance(existing_value, set) and isinstance(value, set):
                # 如果两个值都是集合，则进行集合差操作
                new_dict[key] = existing_value & value
                if not new_dict[key]:  # 如果结果为空集合，删除该键
                    del new_dict[key]
            elif isinstance(existing_value, list) and isinstance(value, list):
                # 如果两个值都是列表，进行元素差操作
                # 只删除第二个列表中出现的第一个列表的元素
                new_list = existing_value[:]
                for item in value:
                    if item not in new_list:
                        new_list.remove(item)
                new_dict[key] = new_list
                if not new_dict[key]:
                    del new_dict[key]
            elif isinstance(existing_value, tuple) and isinstance(value, tuple):
                # 元组不支持原位修改，转换为列表处理后再转回元组
                new_list = list(existing_value)
                for item in value:
                    if item not in new_list:
                        new_list.remove(item)
                new_dict[key] = tuple(new_list)
                if not new_dict[key]:
                    del new_dict[key]
            elif existing_value == value:
                new_dict[key] = existing_value
                if not new_dict[key]:
                    del new_dict[key]
            else:
                # 对于其他不同或不能直接比较的情况，保留原始键值对
                continue
        return MyDict(new_dict)


# 使用示例 满足a+b-b == a的形式，太难写了
a = MyDict({'x': 1, 'y': 2})
b = MyDict({'y': 3, 'z': 4})
print( a - b )  # 输出: {'x': 1,'y':2}
print( a + b )  # {'x': 1, 'y': {2, 3}, 'z': 4}
print( a & b )  # {}
print( a + b - b )  # {'x': 1, 'y': 2}


## 用collection.abc 模块来实现这种通用操作



