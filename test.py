class NodeStack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()

    def peek(self):
        if not self.is_empty():
            return self.items[-1]

    def size(self):
        return len(self.items)


class Node:
    def __init__(self):
        self.stack = NodeStack()
        self.next = None


class CircularLinkedList:
    def __init__(self):
        self.head = None

    def append_stack(self):
        new_node = Node()
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = new_node
            new_node.next = self.head

    def push_to_stack(self, stack_index, data):
        current = self.head
        for _ in range(stack_index):
            current = current.next
        current.stack.push(data)

    def pop_from_stack(self, stack_index):
        current = self.head
        for _ in range(stack_index):
            current = current.next
        return current.stack.pop()

    def display_stacks(self):
        if not self.head:
            return

        temp = self.head
        while True:
            print(f"Stack: {temp.stack.items}")
            temp = temp.next
            if temp == self.head:
                break


# Example usage:
if __name__ == "__main__":
    clist = CircularLinkedList()
    clist.append_stack()
    clist.append_stack()

    clist.push_to_stack(0, 1)
    clist.push_to_stack(0, 2)
    clist.push_to_stack(1, 3)
    clist.push_to_stack(1, 4)

    clist.display_stacks()

    popped_item = clist.pop_from_stack(0)
    print(f"\nPopped Item from Stack 0: {popped_item}")

    clist.display_stacks()
