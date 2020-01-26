class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None


def print_list(Node):
    while Node:
        print(Node.data)
        Node = Node.next


num = int(input())
my_LList = LinkedList()
for i in range(num):
    newNode = Node(input())
    if my_LList.head is None:
        my_LList.head = newNode
    else:
        last = my_LList.head
        while(last.next):
            last = last.next
        last.next = newNode
print_list(my_LList.head)
