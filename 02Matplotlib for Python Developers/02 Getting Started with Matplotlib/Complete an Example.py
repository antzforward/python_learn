
import matplotlib as mpl
# 使用Agg 在plt之前
mpl.use('Agg') #后端渲染选Agg，提高fig的质量

import matplotlib.pyplot as plt

import numpy as np

x = np.arange(1, 5)
plt.plot(x, x*1.5, label='Normal')

plt.plot(x, x*3.0, label='Fast')

plt.plot(x, x/3.0, label='Slow')

plt.grid( True ) #grid show

plt.xlabel('Samples')
plt.ylabel('Value Measured')
plt.title('Sample Growth of a Measure')

plt.legend(loc='upper left')

#plt.show() #使用了Agg 就不能用show了。

# 关闭时保存文件
plt.savefig('plot123.png')