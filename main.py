'''Adjustable Blackjack'''


__author__ = "Umayeer Ahsan"


import display


# Constants


# Global Variables
settings = {
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
        "display_name": "True random cards.",
        "description": "Uses truely (pseudo) random cards instead of using a specific number of decks.\nUse this if you hate card counters.\nWhen true, the 'Deck Count' setting does nothing."
    },
    "deck_count": {
        "default": 6,
        "display_name": "Deck Count",
        "max": 1,
        "min": 12,
        "description": "The number of decks to use when dealing. Each card has an equal weight in the deck.\nInput a number between 1 and 12 (inclusive)."
    }
}


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
    
    The min_ is inclusive but the max_ is exclusive.
    '''
    
    while True:
        n = get_int(message)
        
        if min_ <= n < max_:
            return n
        else:
            print(f"Input out of range. Try a value between {min_} (inclusive) and {max_} (exclusive)")


def get_decision(message: str, choices: [str]):
    '''Prompt the user with the message 
    and retrieve a valid decision present in choices.'''
    
    while True:
        decision = input(message).lower()
        
        if decision in choices:
            return decision
        else:
            print("Please choose a valid option. Try again.")


def start_game():
    pass


def toggle_settings():
    display.settings_menu(settings)
    
    choice = get_int_range("Select a setting: ", 1, len(settings) + 1)
    # Find the setting in position choice
    setting = list(settings.values())[choice]
    print("Would you like to:\n  (c)hange the setting\n  (r)ead a description")
    decision = get_decision("> ", ['c', 'r'])
    
    if decision == 'c':
        print(f"Current Value: {setting['value']}")
        
        if type(setting["value"]) is bool:
            print("Type 0 for False and 1 for True.")
        elif type(setting["value"]) is int:
            if "min" in setting.keys():
                print(f"Enter a value from {setting['min']} to {setting['max']} (inclusive)")
            


def start_tutorial():
    pass


def main():
    '''The main function that handles the primary input and logic of the game interface.'''
    
    # Add a 'value' key into each setting and set it as the default
    for setting in settings.values():
        setting["value"] = setting["default"]

    display.intro()
    
    while True:
        display.menu()
        decision = get_int_range("> ", 1, 5)
        
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