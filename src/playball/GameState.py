"""
Created on Aug 5, 2013

@author: mejones
"""


class GameState(object):
    """
    Contains all important information regarding the state of a game.
    """

    def __init__(self):
        self.bases = [None, None, None, None]
        self.homeTeam = None
        self.awayTeam = None
        self.homeRuns = 0
        self.awayRuns = 0
        self.inning = 1
        self.inningBottom = False
        self.outs = 0
        self.homeOffensiveLineupIndex = 0
        self.awayOffensiveLineupIndex = 0
        self.completed = False

    def add_event(self, event):
        new_state = GameState()
        new_state.homeTeam = self.homeTeam
        new_state.awayTeam = self.awayTeam
        new_state.homeRuns = self.homeRuns
        new_state.awayRuns = self.awayRuns
        new_state.inning = self.inning
        new_state.inningBottom = self.inningBottom
        new_state.outs = self.outs
        new_state.homeOffensiveLineupIndex = self.homeOffensiveLineupIndex
        new_state.awayOffensiveLineupIndex = self.awayOffensiveLineupIndex

        for i in range(1, len(new_state.bases)):
            destination = event.runnerDestinations[i]
            if destination is not None and destination in range(1, len(
                    new_state.bases)):
                new_state.bases[destination] = self.bases[i]

        if new_state.inningBottom:
            new_state.homeRuns += event.runsOnPlay
            new_index = (new_state.homeOffensiveLineupIndex + 1) % 9
            new_state.homeOffensiveLineupIndex = new_index
        else:
            new_state.awayRuns += event.runsOnPlay
            new_index = (new_state.awayOffensiveLineupIndex + 1) % 9
            new_state.awayOffensiveLineupIndex = new_index

        if event.batterDestination == 0:
            new_state.outs += 1
        elif event.batterDestination < 4:
            new_state.bases[event.batterDestination] = event.batter

        return new_state

    def clear_bases(self):
        self.bases = [None, None, None, None]
