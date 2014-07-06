"""
Created on Jul 31, 2013

@author: mejones
"""

from GameState import GameState
from Team import Team
from GameEngine import GameEngine


class Game():
    """
    The game to be played. Contains game logic.
    """

    def __init__(self, engine=None, home_team=None, away_team=None):
        self.state = GameState()
        if home_team is None:
            home_team = Team()
        if away_team is None:
            away_team = Team()
        self.state.homeTeam = home_team
        self.state.awayTeam = away_team

        if engine is None:
            self.engine = GameEngine()
        else:
            self.engine = engine

    def play(self):
        while not self.state.completed and (self.state.inning <= 9 or self.state.homeRuns == self.state.awayRuns):
            # play top half of inning
            for preState, postState, event in self._play_half_inning():
                yield preState, postState, event

            # play bottom half of inning
            if self.state.inning < 9 or self.state.homeRuns <= self.state.awayRuns:
                for preState, postState, event in self._play_half_inning():
                    yield preState, postState, event
            else:
                self.state.completed = True

    def _play_half_inning(self):
        self.state.outs = 0
        self.state.clear_bases()
        while self.state.outs < 3 and self._continue_playing():
            event = self.engine.next_event(self.state)
            prestate = self.state
            poststate = self.state.add_event(event)

            yield prestate, poststate, event

            self.state = poststate
        if self.state.inningBottom:
            self.state.inning += 1
        self.state.inningBottom = not self.state.inningBottom

    def _continue_playing(self):
        return not (self.state.inningBottom and
                    self.state.homeRuns > self.state.awayRuns and
                    self.state.inning >= 9)
