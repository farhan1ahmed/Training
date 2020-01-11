n = int(input("Enter number of Students: "))
my_dict = {}
for i in range(0, n):
    record = input().split()
    my_dict[record[0]] = record[1:]
query = input()
if query in my_dict:
    score = map(float, my_dict[query])
    print(sum(score)/3)
else:
    print("Student not found")