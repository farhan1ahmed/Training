num_cylinders = [int(x) for x in input("Cylinders in each stack: ").split()]
stacks =[]
entries = []
for i in range(3):
    entries.append([int(x) for x in input("Stack"+str(i+1)+": ").split()])

for s in range(3):
    stacks.append([])
    for i in range(len(entries[s])-1, -1, -1):
        cylinder = []
        for h in range(entries[s][i]):
            cylinder.append(entries[s][i])
        stacks[s].append(cylinder)
height =[]

for i in range(3):
    height.append((sum(len(cyl) for cyl in stacks[i])))

while height[0] != height[1] or height[1] != height[2]:
    if height[0] > height[1] and height[0] > height[2]:
        stacks[0].pop()
    elif height[1] > height[2]:
        stacks[1].pop()
    else:
        stacks[2].pop()
    height=[]
    for i in range(3):
        height.append((sum(len(cyl) for cyl in stacks[i])))
print(height)

