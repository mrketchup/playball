'''
Created on Jul 31, 2013

@author: mejones
'''


from GameState import GameState
from Team import Team
from GameEvent import Play
import GameEngine
    
def notify(preState, postState, event):
    tb = "Bottom" if preState.inningBottom else "Top"
    print "-------------- %6s  %2d --------------" % (tb, preState.inning)
    print "Away: %s: %d" % (preState.awayTeam.fullName(), preState.awayRuns)
    print "Home: %s: %d" % (preState.homeTeam.fullName(), preState.homeRuns)
    print "Outs:", preState.outs
    print "-" * 40
    
    print "Batter:", event.batter.fullName()
    print "Batting Result:", Play.PlayTypes.reverse_mapping[event.battingResult]
    
    for i in range(1, len(preState.bases)):
        if preState.bases[i] is not None and i != event.runnerDestinations[i]:
            if event.runnerDestinations[i] >= 4:
                print " * %s scores." % (preState.bases[i].fullName())
            else:
                print " * %s goes to %s." % (preState.bases[i].fullName(), \
                                             event.runnerDestinations[i])
    print ''


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
        
            notify(preState, postState, event)
            
            self.state = postState
        if self.state.inningBottom:
            self.state.inning += 1
        self.state.inningBottom = not self.state.inningBottom
        
    def _continuePlaying(self):
        return not (self.state.inningBottom and \
                    self.state.homeRuns > self.state.awayRuns and \
                    self.state.inning >= 9)
