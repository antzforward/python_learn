'''
这里主要介绍一个可以统计元素的数量的工具，其中提到的
most_common 跟Find n largest or nsmallest 这个内容差不多
但是它增加了很多专用功能，建议还是记住用Counter吧。
'''

words = [
 'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
 'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
 'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
 'my', 'eyes', "you're", 'under'
]
from collections import Counter
word_counts = Counter(words)
top_three = word_counts.most_common(3) #[('eyes', 8), ('the', 5), ('look', 4)]
print(top_three)

# 某个key的数量
print( word_counts['not'])#1
# 所有的总数
print( word_counts.total() )#29
# 更新，我觉得这个用法，非常的差劲

morewords = ['why','are','you','not','looking','in','my','eyes']
for word in morewords:#手动更新，非常不好的方法
    word_counts[word] += 1

# 某个key的数量
print( word_counts['why']) #1
# 所有的总数
print( word_counts.total() )#37

#下面的方法有个update， 这个好太多了
word_counts.update( morewords )
# 某个key的数量
print( word_counts['why']) #2
# 所有的总数
print( word_counts.total() )#45

# 当然支持 一般集合的操作，+ - 操作 & | 的操作 这里展示一下 + 。
# 原始的代码实现，可以让大家了解要支持数学表达式严谨性要哪些类型的操作重载。
a = Counter(words)
b = Counter(morewords)
print( a + b )
