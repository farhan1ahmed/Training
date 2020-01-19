from abc import abstractmethod
class Book:
    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price

    @abstractmethod
    def display(self):
        pass


class MyBook(Book):

    def display(self):
        return"Tile: {}\nAuthor: {}\nPrice: {}".format(self.title, self.author, self.price)


T = input("Enter Title:")
A = input("Enter Author:")
P = input("Enter Price:")
obj = MyBook(T, A, P)
print(obj.display())