'''Contain functions for displaying the cards in the output'''


__author__ = "Umayeer Ahsan"


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
    return card[-2]


def is_hidden(card: str) -> bool:
    return True if card[-1] == "1" else False


def get_rank(card: str) -> int:
    return int(card[:-2])


def get_rank_symbol(rank: int) -> str:
    if rank in rank_symbols:
        return rank_symbols[rank]

    return str(rank)


def hand_value(cards: [str]) -> [int]:
    '''Using only the visible cards in cards, calculate and
    return the possible hand values as an integer list.
    
    If the cards contain an ace, there might be two possible 
    hand values. In almost all other cases, there will only
    be one hand value.
    
    There will never be more than two hand values since only
    one ace can be counted as an 11 at a time without going
    over 21. Therefore, the returned integer list's length 
    will be: 0 < length <= 2.
    
    >>> hand_value([ { "rank": "A", "suit": "clubs", "hidden": false } ])
    [1, 11]
    
    >>> hand_value([ { "rank": "K", "suit": "spades", "hidden": false } ])
    [10]
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
        if primary_value + 11 < 21:
            values.append(primary_value + 11)
    
    return values
            

# TODO ensure that this function ONLY returns the state!
def hand_state(cards: [dict]) -> str:
    values = hand_value(cards)
    
    if len(cards) == 2 and max(values) == 21:
        state = "blackjack"
    elif min(values) > 21:
        state = "bust"
    else:
        state = "safe"

    return state


def graphical_hand_state(primary_hand: dict, secondary_hand: dict=None) -> str:
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
            
            if i != (len(primary_values) - 1):
                state_display += " / "
    
    if secondary_hand != None:
        secondary_values = max(hand_value(secondary_hand["cards"]))
        
        if min(primary_values) <= 21:
            if max(primary_values) == secondary_values:
                state_display += " (PUSH)"
            elif secondary_values > 21 or max(primary_values) > secondary_values:
                state_display += " (WIN)"
            elif max(primary_values) < secondary_values:
                state_display += " (LOSS)"
                
        
    if primary_hand["bet"] > 0:
        state_display += f" - ${primary_hand['bet']}"

    return state_display


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
    
    print_cards(user_hand["cards"])
    print("Value: " + graphical_hand_state(user_hand, dealer_hand))
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
            graphical_state = graphical_hand_state(hand, dealer_hand)
            print(f"  Hand #{i+1}: {graphical_state}")
    else:
        # Use standard layout
        print_user_hand(user_hands[0], dealer_hand)


def intro():
    '''Display the introduction of the game which 
    only plays at the beginning of the game.'''
    
    # TODO Improve this!
    print("BLACKJACK!")


def settings_menu(settings):
    '''Display the settings interface'''

    title("SETTINGS")
    
    counter = 0
    for setting in settings.values():
        counter +=1
        print(f"{counter}. {(setting['display_name']):<30}{setting['value']}")


# QUESTION nullable/default parameter
def await_continue(message: str = "[press enter to continue...]"):
    '''Waits for the user to want to continue by asking for an empty input.'''
    
    print()
    input(message)


# QUESTION nullable/default paramter?
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

