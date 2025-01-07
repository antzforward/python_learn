"""
2024年12月20日 09点54分 -
## 数值类型有：
这里主要讲一下Python提供的数值类型
基本上所有的编程语言都有支持的：
Integer，Float，Complex，Bool，Rational，Decimal
对应的是，整数，浮点数，复数，布尔型，分数，高精度十进制数。

数本身还有 二进制、八进制和十六进制：这些都是进制表现，底层都是二进制的。
还有：
bytes和bytearray：虽不是数值类型，但是可以表示字节值，并可以进行数值运算
memoryview：提供对bytes，bytearray或者其他缓冲区的内存视图，支持数值操作。

## 数值运算：
数值运算：
加，减，乘，除，整除，幂运算，取模，绝对值
运算赋值操作，上操作加上=
比较运算：
等于，不等于，大于，小于，大于等于，小于等于
逻辑运算：
逻辑与，逻辑或，逻辑非
位操作：
按位与，按位或，按位异或，按位非，左移，右移

数学函数（位于math模块）
计算平方根sqrt，计算幂pow，计算自然指数exp，计算自然对数log，计算10为底的对数log10，三角函数，反三角函数。
向上取整ceil，向下取整floor，截断整数tranc，四舍五入round，浮点数绝对值fabs，分离整数部分和小数部分modf
**重点说一下，round的第二个参数，表示小数点后的有效位数，负数就表示整数上的有效位数**

还有随机数的形式。

还有numpy的库中的数学运算的部分。

## 数值计算的精度与误差值
常规的用法，用decimal模块中的Decimal类型，提供任意精度的十进制浮点数算术（getcontext().prec来控制精度）
对于复杂的数学运算，可以使用fractions模块中的Fraction类型，它表示有理数。

对于复杂的数值计算，现在普遍的用法是转向Numpy，这里介绍Numpy常规的用途吧
"""
import math

## bool
true = True
false = False

## int
a = 1_000_000
b = 10_0000
print(a, b) #1000000 100000
c = 'c'
print( chr(ord(c)), ord(c)) #c 99


## float
a = math.e
b = math.pi
c = 1_000.0
print('{:0.3f},{:0.3f},{:0.3f}'.format(a, b, c)) #2.718,3.142,1000.000
### 使用round 四舍五入的方式
a = round( a, 3 )
b = round( b, 3 )
c = round( c, 3)
print('{},{},{}'.format(a, b, c)) #2.718,3.142,1000.0

from decimal import  Decimal
a = Decimal( math.e )
b = Decimal( math.pi )
c = Decimal(  1_000.0 )
print('{:0.3f},{:0.3f},{:0.3f}'.format(a, b, c))

## Decimal 是精度可动态的通过localcontext来设置
a = Decimal(1.3)
b = Decimal(1.7)
print( a/b ) #0.7647058823529412225698141713
from decimal import localcontext
with localcontext() as ctx:
    ctx.prec = 3# 等同round的形式
    print(a/b) #0.765
print( round(a/b, 3))#0.765

## 一个特殊的计算过程,数值范围内的精度超过限制了
a = 1.23e+18
b = -1.23e+18
c = 1_000
print('inf + 1000 - inf: {}'.format(a + c + b )) #1024.0
## 以下用于数值正确的情况。但是类似fsum就可以的吗？
import math
print('inf + 1000 - inf: {}'.format(math.fsum([a , c ,b])) )#1000.0
print('inf + 1000 - inf: {}'.format(Decimal(a)+Decimal(c)+Decimal(b)) )#1000

import sys
import numpy as np

def GetEpsilonWithValue( value:float)->float:
    epsilon = np.finfo(np.float32).eps
    n = np.float32(value)
    if n == 0:
        return epsilon
    # 增加 epsilon 直到它 可以影响 n 的值
    while np.isclose(n + epsilon,n):
        epsilon *= 2
    return epsilon/2


for i in range(8):
    v = float(128<<i)
    print('{} Epsilon is {:0.5f}'.format( v, GetEpsilonWithValue( v)))
print('*-+'*20)
## complex 表示复数，包括实部与虚部两个部分，是著名欧拉公式中必须要用的。
z = complex(3,4)
print( z, z.real, z.imag )#(3+4j) 3.0 4.0
z1 = complex(2, 3)
z2 = complex(1, -1)
# + - * /
print( z1 + z2, z1 - z2,z1 * z2,z1 / z2, sep=',')#(3+2j),(1+4j),(5+1j),(-0.5+2.5j)
# 共轭
print( z, z.conjugate(),sep=',') #(3+4j),(3-4j),可以看到，共轭复数的和是实数，差是虚数
import cmath

# 转换为极坐标的形式
print(abs(z), math.degrees( cmath.phase(z) ),sep=',' ) # 长度，角， 表示为（p*cos(a)+p*sin(a)j)
e_z = cmath.exp( z )
print( z,cmath.polar(z), e_z, z.conjugate(), cmath.polar(z.conjugate()) ,cmath.exp(z.conjugate()),sep=',')
r,phi= cmath.polar( z )
print( (r, phi),complex(r*math.cos(phi), r*math.sin(phi)))

print('*-+'*20)
#有理数，用分数来表示
from fractions import  Fraction
a = Fraction(1,2)
b = Fraction(3,4)
print( a + b, a - b,a * b,a / b, sep=',')#5/4,-1/4,3/8,2/3
print( a<b,float(a),float(b),sep=',') #True,0.5,0.75
for i in range( 1, 10 ):
    print( a*float(i),end=',')
c = Fraction(13, 7)
print('整数部分{} ，小数部分 {}'.format(c.numerator//c.denominator,
                                       Fraction(c.numerator % c.denominator, c.denominator)))

a = Fraction(1,3)
b = Fraction(1,6)
print( '1/3+1/6:',a + b ) #1/3+1/6: 1/2
## 印度老人分牛，牛不能杀了切割。 以下是条件
total = 17#19
first = Fraction(1,2)#Fraction(1,2)
second = Fraction(1,3)#Fraction(1,4)
third = Fraction(1,9)#Fraction(1,5)

### 判断过程，三个儿子的分数相加，转化成极简真分数，其中分子是等于总牛市，就可以按照它的实现过程来做，
totalFrac = first + second + third
if totalFrac.numerator % total == 0:
    allCows = totalFrac.denominator
    firstCows = int(allCows * first)
    secondCows = int( allCows * second )
    thirdCows = int( allCows * third )
    #print( allCows, firstCows, secondCows, thirdCows )
    if firstCows + secondCows + thirdCows  == total:
        print('一共{}只 大儿子占{}有{}只牛，二儿子占{}有{}只牛 三儿子占{}有{}只牛'.format( total,first,firstCows
                                                                                          , second,secondCows
                                                                                          , third,thirdCows))

## 印度老人分牛的反向问题，满足可以分牛的分数和的规律，以下用暴力算法来实现，
## 1、total 总是不会被每个分母整除，因此每一个儿子都不能直接分
## 2、三个儿子的分数的特点是分子为1，分母逐渐增加，并且大儿子固定为1/2，二儿子为1/3或者1/4，变动的是三儿子的数字
## 3、三个分数加起来还是真分子，并且极简真分式的形式
## 4、为了表现出magic的数字1，借一只羊的表现，分子/分母差一只吧
## 为了让遍历数据看起来简单，让牛的量小一点，不超过200只。
print('*-+'*20)
first = Fraction(1,2)
for s in [3,4]:
    second = Fraction( 1, s )
    for t in range( s+1, 200):
        third = Fraction( 1,t)
        totalFrac = first + second + third
        total = totalFrac.numerator
        allCows = totalFrac.denominator
        firstCows = int(allCows * first)
        secondCows = int(allCows * second)
        thirdCows = int(allCows * third)
        if firstCows + secondCows + thirdCows == total and allCows - total == 1:
            print('一共{}只 大儿子占{}有{}只牛，二儿子占{}有{}只牛 三儿子占{}有{}只牛'.format(total, first, firstCows
                                                                                             , second, secondCows
                                                                                             , third, thirdCows))

## 用Fraction来写个24point的玩法来看看，因为Fraction 表示分式 因此加减乘除都是Fraction，那4个初始数字先转成Fraction 最后求值就好了。
"""
放以后再玩，有点麻烦了
"""
