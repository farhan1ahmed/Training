class Student:
    def __init__(self):
        self.age = None
        self.first_name = None
        self.last_name = None
        self.standard = None

    def set_age(self):
        self.age = input("Enter Student's age: ")

    def get_age(self):
        return self.age

    def set_firstname(self):
        self.first_name = input("Enter Student's First name: ")

    def get_firtname(self):
        return self.first_name

    def set_lastname(self):
        self.last_name = input("Enter Student's Last name: ")

    def get_lastname(self):
        return self.last_name

    def set_standard(self):
        self.standard = input("Enter Student's Standard: ")

    def get_standard(self):
        return self.standard

    def to_string(self):
        return "{}, {}, {}, {}".format(self.age, self.first_name, self.last_name, self.standard)


student = Student()
student.set_age()
student.set_firstname()
student.set_lastname()
student.set_standard()
print(student.get_age())
print(student.get_lastname() + ", " + student.get_firtname())
print(student.get_standard())
print(student.to_string())





