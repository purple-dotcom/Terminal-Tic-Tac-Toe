import os
import json
from datetime import date
from collections import defaultdict
import colorama

colorama.init()

SCORE_FILE = './scores.json'

def loadScores():
    if not os.path.exists(SCORE_FILE):
        return []
    with open(SCORE_FILE, 'r') as f:
        return json.load(f)     # returns list
    
def saveScores(difficulty, result):
    scores = loadScores()
    scores.append({
        'date': str(date.today()),
        'difficulty': difficulty,
        'result' : result
    })
    with open(SCORE_FILE, 'w') as f:
        json.dump(scores, f, indent=2)  # rewrites scores.json

def buildScoreTable(scores):
    table = defaultdict(lambda: {'easy': [0,0,0], 'medium': [0,0,0], 'hard': [0,0,0]})
    for match in scores:
        d = match['date']
        diff = match['difficulty']
        if match['result'] == 'win':
            table[d][diff][0] += 1
        elif match['result'] == 'loss':
            table[d][diff][1] += 1
        elif match['result'] == 'draw':
            table[d][diff][2] += 1
    return table

def displayScoreTable():
    scores = loadScores()
    if not scores:
        print("No scores yet.")

    table = buildScoreTable(scores)

    col = 12

    print(f"\n{colorama.Fore.GREEN}(w/l/d){colorama.Style.RESET_ALL}")
    print(f"\n{'Date':<12} {'Easy':^{col}} {'Medium':^{col}} {'Hard':^{col}}")
    print("-" * (12 + col * 3 + 3))

    for d in sorted(table.keys(), reverse=True):
        row = table[d]
        easy   = f"{row['easy'][0]}/{row['easy'][1]}/{row['easy'][2]}"
        medium = f"{row['medium'][0]}/{row['medium'][1]}/{row['medium'][2]}"
        hard   = f"{row['hard'][0]}/{row['hard'][1]}/{row['hard'][2]}"
        print(f"{d:<12} {easy:^{col}} {medium:^{col}} {hard:^{col}}")

    print(f"{colorama.Fore.GREEN}\nPress Enter to return to menu... {colorama.Style.RESET_ALL}")
    waitForEnter()

def resetScores():
    with open(SCORE_FILE, 'w') as f:
        json.dump([], f)    # erase

def waitForEnter():
    if os.name == 'nt':
        import msvcrt
        while msvcrt.getwch() != '\r':
            pass
    else:
        import termios, tty, sys
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while sys.stdin.read(1) != '\r':
                pass
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)