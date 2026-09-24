import turtle
import math

# ======================== 全局设置 ========================
turtle.setup(900, 900)
turtle.tracer(0)
turtle.hideturtle()
turtle.bgcolor("white")

# 画笔：黑色细线，适合涂色
pen = turtle.Turtle()
pen.speed(0)
pen.pensize(1.5)
pen.color("black")
pen.fillcolor("white")  # 涂色书要白色填充


# ======================== 工具函数 ========================
def draw_petal(radius, angle=60):
    """绘制一个标准花瓣（两段弧线）"""
    pen.begin_fill()
    pen.circle(radius, angle)
    pen.left(180 - angle)
    pen.circle(radius, angle)
    pen.left(180 - angle)
    pen.end_fill()


def draw_leaf(radius, angle=45):
    """绘制尖叶（更尖锐的花瓣）"""
    pen.begin_fill()
    pen.circle(radius, angle)
    pen.left(90 + angle / 2)
    pen.circle(radius * 1.2, angle)
    pen.left(90 + angle / 2)
    pen.end_fill()


def draw_circle_dots(radius, count):
    """在指定半径的圆上均匀放置小圆点"""
    for i in range(count):
        pen.penup()
        pen.goto(0, -radius)
        pen.setheading(90 + i * (360 / count))
        pen.forward(radius)
        pen.pendown()
        pen.circle(3)  # 小点
        pen.penup()


def draw_ring(radius, thickness=10):
    """画一个空心圆环（只画轮廓）"""
    pen.penup()
    pen.goto(0, -radius)
    pen.pendown()
    pen.circle(radius)


# ============================================================
#  曼荼罗 ① ：经典莲花（12瓣对称）
# ============================================================
def mandala_lotus():
    pen.clear()
    # 内层小花瓣（密）
    for i in range(16):
        pen.penup()
        pen.goto(0, 0)
        pen.setheading(i * (360 / 16))
        pen.forward(30)
        pen.pendown()
        draw_petal(60, 50)
    # 外层大花瓣（疏）
    for i in range(12):
        pen.penup()
        pen.goto(0, 0)
        pen.setheading(i * (360 / 12) + 15)
        pen.forward(20)
        pen.pendown()
        draw_petal(120, 55)
    # 最外层装饰弧线
    for i in range(24):
        pen.penup()
        pen.goto(0, 0)
        pen.setheading(i * (360 / 24))
        pen.forward(180)
        pen.pendown()
        pen.circle(25, 80)
    # 中心圆点
    draw_circle_dots(30, 12)
    draw_ring(200, 2)
    draw_ring(140, 2)
    draw_ring(80, 2)


# ============================================================
#  曼荼罗 ② ：星爆锯齿（尖锐几何感）
# ============================================================
def mandala_starburst():
    pen.clear()
    # 内层星形
    for i in range(20):
        pen.penup()
        pen.goto(0, 0)
        pen.setheading(i * (360 / 20))
        pen.forward(30)
        pen.pendown()
        draw_leaf(80, 30)
    # 中间锯齿环（三角形尖刺）
    for i in range(24):
        pen.penup()
        pen.goto(0, 0)
        pen.setheading(i * (360 / 24))
        pen.forward(110)
        pen.pendown()
        pen.left(30)
        for _ in range(3):
            pen.forward(20)
            pen.right(120)
        pen.right(30)
    # 外层长尖刺
    for i in range(16):
        pen.penup()
        pen.goto(0, 0)
        pen.setheading(i * (360 / 16) + 5)
        pen.forward(150)
        pen.pendown()
        pen.left(20)
        pen.forward(35)
        pen.backward(35)
        pen.right(40)
        pen.forward(35)
        pen.backward(35)
        pen.left(20)
    # 圆点边界
    draw_circle_dots(220, 32)
    draw_circle_dots(170, 28)
    draw_ring(260, 2)


# ============================================================
#  曼荼罗 ③ ：繁花（曲线重叠）
# ============================================================
def mandala_flower():
    pen.clear()
    # 基础圆环
    draw_ring(250)
    draw_ring(180)
    draw_ring(100)

    # 波浪曲线（非标准花瓣）
    for i in range(18):
        pen.penup()
        pen.goto(0, 0)
        pen.setheading(i * (360 / 18))
        pen.forward(60)
        pen.pendown()
        for j in range(6):
            pen.circle(40, 60)
            pen.right(120)
    # 外圈扭曲花瓣（打破正多边形对称感）
    for i in range(14):
        pen.penup()
        pen.goto(0, 0)
        pen.setheading(i * (360 / 14) + 10)
        pen.forward(200)
        pen.pendown()
        pen.circle(30, 90)
        pen.right(90)
        pen.circle(30, 90)
    # 中心细密点阵
    for radius in range(20, 100, 20):
        count = int(radius / 2)
        draw_circle_dots(radius, count)


# ============================================================
#  曼荼罗 ④ ：【非正形状】飘逸螺旋 + 波浪边缘
#    核心：不依赖固定角度均分，采用斐波那契/黄金角 + 渐变尺寸
# ============================================================
def mandala_organic():
    pen.clear()
    pen.pensize(1.2)

    # 用黄金角 137.5° 产生非周期对称，更自然
    golden_angle = 137.5
    # 绘制一系列尺寸渐变的"逗号"形状
    for i in range(80):
        r = 20 + i * 2.8  # 半径逐渐增大
        offset = i * 0.3  # 轻微偏移制造漩涡感

        pen.penup()
        pen.goto(0, 0)
        pen.setheading(i * golden_angle)
        pen.forward(r)
        pen.pendown()

        # 绘制不规则弧线（每个都不一样）
        pen.circle(10 + i * 0.2, 120)
        pen.right(90)
        pen.circle(8 + i * 0.15, 90)
        pen.left(120)
        pen.circle(12 + i * 0.1, 100)

    # 外圈波浪（非圆形）
    pen.penup()
    pen.goto(0, -220)
    pen.pendown()
    for angle in range(0, 720, 5):  # 两圈
        rad = math.radians(angle)
        # 极坐标：半径随角度正弦波动 = 非正圆
        wave_r = 220 + 30 * math.sin(rad * 6) + 15 * math.cos(rad * 4)
        x = wave_r * math.cos(rad)
        y = wave_r * math.sin(rad)
        pen.goto(x, y)

    # 内部螺旋点阵
    for i in range(150):
        r = 5 + i * 1.6
        ang = i * 137.508  # 黄金角
        x = r * math.cos(math.radians(ang))
        y = r * math.sin(math.radians(ang))
        pen.penup()
        pen.goto(x, y - 3)
        pen.pendown()
        pen.circle(2.5)

    # 最中心标记
    pen.penup()
    pen.goto(0, -15)
    pen.pendown()
    pen.circle(15)


# ============================================================
#  🚀 执行：选择你要生成的曼荼罗（取消注释即可）
# ============================================================
if __name__ == "__main__":
    # 选择你要看的样式（一次只开一个，画完保存再运行下一个）

    mandala_lotus()  # ① 经典莲花
    # mandala_starburst()  # ② 星爆锯齿
    # mandala_flower()     # ③ 繁花
    # mandala_organic()    # ④ 有机螺旋（非正形状！）

    # 更新画面
    turtle.update()

    # 保存为矢量 EPS 文件（可直接打印，无限放大）
    canvas = turtle.getscreen().getcanvas()
    canvas.postscript(file="mandala_output.eps", colormode='color')
    print("✅ 曼荼罗已生成并保存为 mandala_output.eps")

    # 保持窗口显示
    turtle.done()