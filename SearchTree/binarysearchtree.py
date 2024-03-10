
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
    
    def get_val(self):
        return self.val

    def set_val(self, val):
        self.val = val

    def get_left(self):
        return self.left
    
    def set_left(self, left_1):
        self.left = left_1
    
    def get_right(self):
        return self.right
    
    def set_right(self, right_1):
        self.right = right_1

class BinarySearchTree:
    def __init__(self, limit = 0):
        self.root = None
        self.limit = limit

    def is_empty(self):
        return self.root is None
    
    def is_full(self):
        return self.limit and self.size() >= self.limit
    
    def size(self, node):
        if not node:
            node = self.root
        if node is None:
            return 0
        return 1 + self.size(node.get_left()) + self.size(node.get_right())
    

    #BST Insert
    def insert(self, val):
        node = TreeNode(val)
        if self.root is None:
            self.root = node
            return
        
        prev = None
        cur = self.root
        while cur is not None:
            if cur.get_val() > val:
                prev = cur
                cur = cur.get_left()
            elif cur.val < val:
                prev = cur
                cur = cur.get_right()
        if prev.val > val:
            prev.left = node
        else:
            prev.right = node

    #Print_Tree
    def print_tree(self):
        height = self.get_height(self.root)
        width = (1 << height) - 1
        res = [[''] * width for _ in range(height)]
        
        def fill(node, level, left, right):
            if not node:
                return
            mid = (left + right) >> 1
            res[level][mid] = str(node.val)
            fill(node.left, level + 1, left, mid - 1)
            fill(node.right, level + 1, mid + 1, right)
        
        fill(self.root, 0, 0, width - 1)
        for lst in res:
            print(lst)


    def get_height(self, node):
        return 0 if not node else 1 + max(self.get_height(node.get_left()), self.get_height(node.get_right()))
    
      # One step right and then always left
    def successor(self, root: TreeNode) -> int:
            root = root.get_right()
            while root.get_left():
                root = root.get_left()
            return root.get_val()
        
    # One step left and then always right
    def predecessor(self, root: TreeNode) -> int:
        root = root.get_left()
        while root.get_right():
            root = root.get_right()
        return root.get_val()

    #BST Delete
    def delete(self, root: TreeNode, key: int) -> TreeNode:
        if not root:
            return None

        # delete from the right subtree
        if key > root.get_val():
            root.right = self.delete(root.get_right(), key)
        # delete from the left subtree
        elif key < root.get_val():
            root.left = self.delete(root.get_left(), key)
        # delete the current node
        else:
            # the node is a leaf
            if not (root.get_left() or root.get_right()):
                root = None
            # the node is not a leaf and has a right child
            elif root.get_right():
                root.val = self.successor(root)
                root.right = self.delete(root.get_right(), root.get_val())
            # the node is not a leaf, has no right child, and has a left child    
            else:
                root.val = self.predecessor(root)
                root.left = self.delete(root.get_left(), root.get_val())
                        
        return root
    
    #BST Traverse
    def traverse(self):
        result = []
        self._traverse(self.root, result)
        return result

    def _traverse(self, node, result):
        if node:
            self._traverse(node.get_left(), result)
            result.append(node.get_val())
            self._traverse(node.get_right(), result)
    
    #BST Search
    def search(self, val):
        cur = self.root
        while cur:
            if val == cur.get_val():
                return True
            elif val < cur.get_val():
                cur = cur.get_left()
            else:
                cur = cur.get_right()
        return False






'''

References:-
1)What is binary search Tree- https://www.geeksforgeeks.org/binary-search-tree-data-structure/
2)Traversal- https://www.geeksforgeeks.org/binary-search-tree-traversal-inorder-preorder-post-order/
3)Searching in BST- https://www.geeksforgeeks.org/binary-search-tree-set-1-search-and-insertion/
4)Deletion in BST - https://www.geeksforgeeks.org/deletion-in-binary-search-tree/
5) Insertion in BST -https://www.geeksforgeeks.org/insertion-in-binary-search-tree/
6)https://www.geeksforgeeks.org/

'''
