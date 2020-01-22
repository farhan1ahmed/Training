sizeS = int(input("Size of Set S: "))
S = set(int(x) for x in input("S: ").split())
total = int(input("Number of commands: "))
for i in range(total):
    inp = input().split()
    com = inp[0]
    val = ""
    if len(inp) > 1:
        val = inp[1]
    eval("S."+com+"("+val+")")
print(len(S))