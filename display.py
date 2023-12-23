'''Contain functions for displaying the cards in the output'''


__author__ = "Umayeer Ahsan"


suit_symbols = {
    'spades': '♠',
    'hearts': '♥',
    'diamonds': '♦',
    'clubs': '♣',
}

def get_lines(drawings: [str]) -> [str]:
    result = []
    
    COMPLETED = False
    start = 0
    
    while not COMPLETED:
        current_line = ""
        
        for i in range(0, len(drawings)):
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
            

def hand(cards: [dict]):
    card_drawings = []
    
    for i in range(0, len(cards)):
        card = cards[i]
        suit_symbol = suit_symbols[card["suit"]]
        rank = card["rank"]
        
        if i == 0:
            card_drawings.append(f"""╔═══════════╗
║         {rank:<2}║
║         {suit_symbol} ║
║           ║
║  ╚═════╗  ║
║  ║  {suit_symbol}  ║  ║
║  ╚═════╗  ║
║           ║
║ {suit_symbol}         ║
║{rank:>2}         ║
╚═══════════╝""")
        else:
            card_drawings.append(f"""═══╗
 {rank:<2}║
 {suit_symbol} ║
   ║
╗  ║
║  ║
╗  ║
   ║
   ║
   ║
═══╝""")
    
    output_lines = get_lines(card_drawings)
    
    for line in output_lines:
        print(line)
    
    print()


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


# HACK nullable/default parameter
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

