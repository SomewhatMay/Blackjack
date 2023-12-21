'''Adjustable Blackjack'''


__author__ = "Umayeer Ahsan"


import display


# Constants


# Global Variables
Settings = {
    "surrendering": {
        default: False,
        displayName: "Surrendering Enabled",
        desc: "When true, enables the option to surrender on the first round.\nUser loses but receives half of their bet back."
    },
    "doubling": {
        default: True,
        displayName: "Doubling Enabled",
        desc: "When true, enables the option to double the user's bet on the first round.\nUser receives one final card and then their turn ends."
    },
    "splitting": {
        default: True,
        displayName: "Splitting Enabled",
        desc: "When true, enables the option to split on the first round if the user has two of the same value cards.\nEach card is now played as a separate hand."
    },
    "soft_17_hit": {
        default: True,
        displayName: "Dealer Hits on Soft 17",
        desc: "When true, dealer must hit on a soft 17. Otherwise, the dealer stands."
    },
    "true_random": {
        default: False,
        displayName: "True random cards.",
        desc: "Uses truely (pseudo) random cards instead of using a specific number of decks.\nUse this if you hate card counters.\nWhen true, the 'Deck Count' setting does nothing."
    },
    "deck_count": {
        default: 6,
        displayName: "Deck Count",
        min_: 1,
        max_: 12,
        desc: "The number of decks to use when dealing. Each card has an equal weight in the deck.\nInput a number between 1 and 12 (inclusive)."
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
        
        if min <= n < max_:
            return n
        else:
            print(f"Input out of range. Try a value between {min_} (inclusive) and {max_} (exclusive)")


def start_game():
    pass


def toggle_settings():
    pass


def start_tutorial():
    pass


def main():
    '''The main function that handles the primary input and logic of the game interface.'''
    
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