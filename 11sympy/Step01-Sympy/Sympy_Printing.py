# 多种 printer
# 确实适合写ppt啊
### 1. str
### 2. srepr
### 3. ASCII pretty printer
### 4. Unicode pretty printer
### 5. LaTeX
### 6. MathML
### 7. Dot 这个不太熟悉

from sympy import init_printing
print(init_printing())

from sympy import init_session
#print( init_session()) #进入交互环境，这个时候会有正确的输出形式
"""
Python 3.12.3 | packaged by conda-forge | (main, Apr 15 2024, 18:20:11) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(SymPyConsole)
Python console for SymPy 1.13.1 (Python 3.12.3-64-bit) (ground types: python)

These commands were executed:
>>> from sympy import *
>>> x, y, z, t = symbols('x y z t')
>>> k, m, n = symbols('k m n', integer=True)
>>> f, g, h = symbols('f g h', cls=Function)
>>> init_printing()
"""

from sympy import *
x, y, z = symbols('x y z')
init_printing()
expr = Integral(sqrt(1/x),x)
print( expr )
#To get a string form of an expression, use str(expr)
print( str( expr ) ) #Integral(sqrt(1/x), x)
# The srepr form of an expression is designed to show the exact form of an expression.
print( srepr( expr ) )#Integral(Pow(Pow(Symbol('x'), Integer(-1)), Rational(1, 2)), Tuple(Symbol('x')))
pprint( expr, use_unicode=False ) # 与init_session()后的状态差不多
print( pretty(expr, use_unicode=False ) ) # 等同了 pprint( expr, use_unicode=False )
print( latex(expr) ) #\int \sqrt{\frac{1}{x}}\, dx
print_mathml( expr ) # 生成了近似xml的方案
# print_maple_code( expr ) #这个需要按照了maple才能正常使用

from sympy.printing.dot import dotprint
from sympy.abc import x
print(dotprint(x+2)) # 我应该设置了digraph了。这个dot可以成为所有node-based 的中间文件了。