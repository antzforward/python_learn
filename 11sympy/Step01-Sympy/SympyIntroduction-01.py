import math
print( math.sqrt(9)) #3.0
print( math.sqrt(8)) #2.8284271247461903

import sympy
print( sympy.sqrt(9)) #3
print( sympy.sqrt(8)) #2*sqrt(2)

from sympy import  symbols
x,y = symbols('x y')
expr = x + 2 * y
print( expr ) #x + 2*y
print( expr + 1 ) #x + 2*y + 1
print( expr - x ) #2*y
print( x*expr ) #x*(x + 2*y)

# 展开公式，将组合乘法表示为加法 expand，将加法表示组合乘法，factor
# 对应的反操作
from sympy import expand,factor
print( expand(x*expr)) #x**2 + 2*x*y
print( factor(expand(x*expr))) #x*(x + 2*y)

##尝试没有改变print 格式的情况下，表现数学的公式，感觉这个很难得
## 引入所有得公式吧
from sympy import  *
expr2 = diff(sin(x)*exp(x),x)
print( expr2 ) #exp(x)*sin(x) + exp(x)*cos(x) #这是代码形式的
# 要转成Latex的形式
init_printing(use_unicode=True) # 为什么不是use_latex?=> 在这个时候设置是无效的。
print( integrate(expr2,x) )
# oo 定义为无穷大了
print( integrate( sin(x**2),(x,-oo,+oo))) #sqrt(2)*sqrt(pi)/2
## 变量驱动的问题
print( limit( sin(x)/x, x, 0)) #1
## 求解f(x)=0的形式
print( solve(x**2-2,x)) #[-sqrt(2), sqrt(2)]
## 求解ODE的函数普通解
## 定义函数
y = Function('y')
t = symbols('t')
## ODE 等式 Eq表示等式，先出现的是左边y''-y右边为e^t,求y(t) 的普通解
print(dsolve(Eq(y(t).diff(t,t) - y(t),exp(t)),y(t))) #Eq(y(t), C2*exp(-t) + (C1 + t/2)*exp(t))
## 求矩阵的特征值 即Mr=r 然后变成M'r=0 从而|M|=0 从经典的[[1,2],[2,2]]
print(Matrix([[1,2],[2,2]]).eigenvals()) ##{3/2 - sqrt(17)/2: 1, 3/2 + sqrt(17)/2: 1}
## 用factor 改一下格式,看起来好一点？？
print(factor(Matrix([[1,2],[2,2]]).eigenvals())) #{-(-3 + sqrt(17))/2: 1, (3 + sqrt(17))/2: 1}
## 将公式用latex表现一下,直接沾出来可以被latexlive识别，不错的方式哦
print(latex(Integral(cos(x)**2, (x, 0, pi)))) #\int\limits_{0}^{\pi} \cos^{2}{\left(x \right)}\, dx