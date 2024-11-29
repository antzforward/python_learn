import matplotlib.pyplot as plt
# legend 图例，讲多个图的label，集中显示出来。
import numpy as np

x = np.arange(1, 5)
plt.plot(x, x*1.5, label='Normal')

plt.plot(x, x*3.0, label='Fast')

plt.plot(x, x/3.0, label='Slow')

plt.legend() #在左上角显示（默认的设置图例） 默认是0，best由图自己来决定哪个区域比较好放图例。

plt.show()