import pyfiglet
import colorama

def print_menu():
    print("----TIC TAC TOE----")
    print(" type")
    print("'start' to start the game")
    print("'score' to show the scoreboard")
    print("'reset' to reset the score")
    print("'exit' to exit")

def take_command():
    while True:
        c = input("$ ").lower().strip()
        if c in ['start', 'score', 'reset', 'exit']:
            return c
        else:
            print(f"{colorama.Fore.RED}{c} : The term '{c}' is not recognized as the name of a cmdlet function, script file, or operable program.{colorama.Style.RESET_ALL}")

def start():
    pass