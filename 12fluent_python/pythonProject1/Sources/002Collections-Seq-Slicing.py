"""
slicing 切片一般就是对Range和index的使用。
切片就提供一些特好有易读的语句。
1、当只有最后一个位置信息时，我们也可以快速看出切片和区间里有几个元
2、当起止位置信息都可见时，我们可以快速计算出切片和区间的长度，用后一个数减去
第一个下标（stop - start）即可。
3、这样做也让我们可以利用任意一个下标来把序列分割成不重叠的两部分，只要写成
my_list[:x] 和 my_list[x:] 就可以了--这一点确实是写算法中最好的一块啊
4、，我们还可以用 s[a:b:c] 的形式对 s 在 a 和 b 之间以 c 为间隔
取值。c 的值还可以为负，负值意味着反向取值。a:b:c 这种用法只能作为索引或者下标用在 [] 
中来返回一个切片对象：slice(a, b,c)
"""
l = [10, 20, 30, 40, 50, 60]
print( l[:2] ) # 到2，但不包括2
print(l[2:])# 从2开始到尾
print(l[:2]+l[2:])
# 正着数或者倒着数都可以
print( l[:-2] )
print(l[-2:])
print(l[:-2]+l[-2:])
# 使用a:b:c 来处理，每个参数都有默认值，a默认为0，b默认为len(s)+1，c默认为1
s = 'bicycle'
print(s[1::])
print(s[::-1])
print(s[-len(s)::])
print(s[:len(s)+1:])
# 这里要看看那个经典基础算法，找sortedlist中重复数量


#纯文本文件形式的收据以一行字符串的形式被解析
invoice = """
... 0.....6................................40........52...55........
... 1909  Pimoroni PiBrella                    $17.50    3    $52.50
... 1489  6mm Tactile Switch x20                $4.95    2     $9.90
... 1510  Panavise Jr. - PV-201                $28.00    1    $28.00
... 1601  PiTFT Mini Kit 320x240               $34.95    1    $34.95
... """
SKU = slice(0,6)
DESCRIPTION = slice(6, 40)
UNIT_PRICE = slice(40, 52)
ITEM_TOTAL = slice(55, None)
line_items = invoice.split('\n')[2:]
for item in line_items:
    print(item[UNIT_PRICE], item[DESCRIPTION])

## slice 可以赋值，但是赋值对下也是一个range？
from sys import getsizeof
a = list(range(10)) # 0~99
print(a,len(a),getsizeof(a))
#slice for setting,同时还多则增加，少则减少
a[2:5]=[20,30]
print(a,len(a),getsizeof(a))
a[5:]=[]
print(a,len(a),getsizeof(a))
# del slice,不会实际减少内存的。
del a[5:]
print(a,len(a),getsizeof(a))


# 对序列使用+和* 就是数学operator， 从数学角度是 +：增加，* 表示倍乘,类似instances的形式
# 对应的底层代码是 __iadd__ 对应+= ，__imul__ 对应*= ，都有退回的操作（去掉i的函数就行了）
# 用id来判断对象型语法的对象关系，是否指向同一个对下。
print('list add mul operator')
a = list(range(1,4))
print(a,id(a),len(a),getsizeof(a))
a += [12,13,14]
print(a,id(a),len(a),getsizeof(a))
a *= 2
print(a,id(a),len(a),getsizeof(a))
# 对比一下这种情况
board = [['_'] * 3 for i in range(3)]
print(board,id(board),len(board),getsizeof(board))
board[1][2] = 'X'
print(board,id(board),len(board),getsizeof(board))
# 引用的对下
b = ['_'] * 3
board = [ b  for i in range(3)]
print(board,id(board),len(board),getsizeof(board))
board[1][2] = 'X' # board[1] 指一个引用 后面的index 指定引用下index进行修改
b[0]='a'# 直接向引用对下进行修改也行。
print(board,id(board),len(board),getsizeof(board))


weird_board = [['_'] * 3] * 3
print(weird_board,id(weird_board),len(weird_board),getsizeof(weird_board))
weird_board[1][2] = 'O' 
print(weird_board,id(weird_board),len(weird_board),getsizeof(weird_board))
## 多维array的分配形式总是复杂的，参考c#下的，表示形式都不一样

# 不可变的tuple 也支持 += *= 每次会变换一次id
a = tuple(range(5))
b = a
a *= 2
c = d = a
c += (50,80) # tuple += list 已经报错了。
print(id(b),id(a),id(d),c) # 变化了
# 因为list是混合类型的，所以+= 就有变化了

# 在不可变的tuple里面塞个对象，然后修改对象的情况
print('可变的list 放在不可变的tuple里面的结果')
a = [12,13]
b =(1,2,3,a)
print( b )
a += [20,30,50,100]
print( b )# 确实就变化了

