sizeM = input("Size of Set M: ")
M = set(int(x) for x in input("M: ").split())
sizeN = input("Size of Set N: ")
N = set(int(x) for x in input("N: ").split())
sym_diff = sorted(M.difference(N).union(N.difference(M)))
for i in sym_diff:
    print(i)