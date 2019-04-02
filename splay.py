class Node(object):

    def __init__(self, value):
        self.value = value  # The node value
        self.left = None    # Lesser
        self.right = None  # Greater

class SplayTree:

    def OrdinaryComparison(a,b):
        if a < b: return -1
        if a == b: return 0
        return 1

    def __init__(self, comparator = OrdinaryComparison):
        self.root = None
        self.cmpfunc = comparator

    def insert(self,V):
        # inserts a new value
        if not self.root: #inserts when head has no value
          self.root = Node(V)
          self.root.parent = None
        else:
          current_node = self.root
          inserted = False
          while not inserted:
            # value is smaller than node's value
            if self.cmpfunc(V,current_node.value) <= 0:
              if current_node.left: # the current node has a smaller node
                current_node = current_node.left
              else: # creates a new node as the smaller node
                current_node.left = Node(V)
                current_node.left.parent = current_node
                inserted = True
                self.splay(current_node.left) # Splays at the end

            # value is larger than node's value
            elif self.cmpfunc(V,current_node.value) > 0:
              if current_node.right: # the current node has a larger node
                current_node = current_node.right
              else: # creates a new node as the larger node
                current_node.right = Node(V)
                current_node.right.parent = current_node
                inserted = True
                self.splay(current_node.right) #Splays at the end

    def splay(self, node):
        while node.parent:
            if node.parent.parent: #check to see if there is a grandparent node
                grandparent = node.parent.parent
                grand_to_parent = ""
                parent_to_node = ""
                if node.parent == grandparent.left:
                    grand_to_parent = "left"
                else:
                    grand_to_parent = "right"

                if node == node.parent.left:
                    parent_to_node = "left"
                else:
                    parent_to_node = "right"

                if grand_to_parent == parent_to_node: #zig zig
                    self.zig(node.parent)
                    self.zig(node)
                else: # zig zag
                    self.zig(node)
                    self.zig(node)
            else: # current node is one node away from root
                self.zig(node)

    def remove(self, value):
        self.find(value)
        if self.cmpfunc(self.root.value, value) != 0: # If the value that you want to remove is not in the tree
            return
        old_root = self.root
        largest_left_node = old_root.left
        if largest_left_node:
            largest_left_node.parent = None
            while largest_left_node.right:
                largest_left_node = largest_left_node.right
        if largest_left_node:
            self.splay(largest_left_node)
            self.root = largest_left_node
            if old_root.right:
                self.root.right = old_root.right
                self.root.right.parent = self.root
        elif old_root.right:
            self.root = old_root.right
            self.root.parent = None
        else:
            self.root = None

    def find(self, value):
        current_node = self.root
        while current_node:
            if self.cmpfunc(current_node.value, value) == 0:
                self.splay(current_node)
                return
            elif self.cmpfunc(current_node.value, value) > 0:
                if not current_node.left:
                    self.splay(current_node)
                    return
                current_node = current_node.left
            else:
                if not current_node.right:
                    self.splay(current_node)
                    return
                current_node = current_node.right

    def zig(self,node):
        grandparent = node.parent.parent
        if grandparent:
            if node.parent == grandparent.left:
                grandparent.left = node
            elif node.parent == grandparent.right:
                grandparent.right = node

        if node == node.parent.left:
            if node.right:
                node.right.parent = node.parent
            node.parent.left = node.right
            node.right = node.parent
            node.right.parent = node
        elif node == node.parent.right:
            if node.left:
                node.left.parent = node.parent
            node.parent.right = node.left
            node.left = node.parent
            node.left.parent = node
        node.parent = grandparent

        if node.parent == None:
            self.root = node

# If you want to use your own custom comparisons, make a function like the one below
# and use it as the argument when creating the Splay Tree
# def list_cmp(a,b):
#     if len(a) > len(b): return 1
#     elif len(a) == len(b): return 0
#     else: return -1
#
# s = SplayTree(list_cmp)
