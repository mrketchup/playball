'''
Created on Jul 31, 2013

@author: mejones
'''

from random import random

def simulatePA(batter):
    '''
    Crunches the numbers and returns the outcome of a plate appearance.
    '''
    n1B = batter.rate1B
    n2B = n1B + batter.rate2B
    n3B = n2B + batter.rate3B
    nHR = n3B + batter.rateHR
    nBB = nHR + batter.rateBB
    nHBP = nBB + batter.rateHBP
    
    result = 'OUT'
    rand = random()
    if rand < n1B:
        result = '1B'
    elif rand < n2B:
        result = '2B'
    elif rand < n3B:
        result = '3B'
    elif rand < nHR:
        result = 'HR'
    elif rand < nBB:
        result = 'BB'
    elif rand < nHBP:
        result = 'HBP'
        
    return result


def advanceRunners(batter, result, state):
    event = Event()
    event.batter = batter
    event.battingResult = result
    
    for i in range(1, len(state.bases)):
        event.runners[i] = state.bases[i]
        if event.runners[i] is not None:
            event.runnerDestinations[i] = i
    
    if event.battingResult == 'OUT':
        event.batterDestination = 0
        event.outsOnPlay += 1
        
    elif event.battingResult == '1B':
        event.batterDestination = 1
        rand = random()
        if event.runners[3] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[3] = 4
        if event.runners[2] is not None:
            if rand < 0.5:
                event.runnerDestinations[2] = 4
                event.runsOnPlay += 1
            else:
                event.runnerDestinations[2] = 3
        if event.runners[1] is not None:
            if rand < 0.2:
                event.runnerDestinations[1] = 3
            else:
                event.runnerDestinations[1] = 2
        
    elif event.battingResult == '2B':
        event.batterDestination = 2
        if event.runners[3] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[3] = 4
        if event.runners[2] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[2] = 4
        if event.runners[1] is not None:
            if random() < 0.2:
                event.runsOnPlay += 1
                event.runnerDestinations[1] = 4
            else:
                event.runnerDestinations[1] = 3
        
    elif event.battingResult == '3B':
        event.batterDestination = 3
        if event.runners[3] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[3] = 4
        if event.runners[2] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[2] = 4
        if event.runners[1] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[1] = 4
        
    elif event.battingResult == 'HR':
        event.batterDestination = 4
        event.runsOnPlay += 1
        if event.runners[3] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[3] = 4
        if event.runners[2] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[2] = 4
        if event.runners[1] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[1] = 4
            
    elif event.battingResult == 'BB' or event.battingResult == 'HBP':
        event.batterDestination = 1
        if event.runners[3] is not None and event.runners[2] is not None and event.runners[1] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[3] = 4
            event.runnerDestinations[2] = 3
            event.runnerDestinations[1] = 2
        elif event.runners[2] is not None and event.runners[1] is not None:
            event.runnerDestinations[2] = 3
            event.runnerDestinations[1] = 2
        elif event.runners[1] is not None:
            event.runnerDestinations[1] = 2
        
    return event



def printEvent(event):
    print "Batter:", event.batter.fullName
    print "Batting Result:", event.battingResult
    
    for i in range(1, len(event.runners)):
        name = 'None' if event.runners[i] is None else event.runners[i].fullName
        print " * Runner on %d (%s) goes to %s" % (i, name, str(event.runnerDestinations[i]))
    
def printState(state):
    tb = "Bottom" if state.inningBottom else "Top"
    print "-------------- %6s  %2d --------------" % (tb, state.inning)
    print "%s: %d" % (state.awayTeam.fullName, state.awayRuns)
    print "%s: %d" % (state.homeTeam.fullName, state.homeRuns)
    print "Outs:", state.outs
    print "-" * 40


class Event(object):
    '''
    Contains all info regarding an event.
    '''
    def __init__(self):
        self.batter = None
        self.battingResult = None
        self.batterDestination = None
        self.runners = [None, None, None, None]
        self.runnerDestinations = [None, None, None, None]
        self.runsOnPlay = 0
        self.outsOnPlay = 0



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
        self.isComplete = False
        
    def clearBases(self):
        self.bases = [None, None, None, None]
        
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
        newState.isComplete = self.isComplete
        
        for i in range(1, len(newState.bases)):
            dest = event.runnerDestinations[i]
            if dest is not None and dest in range(1, len(newState.bases)):
                newState.bases[dest] = event.runners[i]
                
        if event.batterDestination == 0:
            newState.outs += 1
        elif event.batterDestination < 4:
            newState.bases[event.batterDestination] = event.batter
            
        if newState.inningBottom:
            newState.homeRuns += event.runsOnPlay
            newState.homeLineupIndex = (newState.homeLineupIndex + 1) % 9
        else:
            newState.awayRuns += event.runsOnPlay
            newState.awayLineupIndex = (newState.awayLineupIndex + 1) % 9
            
        return newState
            
        


class Game(object):
    '''
    The game to be played. Contains game logic, scores, and teams.
    '''
    
    def __init__(self, homeTeam=None, awayTeam=None, gameState=None):
        if homeTeam is None or awayTeam is None:
            self.state = gameState
        else:
            self.state = GameState()
            self.state.homeTeam = homeTeam
            self.state.awayTeam = awayTeam
        
    def play(self):
        if self.state.isComplete:
            return
        
        while self.state.inning <= 9 or self.state.homeRuns == self.state.awayRuns:            
            self.state.outs = 0
            self.state.inningBottom = False
            while self.state.outs < 3:
                batter = self.state.awayTeam.lineup[self.state.awayLineupIndex]
                result = simulatePA(batter)
                event = advanceRunners(batter, result, self.state)
                newState = self.state.addEvent(event)
                
                printState(self.state)
                printEvent(event)
                printState(newState)
                
                self.state = newState
                
                
            self.state.clearBases()
            
            if self.state.homeRuns <= self.state.awayRuns or self.state.inning < 9:
                
                self.state.outs = 0
                self.state.inningBottom = True
                while self.state.outs < 3:
                    if self.state.homeRuns > self.state.awayRuns and self.state.inning >= 9:
                        break
                    batter = self.state.homeTeam.lineup[self.state.homeLineupIndex]
                    result = simulatePA(batter)
                    event = advanceRunners(batter, result, self.state)
                    newState = self.state.addEvent(event)
                    
                    printState(self.state)
                    printEvent(event)
                    printState(newState)
                    
                    self.state = newState
                    
                self.state.clearBases()
            
            self.state.inning += 1
            
        self.state.isComplete = True
