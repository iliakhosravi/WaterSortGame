import random

class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("pop from an empty stack")
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            raise IndexError("peek from an empty stack")

    def all(self):
        return self.items

    def size(self):
        return len(self.items)
    


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def display(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")


class WaterSortGame:
    def __init__(self, max_size_of_bottles, colors_list):
        self.max_size_of_bottles = max_size_of_bottles
        self.colors_list = colors_list
        self.bottle = []

        for _ in range(0, len(colors_list)):
            bottle_stack = Stack()
            for _ in range(0, max_size_of_bottles):
                bottle_stack.push(random.choice(colors_list))
            self.bottle.append(bottle_stack)
        
        # create empty bottle
        empty_bottle = Stack()
        for i in range(0, max_size_of_bottles):
            empty_bottle.push("empty")

        self.bottle.append(empty_bottle)

    def display(self):
        for j in range(self.max_size_of_bottles):
            for i in range(len(self.bottle)):
                bottle_items = self.bottle[i].all()
                print(str(bottle_items[j]) + "   ", end="")
            print("\n")


def main():
    game = WaterSortGame(5, ['yellow', 'pink', 'blue'])
    game.display()



if __name__ == "__main__":
    main()

    
