'''Adjustable Blackjack'''


__author__ = "Umayeer Ahsan"


import display

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