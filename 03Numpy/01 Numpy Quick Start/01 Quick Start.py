import sys

import numpy  as np
'''
ndarray 包括以下属性
ndim：维度
size：element 的数量
shape，数组的维度
dtype：元素的类型
itemsize：每个元素的大小，多少字节
data:包含数组实际元素的区域
'''

##1. 基础创建数组，给它一个list
a = np.array([2,3,4])
print( a, a.dtype ) #自动进行类型检查，默认最接近的类型 int32

a = np.array([2.0,3,4])
print( a, a.dtype ) #自动进行类型检查，默认最接近的类型 float64

### 选能包容的
a = np.array([1,1.0,complex(2,3),np.pi])
print( a, a.dtype ) #complex128

## 也可以给个set，将[] 改成{} 即可，相等的值会去掉 set特性
a = np.array({1,1.0,complex(2,3),np.pi})
print( a, a.dtype,a.itemsize ) #{3.141592653589793, 1, (2+3j)} object 8

## 创建多位数组，比如 3x2 数组，这个与数学书上的数组对应,既是3行2列，
## list 里面包含的element 每个是两个元素
## 注意这个与c#中的概念相同，是真正的多维数组形式用a[3,2]表示
## c# 中还有交错数组 也就是数组的数组
## 与c++的也相同，都表示内存是连续存储的。
## 只是python中包含了多维数组的meta信息，可以变换
a = np.array([(1,2),(3,4),(5,6)])
print( a, a.dtype, a.shape, a.strides )# int32 (3, 2),(8,4)
print( a[2,1],a[2][1]) #2*2+(1) 跟一维数组下标计算近似的。结果是6

##1.1 创建给定类型，因为如果类型不对会报错
### 比如希望int8 生成，不超过限制
a = np.array([2,3,4],dtype=np.int8)
print( a, a.dtype,a.itemsize*a.size ) #自动进行类型检查，默认最接近的类型 int8
### 比如希望类型是complex16,但是默认默认复数保存的float，最小的也是float32，所以只能这样处理了
a = np.array([2,3,4],dtype=np.complex64)
print( a, a.dtype,a.itemsize*a.size ) #int8 3
### 可以自己创建dtype 通知底层创建，但是中间过程要转来转去，不一定好
dt = np.dtype([('real',np.int8),('imag',np.int8)]) #complex64 24
a = np.array([2,3,4],dtype=dt)
print( a, a.dtype,a.itemsize*a.size ) #[('real', 'i1'), ('imag', 'i1')] 6

##2.0 其他形式的创建，除了上面给list，set以外的形式
### 特殊值+指定shape的形式 形式
a = np.zeros(3) #数组全0
print(a, a.dtype )#float64
a = np.zeros((3,2), dtype=np.int8)
print(a, a.dtype )#int8

a = np.ones(3) #数组全1
print(a, a.dtype )#float64
a = np.ones((3,2), dtype=np.int8)
print(a, a.dtype )#int8

### 未初始化数组，且符合type限制
a = np.empty((3,2), dtype=np.int8)
print(a, a.dtype )#int8

### range类似的生成list的形式 arange
a = np.arange(10,dtype=np.int8)
print(a, a.dtype )#[0 1 2 3 4 5 6 7 8 9] int8

a = np.arange(2,5,dtype=np.int8)
print(a, a.dtype )#[2 3 4] int8
##### 与这种写法差不多 可能上面速度快？
a = np.array(range(2,5), dtype=np.int8)
print(a, a.dtype )#[2 3 4] int8
### 指定step的形式,6个数
a = np.arange(20,50,5,dtype=np.int8)
print(a, a.dtype )#[20 25 30 35 40 45] int8

### 注意精度的问题，高精度就linspace 的参数是start，end n
#### note：linspace step = stop-start/n
end = np.pi
num = 5
a = np.arange(0,end, end/5)
b = np.linspace(0,end, num )
#### 可以看到精细程度很大，基本上a没有没有得到1的情况
print( np.sin(a)) #[0.         0.58778525 0.95105652 0.95105652 0.58778525]
print( np.sin(b)) #[0.00000000e+00 7.07106781e-01 1.00000000e+00 7.07106781e-01 1.22464680e-16]

### 几个带like的array生成形式,就是类型近似但是修改了部分信息的新的narray
b = np.empty((4,6),dtype=np.int8)
a = np.zeros_like( b, dtype=np.float16 ) #数组全0
print(a,a.shape,a.dtype )#(4, 6) float16

a = np.ones_like( b, dtype=np.float32 ) #数组全0
print(a,a.shape,a.dtype )#(4, 6) float32

c = np.empty_like( b, dtype=np.float32 ) #数组全0,每次都是相同内容，比较指针 用is
print(c,c.shape,c.dtype  )#(4, 6) float32
print("Content comparison:", a.data == c.data)  # 可能返回 True（内容相同）
print("Address comparison:", a.data.obj is c.data.obj)  # 返回 False

###3. random的形式生成
#### 生成[2.0,5.0)间随机数的narray
rng = np.random.default_rng()
print( rng.random())
a = rng.uniform(2.0,5.0,size=(2,4))
print(a ,a.shape, a.dtype)# (2, 4) float64
#### random 随机形式[0,1.0)
a = rng.random(size=(2,4))
print(a ,a.shape, a.dtype)# (2, 4) float16
#### normal 高斯分布 loc 中间值，scale，宽度，最大方差？ 正数
a = rng.normal(2.0,1.0,size=(2,4))
print(a ,a.shape, a.dtype)# (2, 4) float16

###3. arange的形式生成 + reshape 形式
a = np.arange(10,dtype=np.int8).reshape((5,2))
print(a ,a.shape, a.dtype)# (5, 2) int8


###  还有fromfunction,也就是根据上下文变量生成数组，暂时不做例子，之后补充
### 还有从文件中读取数组，这里一般结合定义dtype的形式一起来处理。之后补充。

### 打印形式，这里要注意reshape 并不只改变打印形式，是改了array的shape
print('修改打印形式--Begin')
a = np.arange( 9, dtype=np.int8)
print( a, a.shape, a.dtype )#[0 1 2 3 4 5 6 7 8] (9,) int8
a = a.reshape((3,3)) # 3行3列
print( a, a.shape, a.dtype )#(3, 3) int8
## reshape 的反向 展平
b = np.ravel(a)
print( b, b.shape, b.dtype )#(3, 3) int8
# np.set_printoptions() 才是不用reshape 改变打印效果的设置感觉比较麻烦。
##### 设置超长的linewidth 就能将多维数组打在一行了::TODO::set_printoptions 有问题，都报错了
##with np.set_printoptions( threshold= sys.maxsize ):
#    print( a, a.shape, a.dtype )#(3, 3) int8

print('End')

## array operator：element operator + - * /
a = np.arange(10) # [0,10)
print( a + 20 )# element = element + 20
print( a - 10 )# element = element  - 10
print( a * 1.2 )# element = element * 1.2
print( a / 1.2 )# element = element / 1.2
print( a // 2 ) # element = element // 2
print( a ** 2 ) # element = element ^ 2
print( a ** 2 % 2 ==1 ) # element = element ^ 2 % 2 ==1

## array operator: += like
a = np.arange(10)  * np.pi / 9
print( np.sin(a) )
a += np.pi ## modify an existing array
print( np.sin(a) )
print( np.sin(a) + np.sin(a + np.pi) )
b = np.pi / len(a)
print( np.sin( (a + 1) * b)) ## element = sin( (element + 1) * pi / element count)
## += *=
rg = np.random.default_rng(10000)
a = np.ones((2,2),dtype=int)
b = rg.random((2,2))
a *= 3
print( 'a=' ,a )
print( 'b=' , b)
b += a
print( 'b+=a',b)
## a += b 会出错。int 转float 会丢失精度的

## e^ia = cos(a) + isin(a)的形式
a = np.ones(3, dtype=np.int8)
b = np. linspace(0, np.pi,3)
c = a + b
print( a.dtype, b.dtype, c.dtype )
d = np.exp(c*1j)
print( d.dtype.name, d)

### array 的统计函数
a = rg.normal(loc= 2, scale= 1, size=(3,3))#中值在2附近，上下+-1
print( a, a.dtype)#float64
print( a.sum(), a.min(), a.max(), a.mean() )
print( a.sum(axis=0), a.min(axis=0), a.max(axis=0), a.mean(axis=0) ) #axis 表示的列
print( a.cumsum( axis=0))

### 验证一下cumsum：cumulative sum along each row
b = np.arange(12).reshape(3,4) #3 行 4 列
### axis=1 表示沿着列，向右，逐步累积和
print( 'b: ', b, '\ncumusum b:', b.cumsum(axis=1) ) # 第一列不变，c_i+=c_{i-1}
### axis=0 表示沿着行，向下 逐步累积和
print( 'b: ', b, '\ncumusum b:', b.cumsum(axis=0) ) # 第一行不变，r_i += r_{i-1}
### axis=None,或者不指定，ravel 展平之后，第一元素不变，e_i += e_{i-1}
print( 'b: ', b, '\ncumusum b:', b.cumsum() ) # 第一元素不变，e_i += e_{i-1}
### ravel + cumsum :np.ravel(b).cumsum(axis=0)  或者不指定axis都可以
print( 'b: ', b, '\ncumusum b:', np.ravel(b).cumsum() ) # 第一元素不变，e_i += e_{i-1}

### matrix use 2x2
A = np.arange( 1,5).reshape(2,2)
B = np.array([[1,1],[0,1]])
print( A,' dot ', B,'=', A * B)
print( A,' cross ', B,'=', A @ B)
print( A,' cross ', B,'=', A.dot(B) ) # cross(A,B)

### Universal functions，常用数学方法，与普通math下的就是这个支持narray做参数
P = np.arange( 1, 20, 4, dtype=np.int8)
P2 = np.linspace( 1, 20, 5, endpoint= False,dtype=np.int8)
print(P, P2)
print(np.exp(P, dtype=np.float32),np.sqrt(P2), np.multiply( P, np.sin(P2))) ## 改exp的dtype是值超出范围了


