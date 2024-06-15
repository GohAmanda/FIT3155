
"""
    Amanda Goh Shi Zhen
    32694113
"""

import sys


class BTreeNode:

    """
        Initialize a B-tree node.

        Args:
        - t (int): Minimum degree of the B-tree.
        - leaf (bool): Indicates if the node is a leaf node (default False).
    """
    def __init__(self, t, leaf=False):

        # Minimum degree
        self.t = t

        # True if leaf node
        self.leaf = leaf

        # List of keys
        self.keys = []
        
        # List of children
        self.children = []


class BTree:

    """
        Initialize a B-tree.

        Args:
        - t (int): Minimum degree of the B-tree.
    """
    def __init__(self, t):
        self.t = t  # Minimum degree
        self.root = BTreeNode(t, True)


    """
        Traverse the B-tree and return a sorted list of keys.

        Returns:
        - list: Sorted list of keys in the B-tree.
    """
    def traverse(self):
        nodes = []
        self.traverse_Btree(self.root, nodes)
        return nodes


    """
        Function to traverse the B-tree.

        Args:
        - node (BTreeNode): Current node being traversed.
        - nodes (list): List to store keys of the nodes in traversal order.
    """
    def traverse_Btree(self, node, nodes):

        # Traverse all keys in the node
        for i in range(len(node.keys)):

            # If the node is not a leaf, traverse the children
            if not node.leaf:
                self.traverse_Btree(node.children[i], nodes)
            
            # Append the key to the list
            nodes.append(node.keys[i])

        # Traverse the last child if the node is not a leaf
        if not node.leaf:
            self.traverse_Btree(node.children[len(node.keys)], nodes)


    """
        Search for a key in the B-tree.

        Args:
        - k: Key to search for.
        - node (BTreeNode): Current node being examined.

        Returns:
        - BTreeNode or None: Node containing the key, or None if not found.
    """
    def search_key(self, k, node=None):
        if node is None:
            # Start search from root
            node = self.root

        # Initialize index
        i = 0

        # Find the first key greater than k
        while i < len(node.keys) and k > node.keys[i]:
            i += 1

        # If key is found, return the node
        if i < len(node.keys) and node.keys[i] == k:
            return node

        # If node is a leaf and key is not found, return None
        if node.leaf:
            return None

        # Recursive to the appropriate child
        return self.search_key(k, node.children[i])


    """
        Insert a key into the B-tree.

        Args:
        - k: Key to insert.
    """
    def insert(self, k):

        # Get the root
        root = self.root
        maxKey = 2 * self.t - 1

        # Check if the root node is full, if it is then do splitting
        if len(root.keys) == maxKey:

            # Create a new root
            temp = BTreeNode(self.t, False)

            # Set new root
            self.root = temp

            # Make previous root as child of new root
            temp.children.insert(0, root)

            # Split the previous root
            self.split(temp, 0)

            # Insert the key into the new root
            self.insert_key(temp, k, maxKey)

        else:

            # Insert the key into the root
            self.insert_key(root, k, maxKey)


    """
        Function to insert a key into a B-tree.

        Args:
        - node (BTreeNode): Current node being examined.
        - k: Key to insert.
        - maxKey: maximum number of item allowed in the node
    """
    def insert_key(self, node, k, maxKey):

        # Start from the last key
        i = len(node.keys) - 1

        # If node is a leaf, insert the key directly
        if node.leaf:

            # Append a dummy key to extend the list
            node.keys.append(None)

            # Shift keys greater than k
            while i >= 0 and k < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1

            # Insert the key
            node.keys[i + 1] = k

        else:

            # Find the child to insert the key
            while i >= 0 and k < node.keys[i]:
                i -= 1
            i += 1

            # If the child is full, split it
            if len(node.children[i].keys) == maxKey:
                self.split(node, i)

                # After split, determine which child to insert into
                if k > node.keys[i]:
                    i += 1

            # Recursive to insert the key
            self.insert_key(node.children[i], k, maxKey)


    """
        Split a child node of the B-tree.

        Args:
        - node (BTreeNode): Parent node containing the child to split.
        - i (int): Index of the child node to split.
    """
    def split(self, node, i):

        # Minimum degree
        t = self.t

        # Child that needs to be split
        y = node.children[i]

        # New node to store (t-1) keys of y
        z = BTreeNode(t, y.leaf)

        # The minimum item in the node
        minItem = t-1

        # The maximum item in the node
        maxItem = 2*t -1

        # The maximum child in the tree
        maxChild = 2*t

        # Insert the new child into the parent
        node.children.insert(i + 1, z)

        # Move the middle key of y to the parent
        node.keys.insert(i, y.keys[minItem])

        # Copy the last (t-1) keys of y to z
        z.keys = y.keys[t:(maxItem)]

        # Reduce y to (t-1) keys
        y.keys = y.keys[0:(minItem)]

        # If y is not a leaf, move the last t children of y to z
        if not y.leaf:
            z.children = y.children[t:(maxChild)]
            y.children = y.children[0:t]


    """
        Delete a key from the B-tree.

        Args:
        - k: Key to delete.
    """
    def delete(self, k):

        # Start deletion from root
        self.delete_key(self.root, k)

        # If root becomes empty
        if len(self.root.keys) == 0:

            # If root is not a leaf, make the first child the new root
            if not self.root.leaf:
                self.root = self.root.children[0]

            # If root is a leaf, reset the tree
            else:
                self.root = BTreeNode(self.t, True)


    """
        Function to delete a key from the B-tree.

        Args:
        - node (BTreeNode): Current node being examined.
        - k: Key to delete.
    """
    def delete_key(self, node, k):

        # Minimum degree
        t = self.t

        # Initialize index
        i = 0

        # Find the key in the current node
        while i < len(node.keys) and k > node.keys[i]:
            i += 1
        
        # If key is found
        if i < len(node.keys) and node.keys[i] == k:

            # If the node is a leaf, remove the key
            if node.leaf:
                node.keys.pop(i)
            
            # If the node is not a leaf
            else:

                # If the child before the key has at least t keys
                if len(node.children[i].keys) >= t:

                    # Get the smallest previous key of the current key
                    prev = self.smaller(node, i)

                    # Replace key with the previous key
                    node.keys[i] = prev

                    # Delete the previous key
                    self.delete_key(node.children[i], prev)

                # If the child after the key has at least t keys
                elif len(node.children[i + 1].keys) >= t:

                    # Get the next largest key of the current key
                    after = self.larger(node, i)

                    # Replace key with next key
                    node.keys[i] = after

                    # Delete the next key
                    self.delete_key(node.children[i + 1], after)

                # If both children have less than t keys, merge them
                else:
                    self.merge(node, i)

                    # Delete the key from the merged node
                    self.delete_key(node.children[i], k)

        # Check if the node is not a leaf
        elif not node.leaf:

            # Check if the node is at the minimum allowed of keys
            if len(node.children[i].keys) == t-1:

                # if it is then, it will have to perform the correct action
                self.minKey_Occurs(node, i)

            # Adjust the index if needed after the minKey occurs
            if i == len(node.keys) and i > len(node.children):
                self.delete_key(node.children[i - 1], k)

            else:
                self.delete_key(node.children[i], k)


    """
        Get the previous key that is smaller than the given key.

        Args:
        - node (BTreeNode): Node containing the key.
        - i (int): Index of the key in the node.

        Returns:
        - key.
    """
    def smaller(self, node, i):

        # Go to the left child
        current = node.children[i]

        # Find the rightmost leaf in the subtree
        while not current.leaf:
            current = current.children[len(current.keys)]

        # Return the last key
        return current.keys[len(current.keys) - 1]


    """
        Get the next key that is larger than the given key.

        Args:
        - node (BTreeNode): Node containing the key.
        - i (int): Index of the key in the node.

        Returns:
        - key.
    """
    def larger(self, node, i):

        # Go to the right child
        current = node.children[i + 1]

        # Find the leftmost leaf in the subtree
        while not current.leaf:
            current = current.children[0]

        # Return the first key
        return current.keys[0]


    """
        Fill a child node that has t-1 keys.

        Args:
        - node (BTreeNode): Parent node.
        - i (int): Index of the child node in the parent node.
    """
    def minKey_Occurs(self, node, i):

        # If previous sibling has more than t-1 keys
        if i != 0 and len(node.children[i - 1].keys) >= self.t:
            self.borrow_prev_sibling(node, i)

        # If next sibling has more than t-1 keys
        elif i != len(node.keys) and len(node.children[i + 1].keys) >= self.t:
            self.borrow_next_sibling(node, i)

        # If both siblings is equal t-1 keys
        else:

            # If the child is not the last child
            if i != len(node.keys):
                self.merge(node, i)

            # If the child is the last child
            else:
                self.merge(node, i - 1)


    """
        Borrow a key from the previous sibling of the node.

        Args:
        - node (BTreeNode): Parent node.
        - i (int): Index of the child node in the parent node.
    """
    def borrow_prev_sibling(self, node, i):

        # Child node
        child = node.children[i]

        # Previous sibling node
        sibling = node.children[i - 1]

        # Move the key from parent to the child
        child.keys.insert(0, node.keys[i - 1])

        # Move the sibling's last child to the child node if not leaf
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())
        
        # Move the sibling's last key to the parent
        node.keys[i - 1] = sibling.keys.pop()


    """
        Borrow a key from the next sibling of the node.

        Args:
        - node (BTreeNode): Parent node.
        - i (int): Index of the child node in the parent node.
    """
    def borrow_next_sibling(self, node, i):

        # Child node
        child = node.children[i]

        # Next sibling node
        sibling = node.children[i + 1]

        # Move the key from parent to the child
        child.keys.append(node.keys[i])

        # Move the sibling's first child to the child node if not leaf
        if not child.leaf:
            child.children.append(sibling.children.pop(0))

        # Move the sibling's first key to the parent
        node.keys[i] = sibling.keys.pop(0)


    """
        Merge a child node with its sibling.

        Args:
        - node (BTreeNode): Parent node.
        - i (int): Index of the child node in the parent node.
    """
    def merge(self, node, i):

        # Child node
        child = node.children[i]

        # Next sibling node
        sibling = node.children[i + 1]

        # Move the key from parent to the child
        child.keys.append(node.keys.pop(i))

        # Move all keys from sibling to child
        child.keys.extend(sibling.keys)

        # Move all children from sibling to child if not leaf
        if not child.leaf:
            child.children.extend(sibling.children)
        
        # Remove the sibling from the parent node
        node.children.pop(i + 1)


"""
    Read a file and return its contents as a list of lines.

    Args:
    - file_path (str): Path to the file.

    Returns:
    - list: List of lines in the file.
"""
def read_file(file_path):

    # Open the file for reading
    with open(file_path, 'r') as file:

        # Read and split the lines
        lines = file.read().strip().split('\n')
    
    # Return the list of lines
    return lines


"""
    Main function to execute the B-tree operations based on input files.
"""
def main():

    # Check if the number of arguments is correct
    if len(sys.argv) != 4:

        # Print usage information
        print("Usage: python q2.py <t> <dictionary.txt> <commands.txt>")

        # Exit the function
        return

    # Minimum degree of the B-tree
    t = int(sys.argv[1])

    # Path to the dictionary file
    dictionary_file = sys.argv[2]

    # Path to the commands file
    commands_file = sys.argv[3]

    # Read dictionary words
    dictionary_words = read_file(dictionary_file)

    # Read commands
    commands = read_file(commands_file)

    # Create a B-tree with minimum degree t
    btree = BTree(t)

    # Insert all words from the dictionary into the B-tree
    for word in dictionary_words:
        btree.insert(word)

    # Execute commands on the B-tree
    for command in commands:

        # Split each command into action and word
        action, word = command.split()

        # If action is insert
        if action == "insert":

            # Insert word if it does not exist in the B-tree
            if not btree.search_key(word):
                btree.insert(word)
        
        # If action is delete
        elif action == "delete":

            # Delete word if it exists in the B-tree
            if btree.search_key(word):
                btree.delete(word)

    # Traverse the B-tree to get sorted words
    sorted_words = btree.traverse()

    # Write sorted words to output file
    with open('output_q2.txt', 'w') as output_file:

        # For each word in sorted words
        for word in sorted_words:

            # Write the word to the file
            output_file.write(word + '\n')


if __name__ == "__main__":

    # Call the main function
    main()
