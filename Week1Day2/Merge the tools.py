main_string = str(input("Enter a string: "))
n = len(main_string)
k = int(input("Enter k: "))
l_substring = n//k
a = []
s = 0
for i in range(k):
    b = []
    for l in range(l_substring):
        if main_string[s] not in b:
            b.append(main_string[s])
        s += 1
    a.append(''.join(b[:l_substring]))
print(a)