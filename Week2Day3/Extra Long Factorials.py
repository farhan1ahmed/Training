def factorial(num):
    if num == 1:
        return num
    else:
        fac = num*factorial(num-1)
    return fac


num = int(input("Enter a number: "))
print(factorial(num))