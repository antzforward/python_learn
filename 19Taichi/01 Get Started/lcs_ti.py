import taichi as ti
import numpy as np

ti.init(arch=ti.cpu)

benchmark = True

N = 15000

f = ti.field(dtype=ti.i32, shape=(N + 1, N + 1))

if benchmark:
    a_numpy = np.random.randint(0, 100, N, dtype=np.int32)
    b_numpy = np.random.randint(0, 100, N, dtype=np.int32)
else:
    a_numpy = np.array([0, 1, 0, 2, 4, 3, 1, 2, 1], dtype=np.int32)
    b_numpy = np.array([4, 0, 1, 4, 5, 3, 1, 2], dtype=np.int32)

@ti.kernel
def compute_lcs(a: ti.types.ndarray(), b: ti.types.ndarray()) -> ti.i32:
    len_a, len_b = a.shape[0], b.shape[0]

    ti.loop_config(serialize=True) # Disable auto-parallelism in Taichi
    for i in range(1, len_a + 1):
        for j in range(1, len_b + 1):
               f[i, j] = ti.max(f[i - 1, j - 1] + (a[i - 1] == b[j - 1]),
                          ti.max(f[i - 1, j], f[i, j - 1]))

    return f[len_a, len_b]


print(compute_lcs(a_numpy, b_numpy))

'''
使用指令为
cd "01 Get Started"
cmd /v:on /c "echo !time! & python lcs_ti.py & echo !time!"
直接用文档里面的方案，每次输入time，这个指令要求Enter the new time 就卡了一下。
嗯，虽然不好用，还是能用的。
N = 15000 
输出：
15:57:37.65 
[Taichi] version 1.7.4, llvm 15.0.1, commit b4b956fd, win, python 3.12.3
[Taichi] Starting on arch=x64
2708
15:57:39.50
时间：接近2s 

'''