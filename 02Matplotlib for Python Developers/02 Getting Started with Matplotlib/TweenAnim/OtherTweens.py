def linear(t):
    return t

def easeInQuad(t):
    return t * t

def easeOutQuad(t):
    return t * (2 - t)

def easeInOutQuad(t):
    if t < 0.5:
        return 2 * t * t
    else:
        return -1 + (4 - 2 * t) * t


import math

def easeInSine(t):
    return 1 - math.cos(t * math.pi / 2)

def easeOutSine(t):
    return math.sin(t * math.pi / 2)

def easeInOutSine(t):
    return -(math.cos(math.pi * t) - 1) / 2

def easeInExpo(t):
    return 0 if t == 0 else math.pow(2, 10 * (t - 1))

def easeOutExpo(t):
    return 1 if t == 1 else 1 - math.pow(2, -10 * t)

def easeInOutExpo(t):
    if t == 0:
        return 0
    if t == 1:
        return 1
    if t < 0.5:
        return 0.5 * math.pow(2, (20 * t) - 10)
    else:
        return 1 - 0.5 * math.pow(2, (-20 * t) + 10)

def easeInCirc(t):
    return 1 - math.sqrt(1 - t * t)

def easeOutCirc(t):
    return math.sqrt(1 - (t - 1) * (t - 1))

def easeInOutCirc(t):
    if t < 0.5:
        return (1 - math.sqrt(1 - (2 * t) * (2 * t))) / 2
    else:
        return (math.sqrt(1 - (-2 * t + 2) * (-2 * t + 2)) + 1) / 2

def easeInElastic(t):
    c4 = (2 * math.pi) / 3
    if t == 0:
        return 0
    if t == 1:
        return 1
    return -(math.pow(2, 10 * (t - 1)) * math.sin((t - 1 - 0.075) * c4))

def easeOutElastic(t):
    c4 = (2 * math.pi) / 3
    if t == 0:
        return 0
    if t == 1:
        return 1
    return math.pow(2, -10 * t) * math.sin((t - 0.075) * c4) + 1

def easeInOutElastic(t):
    c5 = (2 * math.pi) / 4.5
    if t == 0:
        return 0
    if t == 1:
        return 1
    if t < 0.5:
        return -(math.pow(2, 20 * t - 10) * math.sin((20 * t - 11.125) * c5)) / 2
    else:
        return (math.pow(2, -20 * t + 10) * math.sin((20 * t - 11.125) * c5)) / 2 + 1

def easeInBounce(t):
    return 1 - easeOutBounce(1 - t)

def easeOutBounce(t):
    if t < 1 / 2.75:
        return 7.5625 * t * t
    elif t < 2 / 2.75:
        return 7.5625 * (t - 1.5 / 2.75) * (t - 1.5 / 2.75) + 0.75
    elif t < 2.5 / 2.75:
        return 7.5625 * (t - 2.25 / 2.75) * (t - 2.25 / 2.75) + 0.9375
    else:
        return 7.5625 * (t - 2.625 / 2.75) * (t - 2.625 / 2.75) + 0.984375

def easeInOutBounce(t):
    if t < 0.5:
        return easeInBounce(t * 2) * 0.5
    else:
        return easeOutBounce(t * 2 - 1) * 0.5 + 0.5

def easeInBack(t):
    c1 = 1.70158
    return t * t * ((c1 + 1) * t - c1)

def easeOutBack(t):
    c1 = 1.70158
    return (t - 1) * (t - 1) * ((c1 + 1) * (t - 1) + c1) + 1

def easeInOutBack(t):
    c1 = 1.70158
    c2 = c1 * 1.525
    if t < 0.5:
        return (t * t * ((c2 + 1) * t - c2)) / 2
    else:
        return ((t - 2) * (t - 2) * ((c2 + 1) * (t - 2) + c2) + 2) / 2


import matplotlib.pyplot as plt
import numpy as np

# 创建图形和轴
fig, ax = plt.subplots()

# 设置 x 轴和 y 轴的范围
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# 设置图形为等比例
ax.set_aspect('equal')

# 设置网格
ax.grid(True)

# 生成 x 值
x = np.linspace(0, 1, 100)

# 绘制缓动曲线
ax.plot(x, [linear(t) for t in x], label='Linear')
ax.plot(x, [easeInQuad(t) for t in x], label='EaseInQuad')
ax.plot(x, [easeOutQuad(t) for t in x], label='EaseOutQuad')
ax.plot(x, [easeInOutQuad(t) for t in x], label='EaseInOutQuad')
ax.plot(x, [easeInSine(t) for t in x], label='EaseInSine')
ax.plot(x, [easeOutSine(t) for t in x], label='EaseOutSine')
ax.plot(x, [easeInOutSine(t) for t in x], label='EaseInOutSine')
ax.plot(x, [easeInExpo(t) for t in x], label='EaseInExpo')
ax.plot(x, [easeOutExpo(t) for t in x], label='EaseOutExpo')
ax.plot(x, [easeInOutExpo(t) for t in x], label='EaseInOutExpo')
ax.plot(x, [easeInCirc(t) for t in x], label='EaseInCirc')
ax.plot(x, [easeOutCirc(t) for t in x], label='EaseOutCirc')
ax.plot(x, [easeInOutCirc(t) for t in x], label='EaseInOutCirc')
ax.plot(x, [easeInElastic(t) for t in x], label='EaseInElastic')
ax.plot(x, [easeOutElastic(t) for t in x], label='EaseOutElastic')
ax.plot(x, [easeInOutElastic(t) for t in x], label='EaseInOutElastic')
ax.plot(x, [easeInBounce(t) for t in x], label='EaseInBounce')
ax.plot(x, [easeOutBounce(t) for t in x], label='EaseOutBounce')
ax.plot(x, [easeInOutBounce(t) for t in x], label='EaseInOutBounce')
ax.plot(x, [easeInBack(t) for t in x], label='EaseInBack')
ax.plot(x, [easeOutBack(t) for t in x], label='EaseOutBack')
ax.plot(x, [easeInOutBack(t) for t in x], label='EaseInOutBack')

# 添加图例
ax.legend()

# 显示图形
plt.show()