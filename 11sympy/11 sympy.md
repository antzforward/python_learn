### **SymPy 学习路径：从符号计算到微分几何**

**核心学习理念：** **“探索、操作、可视化”**。对每个数学概念，我们都将用 SymPy 定义它，对其进行符号操作（化简、求导、积分），并尽可能将其可视化，从而获得代数和几何的双重直觉。

**环境准备：** 确保安装 `sympy`、`matplotlib` 和 `numpy`。对于 3D 可视化，`plotly` 或 `k3d` 库能提供更好的交互体验。

---

#### **第一部分：SymPy 核心基础**

##### **第 1 章：符号、表达式与基本化简**
*   **学习目标：** 掌握 SymPy 最基本的概念：符号、表达式和基本操作。
*   **核心内容：**
    *   使用 `symbols()`, `var()` 定义符号。
    *   构建表达式（算术、多项式、三角函数）。
    *   使用 `simplify()`, `expand()`, `factor()`, `collect()`, `together()`, `apart()` 等函数操作表达式。
*   **示例代码：**
    ```python
    from sympy import symbols, simplify, expand, factor, sqrt, sin, cos
    x, y, a, b = symbols('x y a b')
    expr = (x + 1)**2 + (x - 2)**3
    print("原始表达式:", expr)
    print("展开:", expand(expr))
    print("因式分解:", factor(expand(expr)))
    # 三角恒等式
    trig_expr = sin(x)**2 + cos(x)**2
    print("三角表达式简化:", simplify(trig_expr))
    ```
*   **习题：**
    1.  定义符号 `x` 和 `y`，创建表达式 `(x + y)^3 - x*(x - y)^2`，先展开再因式分解。
    2.  验证双曲函数恒等式 `cosh(x)^2 - sinh(x)^2 = 1`。

##### **第 2 章：方程求解**
*   **学习目标：** 学习使用 SymPy 求解代数方程和方程组。
*   **核心内容：**
    *   使用 `solveset()` 或 `solve()` 求解方程。
    *   求解线性方程组。
    *   处理不等式。
*   **示例代码：**
    ```python
    from sympy import solveset, Eq, solve, linsolve
    # 求解单个方程
    sol = solveset(x**2 - 3*x + 2, x, domain=S.Reals)
    print("方程 x^2 - 3x + 2 = 0 的解:", sol)

    # 使用 Eq 对象定义方程
    eq1 = Eq(x + 2*y, 5)
    eq2 = Eq(3*x - y, 1)
    print("方程组的解:", solve((eq1, eq2), (x, y)))
    # 或者使用 linsolve
    print("线性方程组的解:", linsolve((eq1, eq2), (x, y)))
    ```
*   **习题：**
    1.  求解方程 `e^x = 5`（提示：需要从 `sympy` 导入 `E` 或 `exp`）。
    2.  求解方程组 `{ x^2 + y = 2, x - y = 4 }`。

---

#### **第二部分：微积分（Calculus）**

##### **第 3 章：极限与级数**
*   **学习目标：** 用 SymPy 计算极限和级数展开。
*   **核心内容：**
    *   使用 `limit()` 计算极限。
    *   使用 `series()` 进行泰勒级数展开。
    *   使用 `summation()` 进行求和。
*   **示例代码：**
    ```python
    from sympy import limit, sin, oo, series, summation
    # 计算极限
    print("lim(x->0) sin(x)/x =", limit(sin(x)/x, x, 0))
    print("lim(x->oo) (1 + 1/x)^x =", limit((1 + 1/x)**x, x, oo)) # oo 表示无穷大

    # 泰勒级数展开
    print("sin(x) 在 x=0 处的 6 阶展开:", series(sin(x), x, 0, 7).removeO()) # removeO() 移除余项

    # 求和
    n = symbols('n')
    print("Sum_{n=1}^m n^2 =", summation(n**2, (n, 1, 10))) # 计算具体值
    print("Sum_{n=1}^m n^2 =", summation(n**2, (n, 1, m)))   # 得到符号表达式
    ```
*   **习题：**
    1.  计算极限 `lim(x->0) (1 - cos(x))/x^2`。
    2.  求 `cos(x)` 在 `x=pi` 处的 4 阶泰勒展开式。

##### **第 4 章：微分（Differentiation）**
*   **学习目标：** 掌握符号微分和求偏导数。
*   **核心内容：**
    *   使用 `diff()` 函数求导。
    *   计算高阶导数。
    *   计算多元函数的偏导数。
*   **示例代码：**
    ```python
    from sympy import diff, exp, log
    # 一阶导数
    f = x**3 + sin(x)
    deriv = diff(f, x)
    print("f'(x) =", deriv)

    # 高阶导数
    second_deriv = diff(f, x, 2) # 等价于 diff(diff(f, x), x)
    print("f''(x) =", second_deriv)

    # 多元函数偏导
    f_multi = x**2 * y + y * log(x)
    partial_x = diff(f_multi, x)
    partial_y = diff(f_multi, y)
    print("∂f/∂x =", partial_x)
    print("∂f/∂y =", partial_y)
    # 混合偏导
    partial_xy = diff(f_multi, x, y)
    print("∂²f/∂x∂y =", partial_xy)
    ```
*   **习题：**
    1.  求 `f(x) = x * ln(x)` 的二阶导数。
    2.  对于函数 `f(x, y) = e^(x*y) + x*y`，验证 `∂²f/∂x∂y = ∂²f/∂y∂x`。

##### **第 5 章：积分（Integration）**
*   **学习目标：** 学习使用 SymPy 进行符号积分和数值积分。
*   **核心内容：**
    *   使用 `integrate()` 计算不定积分和定积分。
    *   计算多重积分。
    *   处理特殊函数和数值积分。
*   **示例代码：**
    ```python
    from sympy import integrate, exp
    # 不定积分
    f = cos(x)
    integral_f = integrate(f, x)
    print("∫cos(x) dx =", integral_f)

    # 定积分
    definite_int = integrate(exp(-x), (x, 0, oo))
    print("∫(0 to ∞) e^-x dx =", definite_int)

    # 双重积分
    double_int = integrate(x*y, (x, 0, 1), (y, 0, x)) # ∫∫ xy dy dx, y from 0 to x, x from 0 to 1
    print("双重积分结果:", double_int)
    ```
*   **习题：**
    1.  计算 `∫(1 / (x^2 + 1)) dx`。
    2.  计算 `∫∫(x * sin(y)) dy dx`，其中 `y` 从 `0` 到 `x^2`，`x` 从 `0` 到 `1`。

---

#### **第三部分：解析几何与可视化**

##### **第 6 章：二维几何与绘图**
*   **学习目标：** 用 SymPy 的几何模块定义几何对象并绘制二维图形。
*   **核心内容：**
    *   使用 `Point`, `Line`, `Segment`, `Circle`, `Triangle` 等类。
    *   计算交点、距离、切线等。
    *   使用 `plot()` 和 `plot_implicit()` 绘制函数和隐式方程图像。
*   **示例代码：**
    ```python
    from sympy import Point, Line, Circle, plot, plot_implicit, Eq
    # 定义点和几何对象
    p1, p2 = Point(0, 0), Point(3, 4)
    line = Line(p1, p2)
    circle = Circle(p1, 5)

    # 计算属性
    print("两点距离:", p1.distance(p2))
    print("线的斜率:", line.slope)
    print("线与圆的交点:", intersection = circle.intersection(line))

    # 绘图
    p = plot(line.equation(), (x, -5, 5), show=False) # 画线
    p.extend(plot(circle.equation(), (x, -6, 6), show=False)) # 画圆
    p.show()

    # 绘制隐式方程
    plot_implicit(Eq(x**2 + y**2, 25), (x, -6, 6), (y, -6, 6)) # 另一种画圆的方式
    ```
*   **习题：**
    1.  定义一个点 `(1, 2)` 和一个圆 `x^2 + y^2 = 25`，判断点的位置（圆内、圆上、圆外）。
    2.  绘制双曲线 `x^2 / 4 - y^2 / 9 = 1` 的图像。

##### **第 7 章：三维几何与绘图**
*   **学习目标：** 将几何概念扩展到三维空间并进行可视化。
*   **核心内容：**
    *   使用 `Point3D`, `Line3D`, `Plane`。
    *   使用 `plot3d()` 和 `plot3d_parametric_line()` 绘制三维曲面和曲线。
*   **示例代码：**
    ```python
    from sympy import Point3D, Line3D, Plane, plot3d, cos, sin
    from sympy.abc import u, v
    # 定义3D对象
    point_a = Point3D(1, 2, 3)
    point_b = Point3D(4, 6, 9)
    line_3d = Line3D(point_a, point_b)
    plane = Plane(Point3D(0, 0, 0), normal_vector=(1, 1, 1))

    print("直线的方向向量:", line_3d.direction_ratio)
    print("点到平面的距离:", plane.distance(point_a))

    # 绘制参数曲面 (例如：球面)
    plot3d(
        sin(u)*cos(v), sin(u)*sin(v), cos(u), # 参数方程
        (u, 0, 3.1416), (v, 0, 2*3.1416),     # 参数范围
        title="Sphere", xlabel='x', ylabel='y'
    )
    ```
*   **习题：**
    1.  求点 `(1, 2, 3)` 到平面 `2x - y + 3z = 5` 的距离。
    2.  绘制一个旋转抛物面 `z = x^2 + y^2` 的图像。

---

#### **第四部分：微分几何（Differential Geometry）**

##### **第 8 章：参数曲线**
*   **学习目标：** 用 SymPy 分析和可视化参数曲线，计算曲率和挠率。
*   **核心内容：**
    *   定义参数曲线 `r(t) = (x(t), y(t), z(t))`。
    *   计算切向量、法向量、副法向量。
    *   计算曲率 `κ(t)` 和挠率 `τ(t)`。
*   **示例代码（分析螺旋线）：**
    ```python
    from sympy import symbols, sin, cos, sqrt, simplify, diff
    from sympy.vector import CoordSys3D, express
    t = symbols('t', real=True)
    # 定义螺旋线: r(t) = (cos(t), sin(t), t)
    x_t = cos(t)
    y_t = sin(t)
    z_t = t

    # 计算一阶导（切向量 T）
    r_prime = [diff(x_t, t), diff(y_t, t), diff(z_t, t)]
    # 计算二阶导
    r_double_prime = [diff(coord, t, 2) for coord in [x_t, y_t, z_t]]

    # 计算曲率公式: κ = |r' × r''| / |r'|^3
    # 需要计算叉积的模长
    # ... (具体实现需要用到叉积公式和模长公式)

    # 使用 SymPy 的向量模块可能更简单
    N = CoordSys3D('N')
    r_vec = cos(t)*N.i + sin(t)*N.j + t*N.k
    v_vec = diff(r_vec, t) # 速度向量 (切向量)
    a_vec = diff(v_vec, t) # 加速度向量

    # 曲率计算
    speed = v_vec.magnitude()
    curvature = (v_vec.cross(a_vec)).magnitude() / speed**3
    print("曲率 κ(t):", simplify(curvature))
    ```
*   **习题：**
    1.  对圆的参数方程 `(cos(t), sin(t), 0)` 计算其曲率，并验证是否为常数 `1/R`。
    2.  绘制一条新参数曲线（如 `(t, t^2, t^3)`）并计算其在 `t=1` 处的切向量。

##### **第 9 章：参数曲面**
*   **学习目标：** 分析参数曲面，计算第一基本形式（度量）和第二基本形式。
*   **核心内容：**
    *   定义参数曲面 `r(u, v)`。
    *   计算切向量 `r_u`, `r_v` 和法向量 `N`。
    *   计算第一基本形式系数 `E, F, G` 和第二基本形式系数 `L, M, N`。
    *   计算高斯曲率 `K` 和平均曲率 `H`。
*   **示例代码（分析单位球面）：**
    ```python
    from sympy import symbols, sin, cos, simplify, Matrix
    u, v = symbols('u v')
    # 球面参数方程
    x_uv = sin(u)*cos(v)
    y_uv = sin(u)*sin(v)
    z_uv = cos(u)

    # 计算偏导向量 r_u 和 r_v
    r_u = [diff(x_uv, u), diff(y_uv, u), diff(z_uv, u)]
    r_v = [diff(x_uv, v), diff(y_uv, v), diff(z_uv, v)]

    # 计算法向量 N = (r_u × r_v) / |r_u × r_v|
    # ... (实现叉积和归一化)

    # 计算第一基本形式 E = r_u · r_u, F = r_u · r_v, G = r_v · r_v
    E = sum([comp**2 for comp in r_u]) # r_u · r_u
    F = sum([a*b for a, b in zip(r_u, r_v)]) # r_u · r_v
    G = sum([comp**2 for comp in r_v]) # r_v · r_v
    print("第一基本形式系数 E, F, G:")
    print(simplify(E), simplify(F), simplify(G))

    # 第二基本形式计算需要二阶偏导和法向量点积，略复杂但模式类似
    ```
*   **习题：**
    1.  计算旋转抛物面 `(u*cos(v), u*sin(v), u^2)` 的第一基本形式。
    2.  （挑战）尝试计算单位球面的高斯曲率，并验证其是否为常数 `1`。

---

#### **第五部分：综合应用与项目**

##### **第 10 章：小型研究项目**
*   **学习目标：** 综合运用所学知识解决一个稍复杂的问题。
*   **项目建议：**
    1.  **最速降线问题：** 用变分法推导并验证最速降线是摆线。使用 SymPy 进行符号推导，并绘制摆线与直线、圆弧等路径进行比较。
    2.  **曲面分类：** 选择几种经典曲面（球面、圆柱面、马鞍面、环面），计算它们的高斯曲率和平均曲率，并可视化它们的形状和曲率分布。
    3.  **符号计算器：** 编写一个简单的命令行程序，可以解析用户输入的数学表达式（如 `“diff(sin(x^2), x)”`）并返回结果。

---

**给学习者的最终建议：**

1.  **文档是你的朋友：** SymPy 官方文档非常出色，遇到任何函数或概念，请优先查阅。
2.  **可视化是关键：** 不要只满足于符号推导的结果。养成习惯，将关键的曲线、曲面、向量场绘制出来，这能极大地加深你的理解。
3.  **从特殊到一般：** 当你学习一个新的微分几何概念时（如曲率），先用 SymPy 计算一个你最熟悉的例子（如圆、球面），看看结果是否符合你的几何直觉，然后再推广到更一般的案例。
4.  **动手实现公式：** 虽然可能有现成的函数，但亲手用 SymPy 的基本操作（`diff`, `integrate`, 叉积、点积）来实现微分几何中的公式（曲率、第一基本形式等）是无可替代的学习过程。

这个路径将带你从 SymPy 的基础一直走到微分几何的门口，并通过强大的可视化能力将抽象的数学概念具象化。祝你学习愉快，享受符号计算与数学可视化的魅力！