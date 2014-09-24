"""
Created on Jul 31, 2013

@author: mejones
"""

from GameState import GameState
from Team import Team
from GameEngine import GameEngine
from playball import GameEvent


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
        self.event_callbacks = []
        self.game_end_callbacks = []

        if engine is None:
            self.engine = GameEngine()
        else:
            self.engine = engine

    def register_event_callback(self, callback):
        self.event_callbacks.append(callback)

    def fire_event_callbacks(self, pre_state, post_state, event):
        for callback in self.event_callbacks:
            callback(pre_state, post_state, event)

    def register_game_end_callback(self, callback):
        self.game_end_callbacks.append(callback)

    def fire_game_end_callbacks(self, state):
        for callback in self.game_end_callbacks:
            callback(state)

    def play(self):
        for pre_state, post_state, event in self._play_inning():
            self.fire_event_callbacks(pre_state, post_state, event)
        self.fire_game_end_callbacks(self.state)

    def _play_inning(self):
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
            if isinstance(event, GameEvent.Play):
                poststate = self.state.add_event(event)
            elif isinstance(event, GameEvent.Substitution):
                # TODO - move this to a function (add_substitution)
                team = self.state.homeTeam if event.team == 1 else self.state.awayTeam
                if event.offensiveLineupIndex > 0:
                    team.offensiveLineup[event.offensiveLineupIndex - 1] = event.player
                if 0 < event.defensiveLineupIndex <= 9:
                    team.defensiveLineup[event.defensiveLineupIndex - 1] = event.player
                poststate = prestate
            elif isinstance(event, GameEvent.Comment):
                poststate = prestate
            else:
                raise Exception("Unsupported event type")

            yield prestate, poststate, event

            self.state = poststate
        if self.state.inningBottom:
            self.state.inning += 1
        self.state.inningBottom = not self.state.inningBottom

    def _continue_playing(self):
        return not (self.state.inningBottom and
                    self.state.homeRuns > self.state.awayRuns and
                    self.state.inning >= 9)
