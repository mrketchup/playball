__author__ = 'Sam'


class GameManager:
    def __init__(self, games=None):
        self.games = [] if games is None else games

    def play_games(self):
        for game in self.games:
            game.play()
