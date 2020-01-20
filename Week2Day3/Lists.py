tries = int(input("Enter number of commands: "))
l = []
for t in range(tries):
    com = input().split()
    command = com[0]
    arguments = com[1:]
    if command != 'print':
        s = ", "
        eval("l."+command+"("+s.join(arguments[:])+")")
    elif command == 'print':
        print(l)