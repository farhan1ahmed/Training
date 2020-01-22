number = int(input("Total stamps: "))
stamp = set()
for i in range(number):
    stamp.add(input())
print("Distinct country stamps: " + str(len(stamp)))