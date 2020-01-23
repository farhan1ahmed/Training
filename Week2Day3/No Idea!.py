your_elements = input("Your elements: ").split()
setA = set(input("Set N: "))
setB = set(input("Set M: "))
happy = 0
for element in your_elements:
    if element in setA:
        happy += 1
    if element in setB:
        happy -= 1
print(happy)