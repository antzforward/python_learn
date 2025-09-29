"""Count the prime numbers in the range [1, n]
"""


# Checks if a positive integer is a prime number
def is_prime(n: int):
    result = True
    # Traverses the range between 2 and sqrt(n)
    # - Returns False if n can be divided by one of them;
    # - otherwise, returns True
    for k in range(2, int(n ** 0.5) + 1):
        if n % k == 0:
            result = False
            break
    return result


# Traverses the range between 2 and n
# Counts the primes according to the return of is_prime()
def count_primes(n: int) -> int:
    count = 0
    for k in range(2, n):
        if is_prime(k):
            count += 1

    return count


print(count_primes(10_000_000))

'''
使用指令为
cd "01 Get Started"
cmd /v:on /c "echo !time! & python count_primes.py & echo !time!"
直接用文档里面的方案，每次输入time，这个指令要求Enter the new time 就卡了一下。
嗯，虽然不好用，还是能用的。
n = 10_000_000 
输出：
15:20:42.90
664579
15:22:58.46
大概时间消耗是2分16秒
'''
