
"""
    Amanda Goh Shi Zhen
    32694113
"""

import sys


"""
    Generate all possible strings of length 'string_length'
    using an alphabet of size 'alphabet_size'

    Args:
    - alphabet_size (int): inputted alphabet size
    - string_length (int): inputted length

    Returns:
    - strings: List of strings generated
"""
def generate_strings(alpha_size, str_length):

    # An empty list for all the possible generate character
    alphabet = []

    # generate all the possible characters based on the alpha_size and append into the created list 'alphabets'
    for i in range(alpha_size):
        character = chr(ord('a') + i)
        alphabet.append(character)

    # Check if the length of the string is 0
    if str_length == 0:
        return ['']

    # Empty list for storing the possible string
    strings = []

    # Loop through the alphabets list
    for char in alphabet:

        # Loop through the strings list
        for string in generate_strings(alpha_size, str_length - 1):
            strings.append(char + string)

    # Return the generated strings
    return strings


"""
    Count the number of strings with at least 2, exactly n, and
    exactly 1 distinct cyclic rotations.

    Args:
    - strings (str): strings generated
    - n (int): inputted length

    Returns:
    - count_moreThanEqualsTwo: integer count of distinct that is more than equals to 2
    - count_exactlyN: integer count of distinct that is exactly n
    - count_exactlyOne: integer count of distinct that is exactly 1
"""
def dist_cyclic_rot(strings, n):

    # Initialize the count of strings with at least 2, exactly n, and exactly 1
    count_moreThanEqualsTwo = 0
    count_exactlyOne = 0
    count_exactlyN = 0

    # Go through each string in the list strings
    for string in strings:

        # Count the number of rotations for the current string
        num_rotations = count_dist_cyclic_rot(string)

        # Check if the number of rotations is more than equals to 2
        if (num_rotations >= 2):

            # Increment the count
            count_moreThanEqualsTwo += 1
            
        # Check if the number of rotations is exactly 1
        if (num_rotations == 1):

            # Increment the count
            count_exactlyOne += 1

        # Check if the number of rotations is exactly n
        if (num_rotations == n):

            # Increment the count
            count_exactlyN += 1

    # Return all the counting for different situation
    return count_moreThanEqualsTwo, count_exactlyN, count_exactlyOne


"""
    Count the number of distinct cyclic rotations of a given string.

    Args:
    - string (str): string generated

    Returns:
    - len(rotations): the number of rotation for the string
"""
def count_dist_cyclic_rot(string):

    # Initialize an empty list to store unique rotations of the string
    rotations = []

    # Loop through each character index in the string
    for i in range(len(string)):

        # Generate a rotation by slicing the string from index i to the end and appending the start to index i
        rotation = string[i:] + string[:i]

        # Add the generated rotation to the list only if it's not already present
        if rotation not in rotations:
            rotations.append(rotation)

    # Return the number of unique rotations in the list
    return len(rotations)


"""
    Check if 'count' is an integer multiple of 'n'.

    Args:
    - count (int): the number of distinct or more than or equals to 2
    - n (int): inputted length

    Returns:
    - true (bool): the count is an integer multiple of n
    - false (bool): the count is not an integer multiple of n
"""
def check_intMultN(count, n):

    # Check if the count is divisible by n without any remainder
    if count % n == 0:

        # if there's no remainder it will return True
        return 'true'

    # if there's remainder it will return False
    else:
        return 'false'


"""
    Main function to handle the input, validate constraints, generate strings,
    and perform checks for the number of distinct cyclic rotations.
"""
def main():

    # Check if the argument inputted is not 3, if not then it will print the string
    if len(sys.argv) != 3:
        print('Incorrect input. It should be python q1.py <alphabet size> <string length>')
        return
    
    # set the alphabet size base on the inputted value
    alphabet_size = int(sys.argv[1])

    # set the string length base on the inputted value
    string_length = int(sys.argv[2])

    # Check if the alphabet size inputted is out of the range of 1 to 5
    if 5 < alphabet_size < 1:
        print('Incorrect input. Alphabet size should be within the range [1, 5]')
        return
    
    # Check if the string length inputted is out of the range 1 to 10
    if 10 < string_length < 1:
        print('Incorrect input. String length should be within the range [1, 10]')
        return
    
    # Generate the possible strings based on the inputs
    strings = generate_strings(alphabet_size, string_length)

    # Get the number of distinct for each category needed (>= 2, == N, == 1)
    count_moreThanEqualsTwo, count_exactlyN, count_exactlyOne = dist_cyclic_rot(strings, string_length)

    # Check if count_moreThanEqualsTwo is an integer multiple of N
    check_moreThanEqualsTwo_intMultN = check_intMultN(count_moreThanEqualsTwo, string_length)

    # Final Output
    print(f"Input values:\n{alphabet_size} {string_length}")
    print(f"Output:\n{count_moreThanEqualsTwo} {count_exactlyN} {count_exactlyOne} {check_moreThanEqualsTwo_intMultN}")


"""
    Call the main function
"""
if __name__ == "__main__":
    main()

