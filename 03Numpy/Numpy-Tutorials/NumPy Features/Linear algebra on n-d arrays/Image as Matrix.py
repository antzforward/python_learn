from scipy.datasets import  face

img = face()
type(img)

import matplotlib.pyplot as plt

plt.imshow(img)
plt.show()