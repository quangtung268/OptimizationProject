import random

K = 5  # number of trucks
N = 15  # number of items

d = [random.randint(5, 9) for _ in range(N)]
c = [random.randint(10, 20) for _ in range(N)]
c1 = [random.randint(12, 18) for _ in range(K)]
c2 = [random.randint(22, 28) for _ in range(K)]


def input(filename):
    global N, K
    with open(filename, 'w') as f:
        f.write(f'{N} {K} \n')
        for i in range(N):
            f.write(str(d[i]) + ' ' + str(c[i]) + '\n')
        for j in range(K):
            f.write(str(c1[j]) + ' ' + str(c2[j]) + '\n')


# file name
input('filename')
