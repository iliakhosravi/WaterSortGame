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
        counter = 0
        for i in range(current.stack.size() - 1, -1, -1):
            if current.stack.items[i] == 'empty':
                current.stack.pop()
                counter = counter + 1
        current.stack.pop()
        for i in range(counter + 1):
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
    
    def get_node_count(self):
        if not self.head:
            return 0

        count = 1
        temp = self.head
        while True:
            temp = temp.next
            if temp == self.head:
                break
            count += 1

        return count
    
    

        

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
        self.undo_stack = Stack()
        self.redo_stack = Stack()


        # Create a dictionary to track color counts
        color_counts = {color: 0 for color in colors_list}

        for index in range(len(colors_list)):
            self.bottle.append_stack()
            for _ in range(max_size_of_bottles):
                # Randomly choose a color that hasn't reached max_size_of_bottles
                available_colors = [color for color in colors_list if color_counts[color] < max_size_of_bottles]
                if not available_colors:
                    # All colors have reached max_size_of_bottles, choose from all colors
                    chosen_color = random.choice(colors_list)
                else:
                    chosen_color = random.choice(available_colors)

                # Increment the color count
                color_counts[chosen_color] += 1

                # Push the chosen color to the stack
                self.bottle.push_to_stack(index, chosen_color)
        
        # create empty bottle
        self.bottle.append_stack()
        for i in range(0, max_size_of_bottles):
            self.bottle.push_to_stack(len(self.colors_list), "empty")


    # ----------------------------- display --------------------------------------
    def display(self):
        # print(self.save_state())
        
        # self.bottle.display_stacks()
        # print("--------#-------------")
    
        current = self.bottle.head
        
        for j in range(self.max_size_of_bottles , 0, -1): #decsending

            for i in range(self.bottle.get_node_count()):
                if current.stack.size() >= j:   # it is for checking if the empty bottle is add or no
                    print(current.stack.items[self.max_size_of_bottles - (self.max_size_of_bottles - (j - 1) )] + "   ", end="")
                    current = current.next
                else:
                    current = current.next
                

            print('\n')

        # print(self.bottle.get_top_of_node(3))
        print("--------#-------------")
        # print(self.bottle.get_node_count())
        # print(self.has_won())
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
        for i in range(current.stack.size() -1):
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
            for i in range(current.stack.size() - 1 , -1, -1):
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
    
    # --------------- replace color -----------------------
    def replace_color(self, first_color, second_color):
        current = self.bottle.head
        for _ in range(self.bottle.get_node_count()):
            for i in range(current.stack.size()):
                if current.stack.items[i] == first_color:
                    current.stack.items[i] = second_color
            current = current.next

    #---------------- add empty bottle ----------------
    def add_empty_bottle(self):
        self.bottle.append_stack()
        for _ in range(int((self.max_size_of_bottles)/2)):
            self.bottle.push_to_stack(len(self.colors_list) + 1, "empty")




    # -------------- check wining ---------------------
    def has_won(self):
        current = self.bottle.head
        for i in range(self.bottle.get_node_count()):
            for j in range(current.stack.size()):
                if current.stack.items[0] != current.stack.items[j]:
                    return False
                
            current = current.next
        return True
    
        
# ---------------- undo ------------------
    def save_state(self):
        state = []
        node = self.bottle.head
        for i in range(self.bottle.get_node_count()):
            state.append(node.stack.all()[:]) # using the list slicing notation to create a shallow copy of the list
            node = node.next

        # self.undo_stack.append(state)
        self.undo_stack.push(state)
        print(self.undo_stack.items)

            


    def undo(self):
            
        self.redo_stack.push(self.undo_stack.items[-1])   
        self.undo_stack.pop()
        
        current = self.bottle.head
        for i in range(len(self.undo_stack.items[-1])):
            # if len(self.undo_stack.items[-1]) != self.bottle.get_node_count():
            #     last = self.bottle.head
            #     for i in range(self.bottle.get_node_count()):
            #         last.next
            #     for j in range(last.stack.size()):
            #         last.stack.pop()                  # bayad node akhari hazf sheh
            current.stack.items = self.undo_stack.items[-1][i]
            current = current.next
        
        
        print(self.undo_stack.items)
            

    def redo(self):
    
        self.undo_stack.push(self.redo_stack.items[-1])    
        
        current = self.bottle.head
        for i in range(len(self.redo_stack.items[-1])):
            current.stack.items = self.redo_stack.items[-1][i]
            current = current.next
        
        self.redo_stack.pop()




        





def main():
    game = WaterSortGame(5, ['yellow', 'pink', 'blue'])
    # game = WaterSortGame(5, ['yellow'])
    # game.display()
    # game.add_empty_bottle()
    # game.replace_color('yellow', 'orange')
    
    # game.select(1)
    # game.select(2)
    # game.selectPrevious()
    # game.pour(3)
    # game.swap(3)
    
    # game.select(2)
    # game.pour(4)
    game.display()
    
    game.select(0)
    game.save_state()
    print('--------')
    game.pour(3)
    game.save_state()
    game.display()
    game.add_empty_bottle()
    game.display()
    

    # Print the updated color_list
    game.undo()
    
    

    game.display()
    game.redo()
    game.display()
    
    

    # start = input("type start to start game: ")
    # if start == "start":
    #     max_size_of_bottles = int(input("please enter the max size of bottles: "))
    #     color_list = []
    #     input_string = input("Enter colors separated by space: ")
    #     colors = input_string.split()
    #     color_list.extend(colors)
        
    #     game = WaterSortGame(max_size_of_bottles, color_list)

    #     game.display()
    #     add_empty_bottle_count = 0
    #     while not game.has_won():
    #         method = input("please write your method to make change: ")
    #         # if method == 'select' or method == 'selectNext' or method == 'selectPrevious' or method == 'deselect':
    #         if method == 'select':
    #             number = int(input("enter the number of stack that you want to select it: "))
    #             game.select(number)

    #         if method == 'selectNext':
    #             game.selectNext()

    #         if method == 'selectPrevious':
    #             game.selectPrevious()

    #         if method == 'deselect':
    #             game.deSelect()
            
    #         if method == 'pour':
    #             number = int(input('enter the bottle number that you want to pour in: '))
    #             game.pour(number)
            
    #         if method == 'swap':
    #             number = int(input('enter the bottle number that you want to swap with: '))
    #             game.swap(number)

    #         if method == 'replaceColor':
    #             color1 = input('enter the first color name: ')
    #             color2 = input('enter the second color name: ')
    #             game.replace_color(color1, color2)
            
    #         if method == 'AddEmptyBottle' and add_empty_bottle_count == 0:
    #             game.add_empty_bottle()

    #         game.display()
    #         if game.has_won():
    #             print('YOU WON!')
            

  




    





if __name__ == "__main__":
    main()

    
