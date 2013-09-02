'''
Created on Jul 31, 2013

@author: mejones
'''


from GameState import GameState
from Team import Team
from GameEngine import GameEngine

class GameObserver(object):
    def notify(self, preState, postState, event):
        raise NotImplementedError
        
    
class Game():
    '''
    The game to be played. Contains game logic.
    '''
    
    def __init__(self, engine=None, homeTeam=None, awayTeam=None):
        self.state = GameState()
        if homeTeam is None: homeTeam = Team()
        if awayTeam is None: awayTeam = Team()
        self.state.homeTeam = homeTeam
        self.state.awayTeam = awayTeam
        self.observers = []
        
        if engine is None:
            self.engine = GameEngine()
        else:
            self.engine = engine
        
    def play(self):
        while self.state.inning <= 9 or self.state.homeRuns == self.state.awayRuns:
            self._playHalfInning()
            if self.state.homeRuns <= self.state.awayRuns or self.state.inning < 9:
                self._playHalfInning()
                
    def _playHalfInning(self):
        self.state.outs = 0
        self.state.clearBases()
        while self.state.outs < 3 and self._continuePlaying():
            event = self.engine.nextEvent(self.state)
            preState = self.state
            postState = self.state.addEvent(event)
        
            self._notify(preState, postState, event)
            
            self.state = postState
        if self.state.inningBottom:
            self.state.inning += 1
        self.state.inningBottom = not self.state.inningBottom
        
    def _continuePlaying(self):
        return not (self.state.inningBottom and
                    self.state.homeRuns > self.state.awayRuns and
                    self.state.inning >= 9)
        
    def addObserver(self, observer):
        self.observers.append(observer)
        
    def removeObserver(self, observer):
        self.observers.remove(observer)
        
    def _notify(self, preState, postState, event):
        for observer in self.observers:
            observer.notify(preState, postState, event)
