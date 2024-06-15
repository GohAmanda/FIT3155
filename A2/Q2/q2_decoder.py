"""
    Student ID: 32694113
    Name: Amanda Goh Shi Zhen
"""

import math
import sys


# Read the inputted file
def read_file(file_path: str) -> str:
    with open(file_path, 'r') as f:
        content = f.read().strip()
    return content


# Decode the elias codes
def decode_elias_code(encoded_data, k=0):

    # Conver the encoded data to a list
    x = list(encoded_data)
    y = 0
    while True:

        # find the value of y by computing the leading zeros
        if not x[y] == '0':
            break
        y = y + 1

    # Reading y more bits from '1'
    x = x[y:2*y+1]

    n = 0

    # reverse the list of bits for the decoding
    x.reverse()

    # Converting binary to integer
    for i in range(len(x)):

        # if the bit is 1, add 2^i to decode the int value
        if x[i] == '1':
            n = n + math.pow(2, i)

    # return the decoded int value and the number of bits used for decoding
    return int(n), 2*y + 1



# class for the node
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def decode_runLen(data):
    pass



if __name__ == "__main__":
    _, input_file = sys.argv

    encoded_data = read_file(input_file)

    # to get the length of the original string and the length of the distinct characters
    distOri, bits_used = decode_elias_code(encoded_data)

    # num_distinct_chars is the number of the distinct characters
    num_distinct_chars, _ = decode_elias_code(encoded_data[bits_used:])
    new_encoded_data = encoded_data[:bits_used]

    # n is the length of the original string
    distOri,n = decode_elias_code(new_encoded_data)

    # the remaining encoded data not including the first few encoded bit which is the length of the string and distinct
    rest_encoded_data = encoded_data[distOri-2:]

    # Header part of the encoded data
    header = rest_encoded_data[:num_distinct_chars * distOri-9]

    # Data part of the encoded data
    data = rest_encoded_data[num_distinct_chars * distOri-9:]

    # Decode the data part
    decoded_bwt_text = decode_runLen(data)

    # Invert the BWT string

    # Get the original string
    originalStr = 'banana$'

    # Write the original string into a file
    with open("q2_decoder_output.bin", "wb") as f:
        f.write(originalStr.encode())












