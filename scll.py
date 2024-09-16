
class Node:
    def __init__(self, data):
        # Initialize a node with data and next pointer
        self.data = data
        self.next = None

class SingularCircularLinkedList:
    def __init__(self):
        # Initialize an empty circular linked list with head pointer pointing to None
        self.head = None

    def append(self, data):
        # Append a new node with data to the end of the circular linked list
        new_node = Node(data)
        if not self.head:
            # If the list is empty, make the new node point to itself
            new_node.next = new_node
            self.head = new_node
        else:
            current = self.head
            while current.next != self.head:
                # Traverse the list until the last node
                current = current.next
            # Make the last node point to the new node
            current.next = new_node
            # Make the new node point back to the head
            new_node.next = self.head

    def traverse(self, until):
        # Return the elements of a linked list as a list
        if not self.head:
            return
        current = self.head
        nodes = []
        i = 0
        while True:
            nodes.append(current)
            i += 1
            current = current.next
            if (current == self.head or i == until):
                break
        return(nodes)
    def deleteat(self, position):
        if not self.head:
            return
        if position < 0:
            return

        # Deleting the head node
        if position == 0:

                # Only one node in the list
            if self.head.next == self.head:
                self.head = None
            else:
                current = self.head
                while current.next != self.head:
                    current = current.next
                current.next = self.head.next
                self.head = self.head.next
            return
        current = self.head
        count = 0
        while count < position - 1 and current.next != self.head:
            current = current.next
            count += 1
        if count < position - 1:
            return
        current.next = current.next.next
    def getnodeat(self, position):
        if not self.head:
            return
        current = self.head
        if (position == 0):
            return(self.head)
        i = 0
        while True:
            i += 1
            current = current.next
            if ((current == self.head) or (i == position)):
                node = current
                break
        return(node)
        current.next = current.next.next
    def findnode(self, data):
        if not self.head:
            return
        current = self.head
        i = 0
        while True:
            i += 1
            current = current.next
            if ((current.data == data)):
                pos = i
                break
            elif(current == self.head):
                pos = -1
        return(pos)
