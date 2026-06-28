import os
import json
from datetime import date
from collections import defaultdict
import json
from datetime import date

SCORE_FILE = 'scores.json'

def loadScores():
    if not os.path.exists(SCORE_FILE):
        return []
    with open(SCORE_FILE, 'r') as f:
        return json.load(f)
    
def saveScores(difficulty, result):
    scores = loadScores()
    scores.append({
        'date': str(date.today()),
        'difficulty': difficulty,
        'result' : result
    })
    with open(SCORE_FILE, 'w') as f:
        json.dump(scores, f, indent=2)

def buildScoreTable(scores):
    table = defaultdict(lambda: {'easy': [0,0], 'medium': [0,0], 'hard': [0,0]})
    for match in scores:
        d = match['date']
        diff = match['difficulty']
        table[d][diff][1] += 1          # played
        if match['result'] == 'win':
            table[d][diff][0] += 1      # won
    return table

def displayScoreTable(table):
    pass

def resetScores():
    with open(SCORE_FILE, 'w') as f:
        json.dump([], f)