import numpy as np
import timeit


# input data
def input(filename):
    global N, K, d, c, C1, C2
    with open(filename, 'r') as f:
        for line in f:
            a = line.split()
            N = int(a[0])
            K = int(a[1])
            break
        first = []
        last = []
        for line in f:
            first.append(int(line.split()[0]))
            last.append(int(line.split()[1]))
        d = first[:N]
        c = last[:N]
        C1 = first[N:]
        C2 = last[N:]
        print('Number of customers:', N)
        print('Number of trucks:', K)
        print('Weight:', d)
        print('Value: ', c)
        print('Lower bound: ', C1)
        print('Upper bound: ', C2)
        print()


input('data_8_3.txt')

t0 = timeit.default_timer()

# greedy choice


index = [i for i in range(1, N + 1)]
density = sorted(list(zip(d, c, index)), key=lambda k: k[1] / k[0], reverse=True)
D, C, Index = [], [], []
for w, v, i in density:
    D.append(w)
    C.append(v)
    Index.append(i)


# funtion
def heuristic():
    global N, K
    sol = []
    f = 0
    mark = np.zeros(N, dtype='bool')
    for j in range(K):  # iterate trucks
        k = 0
        mark2 = mark.copy()
        sol.append([])

        while k < N and not mark.all():  # choose first satisfied item of current truck
            current_w = 0
            current_v = 0
            if D[k] != 0:

                for i in range(k, N):  # select next items
                    # check item's state and the upper bound and update the temporary new data
                    if mark[i] == False and current_w + D[i] <= C2[j]:
                        current_w += D[i]
                        current_v += C[i]
                        mark[i] = True

                if current_w >= C1[j]:  # check the lower bound
                    f += current_v
                    for i in range(N):
                        if mark[i] == True and C[i] != 0:  # if satisfy, update the final data
                            sol[j].append(Index[i])
                            D[i] = 0
                            C[i] = 0
                    break
                else:  # if not satisfy, return the previous state
                    mark = mark2.copy()

            k += 1

    for j in range(K):
        if sol[j] != []:
            print(f'Truck {j + 1} with customers', *sol[j], sep=' ')
        else:
            print(f'Truck {j + 1} does not contains any items')
    print('Optimal value:', f)


heuristic()

t1 = timeit.default_timer() - t0
print('Execution time:', t1)
