
class ListNode:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __str__(self):
        return str(self.data)
    
    def get_data(self):
        return self.data

    def set_data(self, data_1):
        self.data = data_1

    def get_next(self):
        return self.next

    def set_next(self, next_1):
        self.next = next_1

class LinkedList:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def is_full(self):
        # Linked lists do not have a fixed size, so they are never "full."
        return False

    def __str__(self):
        if self.is_empty():
            return "Linked List is empty."
        current = self.head
        result = ""
        while current is not None:
            result += str(current) + " -> "
            current = current.get_next()
        return result[:-4]  # Remove the trailing "->"


    #LinkedList Search
    def search(self, data):
        current = self.head
        while current is not None:
            if current.get_data() == data:
                return True
            current = current.get_next()
        return False

    #LinkedList Insert
    def insert(self, data):
        new_node = ListNode(data)
        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            while cur.get_next() is not None:
                cur = cur.get_next()
            cur.next = new_node

    #LinkedList Delete
    def delete(self, data):
        if self.is_empty() is None:
            return  # Empty list

        if self.head.get_data() == data:
            self.head = self.head.get_next()
            return

        current = self.head
        while current.get_next() is not None:
            if current.get_next().get_data() == data:
                current.next = current.get_next().get_next()
                return
            current = current.get_next()

    #LinkedList Traverse
    def traverse(self):
        values = []
        current = self.head
        while current is not None:
            values.append(current.get_data())
            current = current.get_next()
        return values





'''

References:-
1)What is linked list- https://www.geeksforgeeks.org/data-structures/linked-list/
2)Insertion in Linked list- https://www.geeksforgeeks.org/insertion-in-linked-list/
3)Search an element in Linked List- https://www.geeksforgeeks.org/search-an-element-in-a-linked-list-iterative-and-recursive/
4)Length of Linked List- https://www.geeksforgeeks.org/find-length-of-a-linked-list-iterative-and-recursive/
5)Deletion in Linked List- https://www.geeksforgeeks.org/deletion-in-linked-list/
6) https://www.geeksforgeeks.org/

'''
