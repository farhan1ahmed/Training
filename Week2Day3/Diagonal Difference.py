def diagonal_difference():
    size = int(input("Enter size of matrix:" ))
    arr = []
    diag_LR = 0
    diag_RL = 0
    cRL = int(size)
    for r in range(size):
        row = input().split()
        arr.append([])
        for c in range(size):
            arr[r].append(row[c])
            if r == c:
                diag_LR += int(arr[r][c])
            if c == cRL - 1:
                diag_RL += int(arr[r][c])
                cRL -= 1

    print("Absolute difference: "+ str(abs(diag_LR - diag_RL)))


diagonal_difference()