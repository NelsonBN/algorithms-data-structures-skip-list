import random

import random

class Node:
    def __init__(self, key, highest_level):
        self.key = key
        self.forward = [None] * (highest_level + 1)

class SkipList:
    def __init__(self, max_levels = 4):
        self.max_levels = max_levels # Maximum allowed level
        self.p = 0.5 # Probability of level promotion (To simulate a coin flip)
        self.highest_level = 0 # Current level of the list
        self.header = Node(None, self.max_levels - 1) # Header node (sentinel)


    def __get_highest_level(self):
        level = 0
        while random.random() < self.p and level < self.max_levels - 1:
            level += 1
        return level


    def insert(self, key):
        update = [None] * self.max_levels
        current = self.header

        # Traverse levels from top to bottom searching for the correct position to insert the new node
        for i in range(self.highest_level, -1, -1): # Drill down from the highest level to 0 -> O(log n)
            while current.forward[i] and current.forward[i].key < key: # Move forward while the next node's key is less than the key to insert
                current = current.forward[i]
            update[i] = current # For each level, keep track of the last node before the position to insert

        # On this point, 'current' has the last node at level 0 before the position to insert
        # So, we move to the next node at level 0 because we want to insert after it
        current = current.forward[0]

        if current is None or current.key != key:
            highest_level_new_node = self.__get_highest_level()
            if highest_level_new_node > self.highest_level:
                # When the new node has a higher level that means the header node never had a node at that level
                # So, we will create a new shortcut from the header node to the new node at the new levels
                for i in range(self.highest_level + 1, highest_level_new_node + 1):
                    update[i] = self.header
                self.highest_level = highest_level_new_node

            # Update the neighbor nodes
            new_node = Node(key, highest_level_new_node)
            for i in range(highest_level_new_node + 1): # O(log n)
                new_node.forward[i] = update[i].forward[i]
                update[i].forward[i] = new_node


    def delete(self, key):
        update = [None] * self.max_levels
        current = self.header

        for i in range(self.highest_level, -1, -1): # Drill down from the highest level to 0 -> O(log n)
            while current.forward[i] and current.forward[i].key < key: # Move forward while the next node's key is less than the key to insert
                current = current.forward[i]
            update[i] = current

        # Move to the next node at level 0 because it's the supposed node that has the key we are looking for
        current = current.forward[0]

        if current and current.key == key:
            for i in range(self.highest_level + 1): # O(log n)
                if update[i].forward[i] != current:
                    break
                # Update the forward pointers of the cached nodes to the forward pointer of the current node
                # This effectively removes the current node from the list
                update[i].forward[i] = current.forward[i]

            # Update the highest level of the list
            while self.highest_level > 0 and self.header.forward[self.highest_level] is None:
                self.highest_level -= 1


    def search(self, key):
        current = self.header
        for i in range(self.highest_level, -1, -1): # Drill down from the highest level to 0 -> O(log n)
            while current.forward[i] and current.forward[i].key < key: # Move forward while the next node's key is less than the key to insert
                current = current.forward[i]

        # Move to the next node at level 0 because it's the supposed node that has the key we are looking for
        current = current.forward[0]

        if current and current.key == key:
            return True
        return False


    def print(self):
        for i in range(self.highest_level, -1, -1):
            print(f"Level {i}: ", end="")
            current = self.header.forward[i]
            while current:
                print(current.key, end=" -> ")
                current = current.forward[i]
            print("None")


skipList = SkipList()

skipList.insert(3)
skipList.insert(60)
skipList.insert(7)
skipList.insert(42)
skipList.insert(91)
skipList.insert(34)
skipList.insert(124)
skipList.insert(38)
skipList.insert(72)
skipList.insert(82)
skipList.insert(44)
skipList.insert(18)
skipList.insert(9)


# print structure
print("Skip List Structure:")
skipList.print()

print(f'Is 60 in the skip list? {skipList.search(60)}')
print(f'Is 10 in the skip list? {skipList.search(10)}')

print("Deleting 60...")
skipList.delete(60)
print(f'Is 60 in the skip list? {skipList.search(60)}')


print("Skip List Structure after deletion:")
skipList.print()
