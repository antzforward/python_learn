import matplotlib.pyplot as plt
import numpy as np

x = np.arange(1, 5)
plt.plot( x, x*1.5, x, x*3.0, x, x/3.0)
plt.grid( True )
plt.show()