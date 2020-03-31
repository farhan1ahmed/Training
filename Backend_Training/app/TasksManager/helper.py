
class ToDoHelper:
    def __init__(self):
        self.model = ToDoModel()

    def list(self):
        response = self.model.list_items()
        return response

#class UserHelper:
#   def __init__(self):
#        self.model = UserModel()
#
#    def create(self, name, email, password):
#        response = self.model.create(name, email, password)
#        return response

