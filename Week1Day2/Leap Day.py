def leap_check(n):
    return n % 4 == 0 and n % 100 != 0 or n % 400 == 0


year = int(input("Enter the year: "))
print(leap_check(year))