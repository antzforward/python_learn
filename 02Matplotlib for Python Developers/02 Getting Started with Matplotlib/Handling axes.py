import matplotlib.pyplot as plt
import numpy as np

x = np.arange(1, 5)
plt.plot(x, x*1.5, x, x*3.0, x, x/3.0)
print( plt.axis()  ) #显示当前的axis的限制，根据变量数值范围与x，y的值域的范围。
plt.axis([0,5,-1,13]) #set new axes limits
plt.show()

# 注意，无参数的plt.axis() 实际上是get，有参数的是set