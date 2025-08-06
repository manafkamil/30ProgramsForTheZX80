'''


    ENCODING

    From 30 Programmes for Sinclair ZX

    at: https://dn790005.ca.archive.org/0/items/30-programs-for-the-sinclair-zx-80-1-k/30_Programs_for_the_Sinclair_ZX80_1K.pdf

    From the original program printed in the book:

        An absolutely unbeatable method of producing secret messages! 
        As the key to the coding is the ZX-80 random number generator, it would be impossible for
        anyone without a ZX-80 (and a lot of patience) to crack such a message.
        To decode, just enter the negative of the code number that produced the message.

        XJYF BZ TRDUBXA !

        Variables:
            A$: message to be coded/decoded
            T: code number
            B: letter by letter value
                coded/ decoded

        Program description:
        160         Sets coding key
        190 - 280   Coding / decoding

'''

import os



#region Simulate Randomisation

'''
    Simulates the ZX-80 random number generator.
    Generates a pseudo-random series of integers from 0 to 255.
    This is a simplified version of the ZX-80 random number generator.
    In ZX80, the random number generator is based on a linear feedback shift register (LFSR) algorithm.
    Using the same base positive number, the series will always be the same.
    This is a simulation of that process, not an exact replica.
'''
series = [231, 255, 217, 21, 129, 148, 111, 54, 145, 184, 202, 187, 112, 136, 117, 133, 138, 93, 37, 172, 109, 103, 39, 210, 118, 199, 45, 71, 124, 204, 94, 122, 247, 229, 171, 205, 24, 128, 146, 240, 17, 241, 10, 65, 121, 144, 34, 116, 213, 98, 35, 160, 126, 36, 130, 228, 149, 5, 90, 134, 77, 125, 62, 127, 49, 196, 92, 11, 23, 154, 254, 28, 252, 195, 14, 233, 97, 190, 176, 223, 1, 76, 38, 206, 226, 68, 169, 106, 70, 222, 180, 48, 194, 162, 207, 75, 156, 108, 101, 234, 244, 47, 211, 8, 141, 74, 53, 236, 143, 175, 232, 82, 27, 161, 22, 119, 203, 212, 225, 182, 147, 230, 55, 91, 164, 242, 115, 239, 132, 185, 56, 218, 165, 51, 2, 69, 243, 67, 183, 151, 3, 235, 209, 140, 79, 63, 224, 84, 78, 44, 80, 58, 87, 178, 142, 6, 73, 250, 120, 150, 105, 20, 215, 181, 41, 167, 31, 33, 85, 64, 50, 191, 163, 159, 249, 179, 227, 135, 155, 72, 253, 102, 7, 40, 18, 153, 114, 131, 61, 208, 96, 100, 60, 52, 12, 89, 197, 214, 189, 32, 170, 0, 192, 16, 173, 107, 86, 193, 238, 42, 110, 166, 201, 139, 152, 246, 4, 83, 113, 59, 95, 157, 29, 158, 66, 237, 221, 25, 88, 57, 9, 168, 137, 245, 19, 186, 43, 174, 13, 46, 220, 81, 123, 99, 104, 15, 30, 248, 177, 216, 198, 188, 26, 251, 200, 219]


'''
# this is the function that generates the random series
# this series will change every time the program is run
# that is why we are using static value of the series here
def generate_random_series(length):
    """
    Generates a pseudo-random series of integers from 0 to 255.
    This simulates the ZX-80 random number generator.
    """
    global series
    if not series:
        series = [i for i in range(256)]
        for i in range(len(series) - 1, 0, -1):
            j = int.from_bytes(os.urandom(1), 'big') % (i + 1)
            series[i], series[j] = series[j], series[i]
    return series[:length]
'''

def get_code_number(index):
    """
    Returns the code number for the given index.
    The index should be between 0 and 255.
    """
    if 0 <= index < len(series):
        return series[index]
    else:
        raise IndexError("Index out of range. Must be between 0 and 255.")


#endregion // END Simulate Randomisation


s1 = generate_random_series(256)
s2 = generate_random_series(256)
s3 = generate_random_series(256)
s4 = generate_random_series(256)

# save all the series to one file
def save_series_to_file(filename):
    """
    Saves the generated random series to a file.
    """
    with open(filename, 'w') as f:
        f.write("Series 1:\n" + ', '.join(map(str, s1)) + '\n\n')
        f.write("Series 2:\n" + ', '.join(map(str, s2)) + '\n\n')
        f.write("Series 3:\n" + ', '.join(map(str, s3)) + '\n\n')
        f.write("Series 4:\n" + ', '.join(map(str, s4)) + '\n\n')






# test if the two series are identical
def are_series_identical():
    """
    Checks if the two generated random series are identical.
    """
    return s1 == s2

# assert two series are identical
def assert_series_identical():
    """
    Asserts that the two generated random series are identical.
    Raises an AssertionError if they are not.
    """
    assert are_series_identical(), "The two random series are not identical."
    return True

assert_series_identical()
if(are_series_identical()):
    print("The two random series are identical.")
save_series_to_file('random_series1.txt')