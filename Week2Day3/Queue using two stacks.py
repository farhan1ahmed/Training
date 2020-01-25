num_com = int(input("Total commands:"))
front = []
rear = []
for i in range(num_com):
    com = [int(x) for x in input().split()]
    if com[0] == 1:
        while len(front) != 0:
            rear.append(front.pop())
        rear.append(com[1])
    else:
        while len(rear) != 0:
            front.append(rear.pop())
        if com[0] == 2:
            front.pop()
        if com[0] == 3:
            print(front[-1])
