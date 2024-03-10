from binarysearchtree import BinarySearchTree
from linkedlist import LinkedList
from sympy import symbols, Eq, solve
import matplotlib.pyplot as plt
from tqdm import tqdm
from math import log2
import time
import random


# Define X, a list of tree sizes from 5 to 100 with a step size of 5
X = list(range(5, 101, 5))

########################################
# Generating random tree and linked list
########################################

# Function to generate a random BST of size n
def random_tree(n):
    tree = BinarySearchTree()
    values_set = set()
    for _ in range(n):
        while True:
            data = random.randint(1, 1000)
            if data not in values_set:
                values_set.add(data)
                break
        tree.insert(data)
    return tree

# Function to generate a random linked list of size n
def random_linked_list(n):
    linked_list = LinkedList()
    values_set = set()
    for _ in range(n):
        while True:
            data = random.randint(1, 1000)
            if data not in values_set:
                values_set.add(data)
                break
        linked_list.insert(data)
    return linked_list

###################################
# Calculating average search times
###################################

# Function to measure the average search time for a value in a BST
def measure_search_time(tree, value):
    start_time = time.time()
    tree.search(value)
    end_time = time.time()
    search_time = end_time - start_time
    return search_time

# Function to measure the average search time for a value in a BST
def measure_search_time_linked_list(linked_list, value):
    start_time = time.time()
    linked_list.search(value)
    end_time = time.time()
    search_time = end_time - start_time
    return search_time


# Number of iterations per tree size
iterations = 1000

# Initialize Y with zeros for all tree sizes
Y = [0] * len(X)  # BST
Y4 = [0] * len(X)  # Linkedlist

#######################################
# Iterate through different tree sizes
#######################################

for i, size in tqdm(enumerate(X)):
    total_time = 0
    total_time_linked_list = 0
    search_value = 42

    # Generate and search multiple random trees of the same size
    for _ in tqdm(range(iterations)):
        #BinaryTree
        tree = random_tree(size)
        search_time = measure_search_time(tree, search_value)
        total_time += search_time

        #LinkedList
        linked_list = random_linked_list(size)
        search_time_linked_list = measure_search_time_linked_list(
            linked_list, search_value)
        total_time_linked_list += search_time_linked_list

    # Calculate the average search time for this tree size
    average_time = total_time / iterations

    # Calculate the average search time for this Linked List size
    average_time_linked_list = total_time_linked_list / iterations

    # Store the average time in Y
    Y[i] = average_time  # BST
    Y4[i] = average_time_linked_list  # Linkedlist

###########################
# Y2 - linear relationship
###########################
t1 = Y[0]
t2 = Y[1]
n1 = X[0]
n2 = X[1]

# calcualting c,b values using linear equation using sympy library
c, b = symbols('c,b')

# defining equations
eq1 = Eq((c * n1 + b), t1)
eq2 = Eq((c * n2 + b), t2)

# solving equation
res = solve((eq1, eq2), (c, b))
c, b = res[c], res[b]

Y2 = [0] * len(X)
for i, n in enumerate(X):
    Y2[i] = c * n + b

###############################
# Y3 - logarithmic relationship
###############################
t1 = Y[0]
t2 = Y[1]
n1 = X[0]
n2 = X[1]

# calcualting c,b values using log equation in sympy library
c, b = symbols('c,b') 

# defining equations using sympy library
eq1 = Eq((c * log2(n1) + b), t1)
eq2 = Eq((c * log2(n2) + b), t2)

# solving equation using sympy library
res = solve((eq1, eq2), (c, b))
c, b = res[c], res[b]

Y3 = [0] * len(X)
for i, n in enumerate(X):
    Y3[i] = c * log2(n) + b

####################################################
# Plot the curves
####################################################

#3.4
#Plot 1   X vs Y
plt.plot(X, Y)
plt.xlabel('Size of trees')
plt.ylabel('Search time')
plt.ticklabel_format(axis='both', style='sci', scilimits=(0, 0))
plt.title('Complexity analysis X vs Y')
plt.show()

#Plot 2     X vs Y2
plt.plot(X, Y2)
plt.xlabel('Size of trees')
plt.ylabel('Search time')
plt.ticklabel_format(axis='both', style='sci', scilimits=(0, 0))
plt.title('Complexity analysis X vs Y2')
plt.show()

#Plot 3     X vs Y3
plt.plot(X, Y3)
plt.xlabel('Size of trees')
plt.ylabel('Search time')
plt.ticklabel_format(axis='both', style='sci', scilimits=(0, 0))
plt.title('Complexity analysis X vs Y3')
plt.show()

#Plot 4     X vs Y, Y2 and Y3
plt.plot(X, Y)
plt.plot(X, Y2)
plt.plot(X, Y3)
plt.legend(['BST', 'Linear', 'Logarithmic'])
plt.xlabel('Size of trees')
plt.ylabel('Search time')
plt.ticklabel_format(axis='both', style='sci', scilimits=(0, 0))
plt.title('Complexity analysis X vs Y, Y2 and Y3')
plt.show()

#Plot 5    X vs Y4
plt.plot(X, Y4)
plt.xlabel('Size of trees')
plt.ylabel('Search time')
plt.ticklabel_format(axis='both', style='sci', scilimits=(0, 0))
plt.title('Complexity analysis X vs Y4')
plt.show()

#3.7 plot
#Plot 6    X vs Y, Y2, Y3 and Y4
plt.plot(X, Y)
plt.plot(X, Y2)
plt.plot(X, Y3)
plt.plot(X, Y4)
plt.legend(['BST', 'Linear', 'Logarithmic', 'LL'])
plt.xlabel('Size of trees')
plt.ylabel('Search time')
plt.ticklabel_format(axis='both', style='sci', scilimits=(0, 0))
plt.title('Complexity analysis X vs Y, Y2, Y3 and Y4')
plt.show()

# My Comments is as follows:
'''
Complexity analysis X vs Y:

The generated graph is similar to a sub-linear complexity plot. This means that as size of trees (X) increases, the search time (Y) 
grows but its rather slow as compared to linear. It also suggestes that BST search has a better-than-linear complexity which
indicates efficient search times.

Complexity analysis X vs Y, Y2 and Y3:

The generated graph for Y2 is linear (as expected). The generated graph for Y3 is logarithmic (as expected). When we compare
initial graph with linear and logarithmic graphs, it appears that our initial graph is somewhere between linear and logarithmic.
It does not exactly follow linear or logarithmic. The reasons for this could be:

1. Imbalanced tree: Since we are randomly generating trees for this experiment, it can cause search time to be linear or
somewhat linear. To combat this we need to ensure that all the trees are balanced. This can be implemented in a method in the
class itself.

2. Search Algorithm: It could be possible that if searching is not properly implemented, it can lead to increased search times
and which in turn causes the shape of the graph to change drastically as size of tree increases. We need to ensure that the
search method defined is optimal.

Complexity analysis X vs Y, Y2, Y3 and Y4:

The generated graph for Y4 shows linear complexity. This suggests that linked lists have linear-time complexity.
It is closer to Y2, which is also linear. Linear complexity makes searching slower. Out of Y, Y2, Y3 and Y4, 
Y seems to most optimal (sub-linear), followed by Y3 (logarithmic), followed by Y2 (linear BST) and Y3 (linear linked list).The
difference in complexity arises from the fundamental differences in data structure design. BSTs provide faster
search times due to their hierarchical structure and binary search properties.
'''




'''

References:-
1)SYMPY - https://www.sympy.org/en/index.html
2)TQDM - https://github.com/tqdm/tqdm
3) https://www.geeksforgeeks.org/
'''
