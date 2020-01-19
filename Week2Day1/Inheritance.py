class Cls1:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def add(self):
        return self.a + self.b


class Cls2(Cls1):
    def multiply(self):
        return self.a*self.b

    def taks(self):
        return pow(self.a, 2) + pow(self.b, 2)


cases = int(input("Enter number of tries: "))
for case in range(cases):
    numbers = input().split()
    obj = Cls2(int(numbers[0]), int(numbers[1]))
    print(obj.add())
    print(obj.multiply())
    print(obj.taks())
    print(obj.a)