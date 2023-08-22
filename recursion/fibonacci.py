import time


# A naive recursive solution
def fib(n):
    if n == 1 or n == 2:
        result = 1
    else:
        result = fib(n-1) + fib(n-2)
    return result


# A memoized solution
def fib_2(n, memo=[]):
    if memo[n] is not None:
        return memo[n]
    if n == 1 or n == 2:
        result = 1
    else:
        result = fib_2(n-1, memo) + fib_2(n-2, memo)
    memo[n] = result
    return result


def fib_memo(n):
    memo = [None] * (n + 1)
    return fib_2(n, memo)


# A bottom-up solution
def fib_bottom_up(n):
    if n == 1 or n == 2:
        return 1
    bottom_up = [None] * (n+1)
    bottom_up[1] = 1
    bottom_up[2] = 1
    for i in range(3, n+1):
        bottom_up[i] = bottom_up[i-1] + bottom_up[i-2]
    return bottom_up[n]


print("-------------FIBONACCI 5 -------------")
inicio = time.time()
res = fib(5)
fin = time.time()
print("Basic:", res, "Time:", (fin-inicio) * 10000)
inicio = time.time()
res = fib_memo(5)
fin = time.time()
print("Memoized:", res, "Time:", (fin-inicio) * 10000)
inicio = time.time()
res = fib_bottom_up(5)
fin = time.time()
print("Bottom-up:", res, "Time:", (fin-inicio) * 10000)

print("-" * 100)
print("-------------FIBONACCI 35 -------------")
inicio = time.time()
res = fib(35)
fin = time.time()
print("Basic:", res, "Time:", (fin-inicio) * 10000)
inicio = time.time()
res = fib_memo(35)
fin = time.time()
print("Memoized:", res, "Time:", (fin-inicio) * 10000)
inicio = time.time()
res = fib_bottom_up(35)
fin = time.time()
print("Bottom-up:", res, "Time:", (fin-inicio) * 10000)

print("-" * 100)
print("-------------FIBONACCI 100 -------------")
inicio = time.time()
res = fib_memo(100)
fin = time.time()
print("Memoized:", res, "Time:", (fin-inicio) * 10000)
inicio = time.time()
res = fib_bottom_up(100)
fin = time.time()
print("Bottom-up:", res, "Time:", (fin-inicio) * 10000)

print("-" * 100)
print("-------------FIBONACCI 1000 -------------")
inicio = time.time()
try:
    res = fib_memo(1000)
except Exception as e:
    res = f"Couldn't get it ({e})"

fin = time.time()
print("Memoized:", res, "Time:", (fin-inicio) * 10000)
inicio = time.time()
res = fib_bottom_up(1000)
fin = time.time()
print("Bottom-up:", res, "Time:", (fin-inicio) * 10000)
