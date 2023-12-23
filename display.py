'''Contain functions for displaying the cards in the output'''


__author__ = "Umayeer Ahsan"


def intro():
    '''Display the introduction of the game which 
    only plays at the beginning of the game.'''
    
    # TODO Improve this!
    print("BLACKJACK!")


def settings_menu(settings):
    '''Display the settings interface'''

    print()
    print("--------------- SETTINGS ---------------")
    
    counter = 0
    for setting in settings.values():
        counter +=1
        print(f"{counter}. {(setting['display_name']):<30}{setting['value']}")


def await_continue(message: str = "[press enter to continue...]"):
    '''Waits for the user to want to continue by asking for an empty input.'''
    
    print()
    input(message)


def menu():
    '''Display the menu information to the user.'''
    
    print()
    print("--------------- MENU ---------------")
    print("1. Start game")
    print("2. Options")
    print("3. Tutorial")
    print("4. Exit")


def goodbye():
    '''Display the farewell message displayed when 
    the user quits the game'''
    
    print()
    print("Thank you for playing Blackjack!")
    print("Goodbye!")

