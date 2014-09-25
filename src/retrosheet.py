import difflib
import sys
from playball import Game
from playball.GameManager import GameManager
from playball.RetrosheetCallbacks import RetrosheetCallbacks
from playball.RetrosheetEngine import RetrosheetEngine
from playball.RetrosheetGame import RetrosheetGame
from playball.RetrosheetScorebook import RetrosheetScorebook

__author__ = 'sam'

scorebook = RetrosheetScorebook()
scorebook.read("single_game.txt")

retrosheet_game = scorebook.games[0]
engine = RetrosheetEngine(retrosheet_game)

game = Game(engine)
retrosheet_game = RetrosheetGame()
callbacks = RetrosheetCallbacks(retrosheet_game)
game.register_event_callback(callbacks.record_event)
game.register_game_end_callback(callbacks.record_game_end)

manager = GameManager([game])
manager.play_games()

scorebook = RetrosheetScorebook()
scorebook.games.append(retrosheet_game)
scorebook.write("output.txt")

f1 = open("single_game.txt")
f2 = open("output.txt")

for line in difflib.context_diff(f1.readlines(), f2.readlines()):
    sys.stdout.write(line)