num = int(input("Enter number of entries: "))
Entries = []
for i in range(num):
    Entries.append(input().split())

age_sorted = sorted(Entries, key=lambda x: x[2])

def Gender(func):
    def printer():
        if func[3] == 'M':
            salutation= "Mr. "
            return salutation
        if func[3] == 'F':
            salutation = "Ms. "
            return salutation
    return printer()


def nameprint(func):
    def printer():
        for j in func:
            Gender(j)
            print(Gender(j) + j[0] + " " + j[1])
    return printer


nameprint(age_sorted)()