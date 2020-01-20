Students = int(input("Enter number of students: "))
l=[]
s=set()
for student in range(Students):
    Name = input()
    marks = float(input())
    l.append([Name, marks])
    s.add(marks)
for i in range(len(l)):
    if l[i][1] == sorted(list(s))[1]:
        print(l[i][0])
