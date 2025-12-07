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



#region Simulate Randomisationa

'''
    Simulates the ZX-80 random number generator.
    Generates a pseudo-random series of integers from 0 to 255.
    This is a simplified version of the ZX-80 random number generator.
    In ZX80, the random number generator is based on a linear feedback shift register (LFSR) algorithm.
    Using the same base positive number, the series will always be the same.
    This is a simulation of that process, not an exact replica.
'''
# series = []

def generate_random_zx80_series(seed:int):
    '''
    This method is designed to simulate the ZX80's pseudo-random number generator (PRNG).
    The ZX80 used a specific Linear Congruential Generator (LCG) algorithm.
    '''
    modulas = 65537
    multiplier = 75
    increment = 1
    new_seed = float(seed % modulas)
    series = []
    for _ in range(26):
        # apply the lcg formula to generate the next seed value
        new_seed = (multiplier * new_seed + increment) % modulas
        # genberate the random number in float
        rnd = new_seed / modulas
        # convert float to int and scale it 1-26
        series.append(int(rnd * 26) + 1)
    return series

# def get_code_number(index):
#     """
#     Returns the code number for the given index.
#     The index should be between 0 and 25.
#     """
#     global series
#     if 0 <= index < len(series):
#         return series[index]
#     else:
#         raise IndexError("Index out of range. Must be between 0 and 255.")


#endregion // END Simulate Randomisation


#region Simulate ZX80 character set map
'''
    Sinclair ZX80 character set map is very different from the ASCIIT character map
    Using the logic in the original listing will work on ASCII characters
    And it is not feasible to usee the ZX80 character set map in this scenario
    Therefore we are simulating the alph-numeric characters
'''

alpha_numeric_charset =['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                       'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                       'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                       'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd',
                       'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                       'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                       'y', 'z']

def determine_zx80_char_code(char: str)-> int:
    if char in alpha_numeric_charset:
        return alpha_numeric_charset.index(char) + 1 #zx80 codes start from 1
    else:
        return 0 # return 0 for non alpha numberic characters
    
def determine_zx80_char_from_code(code: int)-> str:
    if 0< code<= len(alpha_numeric_charset):
        return alpha_numeric_charset[code - 1] # zx80 codes start from 1
    else:
        return '' # empty string for invalid codes

#endregion // END Simulate ZX80 Character set map

#region Prompt user for input and key

# def method to ask for message to encode/decode
def get_message():
    """
    Prompts the user for a message to encode or decode.
    Returns the message as a string.
    """
    return input("Enter the message to encode/decode: ").strip()

def get_key():
    """
    Prompts the user for a key to use for encoding or decoding.
    Returns the key as an integer.
    """ 
    while True:
        try:
            key = int(input("Enter the key 1 to 26 (-ve val to decode): ").strip())
            if -26 <= key <= 26 and key != 0:
                return key
            else:
                print("Key must be between -26 and 26 (zeros not allowed).")
        except ValueError:
            print("Invalid input. Please enter a number between -26 and 26.")



#endregion // END Prompt user for input and key

#region Encode/Decode message
'''
def encode_message_ai(message, key):
    """
    Encodes the message using the provided key.
    The key is used to determine the offset for each character in the message.
    """
    encoded_message = []
    for char in message:
        if char.isalpha():
            # Get the ASCII value of the character
            ascii_value = ord(char)
            # Get the code number based on the key
            code_number = get_code_number((key + 256) % 256)
            # Encode the character by adding the code number
            encoded_char = chr((ascii_value + code_number) % 256)
            encoded_message.append(encoded_char)
        else:
            # If the character is not a letter, keep it unchanged
            encoded_message.append(char)
    return ''.join(encoded_message)



def decode_message_ai(encoded_message, key):
    """
    Decodes the message using the provided key.
    The key is used to determine the offset for each character in the encoded message.
    """
    decoded_message = []    
    for char in encoded_message:
        if char.isalpha():
            # Get the ASCII value of the character
            ascii_value = ord(char)
            # Get the code number based on the key
            code_number = get_code_number((key + 256) % 256)
            # Decode the character by subtracting the code number
            decoded_char = chr((ascii_value - code_number) % 256)
            decoded_message.append(decoded_char)
        else:
            # If the character is not a letter, keep it unchanged
            decoded_message.append(char)
    return ''.join(decoded_message)

def encode_decode_message_zx80(message, key):
    encoded_message = []
    code_number = get_code_number(25) #abs(key) - 1)
    if key < 0:
        code_number = 26 - code_number #  -1 * code_number
    for char in message:
        ascii_val = ord(char) # we get the ASCII code of the char, like using CODE() in ZX80
        # encode the character
        encoded_val = ascii_val + code_number - 38
        if key > 0:
            encoded_val = encoded_val - 26 * (encoded_val // 26) # this is like using MOD 26 in ZX80
        else:
            # in original listing, this is not needed, I suspect because of the the charqacters set and codes used
            # but for ascii characters, we need to reverse the encoding formula 
            encoded_val = encoded_val + 26 * (encoded_val // 26)
        encoded_val += 38

        print(f'Char: {char} ASCII: {ascii_val} Code number: {code_number} Encoded value: {encoded_val} Chaencoded: {chr(encoded_val)}')
        encoded_message.append(chr(encoded_val))

    return ''.join(encoded_message)

'''

def encode_massage_zx80(message: str, key: int) -> str:
    '''
        message: string to encode
        key: int used to generate the random series. must be higher than 0
    '''
    encoded_msg = []
    rnd_series = generate_random_zx80_series(key)
    code_number = rnd_series[-1]
    for char in message:
        if char.isalpha() or char.isdigit():
            char_code = determine_zx80_char_code(char)
            encoded_val = char_code + code_number -38
            
            # implement modulas for 62 (number fo alphanumeric characters)
            encoded_val -= 62 * (encoded_val // 62) # this is like using MODE 62 in ZX80 
            

            # encoded_val += 38
            encoded_char = determine_zx80_char_from_code(encoded_val)
            encoded_msg.append(encoded_char)
            print(f'Char: {char} ASCII: {char_code} Code number: {code_number} Encoded value: {encoded_val} Char-encoded: {encoded_char}')
        else:
            encoded_msg.append(char)
    return ''.join(encoded_msg)


def decode_message_zx80(encoded_message:str, key: int) -> str:
    '''
        encoded_message: string to decode
        key: int used to generate the random series. must be lower than 0
    '''
    key *= -1 # convert to positive key
    decoded_msg = []
    rnd_series = generate_random_zx80_series(key)
    code_number = rnd_series[-1]
    for char in encoded_message:
        if char.isalpha() or char.isdigit():
            char_code = determine_zx80_char_code(char)
            decoded_val = char_code - code_number + 38

            # implement modulas for 62 (number fo alphanumeric characters)
            decoded_val += 62 * (decoded_val // 62) # this is like using MODE 62 in ZX80 

            # omitted the modulas 26 op for now
            # decoded_val -= 38
            decoded_char = determine_zx80_char_from_code(decoded_val)
            decoded_msg.append(decoded_char)
            print(f'Char: {char} ASCII: {char_code} Code number: {code_number} Encoded value: {decoded_val} Char-encoded: {decoded_char}')
        else:
            decoded_msg.append(char)
    return ''.join(decoded_msg)
#endregion // END Encode/Decode message

msg = get_message()
key = get_key()
# generate the series based on the key provided
# series = generate_random_zx80_series(abs(key))
# print(f'series: {series}')
'''
if key > 0:
    ai_encoded_message = encode_message_ai(msg, key)
    print(f'Message encoded with {key} using AI methoid: {ai_encoded_message}')
else:
    ai_decoded_message = decode_message_ai(msg, key)
    print(f'Message decoded using AI method: {ai_decoded_message}')
'''
# zx80_msg = encode_decode_message_zx80(msg, key)
# print(f'Message processed using zx80 method: {zx80_msg}')
# def main():

# print()
# print(generate_random_series(26))


if key > 0 :
    # encoding
    encoded_message = encode_massage_zx80(msg, key)
    print(f'Message encoded with {key} using psedu ZX80 method: {encoded_message}')
else:
    # decoding
    decoded_message = decode_message_zx80(msg, key)
    print(f'Message decoded with {key} using psedu ZX80 method: {decoded_message}')
    
# tmp_coded_val = 62
# print('lenb of alph-numeric codes: ', len(alpha_numeric_charset))
# print('Alpha num of 1-based code: ',alpha_numeric_charset[tmp_coded_val - 1])
# print('Alpha num of 1-based code: ',alpha_numeric_charset[tmp_coded_val + 1])