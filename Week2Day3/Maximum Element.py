tries = int(input("Number of commands: "))
stack = []
for i in range(tries):
    com = [int(x) for x in input().split()]
    if com[0] == 1:
        stack.append(com[1])
    if com[0] == 2:
        stack.pop()
    if com[0] == 3:
        print(max(stack))