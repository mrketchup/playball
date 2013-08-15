'''
Created on Aug 5, 2013

@author: mejones
'''

class GameState(object):
    '''
    Contains all important information regarding the state of a game.
    '''
    def __init__(self):
        self.bases = [None, None, None, None]
        self.homeTeam = None
        self.awayTeam = None
        self.homeRuns = 0
        self.awayRuns = 0
        self.inning = 1
        self.inningBottom = False
        self.outs = 0
        self.homeLineupIndex = 0
        self.awayLineupIndex = 0
        
    def addEvent(self, event):
        newState = GameState()
        newState.homeTeam = self.homeTeam
        newState.awayTeam = self.awayTeam
        newState.homeRuns = self.homeRuns
        newState.awayRuns = self.awayRuns
        newState.inning = self.inning
        newState.inningBottom = self.inningBottom
        newState.outs = self.outs
        newState.homeLineupIndex = self.homeLineupIndex
        newState.awayLineupIndex = self.awayLineupIndex
        
        for i in range(1, len(newState.bases)):
            dest = event.runnerDestinations[i]
            if dest is not None and dest in range(1, len(newState.bases)):
                newState.bases[dest] = self.bases[i]
                
        if newState.inningBottom:
            newState.homeRuns += event.runsOnPlay
            newState.homeLineupIndex = (newState.homeLineupIndex + 1) % 9
        else:
            newState.awayRuns += event.runsOnPlay
            newState.awayLineupIndex = (newState.awayLineupIndex + 1) % 9
                
        if event.batterDestination == 0:
            newState.outs += 1
        elif event.batterDestination < 4:
            newState.bases[event.batterDestination] = event.batter
            
        return newState
    
    def clearBases(self):
        self.bases = [None, None, None, None]
        