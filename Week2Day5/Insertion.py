class Node:
    def __init__(self, info):
        self.info = info
        self.left = None
        self.right = None
        self.level = None

    def __str__(self):
        return str(self.info)


def preOrder(root):
    if root:
        print(root.info, end=" "),
        preOrder(root.left)
        preOrder(root.right)


class BinarySearchTree:
    def __init__(self):
        self.root = None

    # Node is defined as
    # self.left (the left child of the node)
    # self.right (the right child of the node)
    # self.info (the value of the node)


    def insert(self, val):
        node = Node(val)
        if self.root is None:
            self.root = node
        else:
            current = self.root
            while True:
                if val < current.info:
                    if current.left:
                        current = current.left
                    else:
                        current.left= node
                        break
                elif val > current.info:
                    if current.right:
                        current = current.right
                    else:
                        current.right = node
                        break
                else:
                    break

elements = int(input("Number of nodes: "))
tree = BinarySearchTree()
i = 0
while i < elements:
    i += 1
    tree.insert(input())
preOrder(tree.root)
tree.insert(input())
preOrder(tree.root)