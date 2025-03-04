import math
import time

def root(num, mlsec):
    res = math.sqrt(num)
    time.sleep(mlsec/1000)
    print(res)
num = float(input())
mlsec = int(input())
root(num, mlsec)