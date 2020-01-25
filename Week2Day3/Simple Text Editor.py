num_com = int(input("Total commands:"))
stack = []
memory = []
string = ''


def editor(command):
    global string
    if int(command[0]) == 1:
        string += command[1]
        memory.append(command)
    if int(command[0]) == 2:
        removed=[]
        for x in range(int(command[1])):
            removed.insert(0, list(string).pop())
            string = string[0:-1]
        rem = ''
        for i in removed:
            rem += i
        memory.append([command[0], rem])
    if int(command[0]) == 3:
        print(string[int(command[1])-1])
    if int(command[0]) == 4:
        last_action = memory.pop()
        if int(last_action[0]) == 1:
            string = string[0:-len(last_action[1])]
        elif int(last_action[0]) == 2:
            string += last_action[1]



for i in range(num_com):
    operation = input().split()
    editor(operation)