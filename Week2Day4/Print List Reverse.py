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


def print_singly_linked_list(node, sep):
    while node:
        print(node.data, end='')

        node = node.next

        if node:
            print(sep, end='')


def reversePrint(head):
    if head is not None:
        reversePrint(head.next)
        print(head.data)


if __name__ == '__main__':
    tries = int(input("Enter number of tries: "))
    for i in range(tries):
        elements = int(input("Enter number of elements in the list: "))
        my_llist = SinglyLinkedList()
        for i in range(elements):
            my_llist.insert_node(input())
        reversePrint(my_llist.head)