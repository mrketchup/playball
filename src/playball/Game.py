'''
Created on Jul 31, 2013

@author: mejones
'''


from GameState import GameState
from Team import Team
import GameEngine

def printEvent(event):
    print "Batter:", event.batter.fullName
    print "Batting Result:", event.battingResult
    
    for i in range(1, len(event.runners)):
        name = 'None' if event.runners[i] is None else event.runners[i].fullName
        print " * Runner on %d (%s) goes to %s" % (i, name, str(event.runnerDestinations[i]))
    
def printState(state):
    tb = "Bottom" if state.inningBottom else "Top"
    print "-------------- %6s  %2d --------------" % (tb, state.inning)
    print "Away: %s: %d" % (state.awayTeam.fullName, state.awayRuns)
    print "Home: %s: %d" % (state.homeTeam.fullName, state.homeRuns)
    print "Outs:", state.outs
    print "-" * 40
    


class Game(object):
    '''
    The game to be played. Contains game logic.
    '''
    
    def __init__(self, homeTeam=None, awayTeam=None):
        self.state = GameState()
        if homeTeam is None: homeTeam = Team()
        if awayTeam is None: awayTeam = Team()
        self.state.homeTeam = homeTeam
        self.state.awayTeam = awayTeam
        
    def play(self):
        while self.state.inning <= 9 or self.state.homeRuns == self.state.awayRuns:
            self._playHalfInning()
            if self.state.homeRuns <= self.state.awayRuns or self.state.inning < 9:
                self._playHalfInning()
                
    def _playHalfInning(self):
        self.state.outs = 0
        self.state.clearBases()
        while self.state.outs < 3 and self._continuePlaying():
            event = GameEngine.nextEvent(self.state)
            preState = self.state
            postState = self.state.addEvent(event)
        
            printState(preState)
            printEvent(event)
            printState(postState)
            
            self.state = postState
        if self.state.inningBottom:
            self.state.inning += 1
        self.state.inningBottom = not self.state.inningBottom
        
    def _continuePlaying(self):
        return not (self.state.inningBottom and \
                    self.state.homeRuns > self.state.awayRuns and \
                    self.state.inning >= 9)
