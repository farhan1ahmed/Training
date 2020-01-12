import re
tries = int(input("Enter number of tries: "))
for i in range(tries):
    try:
        re.compile(input("Enter regix:"))
        print(True)
    except re.error:
        print(False)