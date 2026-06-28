import pyfiglet
import colorama
from game import gameloop, chooseLevel, board
from scores import *

colorama.init()
title = pyfiglet.figlet_format("TIC TAC TOE", font="doom")

def print_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(colorama.Fore.BLUE + title + colorama.Style.RESET_ALL)
    print(" Type")
    print("'start' - start game")
    print("'score' - show scoreboard")
    print("'reset' - reset score")
    print("'exit'  - exit")

def take_command():
    while True:
        c = input("$ ").lower().strip()
        if c in ['start', 'score', 'reset', 'exit']:
            if c == 'start':
                start()

            elif c == 'score':
                displayScoreTable()

            elif c == 'reset':
                print("Are you sure? (y/n)")
                if input("$$ ").strip().lower() in ('y', 'yes'):
                    resetScores()
                else:
                    print_menu()
                    continue

            elif c == 'exit':
                raise SystemExit
            
            break

        else:
            if c.strip() == '':
                print(f"{colorama.Fore.RED}Try again{colorama.Style.RESET_ALL}")
            else:
                print(f"{colorama.Fore.RED}The term '{c}' is not recognized as the name of a cmdlet function, script file, or operable program.{colorama.Style.RESET_ALL}")
            
def start():
    diff = chooseLevel()
    diffVerbose = {1:'easy', 2:'medium', 3:'hard'}[diff]
    userScore, gameScore, draws = gameloop(board, diff)
    for _ in range(userScore):
        saveScores(diffVerbose, 'win')
    for _ in range(gameScore):
        saveScores(diffVerbose, 'loss')
    for _ in range(draws):
        saveScores(diffVerbose, 'draw')

if __name__ == '__main__':
    while True:
        print_menu()
        take_command()