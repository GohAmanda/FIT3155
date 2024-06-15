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



# Function to preprocess the bad character table for Boyer-Moore algorithm
def preprocess_bad_char_tbl(pattern):
    
    # A dictionary for bad character table
    bad_char_table = {}

    # Initialise the last occurence index of a character
    last_occurrence = -1

    # Iterates through the pattern backwards, from the last to the first character
    for i in range(len(pattern) - 1, -1, -1):

        # If the character are not in the bad character table
        if pattern[i] not in bad_char_table:

            # update the value
            bad_char_table[pattern[i]] = [0] * len(pattern)
            

        # Update the last occurence index for the character
        bad_char_table[pattern[i]][i] = i + 1

        # checks if last occurence updated from its initial value
        # If there is a previous occurence of the character
        if last_occurrence != -1:

            # iterates from the last_occurence to i
            # updates the bad_char_table for characters that occur between the current character and the 
            # last occurence of the same character
            for j in range(last_occurrence, i):
                
                # checks if the current character in the bad_char_table is zero
                if bad_char_table[pattern[i]][j] == 0:

                    # if it is zero, update it as the last_occurence
                    bad_char_table[pattern[i]][j] = last_occurrence

        # update the last_occurence to the current index
        last_occurrence = i
        
        # Fill positions recursively to the right
        for j in range(i + 1, len(pattern)):

            # Check if the value at index j that is in the bad character table equals to zero
            if bad_char_table[pattern[i]][j] == 0:

                # if value is zero, update it with the value from the previous index 
                bad_char_table[pattern[i]][j] = bad_char_table[pattern[i]][j - 1]

            else:

                # if value is not zero, it is already filled with value hence exit the loop
                break

    # return the bad character table
    return bad_char_table



# Function to flip a string
def flip(string):
    return string[::-1]



# Function to preprocess the Good suffix table that will be use in boyer moore
def preprocess_good_suffix_tbl(pattern):

    # A dictionary that will be used to store the good suffix table
    good_suffix_table = {}
    
    # calculate the z array values for the pattern
    z_array = cal_zArray_values(pattern)

    # calculate the values of gs using the z_array
    gs = cal_gsArray_values(z_array)

    # calculate the values of mp using the pattern
    mp = cal_mp_values(pattern)

    # reverse the z array 
    z_array.reverse()

    # show the z-array values, good-suffix-array values and the mp values in the a table form
    good_suffix_table['z-array'] = z_array
    good_suffix_table['gs'] = gs
    good_suffix_table['mp'] = mp

    # return the good suffix table
    return good_suffix_table



# Function to calculate the mp values that will be store in the good suffix table
# pass in the pattern as the parameter
def cal_mp_values(pattern):

    # flip the pattern
    flip_patt = flip(pattern)

    # calculate the z array for the flipped pattern
    z_array = cal_zArray_values(flip_patt)

    # the length of the z array
    m = len(z_array)

    # create a list of mp array depending on the length of the z array
    mp =  [0]*(m+1)
    
    for i in range(m):

        # sum of the z array value at index i and the current index
        sum = z_array[i] + i

        # check if the sum is equals to the length of z array
        if sum == m:

            # update the mp list of the index i with the value of the z array at index i
            mp[i] = z_array[i]
        
        # if not equals
        else:
            
            # update the mp list at index i with the value of the next mp value
            mp[i] = mp[i+1]

    # reverse the mp list
    mp.reverse()

    # set the previous non zero value
    prev_non_zero_val = 0

    for i in range(m):
        
        # check if the current value is not 0
        if mp[i] != 0:

            # save the non zero value into the prev_non_zero_val
            prev_non_zero_val = mp[i]

        # if the current value is 0    
        else:

            # update the current value with the previous non zero value
            mp[i] = prev_non_zero_val

    # return the mp list
    return mp



# Function to calculate the gs array values that will be store in the good suffix table
# pass in the z array as the parameter
def cal_gsArray_values(z_array):

    # the length of the z array
    m = len(z_array)

    #  create a new empty list called gs_array
    gs_array = [0] * (m + 1)
    
    for j in range(1, m + 1):
        # the the values in gs_array as 0
        gs_array[j] = 0
    
    # start from the right to the left
    for p in range(m - 1, 0, -1): 
        # calculate the value j 
        j =  z_array[p] - 1  

        # update the value of the gs_array index j with the new value 
        gs_array[j] = m - p
    
    # return the gs array
    return gs_array



# Function to calculate the z array values that will be store in the good suffix table
# pass in the pattern as the parameter
def cal_zArray_values(pattern):
    
    # the length of pattern
    n = len(pattern)

    # create a list with default values 0 in the length of pattern
    z_array_val = [0]*n

    # the the variable name left and right as 0
    left = right = 0

    for i in range(1, n):

        # case 1
        if i > right:
            left = right = i

            while right < n and pattern[right - left] == pattern[right]:
                right += 1
            z_array_val[i] = right - left
            right -= 1

        # if i <= right
        else:

            # calculate the index that will be used to get the z array value
            # distance between the index i with the left boundary 
            k = i - left

            # case 2a
            # check if the value in z array index k is less than the remaining (right - i + 1)
            if z_array_val[k] < right - i + 1:
                z_array_val[i] = z_array_val[k]
            
            # case 2b
            # the value in z array index k is more than or equals to the remaining (right - i + 1)
            else:

                # set the left value as the i
                left = i

                # increase the value of right boundary as long as the right boundary is less than n and 
                # the value of pattern at index right - left is equals to the value of pattern at index right
                while right < n and pattern[right -left] == pattern[right]:
                    right += 1
                
                # update the z array value at index i
                z_array_val[i] = right - left

                # decrease the right boundary by one
                right -= 1

    # return the z array values
    return z_array_val



# Function created for Boyer-Moore
# pass in text and pattern as the parameter
def boyer_moore(text, pattern):

    # the length of text
    n = len(text)

    # the length of pattern
    m = len(pattern)

    # create an empty list named positions, which will store the matching positions
    positions = []

    # Get the bad character table by calling the function that preprocess the bad character table 
    bad_character_table = preprocess_bad_char_tbl(pattern)

    # Get the good suffix table by calling the function that preprocess the good suffix table
    good_suffix_table = preprocess_good_suffix_tbl(pattern)
    
    # text index
    i = n-m 

    # the following code will run as long as i is less than and equals to n-m
    while i <= n-m:

        # update the newest start comparing index
        start_index = i 

        # pattern index
        j = 0

        # doing comparing between pattern and text
        # j and i will increase by 1 as long as the while condition is true
        while j < m and 0 <= i < n and pattern[j] == text[i]:
            j += 1
            i += 1

        # check if j is more than m-1, if true match is found
        if j > m-1:

            # add the matching position into the positions list
            positions.append(i-m+1)

            # update the value of j and i 
            j -= m
            i -= m+1

        # found a mismatch
        else:

            # if the entire text have been went through
            if i <= -1:

                # return all the positions
                return positions
    
            # getting the value of shift using bad character by calling the function that will do the calculation
            bc_shift = bc_noOfShift(bad_character_table, text, pattern, i, j)

            # getting the value of shift using the good suffix by calling the function that will do the calculation
            gs_shift = gs_noOfShift(good_suffix_table, pattern, j)
            
            # get the maximum shift between bad character and good suffix 
            max_shift = max(bc_shift, gs_shift)

            # shift the pattern according to the number of shifts
            start_index -= max_shift

            # update the index of i
            i = start_index

    # return the positions
    return positions



# Function that will count the number of shift when using bad character
# passed in the parameter of the bad character table, text, pattern, i and j
def bc_noOfShift(bad_character_table, text, pattern, i, j):

    # get the character from the text at index i
    char_text = text[i]

    # the length of the pattern
    m = len(pattern)

    # the following code will run as long as the character is found in the bad character table
    if char_text in bad_character_table:

        # get the number of shifts from the bad character table according to the character
        shifts = bad_character_table[char_text]

        # if j is less than the length of pattern
        if j < m:

            # update the value of R(x) with the value in shifts at index j
            R_x = shifts[j] 
        else:

            # update the value of R(x) as 0
            R_x = 0 

        # if the R(x) value is less than j
        if R_x < j:

            # the number of shifts will be j - R(x)
            return j - R_x

        # if the R(x) value is greater than or equals to j
        else:

            # the number of shifts will be 1
            return 1
        
    # if the character is not in the bad character table
    else:

        # the number of shifts will be m - j
        return m - j


# Function that will count the number of shift when using good suffix
# passed in the parameter of the good suffix table, pattern and j
def gs_noOfShift(good_suffix_table, pattern, j):

    # the length of pattern
    m = len(pattern)
    
    # if the value at the j-1 index in gs table is more than 0 
    if good_suffix_table['gs'][j - 1] > 0:

        # return the number of shifts
        return m - good_suffix_table['gs'][j - 1]
    
    # if the value at the j-1 index in gs table is equals to 0 
    elif good_suffix_table['gs'][j - 1] == 0:

        # return the number of shifts
        return m - good_suffix_table['mp'][j - 1]
    
    # if the value at the j-1 index in gs table is less than 0 
    else:

        # return the number of shifts
        return m - good_suffix_table['mp'][1]
        

if __name__ == "__main__":
    _, text, pattern = sys.argv

    # the following code will read the file of text and pattern 
    txtcontent = [line.strip() for line in read_file(text)]
    patcontent = [line.strip() for line in read_file(pattern)]

    # create a text file that will show the output of the program
    f = open('output_q1.txt', 'w')

    # run the function Boyer-Moore to get the matching positions
    for pat in patcontent:
        for text in txtcontent:
            # print each of the position on a new line
            positions = boyer_moore(text, pat)
            for position in positions:
                f.write(str(position) + '\n')
