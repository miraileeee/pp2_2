from functools import reduce

def multiply(x, y):
    return x * y
a = list(map(int, input().split()))
res = reduce(multiply, a)
print(res)