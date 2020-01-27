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

def compare_lists(head1, head2):
    if not head1 and not head2:
        return 1
    elif not head1 or not head2:
        return 0
    if head1.data == head2.data:
        return compare_lists(head1.next, head2.next)
    else:
        return 0


if __name__ == '__main__':

    tries = int(input("Enter number of tries: "))
    for i in range(tries):
        my_llist = []
        for l in range(2):
            elements = int(input("Enter number of elements in the list "+str(l+1)+": "))
            my_llist.append(SinglyLinkedList())
            for j in range(elements):
                my_llist[l].insert_node(input())
        print(compare_lists(my_llist[0].head, my_llist[1].head))