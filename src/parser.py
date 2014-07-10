from playball import Game
from playball.GameEventCallbacks import GameEventCallbacks
from playball.GameManager import GameManager
from playball.RetrosheetEngine import RetrosheetParser

__author__ = 'sam'

parser = RetrosheetParser("../data/2012eve/2012BAL.EVA")

games = []
for engine in parser.engines:
    game = Game(engine)
    game.register_event_callback(GameEventCallbacks.print_event)
    game.register_game_end_callback(GameEventCallbacks.print_game_end)
    games.append(game)

manager = GameManager(games)
manager.play_games()
