'''
slice 哪里都可以用，Array默认就支持Indexer
这里核心是把基于Indexer的Range给起了名字，说实在的只有一个方便让人读代码的语法糖。
比如
###### 0123456789012345678901234567890123456789012345678901234567890'
record = '....................100 .......513.25 ..........'
cost = int(record[20:32]) * float(record[40:48])
把第一段命名为shares， 后一段命名为prices，这样通过这些slice 可以访问多个字符串中对应的数值内容。
如
SHARES = slice(20,32)#front,end
PRICE = slice(40,48)
最终用法是
cost = int(record[SHARES]) * float(record[PRICE])

当然，C#8 新增的Indices and Ranges的内容中，
可以写成
Range phrase = 1..4; 这里用两个点 表示从1到4 但是不包括4，数学表示[front,end)这种形式。
'''

###### '0123456789012345678901234567890123456789012345678901234567890'
record = '0123456789012345678901234567890123456789012345678901234567890'
#'....................100 .......513.25 ..........'
cost = int(record[20:32]) * float(record[40:48])
print( f'{int(record[20:32])} * {float(record[40:48])} = {cost}' )
SHARES = slice(20,32) #可以多次使用，如果record是格式化后的字符串数组都可以这样。
PRICE = slice(40,48)
cost = int(record[SHARES]) * float(record[PRICE])
print( f'{int(record[SHARES])} * {float(record[PRICE])} = {cost}' )

# 常规这个slice，写法跟range一样 start，end，stop
SHARES = slice(20,32,2) #可以多次使用，如果record是格式化后的字符串数组都可以这样。
PRICE = slice(40,48,2)
cost = int(record[SHARES]) * float(record[PRICE])
print( f'{int(record[SHARES])} * {float(record[PRICE])} = {cost}' )

#还有跟根据目标IEnumerable的信息，修正slice的start， end， 2
items = [0, 1, 2, 3, 4, 5, 6]
a = slice(2,8,1)
print( items[a] ,' = ', items[2:8:1])
# 由于slice的格式特别像 range，因此可以解构slice 来生成range
for i in range(*a.indices(len(items))):
    print(items[i],end=',')
print()
print('*'*10 )

#另外，slice支持 多次slice,其实每次都进行一次range的生成的
# 这个计算过程 你确定能算出来了 尤其是indices的用法，使用相对距离的indices
print(items[a],items[a][a],items[a][a][a]) #[2, 3, 4, 5, 6] [4, 5, 6] [6]
print(a.indices(len(items)),a.indices(len(items[a])), a.indices(len(items[a][a])))

#在numpy，可以按维度方式slice，注意slice是一维
import numpy as np
a = slice(1,3,1)
arr_1d = np.arange( 16 )
print('1D', arr_1d[a])
arr_2d = np.arange( 16 ) .reshape(4,4)
print('2D', arr_2d[a,a])

# 这里用slice 来作个二分查找，感觉没用啊
def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2  # 计算中间索引
        mid_value = arr[mid]  # 获取中间值

        if mid_value == target:
            return mid  # 找到目标值，返回索引
        elif mid_value < target:
            left = mid + 1  # 搜索右半部分
        else:
            right = mid - 1  # 搜索左半部分

    return -1  # 未找到目标值

# 使用slice来实现二分查找
def binary_search_with_slice(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_value = arr[slice(mid, mid + 1)]  # 使用slice来获取中间值

        if mid_value[0] == target:
            return mid  # 找到目标值，返回索引
        elif mid_value[0] < target:
            left = mid + 1  # 搜索右半部分
        else:
            right = mid - 1  # 搜索左半部分

    return -1  # 未找到目标值

import random
# 测试二分查找函数
arr = [ random.randint(0, 1000) for i in range(1000)]
target = arr[5]
arr = sorted( arr )


index = binary_search(arr, target)
print(f"Index of {target} using binary_search: {index}")

index_with_slice = binary_search_with_slice(arr, target)
print(f"Index of {target} using binary_search_with_slice: {index_with_slice}")