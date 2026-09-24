"""
sequence 的常规操作有：迭代、切片，排序，还有拼接。
容器序列：
    list，tuple和collection.deque 这些序列能存放不同类型的数据
扁平序列：
    str，bytes，bytearray，memoryview和array.array，这类序列只能容纳一种类型。
容器序列存放的是它们所包含的任意类型的对象的引用，而扁平序列里存放的是值而不
是引用。换句话说，扁平序列其实是一段连续的内存空间。由此可见扁平序列其实更加紧
凑，但是它里面只能存放诸如字符、字节和数值这种基础类型。
序列类型还能按照能否被修改来分类。
可变序列
    list、bytearray、array.array、collections.deque 和 memoryview
不可变序列
    tuple、str 和 bytes
"""
##列表推导是构建列表（list）的快捷方式，而生成器表达式则可以用来创建其他任何类型的序列。

symbols =  '$¢£¥€¤' #str,扁平序列
codes = []
for symbol in symbols:
    codes.append( symbol )

print( codes )
# for in 基本上是linq的基础形式来
print([ord(symbol) for symbol in symbols])

#列表推导不会再有变量泄漏的问题
x= 'my precious'
dummy = [x for x in 'ABC']
print(x) #与书上不一致，x没有被覆盖。在2.x下是会被替换的，不过2.x的版本代码不多了。
beyond_ascii = [ord(s) for s in symbols if ord(s) > 127]
print( beyond_ascii )
# 有点麻烦，用海象操作符 但是要包裹一下。
beyond_ascii = [n  for s in symbols if (n := ord(s)) > 127]
print( beyond_ascii )
# 还有一种用得比较少好的，但是不太linq，类型推理要自己写清楚
# map对迭代器上每个元素都执行ord，生成一个迭代器，然后
# 再 filter对迭代结果进行过滤，产生一个filter object
# 然后用list 对内容进行执行。
beyond_ascii = list(filter(lambda c:c>127,map(ord, symbols)))
print( beyond_ascii )

# 性能测试一波
import timeit
TIMES = 10000

SETUP = """
symbols = '$¢£¥€¤'
def non_ascii(c):
    return c > 127
"""

def clock(label, cmd):
    res = timeit.repeat(cmd, setup=SETUP, number=TIMES)
    print(label, *('{:.3f}'.format(x) for x in res))

clock('listcomp        :', '[ord(s) for s in symbols if ord(s) > 127]')
clock('listcomp+walrus :', '[n for s in symbols if (n := ord(s)) > 127]')
clock('listcomp + func :', '[ord(s) for s in symbols if non_ascii(ord(s))]')
clock('filter + lambda :', 'list(filter(lambda c: c > 127, map(ord, symbols)))')
clock('filter + func   :', 'list(filter(non_ascii, map(ord, symbols)))')
print('fastest is  listcomp+walrus')

colors = ['black', 'white','red']
sizes = ['S','M','L','2L','3L','4L']
# 直接生成 list
tshirts = [(color, size)    for color in colors 
                            for size in sizes] 
# 输出 按顺序 element
print( tshirts ) 
# 直接生成,tuple 类型
tshirts = tuple((color, size)    for color in colors 
                            for size in sizes) 
# 输出 按顺序 element
print( tshirts ) 
import array
# 直接生成,array 类型
codes = array.array('I',(ord(symbol) for symbol in symbols)) 
# 输出 按顺序 element
print( codes ) 
# 生成器
tshirts = ((color, size)    for color in colors 
                            for size in sizes)
# 输出 <generator object <genexpr> at 0x0000017618047760>
print( tshirts ) 

# tuple 不可变，可以不指向名字，unpacking过程可以用_ 来替代不想要的
lax_coordinates = (33.9425, -118.408056) 
city, year, pop, chg, area = ('Tokyo', 2003, 32450, 0.66, 8014)
traveler_ids = [('USA', '31195855'), ('BRA', 'CE342567'),('ESP', 'XDA205856')]
for passport in sorted(traveler_ids): 
    print('%s/%s' % passport)
for country, _ in traveler_ids:#不需要的用under line来表示
    print(country)
# 不想要的用_来替代，应该可以支持多次,其他语言不确定。 
city, _, pop, _, _ = ('Tokyo', 2003, 32450, 0.66, 8014)
print('%s/%s' % (city,pop))
# 测试一下自己的想法，想要首尾的,*_的用法，直接用* 是不行的
city,*_,area=('Tokyo', 2003, 32450, 0.66, 8014)
print('%s/%s' % (city,area))
# 可以用*name 把不要的解锁到一起，表示不知道多少的，数量靠推导的。
city,*mid,_=('Tokyo', 2003, 32450, 0.66, 8014)
print('%s/%s' % (city,mid))
#使用*运算符把一个可迭代对下拆开作为函数的参数
t = (20,8)
print(f"tuple mode:{divmod(*t)}")
t=[20,8]
print("list mode:%s"%(divmod(*t),))
quotient, remainder = divmod(*t)
print("custom mode:%s,%s"%(quotient,remainder))

# 这里说到过在国际化软件中，那么 _ 可能就不是一个理想的占位符
# 还有就是，我知道"_"本身就是Qt等宏设计的内容，如果要转代码，_就不能用。

# --- 
# 函数用*args的来支持不确定数量的参数，比如c++等的main函数都这样。
a,b,*rest= range(5)
print("1st:%s,2nd:%s"%(a,b))
a,b,*_ = range(5)
print("1st:%s,2nd:%s"%(a,b))
a,b,*rest= range(10)
print(f"other:{rest}")
*rest,a,b,_= range(10)
print(f"head -3 :{rest}")
rest = list(range(10)[:-3])
print(f"head -3 :{rest}")
# 特别注意，一个表达式中只有一个*才能正常推导出来
a,*rest,b= range(1,6)
#下面这行多出来一个tuple的包裹形式。必须要包裹了，因为只有一个{}
print(f"other:{a,rest,b}")
#这种就是正常的
print(f"normal other:{a},{rest},{b}")
print(f"normal other:%s,%s,%s"%(a,rest,b))
# 嵌套元组拆包,但是我认为核心在fmt的定义
metro_areas = [
    ('Tokyo','JP',36.933,(35.689722,139.691667)),  # 
    ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
    ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
    ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
    ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]
#这里的format还挺好用的，就是要理解它的语法了。
print('{:15} | {:^9} | {:^9}'.format('', 'lat.', 'long.'))
fmt = '{:15} | {:9.4f} | {:9.4f}'
for name, cc, pop, (latitude, longitude) in metro_areas:
    if longitude <= 0:
        print(fmt.format(name, latitude, longitude))

# 重点，tuple不适合作为参数，但是变参函数的形式还是支持的。还是类型推导的过程。
# 还有就是基础的数学操作在这个上面失效，比如dot cross之类的，尤其是cross，超过维度就没有意思了吧
# 首先还是namedtuple形式
from collections import namedtuple
City = namedtuple('City','name country population coordinates')
print(City._fields)
cities = [City(*info) for info in metro_areas]
print(cities[2].name )
# 或者生成generator
cities = (City(*info) for info in metro_areas)
# 或者调用namedtuple自己的函数_make,注意这里的产生形式不一样
cities = (City._make(info) for info in metro_areas)
print('\nnew format:\n{:15} | {:^9} | {:^9}'.format('', 'lat.', 'long.'))
for name, cc, pop, (latitude, longitude) in cities:
    if longitude <= 0:
        print(fmt.format(name, latitude, longitude))

LatLong = namedtuple('LatLong', 'lat long')
delhi_data = ('Delhi NCR', 'IN', 21.935, LatLong(28.613889, 77.208889))
delhi = City._make(delhi_data)#与City(*delhi_data)一样的
print(delhi._asdict())
[print(key + ':', value) for key, value in delhi._asdict().items()]
# 清楚field 的内容
