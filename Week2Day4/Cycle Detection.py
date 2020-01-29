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


def print_singly_linked_list(node, sep, fptr):
    while node:
        fptr.write(str(node.data))

        node = node.next

        if node:
            fptr.write(sep)


def has_cycle(head):
    address = []
    node = head
    if not head:
        status = 0
    else:
        while node is not None:
            if node.data not in address:
                address.append(node.data)
                node = node.next
                status = 0
            else:
                return 1

    return status


if __name__ == '__main__':
    tries = int(input("Enter number of tries: "))
    for i in range(tries):
        my_llist = SinglyLinkedList()
        elements = int(input("Enter number of elements in the list: "))
        for j in range(elements):
            my_llist.insert_node(input())
        print(has_cycle(my_llist.head))