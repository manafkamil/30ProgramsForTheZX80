
'''
    Leap Frog

    From 30 Programmes for Sinclair ZX

    at: https://dn790005.ca.archive.org/0/items/30-programs-for-the-sinclair-zx-80-1-k/30_Programs_for_the_Sinclair_ZX80_1K.pdf


    
    Sinclais Spectrum Basic Emulators:
    - https://spectrumcomputing.co.uk/emulators/zxsp  ??
    - https://fuse-emulator.sourceforge.io/  ??
    - https://worldofspectrum.org/emulators  ??
    - https://spectrumonline.co/emulators/   ??
    - https://spectrum.greatpeoples.net/     ??
    
    
    - https://zx.researcher.su/en/

    From the original program printed in the book:
        LEAP FROG

        This is a nice simple program, testing
        the player's logic. The object is to move
        all the frogs on the left to the right, and
        vice versa. Frogs can only leap over one
        frog or move to an adjacent empty space.
        0000 0000
        123456789

        The first move could be 35, 45, 65 or 75.

        Variables:
            P Position of frogs
            C Number of moves to date
            F "from"
            T "to"

        Program description:
        100 - 250 Initialisation
        300 - 370 Print routine
        500 - 620 Input player move
        700 - 760 Test if finished
        800 - 900 End

'''

import os

#region Declarations

# lines 100 - 250
# init positions
slots = ['X', 'X', 'X', 'X', ' ', 'O', 'O', 'O', 'O']
# target positions
target_slots = ['O', 'O', 'O', 'O', ' ', 'X', 'X', 'X', 'X']

# number of moves
num_moves = 0

#commands:
reset_command = 'r'  # Reset command
quit_command = 'q'   # Quit command
game_complete = 's'
#endregion // END Declarations

#region Check and Print Status
def clear_console():
    """
    Clears the console screen based on the operating system.
    """
    # Check if the operating system is Windows ('nt')
    if os.name == 'nt':
        _ = os.system('cls')  # Use 'cls' command for Windows
    # Otherwise, assume it's a Unix-like system (Linux, macOS, etc.)
    else:
        _ = os.system('clear') # Use 'clear' command for Unix-like systems

def check_status() -> bool:
    res = [slots[i] == target_slots[i] for i in range(len(slots))]
    return all(res)

def print_status():
    print('\nCurrent slots:')
    print(' '.join(slots))
    print(f'Moves: {num_moves}')
    # print command options
    print(f'Commands: {reset_command.upper()} to reset game, {quit_command.upper()} to quit')

#endregion  // Check and Print Status

#region Get and Validate Move

def get_move():
    global reset_command, quit_command
    print(f'\nEnter next move (Q to quit):')
    while True:
        try:
            move = input('From (1-9) TO (1-9): ')
            if (move.isdigit() and 10 < int(move) <= 91) or move.lower() == quit_command or move.lower() == reset_command:
                if move.lower() == quit_command:
                    print('Exiting the game.')
                    return quit_command
                if move.lower() == reset_command:
                    print('Resetting the game.')
                    return reset_command
                move = int(move)
                validation_message = validate_move(move)
                if validation_message:
                    # Print the validation message and continue to prompt for a valid move
                    print(validation_message)
                    continue
                return move
            else:
                print('Invalid input. Please enter a number between 11 and 91.')
        except ValueError:
            print('Invalid input. Please enter a number between 11 and 91.')



def validate_move(move : int) -> str:
    origin_index = (move // 10) - 1
    destination_index = (move % 10) - 1
    if slots[origin_index] == ' ': # Cannot move an empty slot
        return 'Cannot move an empty slot.'
    if slots[destination_index] != ' ': # Cannot move to a non-empty slot
        return 'Cannot move to a non-empty slot.'
    leap_length = abs(origin_index - destination_index)
    if leap_length == 0: # Cannot move to the same slot
        return 'Cannot move to the same slot.'
    if leap_length > 2: # Cannot leap more than one frog
        return 'Cannot leap more than one frog.'
    
    if leap_length in [1, 2] : # Leap over a frog or to adjacent empty space   
        return '' # Valid move


#endregion // END Get and Validate Move


#region Main Program
def reset_game():
    global slots, num_moves
    slots = ['X', 'X', 'X', 'X', ' ', 'O', 'O', 'O', 'O']
    num_moves = 0


def start_game():
    global num_moves
    num_moves = 0
    while not check_status():
        print_status()
        next_move = get_move()
        if next_move in [quit_command, reset_command]:
            return next_move
        origin_index = (next_move // 10) - 1
        destination_index = (next_move % 10) - 1
        slots[destination_index] = slots[origin_index]
        slots[origin_index] = ' '
        num_moves += 1
    return game_complete

#endregion Main Program


def play_again():
    while True:
        response = input('Do you want to play again? (y/n): ').strip().lower()
        if response in ['y', 'n']:
            return response == 'y'
        print('Invalid input. Please enter "y" or "n".')

if __name__ == "__main__":
    clear_console()
    print('Welcome to Leap Frog!')
    reset_game()
    while True:
        result = start_game()
        if result == quit_command:
            print('Thanks for playing!')
            break
        elif result == reset_command:
            print('Game reset.')
            reset_game()
        elif result == game_complete:
            print('Congratulations! You completed the game in', num_moves, 'moves.')
            if not play_again():
                print('Thanks for playing!')
                break
            else:
                print('Resetting the game...')
            reset_game()
        else:
            print('Unexpected result:', result)
