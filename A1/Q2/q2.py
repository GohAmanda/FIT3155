"""
    Student ID: 32694113
    Name: Amanda Goh ShiZhen
"""

import sys

# Function to read the content of a file and return it as a string
def read_file(file_path: str) -> str:
    f = open(file_path, 'r')
    line = f.readlines()
    f.close()

    return line



# Function that will count all the bitvectors
def count_bitvectors(text, pattern):

    # the length of pattern
    m = len(pattern)

    # the legnth of text
    n = len(text)

    # create a empty list for storing all the bitvector
    bitvectors = []

    # create a empty list for storing the bitvector m
    bitvector_m = []

    # Compare text and pattern for the first m characters
    for i in range(m):

        # check if the character is the same
        if text[i] == pattern[i]:

            # add bit 0 into the bitvector_m list
            bitvector_m.append(0)
        
        # if the character is different
        else:

            # add bit 1 into the bitvector_m list
            bitvector_m.append(1)
        
    # add the bitvector_m into the bitvectors
    bitvectors.append(bitvector_m)

    # Compare text[m+j] with pattern[0] to pattern[m-1] in reverse order
    # compare the text m+1 with the pattern in reverse
    for j in range(n - m  + 1): 

        # create a empty list for delta
        delta = []

        # loop through the pattern in reverse
        for k in range(m - 1, -1, -1):

            # check if within the text
            if m+j < n:
                
                # within the text
                # Compare the text and pattern characters
                if text[m + j] == pattern[k]:
                        
                        # if the text and pattern character matches, add bit 0 
                        delta.append(0)
                else:
                        # if not match, add bit 1
                        delta.append(1)
            
            # if not within the text
            else:

                # break the loop since out of text
                break
        
        # getting the previous bitvector of the current delta
        prev_bit = bitvectors[-1]

        # shift on bit to the left for the previous bitvector
        prev_bit_shift = shift_left(prev_bit)

        # create an empty list to store the next bitvector
        next_bitvector = []

        # combine shifted previous bitvector with delta using the bitwise OR operation
        for i in range(len(delta)):
             next_bitvector.append(prev_bit_shift[i] | delta[i])

        # add the new bitvector into the lists bitvectors
        bitvectors.append(next_bitvector)
 
    # return the bitvectors
    return bitvectors



# Function that shifts the bitvector to the left by 1              
def shift_left(bitvector):
   
   # update the bitvector by shifting to the left (add a 0 at the right)
   shifted_bitvector = bitvector[1:] + [0]

   # return the shifted bitvector
   return shifted_bitvector



# Function that checks if there's a match between the pattern and the text using the bitvectors
def check_match(text, pattern):

    # getting the bitvectors by calling the count_bitvectors method
    # passing in the parameter text and pattern
    bitvectors = count_bitvectors(text, pattern)

    # get all the bitvector that are not empty
    non_empty_bitvectors = []

    # create an emtpy list that will store the matching positions
    match_pos = []

    # for checking whether the bitvector for the first m characters are all 0's
    all_0 = True

    # iterate over each bitvector
    for bitvector in bitvectors:

        # Check if the sublist is not empty
        if bitvector:

            # Add non-empty sublist to the new list
            non_empty_bitvectors.append(bitvector)

    # naming the first non empty bitvectors as 1st bitvector
    first_bitvector = non_empty_bitvectors[0]

    # Check if the 1st bitvector contains all 0's
    for bit in first_bitvector:

        # if there's bit that is 1 , means no matching for the first m characters
        if bit == 1:

            # set all_0 as false
            all_0 = False

            break
    
    # if all the bit in the 1st bitvector is all 0's
    if all_0:

        # add this position into the match_pos
        match_pos.append(1)
    
    # Check if the rest of the non empty bitvectors has a matching pos
    for i in range(1, len(non_empty_bitvectors)):
        if bitvectors[i][0] == 0:

            # if there's a matching , the position will be added into match_pos
            match_pos.append(i+1)

    # return all the matching position
    return match_pos



if __name__ == "__main__":
    _, text, pattern = sys.argv

    # the following code will read the file of text and pattern 
    txtcontent = [line.strip() for line in read_file(text)]
    patcontent = [line.strip() for line in read_file(pattern)]

    # create a text file that will show the output of the program
    f = open('output_q2.txt', 'w')

    # run the function check match to get the matching positions
    for pat in patcontent:
        for text in txtcontent:
            positions = check_match(text,pat)

            # print each of the position on a new line
            for pos in positions:
                f.write(str(pos) + '\n')

