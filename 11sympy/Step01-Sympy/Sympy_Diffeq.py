from sympy import  *
y,x,a = symbols('y,x,a')

y = x**2*cos(a*x)
print(expand(y.diff(x,50)))
y = sqrt(1+sin(x))
print(Integral(sqrt(1+sin(x)),x).doit())

integ = Integral(sin(x**2), x)
print( integ.doit() )