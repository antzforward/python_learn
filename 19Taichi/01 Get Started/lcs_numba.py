import numpy as np
from numba import jit

benchmark = True

N = 15_000

if benchmark:
    a_numpy = np.random.randint(0, 100, N, dtype=np.int32)
    b_numpy = np.random.randint(0, 100, N, dtype=np.int32)
else:
    a_numpy = np.array([0, 1, 0, 2, 4, 3, 1, 2, 1], dtype=np.int32)
    b_numpy = np.array([4, 0, 1, 4, 5, 3, 1, 2], dtype=np.int32)

# 使用numba加速的函数
@jit(nopython=True)
def compute_lcs_numba(a, b):
    len_a, len_b = a.shape[0], b.shape[0]
    # 初始化一个二维数组，注意numba不支持np.zeros的dtype参数为np.int32，但我们可以之后转换
    f = np.zeros((len_a+1, len_b+1), dtype=np.int32)
    for i in range(1, len_a+1):
        for j in range(1, len_b+1):
            if a[i-1] == b[j-1]:
                f[i, j] = f[i-1, j-1] + 1
            else:
                f[i, j] = max(f[i-1, j], f[i, j-1])
    return f[len_a, len_b]

print(compute_lcs_numba(a_numpy, b_numpy))

'''
使用指令为
cd "01 Get Started"
cmd /v:on /c "echo !time! & python lcs_numba.py & echo !time!"
直接用文档里面的方案，每次输入time，这个指令要求Enter the new time 就卡了一下。
嗯，虽然不好用，还是能用的。
N = 15000 
输出：
16:22:34.42 
2732
16:22:39.04

时间：接近5s 还行，但是形式已经很接近了

'''