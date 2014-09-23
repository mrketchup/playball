from playball import Game
from playball.GameEventCallbacks import GameEventCallbacks
from playball.GameManager import GameManager
from playball.RetrosheetEngine import RetrosheetEngine
from playball.RetrosheetScorebook import RetrosheetScorebook

__author__ = 'sam'

scorebook = RetrosheetScorebook()
scorebook.read("single_game.txt")

game = scorebook.games[0]
engine = RetrosheetEngine(game)

game = Game(engine)
game.register_event_callback(GameEventCallbacks.print_event)
game.register_game_end_callback(GameEventCallbacks.print_game_end)

manager = GameManager([game])
manager.play_games()
