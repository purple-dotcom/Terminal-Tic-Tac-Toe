import random
import time
import colorama
import os
import shutil
import json

board = {'A1' : ' ', 'A2' : ' ', 'A3': ' ',
         'B1' : ' ', 'B2' : ' ', 'B3' : ' ',
         'C1' : ' ', 'C2' : ' ', 'C3' : ' '}

colorama.init()

def displayBoard(board, highlight=None, color=None, message=None):
    os.system('cls' if os.name == 'nt' else 'clear')
    
    termWidth = shutil.get_terminal_size().columns
    boardWidth = 14
    hPad = " " * ((termWidth - boardWidth) // 2)
    
    print(hPad + "    1   2   3")
    for row in 'ABC':
        print(hPad + "  -------------")
        cells = ""
        for col in '123':
            tile = row + col
            char = board[tile]
            if highlight and tile in highlight:
                cells += f"| {color}{char}{colorama.Style.RESET_ALL} "
            else:
                cells += f"| {char} "
        cells += "|"
        print(f"{hPad}{row} {cells}")
        if row == 'C':
            print(hPad + "  -------------")
    
    if message:
        print(message)

def chooseLevel():
    while True:
        print("Choose dificulty -> Easy (1) | Medium (2) | Hard (3) ")
        lvl = input("$ ").lower().strip()
        if lvl == 'exit':
            raise SystemExit
        elif lvl.strip() not in ['1','2','3']:
            print("Try again!")
        else:
            print(f"{colorama.Fore.LIGHTRED_EX} Press 'q' to quit and return to main menu {colorama.Style.RESET_ALL}")
            print("Loading", end='', flush=True)
            for _ in range(3):
                time.sleep(0.7)
                print('.', end = ' ', flush=True)
            time.sleep(1)
            return int(lvl)
        
class QuitGame(Exception):
    pass
    
def userTurn(board, userChar):
    print("your turn~")
    while True:
        print(f"place your {userChar}")
        tile = input(">>> ").upper().strip()

        if tile == 'Q':
            print("Are you sure you want to quit? (y/n)")
            if input(">>> ").lower().strip() in ['y', 'yes']:
                raise QuitGame()    #return to main menu
            else:
                continue

        if len(tile) != 2 or tile[0] not in ['A','B','C'] or tile[1] not in ['1','2','3']:
            print("Invalid. Try again")
        else:
            if board[tile] != ' ':
                print("Tile already taken. Try again")
            else:
                board[tile] = userChar
                break

def gameTurn(board, userChar, diff):
    print("CPU's turn~")
    for _ in range(3):
        time.sleep(0.5)
        print(".", end=' ', flush=True)
        time.sleep(0.2)
    gameChar = 'X' if userChar == 'O' else 'O'

    #easy
    if diff == 1: 
        empty_tiles = [i for i in board if board[i] == ' ']
        move = random.choice(empty_tiles)
        board[move] = gameChar

    #medium
    elif diff == 2: 
        move = findWinningMove(board, gameChar)
        if not move:
            move = findWinningMove(board, userChar)
        if not move and board['B2'] == ' ':
            move = 'B2'
        if not move:
            emptyCorners = [t for t in ['A1','A3','C1','C3'] if board[t] == ' ']
            if emptyCorners:
                move = random.choice(emptyCorners)
        if not move:
            empty = [t for t in board if board[t] == ' ']
            move = random.choice(empty)
        
        board[move] = gameChar

    else:
        #hard
        pass
    
    return move

winningPatterns = [['A1','A2','A3'], ['B1','B2','B3'], ['C1','C2','C3'],  # rows
                    ['A1','B1','C1'], ['A2','B2','C2'], ['A3','B3','C3'],  # cols
                    ['A1','B2','C3'], ['A3','B2','C1']]                    # diagonals


def winningCondition(board):
    for pattern in winningPatterns:
        vals = [board[tile] for tile in pattern]
        if vals[0] != ' ' and vals[0] == vals[1] == vals[2]:
            return vals[0], pattern
    return None, None

def drawCondition(board):
    return all(board[tile] != ' ' for tile in board)

#for medium difficulty
def findWinningMove(board, char):
    for pattern in winningPatterns:
        vals = [board[tile] for tile in pattern]
        if vals.count(char) == 2 and vals.count(' ') == 1:
            return pattern[vals.index(' ')]
    return None

def playAgainPrompt():
    while True:
        print("Play again? (y/n)")
        p = input(">> ").lower().strip()
        if p not in ['y','n']:
            print("Try again...")
        elif p == 'y':
            return True
        return False
            
def resetBoard(board):
    for x in board:
        board[x] = ' '

def gameloop(board, diff):
    userScore = 0
    gameScore = 0
    draws = 0
    userChar = 'X' # new gameloop config

    try:
        #session loop
        while True:
            gameChar = 'O' if userChar == 'X' else 'X'
            resetBoard(board)

            currentTurn = 'X' #1st loop config
            lastMessage = None 

            #gameloop
            while True:
                displayBoard(board, message=lastMessage)
                lastMessage = None

                if currentTurn == userChar:
                    userTurn(board, userChar)

                else:
                    move = gameTurn(board, userChar, diff)
                    lastMessage = f"CPU chose {move}!"

                winner, pattern = winningCondition(board)
                if winner == userChar:
                    displayBoard(board, highlight=pattern, color=colorama.Fore.GREEN)
                    print(f"\n{colorama.Fore.GREEN}You win!! ;){colorama.Style.RESET_ALL}")
                    userScore += 1
                    break

                elif winner == gameChar:
                    displayBoard(board, highlight=pattern, color=colorama.Fore.RED, message=f'CPU chose {move}!')
                    print(f"\n{colorama.Fore.RED}You lose! :({colorama.Style.RESET_ALL}")
                    gameScore += 1
                    break
                
                elif drawCondition(board):
                    displayBoard(board, highlight=board, color=colorama.Fore.YELLOW)
                    print(f"\n{colorama.Fore.YELLOW}Draw! :/{colorama.Style.RESET_ALL}")
                    draws += 1
                    break

                currentTurn = 'O' if currentTurn == 'X' else 'X' #one turn over, changing currentTurn char
                
            print(f"Score : You {userScore} | CPU {gameScore} | Draws {draws}")

            if playAgainPrompt():
                print("Loading", end='', flush=True)
                for _ in range(3):
                    time.sleep(0.5)
                    print(".", end='', flush=True)
                print()

                userChar = 'O' if userChar == 'X' else 'X'
            else:
                return userScore, gameScore, draws
            
    except QuitGame:
        return userScore, gameScore, draws
        

#add hard difficulty
#return scores to main scoreboard
#return to main menu after q

if __name__ == '__main__':
    gameloop(board, chooseLevel())