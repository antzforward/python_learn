import numpy as np


benchmark = True

N = 15000

# 初始化二维数组 f，使用 numpy 数组而不是 Taichi field
f = np.zeros((N + 1, N + 1), dtype=np.int32)

if benchmark:
    a_numpy = np.random.randint(0, 100, N, dtype=np.int32)
    b_numpy = np.random.randint(0, 100, N, dtype=np.int32)
else:
    a_numpy = np.array([0, 1, 0, 2, 4, 3, 1, 2, 1], dtype=np.int32)
    b_numpy = np.array([4, 0, 1, 4, 5, 3, 1, 2], dtype=np.int32)

def compute_lcs(a: np.ndarray, b: np.ndarray) -> int:
    len_a, len_b = a.shape[0], b.shape[0]
    for i in range(1, len_a + 1):
        for j in range(1, len_b + 1):
               f[i, j] = max(f[i - 1, j - 1] + (a[i - 1] == b[j - 1]),
                          max(f[i - 1, j], f[i, j - 1]))

    return f[len_a, len_b]

print(compute_lcs(a_numpy, b_numpy))

'''
使用指令为
cd "01 Get Started"
cmd /v:on /c "echo !time! & python lcs.py & echo !time!"
直接用文档里面的方案，每次输入time，这个指令要求Enter the new time 就卡了一下。
嗯，虽然不好用，还是能用的。
N = 15000 
输出：
16:10:44.39
2727
16:15:47.83
时间：接近3分多， 接近2.25亿次操作 哈哈哈
'''