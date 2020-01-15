num = int(input("Enter number of entries: "))
Entries = []
for i in range(num):
    Entries.append(input())
sortedEntries = sorted(Entries)


def arrange(func):
    def number():
        for n in func:
            print("+91 "+n[-10:-5]+" "+n[-5:])
    return number


arrange(sortedEntries)()