'''Adjustable Blackjack'''


__author__ = "Umayeer Ahsan"


import display
import random
import time


## Constants ##
SUITS = [
    "c", # clubs
    "d", # diamonds
    "s", # spades
    "h" # hearts
]

## Global Variables ##
DEFAULT_BALANCE = 1000.0
current_balance = 0

settings = {
    # Each settings dictionary will have an additional 'value' 
    # property (a exact copy of their 'default' property) assigned to them during runtime
    "surrendering": {
        "default": False,
        "display_name": "Surrendering Enabled",
        "description": "When true, enables the option to surrender on the first round.\nUser loses but receives half of their bet back."
    },
    "doubling": {
        "default": True,
        "display_name": "Doubling Enabled",
        "description": "When true, enables the option to double the user's bet on the first round.\nUser receives one final card and then their turn ends."
    },
    "splitting": {
        "default": True,
        "display_name": "Splitting Enabled",
        "description": "When true, enables the option to split on the first round if the user has two of the same value cards.\nEach card is now played as a separate hand."
    },
    "soft_17_hit": {
        "default": True,
        "display_name": "Dealer Hits on Soft 17",
        "description": "When true, dealer must hit on a soft 17. Otherwise, the dealer stands."
    },
    "true_random": {
        "default": False,
        "display_name": "True Random Cards.",
        "description": "Uses truely (pseudo) random cards instead of using a specific number of decks.\nUse this if you hate card counters.\nWhen true, the 'Deck Count' setting does nothing."
    },
    "deck_count": {
        "default": 6,
        "display_name": "Deck Count",
        "min": 1,
        "max": 12,
        "description": "The number of decks to use when dealing. Each card has an equal weight in the deck.\nInput a number between 1 and 12 (inclusive)."
    },
    
    # The following dictionaries are used for 
    # display purposes and not true settings
    "reset": {
        "default": "",
        "display_name": "Reset All Settings",
    },
    "return": {
        "default": "",
        "display_name": "Return to Menu",
    }
}

ranks = list(range(1, 14)) # FIXME fix this
remaining_cards = {}
remaining_suits = {}


def get_int(message: str) -> int:
    '''Prompt the user with message to enter an integer which is then returned.'''
    
    while True:
        try:
            n = int(input(message))
            return n
        except ValueError:
            print("Invalid input. Please try again.")
            

def get_int_range(message: str, min_: int, max_: int) -> int:
    '''Prompt the user with message to enter an integer between min_ and max_ 
    to be returned.
    
    The min_ and max_ are both inclusive.
    '''
    
    while True:
        n = get_int(message)
        
        if min_ <= n <= max_:
            return n
        else:
            print(f"Input out of range. Try a value from {min_} to {max_} (both inclusive)")


def get_decision(message: str, choices: [str]) -> str:
    '''Prompt the user with the message, accepting and returning 
    the user's decision only if it is present in choices.'''
    
    while True:
        decision = input(message).lower()
        
        if decision in choices:
            return decision
        else:
            print("Please choose a valid option. Try again.")


def shuffle_deck():
    '''Reset the remaining_cards and the remaining_suits dictionaries with 
    their original values to simulate shuffled decks.'''
    
    for rank in ranks:
        remaining_cards[rank] = settings["deck_count"]["value"] * len(SUITS)
        
        for suit in SUITS:
            remaining_suits[rank][suit] = settings["deck_count"]["value"]


## Main game functions ##

#########################
## DEPLOY remove this before deploying!
mock_deck = [2] * 4
#########################

def draw_card(hidden: bool=False) -> str:
    '''Draw a random card from the deck and return it as a string.
    
    Each card is stored as a str with the integer rank, the suit initial,
    and the card's visibility as a 0 or 1. 
    The format is f"{rank}{suit}{is_hidden}".
    For example, an ace of hearts that is visible would be stored as "1h0".
    '''
    
    #########################
    ## DEPLOY remove this before deploying!
    global mock_deck
    
    card = ""
    
    if len(mock_deck) != 0:
        rank = mock_deck[0]
        
        suit = random.choice(SUITS)
        
        mock_deck = mock_deck[1:]
    #########################
    
    elif settings["true_random"]["value"] == True:
        rank = random.choice(ranks)
        suit = random.choice(SUITS)
    else:
        # Reshuffle the deck if there are no more cards left
        if sum(remaining_cards.values()) == 0:
            shuffle_deck()
        
        rank = random.choices(list(remaining_cards.keys()), weights=list(remaining_cards.values()))[0]
        remaining_cards[rank] -= 1
        
        available_suits = remaining_suits[rank]
        suit = random.choices(list(available_suits.keys()), weights=list(available_suits.values()))[0]
        available_suits[suit] -= 1
    
    card = f"{rank}{suit}"
    card += "1" if hidden else "0"

    return card


def new_hand(bet: float, cards: [str]) -> dict:
    '''Create and return a new hand as a dictionary containing
    information such as the bet and the cards it contains.
    
    >>> new_hand(10.0, ["1c0", "11s0"])
    {"bet": 10.0, "cards": ["1c0", "11s0"], "is_split": False, "double_bet": False}
    >>> new_hand(12.0, ["12d1"])
    {"bet": 12.0, "cards": ["12d1"], "is_split": False, "double_bet": False}
    '''
    
    return {
        "bet": bet,
        "cards": cards,
        "is_split": False,
        "double_bet": False,
    }


def hit(hand: dict):
    '''Draw and insert a new card into hand and display the card's rank and symbol.'''
    
    new_card = draw_card()
    hand["cards"].insert(0, new_card)
    
    suit_symbol = display.suit_symbols[display.get_suit(new_card)]
    
    print(f"Drew a {display.get_rank_symbol(display.get_rank(new_card))}{suit_symbol}.")
    print()


def split(hand: dict, user_hands: [dict]):
    '''Split hand, their cards, and their bets into two individual hands,
    appending both hands to user_hands.
    
    It is assumed that hand contains only 2 same-rank
    cards.
    '''
    
    second_card = hand["cards"].pop()
    hand["bet"] /= 2
    hand["is_split"] = True

    split_hand = new_hand(hand["bet"], [second_card])
    split_hand["is_split"] = True
    user_hands.append(split_hand)
    
    print("You have split your hands.")
    print(f"You now have {len(user_hands)} hands.")
    print()


def play_user(user_hands: [dict], dealer_hand: dict, initial_bet: float) -> dict:    
    # TODO Too wordy? Do I need to incorporate what the 'final state' means?
    '''Manage the player's turn, return the final state of the turn, 
    comparing their hand(s) to the dealer_hand and allowing them to hit, 
    stand, split, double the initial_bet, or even forfeit 
    each of the individual user_hands.'''

    global current_balance
    
    # Use a while loop since the length of hands can change
    # in the middle of the game by splitting hands.
    forfeited = False
    busted = False
    doubled = False
    i = 0
    while (not forfeited) and (not busted) and i < len(user_hands):
        hand_complete = False
        turn = 0
        hand = user_hands[i]
        
        while (not hand_complete) and (not forfeited):
            turn += 1
            
            hand_count_ratio = f"{i+1}/{len(user_hands)}"
            display.print_hands(dealer_hand, hand, hand_count_ratio)
            
            if hand["is_split"] == True or hand["double_bet"] == True:
                print()
                display.await_continue("[press enter to draw your final card...]")
                    
                hit(hand)
                
                display.print_hands(dealer_hand, hand, hand_count_ratio)
                
                if hand["is_split"]:
                    # We only provide the option to split if the first and
                    # second cards in the hand have the same rank
                    if display.get_rank(hand["cards"][0]) == display.get_rank(hand["cards"][1]):
                        print("Would you like to:\n  (sp)lit\n  (s)tand")
                        decision = get_decision("> ", ['s', "sp"])
                        
                        if decision == "sp":
                            split(hand, user_hands)

                            # If we split this hand into two again, the hand is still not 
                            # complete since it must have at least two cards to be complete.
                            # Therefore, we do not mark this hand as complete, and iterate
                            # over to the next loop, allowing the user to draw one final card.
                            continue
                    else:
                        print()
                        display.await_continue("[press enter to complete this hand...]")
                else:
                    print()
                    display.await_continue("[press enter to end your turn...]")

                # Mark the hand as complete if the user does has received a second card.
                hand_complete = True
            else:
                choices_display = "  (h)it\n  (s)tand"
                choices = ['h', 's']
                
                if turn == 1:
                    # Allow each of the following decisions if they are enabled
                    # in the settings and the hand state is proper.
                    
                    if settings["splitting"]["value"] == True and display.get_rank(hand["cards"][0]) == display.get_rank(hand["cards"][1]):
                        choices_display += "\n  (sp)lit hands"
                        choices.append("sp")
                    
                    if settings["doubling"]["value"] == True and (current_balance >= initial_bet):
                        choices_display += "\n  (d)ouble down"
                        choices.append('d')
                    
                    if settings["surrendering"]["value"] == True:
                        choices_display += "\n  (f)orfeit"
                        choices.append('f')
                
                print(f"Would you like to:\n{choices_display}")
                decision = get_decision("> ", choices)
                
                if decision == 's':
                    print("You've chosen to stand.")
                    hand_complete = True

                elif decision == 'h':
                    hit(hand)
                    
                elif decision == 'd':
                    current_balance -= hand["bet"]
                    hand["bet"] *= 2
                    hand["double_bet"] = True
                    doubled = True
                    print(f"You've doubled your bet to a total bet of ${hand['bet']:.2f}.")
                    print(f"Your current balance: {current_balance:.2f}")
                    
                elif decision == 'sp':
                    split(hand, user_hands)
                
                elif decision == 'f':
                    print(f"You've forfeited and have been returned ${initial_bet / 2} (half of your initial bet).")
                    current_balance += initial_bet / 2

                    hand_complete = True
                    forfeited = True
                
            if min(display.hand_value(hand["cards"])) > 21:
                print("You have busted!")
                busted = True
                hand_complete = True
                
        i += 1

    return {
        "forfeited": forfeited,
        "busted": busted,
        "doubled": doubled,
    }


def reveal_hidden_card(dealer_hand: dict):
    '''Reveal the hidden dealer's hidden card by changing the last character
    of the dealer_hand's second card to a 0 instead of a 1, indicating 
    that the card is now visible.'''
    
    second_card = dealer_hand["cards"][1]
    
    dealer_hand["cards"][1] = dealer_hand["cards"][1][:-1] + "0"

    suit_symbol = display.suit_symbols[display.get_suit(second_card)]
    
    print()
    print(f"The dealer's hidden card was a {display.get_rank_symbol(display.get_rank(second_card))}{suit_symbol}!")


def play_dealer(dealer_hand: dict, user_hands: [dict]):
    '''Simulate the dealer's turn by displaying the hidden card, drawing until the
    dealer_hand's overall value is greater than or equalled to a hard 17, 
    and displaying the state of the each of the user_hands and the dealer_hand.'''
    
    reveal_hidden_card(dealer_hand)
    display.print_hands_all(dealer_hand, user_hands)

    while min(display.hand_value(dealer_hand["cards"])) < 17:
        print()
        display.await_continue()
        hit(dealer_hand)
        display.print_hands_all(dealer_hand, user_hands)


def tutorial():
    '''Display the interactive tutorial dialogue, teaching the user how to play
    the game properly.'''
    
    display.print_yield("Welcome to BLACKJACK!")

    print("Game:")
    display.print_yield("  Here is how to play:")
    display.print_yield("  You bet a specific amount before the game begins.")
    display.print_yield("  The objective of the game is simple: get as close to a hand value of 21 as possible WITHOUT going over.")
    display.print_yield("  If you go over, you 'bust', meaning you lose!")
    display.print_yield("  You are playing against the dearler, who has the same objective.")
    display.print_yield("  If the dealer goes over 21, you win!")
    
    print("\nYou:")
    display.await_continue("  What happens if neither of us go over 21? [press enter to continue...]")

    print("\nGame:")
    display.print_yield("  Glad you asked!")
    display.print_yield("  The player that has a closer hand value to 21 wins!")

    print("You:")
    display.await_continue("  Wow! I'm so excited to play! What are the controls of the game? [press enter to continue...]")

    print("\nGame:")
    display.print_yield("  There are two primary controls:")
    display.print_yield("    (h)it - You choose to pick up a new card.")
    display.print_yield("      You can choose to hit for as long as you wish or until you go over 21.")
    display.print_yield()
    display.print_yield("    (s)tand - You choose to end your turn.")
    display.print_yield("      Now the dealer will reveal their card and deal for themself.")
    display.print_yield("  Assuming you havent busted, once the dealer completes dealing for themself, you have results of the game!")
    display.print_yield("  If you win, you get twice what you bet. If you lose, you lose everything you bet.")
    
    print("\nYou:")
    display.await_continue("  Nice! Seems intuitive. Are there any other things I should be aware of? [press enter to continue...]")

    print("\nGame:")
    display.print_yield("  Yes, there are two more controls that are only available at specific circumstances:")
    display.print_yield("    (d)ouble - Double your bet (therefore doubling your return if you win).")
    display.print_yield("      You can only draw one more card; this will be your final card.")
    display.print_yield("      Only available on the first turn.")
    display.print_yield()
    display.print_yield("    (sp)lit - Split your hand into two separate hands.")
    display.print_yield("      Your bet will be split evenly between both hands.")
    display.print_yield("      You can only draw one more card per hand before that hand is complete.")
    display.print_yield("      Only available when you have only two cards and they are of the same *rank* (not same value).")

    print("\nYou:")
    display.await_continue("  Great! Let's start the game! [press enter to start a game...]")

    print("Game:")
    display.print_yield("  Great! Let's begin.")

    start_game()


def start_game():
    '''Commence the main game, handle betting, user's turn, dealer's turn, and display
    the results of the game.'''
    
    global current_balance
    
    display.title("GAME")

    # FIXME do something when the user has no more money
    print(f"Balance: ${current_balance:.2f}")
    print("Enter an integer dollar amount to bet: ")
    initial_bet = get_int_range("> $", 1, current_balance) * 1.0
    total_bet = initial_bet
    current_balance -= initial_bet
    print(f"Your bet: ${initial_bet}")
    print()
    
    shuffle_deck()
    
    display.print_yield("Dealing cards...", 1)
    
    # Since the user can have multiple hands by splitting,
    # we will have a list that contains all of them.
    user_hands = []
    
    # Create the initial user and dealer hands
    user_hands.append(
        new_hand(initial_bet, [draw_card(), draw_card()])
    )
    dealer_hand = new_hand(0, [draw_card(), draw_card(True)])
    
    # The user_result variable contains information regarding whether
    # the user doubled, forefitted, or busted during their turn. 
    user_result = play_user(user_hands, dealer_hand, initial_bet)
    print()
    
    if user_result["doubled"]:
        total_bet *= 2
    
    if user_result["busted"] or user_result["forfeited"]:
        reveal_hidden_card(dealer_hand)
        
        print("Final hands:")
        display.print_hands_all(dealer_hand, user_hands)
     
        print("Game Over.")
        print(f"Lost bet: {total_bet}")
    else:
        print("Your turn is complete. Dealer will deal now.\n")
        display.await_continue()
        
        play_dealer(dealer_hand, user_hands)
        dealer_values = display.hand_value(dealer_hand["cards"])
        
        # Calculate the user's profit from this game
        profit = 0
        for hand in user_hands:
            user_values = display.hand_value(hand["cards"])
            
            if min(user_values) <= 21:
                if max(user_values) == max(dealer_values):
                    profit += hand["bet"]
                elif max(dealer_values) > 21 or max(user_values) > max(dealer_values):
                    profit += (hand["bet"] * 2)
        
        total_outcome = profit - total_bet
        
        # Store the sign of total_outcome so we can position
        # it before the dollar sign in the output.
        sign = "" if total_outcome >= 0 else "-"
        
        current_balance += profit
        
        print()
        print("Results:")
        print(f"  Return: ${profit:.2f}")
        print(f"  Total bet: -${total_bet:.2f}")
        print(f"  Total earnings: {sign}${abs(total_outcome):.2f}")
    
    display.title("GAME OVER")
    print()


## Settings functions ##
def reset_settings():
    '''Reset each setting to its default value.'''

    for setting in settings.values():
        setting["value"] = setting["default"]
    
    print("Reset all settings to default value.")


def change_setting(setting: dict):
    '''Display the change settings interface with specific information such
    as the current value of the setting, instructions on how to change the setting's value,
    and also handle updating the setting.'''
    
    print(f"\nCurrent value: {setting['value']}")
            
    # Retrieve a new value depending on the type of setting.
    if type(setting["value"]) is bool:
        print("Type 0 for False and 1 for True.")
        
        new = get_int_range("New value: ", 0, 1)
        
        if new == 0:
            new = False
        else:
            new = True
        
    elif type(setting["value"]) is int:
        if "min" in setting.keys():
            _min = setting["min"]
            _max = setting["max"]
            print(f"Enter an integer from {_min} to {_max} (inclusive)")

            new = get_int_range("New value: ", _min, _max)
        else:
            print("Enter an integer")
            
            new = get_int("New value: ")

    setting["value"] = new
    print(f"Setting updated to: {new}")


def toggle_settings():
    '''Toggle and handle the settings interface and user input such as changing the setting
    or reading the description of a setting.'''
    
    while True:
        display.settings_menu(settings)
        
        selection = get_int_range("Select a setting: ", 1, len(settings))
        
        # Second last option (reset settings).
        if selection == len(settings) - 1:
            reset_settings()
            print()
            display.await_continue("[press enter to return to settings menu...]")
            continue

        # Last option (return to menu).
        elif selection == len(settings):
            return
        
        # Find the zero-indexed position of the selected setting.
        setting = list(settings.values())[selection - 1]
        
        print("\nWould you like to:\n  (c)hange the setting\n  (r)ead the description\n  (g)o back")
        decision = get_decision("> ", ['c', 'r', 'g'])
       
        if decision == 'c':
            change_setting(setting)
            
        elif decision == 'r':
            print(f"\n{setting['display_name']}:\n{setting['description']}")
        
        elif decision == 'g':
            continue
        
        print()
        display.await_continue("[press enter to return to settings menu...]")


def restart_game():
    '''Reset the statistics of the user if they confirm they want
    to restart, making it seem like a new game.'''

    global current_balance
    
    print()
    print("Are you sure you want to restart game? This will reset your balance!")
    print("(y)es/(n)o")
    decision = get_decision("> ", ['y', 'n'])
    
    if decision == 'y':
        current_balance = DEFAULT_BALANCE


def main():
    '''Handles the primary input and logic of the game interface.'''
    
    global ranks, current_balance
    
    # Add a 'value' key into each setting and set it as the default.
    for setting in settings.values():
        setting["value"] = setting["default"]
    
    # Add a key for each rank in remaining_suits, storing a dictionary
    # of suits as keys and the corresponding remaining cards of that 
    # rank and suit as values
    for rank in ranks:
        available_suits = {}
        
        for suit in SUITS:
            available_suits[suit] = 0
        
        remaining_suits[rank] = available_suits

    display.intro()
    
    current_balance = DEFAULT_BALANCE
    
    while True:
        display.menu()
        decision = get_int_range("> ", 1, 6)

        if decision == 1:
            start_game()
        elif decision == 2:
            toggle_settings()
        elif decision == 3:
            # TODO Maybe add some other statistics if we have enough time?
            print(f"\nYour balance is ${current_balance:.2f}")
        elif decision == 4:
            restart_game()
        elif decision == 5:
            tutorial()
        elif decision == 6:
            display.goodbye()
            
            break
        

if __name__ == "__main__":
    main()