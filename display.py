'''Contain functions for displaying the cards in the output'''


__author__ = "Umayeer Ahsan"


suit_symbols = {
    'spades': '♠',
    'hearts': '♥',
    'diamonds': '♦',
    'clubs': '♣',
}

def hand_value(cards: [dict]) -> [int]:
    has_ace = False
    primary_value = 0

    for card in cards:
        if card["hidden"] == True:
            continue
        
        rank = card["rank"]
        
        if rank == 'A':
            if has_ace:
                primary_value += 1
            else:
                has_ace = True
        elif rank == 'J' or rank == 'Q' or rank == 'K':
            primary_value += 10
        else:
            primary_value += rank
    
    values = [primary_value]
    
    if has_ace:
        values[0] += 1
        
        # Only include the 'ace as an 11-value card' if it is below 21!
        if primary_value + 11 < 21:
            values.append(primary_value + 11)
    
    return values
            

def hand_state(cards: [dict]) -> dict:
    values = hand_value(cards)
    
    if len(cards) == 2 and max(values) == 21:
        state = "blackjack"
    elif min(values) > 21:
        state = "bust"
    else:
        state = "safe"

    return {
        "state": state,
        "values": values,
    }


# QUESTION using nullable type in parameter?
def graphical_hand_state(state_info: [dict], msg: str="Hand Value: "):
    state = state_info["state"]
    values = state_info["values"]
    
    state_display = msg
    
    if state == "blackjack":
        state_display += "BLACKJACK"
    elif state == "bust":
        state_display += f"{values[0]} (BUST)"
    else:
        for i in range(len(values)):
            state_display += str(values[i])
            
            if i != (len(values) - 1):
                state_display += " / "

    return state_display


def get_lines(drawings: [str]) -> [str]:
    result = []
    
    COMPLETED = False
    start = 0
    
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


def print_cards(cards: [dict]):
    card_drawings = []
    
    for i in range(len(cards)):
        card = cards[i]
        suit_symbol = suit_symbols[card["suit"]]
        rank = card["rank"]
        
        if i == 0:
            drawing = full_card(card["hidden"])
        else:
            drawing = half_card(card["hidden"])
        
        card_drawings.append(drawing.format(rank, suit_symbol, suit_symbol, suit_symbol, rank))
    
    output_lines = get_lines(card_drawings)
    
    for line in output_lines:
        print(line)
    
    print()


def print_hands(dealer_hand: [dict], user_hand: [dict], hand_count_ratio: str):
    print("Dealer's hand:")
    print_cards(dealer_hand["cards"])
    # QUESTION should I split up the nested function calls?
    print(graphical_hand_state(hand_state(dealer_hand["cards"])))
    print()

    print(f"Your hand {hand_count_ratio}:")
    print_cards(user_hand["cards"])
    # QUESTION should I split up the nested function calls?
    print(graphical_hand_state(hand_state(user_hand["cards"])))
    print(f"Your bet: ${user_hand['bet']:.2f}")
    print()


def print_hands_min(dealer_hand: [dict], user_hands: [dict]):
    print("Dealer's hand:")
    print_cards(dealer_hand["cards"])
    # QUESTION should I split up the nested function calls?
    dealer_state_info = hand_state(dealer_hand["cards"])
    dealer_values = dealer_state_info["values"]
    print(graphical_hand_state(dealer_state_info))
    print()
    
    print("Your hands:")
    for i in range(len(user_hands)):
        hand = user_hands[i]
        state_info = hand_state(hand["cards"])
        user_values = state_info["values"]
        output = graphical_hand_state(state_info, f"Hand {i+1}: ")
        
        if min(user_values) <= 21:
            if max(user_values) == max(dealer_values):
                output += " (PUSH)"
            elif max(dealer_values) > 21:
                output += " (WIN)"
            elif max(user_values) < max(dealer_values):
                output += " (LOSS)"
        
        output += f" - ${hand['bet']}"
        
        print("  " + output)
        

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


def menu():
    '''Display the menu information to the user.'''
    
    title("MENU")
    print("1. Start game")
    print("2. Options")
    print("3. View Balance")
    print("4. Tutorial")
    print("5. Exit")


def title(label: str):
    print()
    print(f"--------------- {label} ---------------")


def goodbye():
    '''Display the farewell message displayed when 
    the user quits the game'''
    
    print()
    print("Thank you for playing Blackjack!")
    print("Goodbye!")

