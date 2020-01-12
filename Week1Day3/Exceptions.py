tries = int(input("Enter number of tries: "))
for i in range(tries):
    num = input("Enter two numbers to divide: ").split()
    try:
        print(int(num[0])//int(num[1]))
    except ZeroDivisionError as zero:
        print("Error: ", zero)
    except ValueError as ver:
        print("Error: ", ver)