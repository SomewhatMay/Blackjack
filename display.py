'''Contain functions for displaying the cards in the output'''


__author__ = "Umayeer Ahsan"


# TODO rename file to util.py


import time


suit_symbols = {
    's': '♠',
    'h': '♥',
    'd': '♦',
    'c': '♣',
}

rank_symbols = {
    1: 'A',
    11: 'J',
    12: 'Q',
    13: 'K',
}


def get_suit(card: str) -> str:
    '''Determine the suit initial of card and 
    return it as a string.
    
    >>> get_suit("11h0")
    "h"
    >>> get_suit("1c0")
    "c"
    '''
    
    return card[-2]


def is_hidden(card: str) -> bool:
    '''Return true if and only if the last character in card,
    representing the visibility of the card, equals '1'.
    
    >>> is_hidden("12s0")
    False
    >>> is_hidden("3c1")
    True
    '''
    
    return True if card[-1] == "1" else False


def get_rank(card: str) -> int:
    '''Return the rank of card as an integer by slicing
    card and including all the characters up to but not including
    the second last character.
    
    >>> is_hidden("12s0")
    12
    >>> is_hidden("3c1")
    3
    '''
    
    return int(card[:-2])


def get_rank_symbol(rank: int) -> str:
    '''If rank has a specific character representation of it 
    in rank_symbols then return it, otherwise, return rank
    as a string
    
    >>> get_rank_symbol(2)
    "2"
    >>> get_rank_symbol(1)
    "A"
    '''
    
    if rank in rank_symbols:
        return rank_symbols[rank]

    return str(rank)


def hand_value(cards: [str]) -> [int]:
    '''Using only the visible cards in cards, calculate and
    return the possible hand values as an integer list.
    
    If the cards contain an ace, there might be two possible 
    hand values. In all other cases, there will only
    be one hand value.
    
    There will never be more than two hand values since only
    one ace can be counted as an 11 at a time without going
    over 21. Therefore, the returned integer list's length 
    will be: 0 < length <= 2.
    
    >>> hand_value(["1c0", "2s0"])
    [3, 13]
    >>> hand_value(["5d0", "7h1"])
    [5]
    '''

    has_ace = False
    primary_value = 0

    for card in cards:
        if is_hidden(card) == True:
            continue
        
        rank = get_rank(card)
        
        if rank == 1:
            if has_ace:
                primary_value += 1
            else:
                has_ace = True
        elif int(rank) >= 10:
            # Ensure that a 10, Jack, Queen, and King all are valued at 10.
            primary_value += 10
        else:
            primary_value += int(rank)
    
    values = [primary_value]
    
    if has_ace:
        values[0] += 1
        
        # Only include the 'ace as an 11-value card' if it is below 21!
        if primary_value + 11 <= 21:
            values.append(primary_value + 11)
    
    return values
            

def hand_state(cards: [dict]) -> str:
    '''Return, as a string, whether the total value of cards 
    denotes a blackjack, bust, or it is safe.
    
    >>> hand_state(["5c0", "3s0"])
    "safe"
    >>> hand_state(["1s0", "10d0"])
    "blackjack"
    '''

    values = hand_value(cards)
    
    if len(cards) == 2 and max(values) == 21:
        state = "blackjack"
    elif min(values) > 21:
        state = "bust"
    else:
        state = "safe"

    return state


def graphical_hand_state(primary_hand: dict) -> str:
    '''Determine and return, as a string, the state, hand value(s), and the bet 
    of primary_hand in a graphical state that will be displayed to the output.
    
    >>> graphical_hand_state( { "bet": 15, "cards": ["1s0", "10d0"], "is_split": False, "double_bet": False } )
    "BLACKJACK - $15.00"
    
    >>> graphical_hand_state( { "bet": 10.0, "cards": ["1s0", "5d0"], "is_split": False, "double_bet": False } )
    "6 / 16 - $10.00"
    
    >>> graphical_hand_state( { "bet": 20.0, "cards": ["2s0", "3d0"], "is_split": False, "double_bet": False } )
    "5 - $20.00"
    '''

    primary_cards = primary_hand["cards"]
    primary_state = hand_state(primary_cards)
    primary_values = hand_value(primary_cards)
    
    state_display = ""
    
    if primary_state == "blackjack":
        state_display += "BLACKJACK"
    elif primary_state == "bust":
        state_display += f"{primary_values[0]} (BUST)"
    else:
        for i in range(len(primary_values)):
            state_display += str(primary_values[i])
            
            # Only append a slash if it is not the last value
            # in the primary_values list
            if i != (len(primary_values) - 1):
                state_display += " / "
        
    if primary_hand["bet"] > 0:
        state_display += f" - ${primary_hand['bet']:.2f}"

    return state_display


def graphical_hand_comparison(primary_cards: [str], secondary_cards: [str]) -> str:
    primary_values = hand_value(primary_cards)
    
    # The maximum hand value of the secondary hand value(s)
    # is what the primary hand is compared to
    secondary_value = max(hand_value(secondary_cards))

    comparison = ""
        
    if min(primary_values) <= 21:
        if max(primary_values) == secondary_value:
            comparison += " (PUSH)"
        elif secondary_value > 21 or max(primary_values) > secondary_value:
            comparison += " (WIN)"
        elif max(primary_values) < secondary_value:
            comparison += " (LOSS)"
    
    return comparison


def get_lines(drawings: [str]) -> [str]:
    result = []
    
    COMPLETED = False
    
    while not COMPLETED:
        current_line = ""
        
        for i in range(len(drawings)):
            drawing = drawings[i]
            new_line_index = drawing.find('\n')
            
            if new_line_index == -1:
                COMPLETED = True
                current_line += drawing
            else:
                current_line += drawing[:new_line_index]
                drawings[i] = drawing[new_line_index + 1:]
        
        result.append(current_line)

    return result


def full_card(hidden: bool):
    if hidden == True:
        return """╔═══════════╗
║?╔═══════╗?║
║ ║       ║ ║
║ ║       ║ ║
║ ║       ║ ║
║ ║       ║ ║
║ ║       ║ ║
║ ║       ║ ║
║ ║       ║ ║
║?╚═══════╝?║
╚═══════════╝"""
    else:
        return """╔═══════════╗
║        {:>2} ║
║         {} ║
║           ║
║  ╚═════╗  ║
║  ║  {}  ║  ║
║  ╚═════╗  ║
║           ║
║ {}         ║
║ {:<2}        ║
╚═══════════╝"""


def half_card(hidden: bool):
    if hidden == True:
        return """═══╗
═╗?║
 ║ ║
 ║ ║
 ║ ║
 ║ ║
 ║ ║
 ║ ║
 ║ ║
═╝?║
═══╝"""
    else:
        return """═══╗
{:>2} ║
 {} ║
   ║
╗  ║
║  ║
╗  ║
   ║
   ║
   ║
═══╝"""


def print_cards(cards: [str]):
    card_drawings = []
    
    for i in range(len(cards)):
        card = cards[i]
        suit_symbol = suit_symbols[get_suit(card)]
        rank = get_rank(card)
        hidden = is_hidden(card)
        rank_symbol = get_rank_symbol(rank)
        
        if i == 0:
            drawing = full_card(hidden)
        else:
            drawing = half_card(hidden)
        
        card_drawings.append(drawing.format(rank_symbol, suit_symbol, suit_symbol, suit_symbol, rank_symbol))
    
    output_lines = get_lines(card_drawings)
    
    for line in output_lines:
        print(line)


def print_dealer_hand(dealer_hand: dict):
    print("Dealer's hand:")
    print_cards(dealer_hand["cards"])
    print("Value: " + graphical_hand_state(dealer_hand))
    print()


def print_user_hand(user_hand: dict, dealer_hand: dict, hand_count_ratio: str=None):
    hand_count_output = "Your hand"
    
    if hand_count_ratio != None:
        hand_count_output += " " + hand_count_ratio
    
    print(hand_count_output + ":")
    
    user_cards = user_hand["cards"]
    dealer_cards = dealer_hand["cards"]
    print_cards(user_cards)
    print("Value: " + graphical_hand_state(user_hand) + graphical_hand_comparison(user_cards, dealer_cards))
    print()


def print_hands(dealer_hand: dict, user_hand: [dict], hand_count_ratio: str=None):
    print_dealer_hand(dealer_hand)
    print_user_hand(user_hand, dealer_hand, hand_count_ratio)


def print_hands_all(dealer_hand: dict, user_hands: [dict]):
    print_dealer_hand(dealer_hand)
    
    if len(user_hands) > 1:
        # Use minimal layout if the user has multiple hands
        print("Your hands:")
        
        for i in range(len(user_hands)):
            hand = user_hands[i]
            
            graphical_state = graphical_hand_state(hand) + graphical_hand_comparison(hand["cards"], dealer_hand["cards"])
            print(f"  Hand #{i+1}: {graphical_state}")
    else:
        # Use standard layout
        print_user_hand(user_hands[0], dealer_hand)


def intro():
    '''Display the introduction of the game which 
    only plays at the beginning of the game.'''

    print()
    print(""" /$$$$$$$  /$$        /$$$$$$   /$$$$$$  /$$   /$$    /$$$$$  /$$$$$$   /$$$$$$  /$$   /$$
| $$__  $$| $$       /$$__  $$ /$$__  $$| $$  /$$/   |__  $$ /$$__  $$ /$$__  $$| $$  /$$/
| $$  \ $$| $$      | $$  \ $$| $$  \__/| $$ /$$/       | $$| $$  \ $$| $$  \__/| $$ /$$/ 
| $$$$$$$ | $$      | $$$$$$$$| $$      | $$$$$/        | $$| $$$$$$$$| $$      | $$$$$/  
| $$__  $$| $$      | $$__  $$| $$      | $$  $$   /$$  | $$| $$__  $$| $$      | $$  $$  
| $$  \ $$| $$      | $$  | $$| $$    $$| $$\  $$ | $$  | $$| $$  | $$| $$    $$| $$\  $$ 
| $$$$$$$/| $$$$$$$$| $$  | $$|  $$$$$$/| $$ \  $$|  $$$$$$/| $$  | $$|  $$$$$$/| $$ \  $$
|_______/ |________/|__/  |__/ \______/ |__/  \__/ \______/ |__/  |__/ \______/ |__/  \__/""")
    # print("------------------------------------------------------------------------------------------")


def settings_menu(settings):
    '''Display the settings interface'''

    title("SETTINGS")
    
    counter = 0
    for setting in settings.values():
        counter +=1
        print(f"{counter}. {(setting['display_name']):<30}{setting['value']}")


def await_continue(message: str = "[press enter to continue...]"):
    '''Waits for the user to want to continue by asking for an empty input.'''
    
    input(message)


def print_yield(message: str="", duration: int=.5):
    print(message)
    time.sleep(duration)


def menu():
    '''Display the menu information to the user.'''
    
    title("MENU")
    print("1. Start game")
    print("2. Options")
    print("3. View Balance")
    print("4. Restart game")
    print("5. Tutorial")
    print("6. Exit")


def title(label: str):
    print()
    print(f"--------------- {label} ---------------")


def goodbye():
    '''Display the farewell message displayed when 
    the user quits the game'''
    
    print()
    print("Thank you for playing Blackjack!")
    print("Goodbye!")

