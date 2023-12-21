'''Contain functions for displaying the cards in the output'''


__author__ = "Umayeer Ahsan"


import main


def intro():
    '''Display the introduction of the game which 
    only plays at the beginning of the game.'''
    
    # TODO Improve this!
    print("BLACKJACK!")


def settings():
    '''DIsplay the settings interface'''

    print("--------------- SETTINGS ---------------")
    
    for setting in main.Settings.items():
        print(f"{setting.displayName}:\t\t{settings.value}")


def menu():
    '''Display the menu information to the user.'''
    
    print()
    print("--------------- MENU ---------------")
    print("1. Start game")
    print("2. Options")
    print("4. Tutorial")
    print("3. Exit")
    print("Make a choice") # TODO Might be redundant
    

def goodbye():
    '''Display the farewell message displayed when 
    the user quits the game'''
    
    print("Thank you for playing Blackjack!")
    print("Goodbye!")

