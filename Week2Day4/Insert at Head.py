
class SinglyLinkedListNode:
    def __init__(self, node_data):
        self.data = node_data
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None


def print_singly_linked_list(node):
    while node:
        print(node.data)
        node = node.next


def insertNodeAtHead(llist, data):
    if llist.head is None:
        llist.head = SinglyLinkedListNode(data)
    else:
        shift = llist.head
        llist.head = SinglyLinkedListNode(data)
        llist.head.next = shift
    return llist.head


if __name__ == '__main__':
    inputs = [383, 484, 392, 975, 321]
    my_llist = SinglyLinkedList()
    for i in inputs:
        insertNodeAtHead(my_llist, i)
    print_singly_linked_list(my_llist.head)