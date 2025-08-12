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
'''

import random

#region Declarations

odds = [] 
horses = {'A':0, 'B':0, 'C':0, 'D':0} # 4 horses and their odds
distance = {'A':0, 'B':0, 'C':0, 'D':0}  # Distance covered by each horse
finished = {'A':False, 'B':False, 'C':False, 'D':False}  # Whether each horse has finished


money = 100  # Starting money
bet = 0  # Bet amount
bet_horse = ''  # Horse on which the bet is placed
#endregion // END Declarations 


#region Printing Functions

def print_horses():
    print("Horses and Odds:")
    for horse, odds_value in horses.items():
        print(f"Horse {horse}: Odds {odds_value}")

def print_bet():
    print(f"Your bet: £{bet} on horse {bet_horse}")        

def print_odds():
    print("Current Odds:")
    for horse, odds_value in horses.items():
        print(f"Horse {horse}: Odds {odds_value}")

def print_race_status():
    print("Current Race Status:")
    for horse, dist in distance.items():
        status = "Finished" if finished[horse] else f"Distance: {dist}"
        print(f"Horse {horse}: {status}")
    
def print_winner(winner):
    if winner:
        print(f"The winner is Horse {winner}!")
    else:
        print("No winner yet.")

def print_money():
    print(f"Money left: £{money}")
#endregion // END Printing Functions


def reset_race():
    global horses, distance, finished, money, bet, bet_horse, odds
    odds = []
    horses = {'A':0, 'B':0, 'C':0, 'D':0}
    distance = {'A':0, 'B':0, 'C':0, 'D':0}
    finished = {'A':False, 'B':False, 'C':False, 'D':False}
    bet = 0
    bet_horse = ''


#region Betting Functions
def set_odds():
    global odds, horses
    odds = [random.randint(1, 10) for _ in range(4)]  # Random odds between 1 and 10
    total_odds = sum(odds)
    
    # Normalize odds to ensure they sum to 100
    for i, horse in enumerate(horses.keys()):
        horses[horse] = round((odds[i] / total_odds) * 100, 2)


def place_bet():    
    global bet, bet_horse, money
    print_horses()
    bet_horse = input("Place your bet on horse (A, B, C, D): ").upper()
    
    if bet_horse not in horses:
        print("Invalid horse choice. Please choose A, B, C, or D.")
        return
    
    try:
        bet = int(input(f"Enter your bet amount (You have £{money}): "))
        if bet <= 0 or bet > money:
            print("Invalid bet amount. Please try again.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return
    
    money -= bet
    print_bet()


#endregion // END Betting Functions