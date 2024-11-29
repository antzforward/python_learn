import numpy as np
x = np.array([1, 2, 3])
print( x ) # array([1, 2, 3])

print(x[1:]) #array([2, 3])
print( x[2] ) #3

print( x*2) # array([2, 4, 6])
print( x**2) # array([1, 4, 9])

l = [1, 2, 3]
print([2*li for li in l])#[2, 4, 6]
print( l*2 ) #[1, 2, 3, 1, 2, 3]
# print( l**2 ) #不支持，其实从上面就知道了
print([li**2 for li in l])#[1, 4, 9]

a = np.array([1, 2, 3])
b = np.array([3, 2, 1])
print(a + b ) # array([4, 4, 4]) 逐项相加
# print(a + np.array([1,2])) #如果shape不同,出现ValueError
#对比Array基本形式
print([1, 2, 3] + [3, 2, 1]) #类似append操作 [1, 2, 3, 3, 2, 1]

M = np.array([[1, 2, 3], [4, 5, 6]])
print( M[1,2]) #6,第1+1行，第2+1列 数字 6
print( M.shape ) #(2,3)

# Python 默认不支持int[,] (c#中的同等类型）
N=[[1, 2, 3], [4, 5, 6]]
print( N[1][2] )#6,第1+1行，第2+1列 数字 6
print(f"({len(N)},{len(N[0])})")

# 生成1维数组，用range的方式，注意现在不一定是实例话的
c = range(6)
print( c )#range(0, 6)
c = list(range(6))
print( c ) #[0, 1, 2, 3, 4, 5]
c =  np.arange(6)
print( c ) #[0 1 2 3 4 5]