from playball.GameEngine import GameEngine

__author__ = 'Sam'


class RetrosheetEngine(GameEngine):
    def __init__(self, retrosheet_game):
        self.retrosheet_game = retrosheet_game
        self.event_idx = 0

    def next_event(self, state):
        event = self.retrosheet_game.event_records[self.event_idx].to_event()
        self.event_idx += 1
        return event
