from ortools.sat.python import cp_model
import timeit

model = cp_model.CpModel()
t0 = timeit.default_timer()


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
            last.append(int(line.split()[-1]))
        D = first[0:N]
        C = last[0:N]
        C1 = first[N:]
        C2 = last[N:]
        print('Number of customers:', N)
        print('Number of trucks:', K)
        print('Weight:', D)
        print('Value: ', C)
        print('Lower bound: ', C1)
        print('Upper bound: ', C2)
        print()


input('data_8_3.txt')


# declare variables

x = {}
for i in range(N):
    for j in range(K):
        x[i, j] = model.NewIntVar(0, 1, f'x[{i},{j}]')


# one package at most one car
for i in range(N):
    model.Add(sum(x[i, j] for j in range(K)) <= 1)

# upper bound constraint
for j in range(K):
    model.Add(sum(D[i] * x[i, j] for i in range(N)) <= C2[j])

# lower bound constraint
for j in range(K):
    b = model.NewBoolVar('b')
    model.Add(sum(x[i, j] for i in range(N)) != 0).OnlyEnforceIf(b)
    model.Add(sum(x[i, j] for i in range(N)) == 0).OnlyEnforceIf(b.Not())
    model.Add(sum(D[i] * x[i, j] for i in range(N)) >= C1[j]).OnlyEnforceIf(b)

# objective function
model.Maximize(sum(C[i] * x[i, j] for i in range(N) for j in range(K)))

solver = cp_model.CpSolver()
status = solver.Solve(model)


# Print solution

print('Objective value =', solver.ObjectiveValue())
for j in range(K):
    print('Truck', j + 1, 'with customers', end=' ')
    sum = 0
    for i in range(N):
        if solver.Value(x[i,j]) > 0:
            sum += D[i]
            print(i + 1, end = ' ' )
    print('and total weight', sum)

t1 = timeit.default_timer()
print('Execution time:', t1 - t0)


