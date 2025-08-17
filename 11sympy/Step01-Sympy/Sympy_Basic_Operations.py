import numpy as np
from sympy import *
x, y, z = symbols('x y z')
expr = cos(x) + 1
print( expr.subs(x,y))
print( expr.subs(x,0))
expr = x**y
print( expr.subs(y, x**y))
print( expr.subs(y, x**x))

expr = sin(2*x) + cos(2*x)
print(expand_trig(expr))#2*sin(x)*cos(x) + 2*cos(x)**2 - 1

#expr immutable
print( expr.subs(x,0) is expr ) #False 不是同一个对象

# 多个参数的情况
expr = x**3+4*y**2+z
print( expr.subs([(x,0),(y,1),(z,2)])) #6
print( expr.subs([(x,0),(y,1)])) #z + 4

# str to expr
sz_expr = 'x**3+4*y**2+z'
expr = sympify( sz_expr ) #等同于eval
print( expr.subs([(x,0),(y,1),(z,2)])) #6

## evalf 计算浮点数，默认是符号表示
print(pi.evalf(10)) #3.141592654
print(pi) #pi
print(sqrt(8)) #2*sqrt(2)
print(sqrt(8).evalf(10))#2.828427125
expr = cos(2*x)
print(expr.evalf(subs={x: 2.4}))#0.0874989834394464
one = cos(1)**2 + sin(1)**2
print((one - 1).evalf())#-0.e-124
print((one - 1).evalf(chop=True)) #0

## lambdaify,用subs或者evalf求值，在多参数求值的时候，比如用numpy生成array
import numpy
# 精确等分且排除结束值：np.linspace(0, 1, 10, endpoint=False)
# 简单步长控制：np.arange(0, 1, 0.1)（注意浮点精度）
a = numpy.arange(0,1,0.1) #numpy.linspace(0,1,10)
expr = sin(x)
f = lambdify(x, expr, "numpy") #看来是用numpy指向的类型
#[0.         0.09983342 0.19866933 0.29552021 0.38941834 0.47942554
#  0.56464247 0.64421769 0.71735609 0.78332691]
print( f(a) )
b = [i*0.1 for i in range(0,10)]
f = lambdify(x, expr, "math")
print( [f(i) for i in b] )  # 0.09983341664682815  注意lambdify 和evalf 二选一,

## 或者自己定义一个函数来处理部分函数
import math
def myApproxSin(x):
    if x< 0.1:
        return x
    return round(math.sin(x),9)

a = [i*0.01 for i in range(10)]
a.extend( [round(i*0.1,1) for i in range(1,11)])
# {functionName: function}
f = lambdify(x, expr, {"sin":myApproxSin}) # 自己实现函数 lambdify指向sin到自己的函数里面
#[0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09,
# 0.099833417, 0.198669331, 0.295520207, 0.389418342, 0.479425539,
# 0.564642473, 0.644217687, 0.717356091, 0.78332691, 0.841470985]
print( [f(i) for i in a] )