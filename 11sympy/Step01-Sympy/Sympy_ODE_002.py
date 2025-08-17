from sympy import  *
y = Function('y')
t = symbols('t')
print(dsolve(Eq(y(t).diff(t) - y(t),exp(t)),y(t))) #Eq(y(t), (C1 + t)*exp(t))
print(dsolve(Eq(y(t).diff(t,t) - y(t),cos(t)),y(t))) #Eq(y(t), C1*exp(-t) + C2*exp(t) - cos(t)/2)

#y'+y=0,y(3)=2 求y
general_solution = dsolve(Eq(y(t).diff(t)+y(t),0),y(t),ics={y(3):2})
print(f'y(t)={general_solution.rhs}')
print(f"y''+4y=0,y(0)=0,y'(0)=1,y(t)={dsolve(Eq(y(t).diff(t,2)+4*y(t),0),y(t),ics={y(0):0,y(t).diff(t).subs(t,0):1}).rhs}")
print(f"y''+4y=0,y(pi/8)=0,y(pi/6)=1,y(t)={dsolve(Eq(y(t).diff(t,2)+4*y(t),0),y(t),ics={y(pi/8):0,y(pi/6):1}).rhs}")
x = symbols('x')
#曲线切线斜率是横坐标的2倍，过P(3,4) 求曲线
print(f"y'(x)=2*x,y(3)=4,y(x)={dsolve(Eq(y(x).diff(x),2*x),y(x),ics={y(3):4}).rhs}")
## 曲线任一点的切线，切点到原点向径以及x轴可以围成一个等腰三角形（以x轴为底）且过点P（1，2）
solutions = dsolve(Eq(sqrt(x**2+y(x)**2),sqrt((y(x)/y(x).diff(x))**2+y(x)**2)),y(x),ics={y(1):2})
def solutionsStr( solution ):
    if isinstance( solutions, list):
        ret = f"方程有多重解"
        for i, sol in enumerate(solution):
            ret +=f"\n解 {i}: {sol.rhs}"
        return ret
    else:
        return f"方程的解: {solutions.rhs}"
print(f"sqrt(x**2+y(x)**2)=sqrt((y(x)/y'(x))**2+y(x)**2),y(1)=2 "
      f"{solutionsStr(dsolve(Eq(sqrt(x**2+y(x)**2),sqrt((y(x)/y(x).diff(x))**2+y(x)**2)),y(x),ics={y(1):2}))}")