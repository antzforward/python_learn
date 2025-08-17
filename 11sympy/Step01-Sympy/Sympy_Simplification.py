from sympy import *
x,y,z = symbols('x y z')
init_printing( use_unicode= True )
## simplify,这就是表达式化简
print( simplify(sin(x)**2 + cos(x)**2) )# 1
print( simplify((x**3 + x**2 - x - 1)/(x**2 + 2*x + 1)) ) # x - 1
print ( simplify(gamma(x)/gamma(x - 2)) )#(x - 2)*(x - 1)
print( latex(gamma(x)/gamma(x - 2)))#\frac{\Gamma\left(x\right)}{\Gamma\left(x - 2\right)}
print( simplify( x**2 + 2*x + 1)) #x**2 + 2*x + 1 展开expand
print( factor(x**2 + 2*x + 1)) #(x+1)**2 组合factor
print( expand((x+1)**2)) #x**2 + 2*x + 1
print( expand((x - 2)*(x - 1))) #x**2 - 3*x + 2
print( expand((x + 1)*(x - 2) - (x - 1)*x) )

## collect,将多项式展示成主参数的多项式
expr = x*y + x - 3 + 2*x**2 - z*x**2 + x**3
print( expr ) #x**3 - x**2*z + 2*x**2 + x*y + x - 3
print( factor( expr )) # 没有任何动作，因为是多变量，以哪个为主
#要用到collect来指向
print( collect(expr, x)) #指向x为主参数 #x**3 + x**2*(2 - z) + x*(y + 1) - 3
print(factor( collect(expr, x) )) #无用的写法
# 如果在指向主参数的n阶的系数 coeff的形式
print( collect(expr,x).coeff(x, 2)) #2-z

## cancel，多项式除法做化简,简单形式的分式
expr = (x**2 + 2*x + 1)/(x**2 + x)
print( expr )
print( cancel( expr )) #(x + 1)/x
expr = 1/x + (3*x/2 - 2)/(x - 4)
print( cancel(expr)) #(3*x**2 - 2*x - 8)/(2*x**2 - 8*x)

expr = (x*y**2 - 2*x*y*z + x*z**2 + y**2 - 2*y*z + z**2)/(x**2 - 1)
print(cancel(expr))#(y**2 - 2*y*z + z**2)/(x - 1)
## 将分母分子形式分解成分子表达式相加的形式 在积分中情况下很有用。
### 这里叫apart() performs a partial fraction decomposition on a rational function.
expr = (4*x**3 + 21*x**2 + 10*x + 12)/(x**4 + 5*x**3 + 5*x**2 + 4*x)
print( apart( expr ))#(2*x - 1)/(x**2 + x + 1) - 1/(x + 4) + 3/x


## 三角函数的部分
"""
cos(acos(x)) = x 是反函数的基本性质，在定义域内必然成立。
acos(cos(x)) ≠ x  是函数多值性的结果，Sympy 为保持数学严谨性不自动简化（除非限制 x ∈ [0, π]）。
"""
expr = cos(x)
print(f"{expr} {acos(expr)} {cos(acos(x)).simplify()} {asin(1)}")#cos(x) acos(cos(x)) x pi/2
x1 = symbols('x1',real=True,finite=True)
print(f"{expr} {acos(cos(x1)).simplify()} {cos(acos(x))} {asin(1)}")#cos(x) acos(cos(x)) x pi/2
x2 = symbols('x2', real = True, finite=True,domain=Interval(0,pi))
#acos(cos(x2)) acos(cos(x2)) acos(cos(x2)) pi/2
print(f"{acos(cos(x2)).trigsimp()} {acos(cos(x2)).simplify()} {acos(cos(x2)).refine()} {acos(cos(pi/2))}")
## 先创建 再简化，如果这样是真的，这个逻辑就有问题了
expr2 = acos(cos(x2))
trig_expr2 = trigsimp(expr2)
print(f"{trig_expr2} {simplify(expr2)} {refine(expr2)} {acos(cos(pi/2))}")
# 以上都不是了，不能简化也没关系，这种 也没多大问题吧。

## 恒等式来看看
print(trigsimp(sin(x)**2+cos(x)**2)) #1
print(trigsimp(sin(x)*tan(x)/sec(x))) #sin(x)**2
print(trigsimp(cosh(x)**2 + sinh(x)**2))#cosh(2*x)
print(expand_trig(sin(x + y)))#sin(x)*cos(y) + sin(y)*cos(x)

## 试试三角函数的加法形式,加法减法很好替换就不做了减法了
print(expand_trig(cos(x + y)))#-sin(x)*sin(y) + cos(x)*cos(y)
print(expand_trig(tan(x + y)))#(tan(x) + tan(y))/(-tan(x)*tan(y) + 1)

## 半角替换，倍角替换这些能表现出来吗？
print(trigsimp(1-2*sin(x)**2)) #cos(2*x)
print(trigsimp(-1+2*cos(x)**2)) #cos(2*x)
print(expand_trig(cos(3*x)))#4*cos(x)**3 - 3*cos(x)
print(trigsimp(sin(x)+cos(x)))#sqrt(2)*sin(x + pi/4) 这个代表应该是可以的
print(expand_trig(tan(2*x)))#2*tan(x)/(1 - tan(x)**2)
## 半角正切替换
print(sin(x).rewrite(tan))#2*tan(x/2)/(tan(x/2)**2 + 1)
print(cos(x).rewrite(tan))#(1 - tan(x/2)**2)/(tan(x/2)**2 + 1)
print(tan(x).rewrite(tan))#tan(x) 想要半角替换要麻烦一点
# tan 用sin/cos 表示,其实还有更简单的就是直接把tan(2*x) 展开，然后用x/2替代x就可以了
#2*tan(x/2)/(1 - tan(x/2)**2)
print((sin(x).rewrite(tan)/cos(x).rewrite(tan)))#加上simplify或者trigsimp就退回到tan(x) 不加就对了

### 用变元法或者换元法还有一类是自定义变元规则的 这个就不是解题的范围问题了
## 下次再学习一下，感觉还是一种思路，嗯 秒的。
x, t = symbols('x t')

# 1. 定义半角替换公式
half_angle_subs = {
    sin(x): 2*t/(1 + t**2),       # sin(x) = 2t/(1+t²)
    cos(x): (1 - t**2)/(1 + t**2), # cos(x) = (1-t²)/(1+t²)
    tan(x): 2*t/(1 - t**2)         # tan(x) = 2t/(1-t²) [需要单独处理!]
}


# 2. 同时处理 tan 函数的高级方法
def half_angle_replace(expr, t_var):
    """执行完整的正切半角替换"""
    # 先处理 tan(x) 的替换
    expr = expr.replace(tan(x), 2 * t_var / (1 - t_var ** 2))

    # 再处理 sin(x) 和 cos(x)
    expr = expr.rewrite(tan).subs(tan(x / 2), t_var)

    # 化简结果
    return expr.simplify()

# 使用示例 =====================================

# 示例 1: 单独处理 tan(x)
expr_tan = tan(x)
result_tan = expr_tan.subs(half_angle_subs)  # 得到 2*t/(1 - t**2)

# 示例 2: 混合三角函数表达式
expr_mixed = sin(x) + cos(x)*tan(x)
result_mixed = expr_mixed.subs(half_angle_subs).simplify()

# 示例 3: 使用高级函数处理
expr_complex = tan(x)/(sin(x) + cos(x))
result_complex = half_angle_replace(expr_complex, t)

print("tan(x) 替换结果:", result_tan)#tan(x) 替换结果: 2*t/(1 - t**2)
print("混合表达式结果:", result_mixed)#混合表达式结果: 4*t/(t**2 + 1)
print("高级函数处理结果:", result_complex)#高级函数处理结果: -2*t*(t**2 + 1)/((t**2 - 1)*(-t**2 + 2*t + 1))