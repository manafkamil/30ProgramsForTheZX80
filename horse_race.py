'''
    HORSE RACE
    A day at the races without even having
    to leave the ZX-80! Four horses (A, B, C,
    and D) are assigned odds and you have £100
    betting money.

    Line 360 calculates how well the horse
    runs — the favourite is more predictable,
    but the long odds have more likelihood of
    being surprising.

    This program is very full, especially
    when the race is being run as the screen
    display occupies a lot of memory.

    The characters which make up the horses
    are (the shifted characters above the letters)
    A$: F,T,S. B$: (space),S,G,Q. C$: R, (space),
    (space), E.


    Variables: 	M Money left
                B Bet
                O(1)Odds for each horse
                D, D(I) Distance covered

    Sections in original listing:
        lines 50-130 : Declarations
        lines 130-160: Sub to print distance lapsed by one horse
        lines 170-270 : Reset variables
        lines 280-320 : User betting input
        lines 330-530 : Horse racing (4 laps)
        lines 540-580 : Print winner and calculate winnings
        lines 590-620 : Decide to play again?

        
    This version tries to closely replicate the BASIC listing


    basic programme tried on:
    - https://zx.researcher.su/en/


'''

import random
import os

O = [] #odds
MD = 0 #max distance, to replace D in original listing and eleminate confusion in the code
D = [0,0,0,0] #distance covered
M = 100 #money left
B = 0 # bet amount

# special characters for horses
# ASCIIT art from https://www.ascii-art.de/

# AS = '._/'
# BS = ' /~|'
# CS = '´  `'

AS = '            .\'\''
BS = '  ._.-.___.\' (`\\'
CS = ' //(        ( `\''
DS = '\'/ )\\ ).__. )   '
ES = '\' <\' `\\ ._/\'\\'
FS = '   `   \\     \\'

HORSE_ART = [AS, BS, CS, DS, ES, FS]

#region printing
def get_distance_marker(distance:int, factor :int = 1)-> str:
    '''
    for sub-routine in lines 130 to 160
    '''
    return '^' * distance * factor  # each unit of distance is represented by two '^' characters

def print_distance_marker(distance :int):
    '''
    for sub-routine in lines 130 to 160
    '''
    print(get_distance_marker(distance))


def print_ords():    
    '''
    for sub-routine in lines 130 to 160
    '''
    global O
    print("Odds for the horses are:")
    for i in range(4):
        print(f"Horse {chr(65 + i)}: {O[i]} to 1")

#endregion // END printing

def generate_odds():
    global O
    O = [random.randint(1, 10) for _ in range(4)]
    # print("Odds generated:", O)

def reset_variables():
    '''
    for sub-routine in lines 170 to 270
    '''
    global D, B, O
    D = [0, 0, 0, 0]  # Reset distances for each horse
    B = 0  # Reset bet amount
    O = []  # Reset odds

while M > 0:
    # 1 - reset variables
    reset_variables()
    # 2- generate odds
    generate_odds()
    print_ords()
    # 3 - get bet
    print(f'You have £{M} to bet.') 
    B = -1
    while B < 0:
        try:
            B = int(input("Enter your bet amount (enter 0 to exit): "))
            if B < 0 or B > M:
                print(f"Invalid bet amount. You can bet between 1 and {M}.")
                B = -1
        except ValueError:
            print("Please enter a valid integer for the bet amount.")
    if B == 0:
        break  # exit if bet is 0
    
    # 4 - get horse
    H = ''
    while H not in ['A', 'B', 'C', 'D']:
        H = input("Enter the horse you want to bet on (A, B, C, D): ").upper()
        if H not in ['A', 'B', 'C', 'D']:
            print("Invalid horse. Please choose A, B, C, or D.")
            H = ''

    # 5 - start racing
    '''
        for race logic in lines 330 to 530
    '''
    J = -1 # current winner
    MD = 0 # current max distance
    for l in range(4): # 4 laps
        # clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Lap {l + 1}")
        for i in range(4): # 4 horses
            if not D[i] >= 10: # if horse has not finished
                D[i] +=  5 + 7/O[i] + random.randint(0, 2 * O[i] // 3)  # distance covered by horse (this is a specific formula given without explanation!)
                if D[i] > MD:
                    MD = D[i]
                    J = i
                '''
                    lines 370 and 380 in the original listing doesn't make any sense!
                        370 IF D(I) > D(0) THEN LET D(0) = D(I)
                        380 IF D(0) = D(I) THEN LET J = I
                    Can anyone explains???
                '''
        # print horses anbd distances
        for i in range(4):
            print(f"Horse {chr(65 + i)}: ")   
            for line_index in range(len(HORSE_ART)):
                txt = get_distance_marker(int(D[i]), 3) + '  ' + HORSE_ART[line_index]
                print(txt)
            print(f" Distance covered: {int(D[i])} units")
            print()



        # user hit a key to continue to next lap
        if l < 3:
            input("Press Enter to continue to the next lap...")

    print(f"Horse {chr(65 + J)} is the winner!")
    #calculate winnings
    S = 1 * (chr(65 + J) == H)
    M =  M - B + S * B * O[J]  # winnings or loss
    #M + (B * O[J]) if S else M - B  # winnings or loss
    print(f"You {'won' if S else 'lost'}! Your new balance is £{M}.")
    # do you wnat to play again?
    play_again = input("Do you want to play again? (y/n): ").lower()
    if play_again != 'y':
        break

# print final balance
print(f"Your final balance is £{M}. Thank you for playing!")
