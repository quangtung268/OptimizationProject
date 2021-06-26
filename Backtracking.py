import numpy as np


def input(filename):
    global N, K, d, c, C1, C2
    with open(filename, 'r') as f:
        for line in f:
            a = line.split()
            N = int(a[0])
            K = int(a[-1])
            break

        first = []
        last = []
        for line in f:
            first.append(int(line.split()[0]))
            last.append(int(line.split()[-1]))
        d = first[0:N]
        c = last[0:N]
        C1 = first[-K:]
        C2 = last[-K:]
        print('Number of customers:', N)
        print('Number of trucks:', K)
        print('Weight:', d)
        print('Value: ', c)
        print('Lower bound: ', C1)
        print('Upper bound: ', C2)
        print()



input('data_15_3.txt')


x = np.zeros(N, dtype='int')
x_best = np.zeros(N, dtype='int')
Ci = np.zeros(K, dtype='int')  # weight each truck

sum = 0
sum_best = 0



def check_bound(Ci):
    for i in range(K):
        if Ci[i] != 0 and (Ci[i] < C1[i] or Ci[i] > C2[i]):
            return False
    return True


def check_upperbound(Ci):
    for i in range(K):
        if Ci[i] > C2[i]:
            return False
    return True


def Solution():
    global sum, sum_best, x, x_best
    if sum > sum_best:
        x_best[:] = x[:]
        sum_best = sum


def Try(n):
    global sum, sum_best, Ci, c, d
    for i in range(K + 1):
        x[n] = i
        if i != 0:
            Ci[i-1] += d[n]
            sum += c[n]
        if n == N - 1:
            if check_bound(Ci):
                Solution()
        else:
            if check_upperbound(Ci):
                Try(n + 1)
        if i != 0:
            Ci[i-1] -= d[n]
            sum -= c[n]

import time
startTime = time.time()

Try(0)
def truck(x):
    S = []
    for i in range(N):
        if x_best[i] == x:
            S.append(i+1)
    return S

for i in range(1,K+1):
    print(f'Truck {i} contains:' ,truck(i))
print('Total value: ', sum_best)
executionTime = (time.time() - startTime)

print(executionTime)
