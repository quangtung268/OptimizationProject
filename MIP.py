from ortools.linear_solver import pywraplp
import numpy as np
import timeit

solver = pywraplp.Solver.CreateSolver('CBC')
INF = np.inf

# input data
def input(filename):
    global N, K, D, C, C1, C2
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
        D = first[:N]
        C = last[:N]
        C1 = first[N:]
        C2 = last[N:]

        print('Number of customers:', N)
        print('Number of trucks:', K)
        print('Weight:', D)
        print('Value: ', C)
        print('Lower bound: ', C1)
        print('Upper bound: ', C2)
        print()


# file name
input('data_8_3.txt')

t0 = timeit.default_timer()


# declare variables

X = {}
Y = {}
M = 1e9

for i in range(N):
    for j in range(K):
        X[i, j] = solver.IntVar(0, 1, f'X[{i},{j}]')

for j in range(K):
    Y[j] = solver.IntVar(0, 1, f'Y{j}')

# upper bound constraint
for j in range(K):
    solver.Add(sum((D[i] * X[i, j] for i in range(N))) <= C2[j])

# lower bound constraint
for j in range(K):
    solver.Add(sum(X[i, j] for i in range(N)) <= M * Y[j])
    solver.Add(sum((D[i] * X[i, j] for i in range(N))) + M * (1 - Y[j]) >= C1[j])

# one package at most one car
for i in range(N):
    solver.Add(sum((X[i, j] for j in range(K))) <= 1)

# objective
obj = solver.Objective()
for i in range(N):
    for j in range(K):
        obj.SetCoefficient(X[i, j], float(C[i]))

obj.SetMaximization()

result_status = solver.Solve()

# print result
if result_status == pywraplp.Solver.OPTIMAL:
    print('Optimal value =', solver.Objective().Value())
    for j in range(K):
        sum = 0
        print('Truck', j + 1, 'with customers', end=' ')
        for i in range(N):
            if X[i, j].solution_value() > 0:
                sum += C[i]
                print(i + 1, end=' ')
        print('with sum', sum)

t1 = timeit.default_timer()
print('Execution time: ', t1 - t0)
