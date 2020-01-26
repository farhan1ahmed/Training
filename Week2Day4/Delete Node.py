class SinglyLinkedListNode:
    def __init__(self, node_data):
        self.data = node_data
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_node(self, node_data):
        node = SinglyLinkedListNode(node_data)

        if not self.head:
            self.head = node
        else:
            self.tail.next = node


        self.tail = node

def print_singly_linked_list(node):
    while node:
        print(node.data)
        node = node.next

def deleteNode(head, position):
    node = head
    for j in range(position-1):
        node = node.next
    node.next = node.next.next


if __name__ == '__main__':
    elements = int(input("Enter number of elements in the list: "))
    my_llist = SinglyLinkedList()
    for i in range(elements):
        my_llist.insert_node(input())
    pos = int(input("New node position to delete: "))
    deleteNode(my_llist.head, pos)
    print_singly_linked_list(my_llist.head)