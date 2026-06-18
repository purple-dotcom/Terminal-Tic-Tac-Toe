import random
import time

board = {'A1' : ' ', 'A2' : ' ', 'A3': ' ',
         'B1' : ' ', 'B2' : ' ', 'B3' : ' ',
         'C1' : ' ', 'C2' : ' ', 'C3' : ' '}

def displayBoard(board):
    print("    1   2   3")
    for row in 'ABC':
        print("  -------------")
        cells = f"| {board[row+'1']} | {board[row+'2']} | {board[row+'3']} |"
        print(f"{row} {cells}")
        if row == 'C':
            print("  -------------")

def chooseLevel():
    while True:
        print("Choose dificulty -> Easy (1) | Medium (2) | Hard (3) ")
        lvl = input("$ ")
        if lvl.strip() not in ['1','2','3']:
            print("Try again!")
        else:
            return int(lvl)
    
def userTurn(board, userChar):
    print("your turn~")
    while True:
        print(f"place your {userChar}")
        tile = input(">>> ").upper().strip()

        if tile == 'Q':
            print("Are you sure you want to quit? (y/n) ")
            if input(">>> ").lower().strip() == 'y':
                #return to main menu
                break
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
    print()
    gameChar = 'X' if userChar == 'O' else 'O'

    if diff == 1:
        empty_tiles = [i for i in board if board[i] == ' ']
        move = random.choice(empty_tiles)
        board[move] = gameChar

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

    print(f"CPU chose {move}!")

    
    

winningPatterns = [['A1','A2','A3'], ['B1','B2','B3'], ['C1','C2','C3'],  # rows
                    ['A1','B1','C1'], ['A2','B2','C2'], ['A3','B3','C3'],  # cols
                    ['A1','B2','C3'], ['A3','B2','C1']]                    # diagonals


def winningCondition(board):
    for pattern in winningPatterns:
        vals = [board[tile] for tile in pattern]
        if vals[0] != ' ' and vals[0] == vals[1] == vals[2]:
            return vals[0]
    return False

def drawCondition(board):
    return all(board[tile] != ' ' for tile in board)

def findWinningMove(board, char):
    for pattern in winningPatterns:
        vals = [board[tile] for tile in pattern]
        if vals.count(char) == 2 and vals.count(' ') == 1:
            return pattern[vals.index(' ')]
    return None

def playAgainPrompt():
    while True:
        print("Play again? (y/n)")
        p = input("$ ").lower().strip()
        if p not in ['y','n']:
            print("Try again...")
        else:
            if p == 'y':
                return True
            else:
                return False
            
def resetBoard(board):
    for x in board:
        board[x] = ' '

def gameloop(board, diff):
    userScore = 0
    gameScore = 0
    draws = 0
    userChar = 'X'

    #session loop
    while True:
        gameChar = 'O' if userChar == 'X' else 'X'
        resetBoard(board)

        #gameloop
        currentTurn = 'X'
        while True:
            displayBoard(board)
            if currentTurn == userChar:
                userTurn(board, userChar)
            else:
                gameTurn(board, userChar, diff)

            if winningCondition(board) == userChar:
                displayBoard(board)
                print("You win!! ;) ")
                userScore += 1
                break

            elif winningCondition(board) == gameChar:
                displayBoard(board)
                print("You lose! :(")
                gameScore += 1
                break
            
            elif drawCondition(board):
                displayBoard(board)
                print("Draw! :/")
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
        
gameloop(board, chooseLevel())