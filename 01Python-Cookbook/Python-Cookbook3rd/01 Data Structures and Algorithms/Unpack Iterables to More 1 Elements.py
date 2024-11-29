# 任意的Elements 可以用变量名前加*来标志 这个变量可能解析的是一个Iterable 对象
record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
name, email, *phone_numbers = record  #phone_numbers 前加* 表示解释了，除了前两个Element之外的其他
print(name, email, phone_numbers, end='\n')

from typing import Iterable
#或者我不清楚结构，每次都拆结Element 比如下面：：Custom Example
def drap_head(elements:Iterable )->None:
    if len(elements) == 1:
        print(elements[0])
    else:
        first, *other = elements # other 最后解析的是[last]
        print(first, end=',')
        drap_head(other)

drap_head( record )

# 当然可以倒着解析 嘿嘿
def drap_last( elements:Iterable )->None:
    if len(elements) == 1:
        print(elements[-1])
    else:
        *other,last = elements # other 最后解析的是[last]
        print(last, end=',')
        drap_last(other)

drap_last( record )

*trailing, current = [10, 8, 7, 1, 9, 5, 10, 3]
print(trailing,current,end='\n')

# 这里类似pattern match的模型，在c# 里面算是典型应用,但是c# 里面估计要用到is 语句
records = [
 ('foo', 1, 2),
 ('bar', 'hello'),
 ('foo', 3, 4),
]

def do_foo(x:int, y:int)->None:
    print('foo', x, y)
def do_bar(s:str)->None:
    print('bar', s)
for tag, *args in records:
    if tag == 'foo':
        do_foo(*args)
    elif tag == 'bar':
        do_bar(*args)

line = 'nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false'
uname, *fields, homedir, sh = line.split(':')
print(uname, homedir,sh, end='\n')

#能用*_这种形式吗？ 可以，但是_不行的，*才是任意长度匹配的keyword
uname, *_, homedir, sh = line.split(':')
print(uname, homedir,sh, end='\n')

record = ('ACME', 50, 123.45, (12, 18, 2012))
name, *_, (*_, year) = record
print(name, year, end='\n')

items = [1, 10, 7, 4, 5, 9]
head, *tail = items
print(head, tail, end='\n')

def sum( elements ):
    head, *tail = elements
    return head + sum(tail) if tail else head # 这是改进的版本，我把前面的代码再修改一下

print( sum( items ) )

def drap_head2(elements:Iterable )->str:
    head,*tail = elements
    return str(head) +',' + drap_head2( tail ) if tail else str(head) # 注意这里不满足尾递归的。

print( drap_head2( record ))
