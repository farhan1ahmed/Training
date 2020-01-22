def staircase():
    size = int(input("Enter size of staircase:" ))
    a =[]
    for r in range(size+1):
        stair = (size-r)*" "+r*"#"
        print(stair)

staircase()