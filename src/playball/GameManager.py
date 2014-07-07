__author__ = 'Sam'


class GameManager:
    def __init__(self, games=None):
        self.event_callbacks = []
        self.game_end_callbacks = []
        self.games = [] if games is None else games

    def play_games(self):
        for game in self.games:
            post_state = None
            for pre_state, post_state, event in game.play():
                self.fire_event_callbacks(pre_state, post_state, event)
            self.fire_game_end_callbacks(post_state)

    def subscribe_event_callback(self, callback):
        self.event_callbacks.append(callback)

    def fire_event_callbacks(self, pre_state, post_state, event):
        for callback in self.event_callbacks:
            callback(pre_state, post_state, event)

    def subscribe_game_end_callback(self, callback):
        self.game_end_callbacks.append(callback)

    def fire_game_end_callbacks(self, state):
        for callback in self.game_end_callbacks:
            callback(state)