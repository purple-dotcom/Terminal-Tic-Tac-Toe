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
    c = input("$ ").lower().strip()
    return c

