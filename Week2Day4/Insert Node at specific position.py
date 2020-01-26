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


def insertNodeAtPosition(head, data, position):
    newnode = SinglyLinkedListNode(data)
    if position == 0:
        shift = head
        newnode.next = shift
        head = newnode
    else:

        node = head
        for i in range(position-1):
            node = node.next
        shift = node.next
        node.next = newnode
        newnode.next = shift
    return head


if __name__ == '__main__':
    elements = int(input("Enter number of elements in the list: "))
    my_llist = SinglyLinkedList()
    for i in range(elements):
        my_llist.insert_node(input())
    d = int(input("New node data: "))
    pos = int(input("New node position: "))
    insertNodeAtPosition(my_llist.head, d, pos)
    print_singly_linked_list(my_llist.head)
