'''Adjustable Blackjack'''


__author__ = "Umayeer Ahsan"


import display
import random
import time


## Constants ##
SUITS = ["clubs", "diamonds", "spades", "hearts"] # HACK Making this list a constant since it will never be changed

## Global Variables ##
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
        "default": True,
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

ranks: [str] = [] # HACK loaded during runtime - is this okay? Should they be loaded in main()?
remaining_cards = {}
remaining_suits = {} # HACK loaded during runtime as well...

def get_int(message: str) -> int:
    '''Prompt the user with message to enter an integer to be returned.'''
    
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
            print(f"Input out of range. Try a value between {min_} and {max_} (both inclusive)")


def get_decision(message: str, choices: [str]):
    '''Prompt the user with the message 
    and retrieve a valid decision present in choices.'''
    
    while True:
        decision = input(message).lower()
        
        if decision in choices:
            return decision
        else:
            print("Please choose a valid option. Try again.")


## Main game functions ##
# HACK default nullable parameter
def draw_card(hidden: bool=False) -> dict:
    '''Get a random card from the deck and return its information.'''
    
    if settings["true_random"]["value"] == True:
        rank = random.choice(ranks)
        suit = random.choice(SUITS)
    else:
        # Reshuffle the deck if there are no more cards left
        if sum(remaining_cards.values()) == 0:
            shuffle_deck()
        
        # HACK random.choices; the hacky indexing;
        # FIXME might have to cast to list before this function works
        rank = random.choices(remaining_cards.keys(), weights=remaining_cards.values())[0]
        remaining_cards[rank] -= 1
        
        available_suits = remaining_suits[rank]
        suit = random.choices(available_suits.keys(), weights=available_suits.values())[0]
        remaining_suits[suit] -= 1
        
    return {
        "rank": rank,
        "suit": suit,
        "hidden": hidden,
    }


def shuffle_deck():
    if settings["true_random"]["value"] != True:
        for rank in ranks:
            remaining_cards[rank] = settings["deck_count"]["value"] * len(SUITS)
            
            for suit in SUITS:
                remaining_suits[rank][suit] = settings["deck_count"]["value"]


def start_game():
    display.title("GAME")
    
    shuffle_deck()
    
    print("Dealing cards...")
    time.sleep(1)
    
    user_hands = []
    dealer_hand = []
    
    user_hands.append([draw_card(), draw_card()])
    dealer_hand.append([draw_card()])
    
    print("Dealer:")
    display.hand()
    


## Settings functions ##
def reset_settings():
    for setting in settings.values():
        setting["value"] = setting["default"]
    
    print("Reset all settings to default value.")


def change_setting(setting: dict):
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
    while True:
        display.settings_menu(settings)
        
        # Add two to upper bound since the last two 
        # selections are for resetting all settings and returning to menu.
        selection = get_int_range("Select a setting: ", 1, len(settings))
        
        # Second last option (reset settings).
        if selection == len(settings) - 1:
            reset_settings()
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
            
        display.await_continue("[press enter to return to settings menu...]")
           

def start_tutorial():
    pass


def main():
    '''The main function that handles the primary input and logic of the game interface.'''
    
    global ranks
    
    # Add a 'value' key into each setting and set it as the default.
    for setting in settings.values():
        setting["value"] = setting["default"]
    
    # Add the ranks
    ranks.append('A')
    
    for i in range(2, 11):
        ranks.append(i)
    
    ranks += ['J', 'Q', 'K']
    
    # Add a key for each rank in remaining_suits, storing a dictionary
    # of suits as keys and the corresponding remaining cards of that 
    # rank and suit as values
    for rank in ranks:
        available_suits = {}
        
        for suit in SUITS:
            available_suits[suit] = 0
        
        remaining_suits[rank] = available_suits
    
    
    while True:
        hand = []
        print("Drawing: ", end='')
        
        for i in range(0, random.randrange(1, 15)):
            card = draw_card(random.choices([True, False])[0])
            print( ("{}{}" if (card["hidden"] == False) else "({}{})").format(card["rank"], display.suit_symbols[card["suit"]]) , end='' )
            hand.append(card)

        print()
        display.hand(hand)
        input()

    display.intro()
    
    while True:
        display.menu()
        decision = get_int_range("> ", 1, 4)
        
        if decision == 1:
            start_game()
        elif decision == 2:
            toggle_settings()
        elif decision == 3:
            start_tutorial()
        elif decision == 4:
            display.goodbye()
            
            break
        

if __name__ == "__main__":
    main()