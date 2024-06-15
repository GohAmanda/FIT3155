"""
    Student ID: 32694113
    Name: Amanda Goh Shi Zhen
"""

import sys

# Read the inputted file
def read_file(file_path:str) -> str:
    with open(file_path, 'r') as f:
        content = f.read()
    return content.strip()


# Class for Suffix tree
class SuffixTree(object):

    # class for the node in the suffix tree
    class Node(object):
        def __init__(self, lab):
            self.lab = lab # label
            self.out = {}  # dictionary for storing the outgoing edges from the node


    def __init__(self, s):

        # the root of the node
        self.root = self.Node(None)

        # add the 1st character of the string to the root
        self.root.out[s[0]] = self.Node(s)

        # go through the string starting from the 2nd character
        for i in range(1, len(s)):

            # start from the child node
            current = self.root
            j = i

            # Iterate through the string from the current pos to the end
            while j < len(s):

                # check f the character is already in the outgoing edges
                if s[j] in current.out:

                    # getting the child node
                    childNode = current.out[s[j]]

                    # the label of child node
                    lab = childNode.lab
                    k = j + 1

                    # check if the characters match
                    while k - j < len(lab) and s[k] == lab[k - j]:
                        k += 1

                    # check if the characters match completely
                    if k - j == len(lab):

                        # update the child node
                        current = childNode
                        j = k
                    
                    # if the characters do not match
                    else:

                        # create new node and adjust the tree
                        childExist, newChild = lab[k - j], s[k]

                        # new node with the common prefix
                        nodeNew = self.Node(lab[:k - j])

                        # add the new character into the new node
                        nodeNew.out[newChild] = self.Node(s[k:])

                        # move the existing child to the new node
                        nodeNew.out[childExist] = childNode

                        # update the lable of the existing child node
                        childNode.lab = lab[k - j:]

                        # update the outgoing edge of the current node
                        current.out[s[j]] = nodeNew
                else:

                    # add the remaining suffix to the new node
                    current.out[s[j]] = self.Node(s[j:])


    # follow the given path in the suffix tree
    def followPath(self, s):
        current = self.root
        i = 0
        while i < len(s):
            char = s[i]

            # if the character is not in the outgoing edges
            if char not in current.out:

                # return none
                return (None, None)
            
            # Get the child node
            child = current.out[s[i]]

            # Get the label of the child node
            lab = child.lab
            j = i + 1

            # Check if the characters match
            while j - i < len(lab) and j < len(s) and s[j] == lab[j - i]:
                j += 1

            # Check if the characters match completely
            if j - i == len(lab):

                # move the child node
                current = child
                i = j

            # Check if the path ends
            elif j == len(s):

                # return the child node and the offset
                return (child, j - i)
            
            # If characters does not match completely
            else:basicall
                # return none
                return (None, None)
        
        # return the current node and none
        return (current, None)


    # Check if the suffix tree contains a substring
    def hasSubstring(self, s):
        node, offset = self.followPath(s)
        return node is not None


    # Check if the suffix tree contains a particular suffix
    def hasSuffix(self, s):
        node, offset = self.followPath(s)
        if node is None:
            return False
        if offset is None:
            return '$' in node.out
        else:
            return node.lab[offset] == '$'


    # Traverse the suffix tree in inorder and append the suffixes to the array
    def inorder_aux(self, node, array, path=''):

        # check if node is none
        if node is None:
            return
        
        # check if the node represents a suffix
        if node.lab is not None and '$' in node.lab:

            # append to the array
            array.append(path + node.lab)

        # Recursively traverse the child nodes in sorted order
        for label, child in sorted(node.out.items()):
            self.inorder_aux(child, array, path + (node.lab if node.lab is not None else ''))


if __name__ == "__main__":
    _, text, position = sys.argv

    # Read the string content
    stringcontent = read_file(text)

    # Read the position content
    positioncontent = read_file(position)

    # Build the string suffix tree
    suffix_tree = SuffixTree(stringcontent)

    # Perform an inorder traversal of the suffix tree to get all suffixes
    result = []
    suffix_tree.inorder_aux(suffix_tree.root, result)
    suffixes = sorted(result)

    # Extract the positions from the position content
    positions = [int(x) for x in positioncontent.splitlines()]

    # Initialize an empty list for storing the final output
    output = []

    # Iterate through the positions
    for pos in positions:

        # extract the suffix string starting from the given position
        suffix = stringcontent[pos - 1:]

        # finding the rank of the duffix in the sorted list of all the suffixes
        rank = suffixes.index(suffix) + 1

        # Append the rank into the output list
        output.append(str(rank))

    # Write the output to a file
    with open('output_q1.txt', 'w') as f:
        f.write("\n".join(output))




