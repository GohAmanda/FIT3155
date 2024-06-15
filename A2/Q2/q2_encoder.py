"""
    Student ID: 32694113
    Name: Amanda Goh Shi Zhen
"""

import sys

# Read the inputted file
def read_file(file_path:str) -> str:
    with open(file_path, 'r') as f:
        content = f.read().strip()
    return content


# This function will generate the Suffix array and the BWT
def generateSA_BWT(string):

    # length od the string
    strLen = len(string)

    # Array of structures to store rotations and their indexes
    arr = [(i, string[i:]) for i in range(strLen)]

    # Sorts rotations using comparison function defined above
    arr.sort(key=lambda x: x[1])

    # Stores the indexes of sorted rotations
    suffix_arr = [i for i, _ in arr]

    # Generate the BWT string
    bwt_str = generateBWT(string, suffix_arr, strLen)

    # Return the BWT string
    return bwt_str


# Generate the BWT
def generateBWT(string, suffix_arr, strLen):
    
    # creted to store all the last characters
    bwt_str = ""

    # Iterates over the suffix array to get the last char of each cyclic rotation
    for i in range(strLen):

        # Computes the last char
        j = suffix_arr[i] - 1
        if j < 0:
            j = j + strLen
        
        # add the last char into btw_str
        bwt_str += string[j]

    # Returns the computed Burrows-Wheeler Transform
    return bwt_str


# Generate the Elias bit for the bwt create, number of distinct and the length of the huffmans
def eliasBit(bwtLen, distLen, huffmansLen):

    # Getting the bwt elias bit
    bwtElias = '0' + eliasBitSing(bwtLen)

    # Getting the distinct elias bit
    distElias = '0' + eliasBitSing(distLen)

    # Create to store the huffmans elias
    huffmansElias = {}

    # Get the elias for each char and code in the huffmansLen
    for char, code in huffmansLen.items():
        codeLen = len(code)
        huffmansElias[char] = eliasBitSing(codeLen)

    # return the elias of bwt, distinct and huffmans
    return bwtElias, distElias, huffmansElias


# Generate the bit of the passed in parameter
def eliasBitSing(n):
    binN = bin(n)[2:]
    k = len(binN)
    
    code = '0' * (k-1) + binN

    return code


# Getting the unique number of characters from the string
def uniqueNo(string):
    uniqueStr = set(string)
    return len(uniqueStr)


# To get the length of the distinct characters and all the distinct characters
def countDist(s):

    # Stores all distinct characters
    s = set(s)
    s.remove('$')

    # Sort the characters
    sorted_str = ''.join(sorted(s)) + '$'

    # Return the size of the distinct characters and the distinct characters
    return len(sorted_str), sorted_str


# Encoding each character
def eachChar(s):

    # store all the created encoded character in
    encoded_chars = {}
    for i, char in enumerate(s):

        # Encode each character using 7-bit ASCII code
        encoded_chars[char] = format(ord(char), '07b')
    
    # return the encoded characters
    return encoded_chars


# Class of huffman tree
class HuffmanNode:
    def __init__(self, char, freq):

        # character
        self.char = char

        # frequency
        self.freq = freq

        # left child node
        self.left = None

        # right child node
        self.right = None


# Building the huffman tree for the given text
def build_huffman_tree(text):

    # A dictionary to store the fequency of each characters in the text
    freq = {}

    # Go through each character in the text
    for char in text:

        # If the character are already in the freq
        if char in freq:
            freq[char] += 1
        else:
            freq[char] = 1
    
    # List of huffmanNode objects, 1 for the character, and sort it by the frequency
    heap = [HuffmanNode(char, freq) for char, freq in freq.items()]
    heap.sort(key=lambda x: x.freq)
    
    # Build the huffman tree
    while len(heap) > 1:
        left = heap.pop(0)
        right = heap.pop(0)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heap.append(merged)
        heap.sort(key=lambda x: x.freq)

    # Return the root of the huffman tree
    return heap[0]


# Recursively build the huffman codes for the characters that is in the huffman tree
def build_huffman_codes(root, code='', codes={}):
    if root is not None:

        # if the current node is a leaf node
        # assign its huffman code to the character
        if root.char is not None:
            codes[root.char] = code

        # traverse through the left subtree with code 0
        build_huffman_codes(root.left, code + '0', codes)

        # traverse right subtree with code 1
        build_huffman_codes(root.right, code + '1', codes)
    return codes


# Encode the text using the huffman coding
def huffman_encoding(text):

    # check if the length of the text is 0, return as empty huffman codes and None
    if len(text) == 0:
        return {}, None
    
    # build a huffman tree for the text
    root = build_huffman_tree(text)

    # build the huffman codes for characters in the huffman tree
    codes = build_huffman_codes(root)

    # sort the huffman codes by the characters and ensuring that the last character is $
    sorted_codes = {char: codes[char] for char in sorted(codes.keys())}
    if '$' in sorted_codes:
        sorted_codes['$'] = sorted_codes.pop('$')

    # return the sorted huffman codes and the root of the huffman tree
    return sorted_codes, root


# Generate the output for the header part
def generate_output(encoded_bwt_length, encoded_distinct_length, cASCII, encoded_huffman_lengths, huffmanCodes):
    output = []
    
    # Concatenate Elias BWT length code and Elias Distinct length code
    output.append(encoded_bwt_length)
    output.append(encoded_distinct_length)
    
    # Concatenate ASCII, Elias code, and Huffman code for each character
    for char, ascii_code in cASCII.items():
        output.append(ascii_code)
        output.append(encoded_huffman_lengths[char])
        output.append(huffmanCodes[char])
    
    # returning the final joining output
    return ''.join(output)


# encode the run len of the btw using the huffman codes
def runLenEncode(bwt_str, huffmanCodes):

    encoding = []

    # Initialize the current character as the first character
    current_char = bwt_str[0]

    # Initialize the run length as 1
    run_length = 1
    
    # Iterate through the BWT string
    for char in bwt_str[1:]:

        # check if the current character is the same as the previous character
        if char == current_char:
            run_length += 1
        
        # if the it is different
        else:

            # append the character, run length, huffman code as tuple into the encoding
            encoding.append((current_char, run_length, huffmanCodes[current_char]))

            # update the current character
            current_char = char

            # reset the run length to 1
            run_length = 1
    
    # append the las tuple into the encoding list
    encoding.append((current_char, run_length, huffmanCodes[current_char]))
    
    # return the list of encoding tuples
    return encoding


if __name__ == "__main__":
    _, input_file = sys.argv

    # the inputted string by reading the file
    input_str = read_file(input_file)

    # Getting the BWT string
    bwtStr = generateSA_BWT(input_str)

    # The length of BWT
    bwtLen = len(bwtStr)

    # the distinct characters and the total number of distinct characters are generated
    distLen, distStr = countDist(bwtStr)

    # Generating the ASCII of each distinct characters
    charASCII = eachChar(distStr)

    # Encoding the btw string using the huffmans
    huffCodes, tree = huffman_encoding(bwtStr)

    # sort the huffmanCodes items gotton from the previous code
    sorted_huff_codes = dict(sorted(huffCodes.items()))

    # Generating the elias for BWT, distinct and the huffmans
    eliasBWT, eliasDIST, eliaseHUFF = eliasBit(bwtLen, distLen, huffCodes)

    # Generating the final bit for the header part
    headerPart = generate_output(eliasBWT, eliasDIST, charASCII, eliaseHUFF, huffCodes)

    # dataPart to store the final bit of the data part
    dataPart = ""

    # Encode the btw string with the huffman codes
    encoding = runLenEncode(bwtStr, huffCodes)

    # adding the bit for each char into the data part
    for char, run_length, huffman_code in encoding:

        # getting the elias code of the run length
        elias_code = eliasBitSing(run_length)
        dataPart += huffman_code + elias_code

    # Adding the final bit fo header part and data part together
    finalBit = headerPart + dataPart

    # Showing the final bit in a bin file
    with open("q2_encoder_output.bin", "wb") as f:
        f.write(finalBit.encode())








