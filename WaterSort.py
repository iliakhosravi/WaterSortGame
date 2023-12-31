import random

class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        counter = 0
        for i in range(len(self.items)):
            if self.items[i] == "empty":
                counter = counter + 1
        if counter == len(self.items):
            return True
        return False
    
    def is_full(self):
        counter = 0
        for i in range(len(self.items)):
            if self.items[i] != "empty":
                counter = counter + 1
        if counter == len(self.items):
            return True
        return False

    def push(self, item):
        self.items.append(item)

    def pop(self):
        # if not self.is_empty():
        return self.items.pop()
        # else:
        #     raise IndexError("pop from an empty stack")
    
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
    def __init__(self):
        self.stack = Stack()
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
        current.stack.pop()
        current.stack.push("empty")
    
    def get_node(self, stack_index):
        current = self.head
        for _ in range(stack_index):
            current = current.next
        return current.stack.all()

    # get top of node that isn't empty
    def get_top_of_node(self, stack_index):
        current = self.head
        for _ in range(stack_index):
            current = current.next
        top = current.stack.items[-1]
        index = -1
        counter = 1
        while top == "empty" and counter != current.stack.size():
            index = index - 1
            counter = counter + 1
            top = current.stack.items[index]

        return top
    
    # all items are one color
    def is_stack_complete(self, stack_index):
        current = self.head
        for _ in range(stack_index):
            current = current.next
        if current.stack.items[0] == "empty":
            return False
        for i in range(current.stack.size() - 1):
            if current.stack.items[i] != current.stack.items[i+1]:
                return False
        
        return True
    
    

        

    def display_stacks(self):
        if not self.head:
            return

        temp = self.head
        while True:
            print(f"Stack: {temp.stack.items}")
            temp = temp.next
            if temp == self.head:
                break


class WaterSortGame:

    #  ----------------------------- constructor ------------------------------
    def __init__(self, max_size_of_bottles, colors_list):
        self.max_size_of_bottles = max_size_of_bottles
        self.colors_list = colors_list
        self.bottle_selected_number = -1
        self.bottle_selected = -1
        self.bottle = CircularLinkedList()


        for index in range(0, len(colors_list)):
            # bottle_stack = Stack()
            self.bottle.append_stack()
            for _ in range(0, max_size_of_bottles):
                self.bottle.push_to_stack(index, random.choice(colors_list))
           
        
        # create empty bottle
        self.bottle.append_stack()
        for i in range(0, max_size_of_bottles):
            self.bottle.push_to_stack(len(self.colors_list), "empty")


    # ----------------------------- display --------------------------------------
    def display(self):
        
        self.bottle.display_stacks()
        print("--------#-------------")
    
        current = self.bottle.head
        # print(current)
        for j in range(self.max_size_of_bottles , 0, -1): #decsending

            for i in range(len(self.colors_list) + 1):
                print(current.stack.items[self.max_size_of_bottles - (self.max_size_of_bottles - (j - 1) )] + "   ", end="")
                current = current.next
            print('\n')

        # print(self.bottle.get_top_of_node(3))
        print("--------#-------------")
        # print(self.bottle.get_node(1))
        # print(self.select(1))
        # print(self.bottle.get_top_of_node(4))


    # ---------------------------- selection part ---------------------------------
    def select(self, bottle_number):

        current = self.bottle.head
        for _ in range(bottle_number):
            current = current.next
        
        self.bottle_selected_number = bottle_number
        self.bottle_selected = current
        is_selected = True
        bottle_items = current.stack.all()
        counter = 0
        for i in range(self.max_size_of_bottles -1):
            if bottle_items[i] == bottle_items[i+1]:
                counter = counter + 1

        if counter == self.max_size_of_bottles and bottle_items[0] != "empty":
            is_selected = False
        return is_selected
    
    def deSelect(self):
        self.bottle_selected_number = -1
        self.bottle_selected = -1
    
    def selectNext(self):
        if self.bottle_selected == -1:
            return
        self.bottle_selected = self.bottle.head.next
        self.bottle_selected_number = self.bottle_selected_number + 1
    
    def selectPrevious(self):
        if self.bottle_selected == -1:
            return
        
        self.bottle_selected_number = self.bottle_selected_number - 1
        pointer = self.bottle.head
        for i in range(self.bottle_selected_number):
            pointer = pointer.next
        
        self.bottle_selected = pointer
        


    # --------------------------- pour part ---------------------------

    def pour(self, bottle_number):
        is_pour = True

        if self.bottle_selected == -1:
            return False
        
        # if self.select != True:
        #     return False
        
        # selected bottle should not be empty
        current = self.bottle.head
        for _ in range(self.bottle_selected_number):
            current = current.next
        if current.stack.is_empty():
            return False
        

        # destination bottle should not be full
        current = self.bottle.head
        for _ in range(bottle_number):
            current = current.next
        if current.stack.is_full():
            return False


        origin_bottle_number = self.bottle_selected_number

        destination_bottle_number = bottle_number
 
        temp_data = self.bottle.get_top_of_node(origin_bottle_number)
        if current.stack.items[0] == "empty" or self.bottle.get_top_of_node(destination_bottle_number) == self.bottle.get_top_of_node(origin_bottle_number):
            
            counter = 0
            for i in range(self.max_size_of_bottles - 1 , -1, -1):
                if current.stack.items[i] == "empty":
                    current.stack.pop()
                    counter = counter + 1
            self.bottle.push_to_stack(destination_bottle_number, temp_data)
            for i in range(counter - 1):
                self.bottle.push_to_stack(destination_bottle_number, "empty")

            self.bottle.pop_from_stack(origin_bottle_number)
            
            is_pour = True

        
        return is_pour

    # ------------------------------ swap bottle part -------------------------
    def swap(self, bottle_number):
        if self.bottle_selected == -1:
            return False

        current_selected = self.bottle.head
        for _ in range(self.bottle_selected_number):
            current_selected = current_selected.next

        current_destination = self.bottle.head
        for _ in range(bottle_number):
            current_destination = current_destination.next

        # Check if the selected bottle and destination bottle are not empty
        # if current_selected.stack.is_empty() or current_destination.stack.is_empty():
        #     return False

        # Swap the contents of the selected bottle and destination bottle
        temp = []
        for i in range(self.max_size_of_bottles):
            temp.append(current_destination.stack.items[i])
        
        for _ in range(self.max_size_of_bottles):
            current_destination.stack.pop()

        for i in range(self.max_size_of_bottles):
            current_destination.stack.push(current_selected.stack.items[i])
        
        for _ in range(self.max_size_of_bottles):
            current_selected.stack.pop()

        for i in range(self.max_size_of_bottles):
            current_selected.stack.push(temp[i]) 
    
        return True
        
        





def main():
    game = WaterSortGame(5, ['yellow', 'pink', 'blue'])
    game.display()
    game.select(1)
    # game.selectPrevious()
    # game.pour(3)
    game.swap(3)
    
    # game.select(2)
    # game.pour(3)
    game.display()




if __name__ == "__main__":
    main()

    
