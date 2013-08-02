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
    runs = 0
    
    if result == 'OUT':
        pass
        
    elif result == '1B':            
        rand = random()
        if state.thirdBase is not None:
            runs += 1
            state.thirdBase = None
        if state.secondBase is not None:
            if rand < 0.5:
                runs += 1
            else:
                state.thirdBase = state.secondBase
            state.secondBase = None
        if state.firstBase is not None:
            if rand < 0.2:
                state.thirdBase = state.firstBase
            else:
                state.secondBase = state.firstBase
            state.firstBase = None
        
        state.firstBase = batter
        
    elif result == '2B':            
        if state.thirdBase is not None:
            runs += 1
            state.thirdBase = None
        if state.secondBase is not None:
            runs += 1
            state.secondBase = None
        if state.firstBase is not None:
            if random() < 0.2:
                runs += 1
            else:
                state.thirdBase = state.firstBase
            state.firstBase = None
            
        state.secondBase = batter
        
    elif result == '3B':            
        if state.thirdBase is not None:
            runs += 1
            state.thirdBase = None
        if state.secondBase is not None:
            runs += 1
            state.secondBase = None
        if state.firstBase is not None:
            runs += 1
            state.firstBase = None
            
        state.thirdBase = batter
        
    elif result == 'HR':
        runs += 1
        
        if state.thirdBase is not None:
            runs += 1
            state.thirdBase = None
        if state.secondBase is not None:
            runs += 1
            state.secondBase = None
        if state.firstBase is not None:
            runs += 1
            state.firstBase = None
            
    elif result == 'BB' or result == 'HBP':            
        if state.thirdBase is not None and state.secondBase is not None and state.firstBase is not None:
            runs += 1
            state.thirdBase = state.secondBase
            state.secondBase = state.firstBase
        elif state.secondBase is not None and state.firstBase is not None:
            state.thirdBase = state.secondBase
            state.secondBase = state.firstBase
        elif state.firstBase is not None:
            state.secondBase = state.firstBase
            
        state.firstBase = batter
        
    return runs


class GameState(object):
    '''
    Contains all important information regarding the state of a game.
    '''
    def __init__(self):
        self.firstBase = None
        self.secondBase = None
        self.thirdBase = None
        self.homeTeam = None
        self.awayTeam = None
        self.homeRuns = 0
        self.awayRuns = 0
        self.inning = 1
        self.outs = 0
        self.homeLineupIndex = 0
        self.awayLineupIndex = 0
        self.isComplete = False
        
    def clearBases(self):
        self.firstBase = None
        self.secondBase = None
        self.thirdBase = None
        


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
            while self.state.outs < 3:
                batter = self.state.awayTeam.lineup[self.state.awayLineupIndex]
                result = simulatePA(batter)
                runs = advanceRunners(batter, result, self.state)
                self.state.awayRuns += runs
                if result == 'OUT':
                    self.state.outs += 1
                self.state.awayLineupIndex = (self.state.awayLineupIndex + 1) % 9
                
            self.state.clearBases()
            
            if self.state.homeRuns <= self.state.awayRuns or self.state.inning < 9:
                
                self.state.outs = 0
                while self.state.outs < 3:
                    if self.state.homeRuns > self.state.awayRuns and self.state.inning >= 9:
                        break
                    batter = self.state.homeTeam.lineup[self.state.homeLineupIndex]
                    result = simulatePA(batter)
                    runs = advanceRunners(batter, result, self.state)
                    self.state.homeRuns += runs
                    if result == 'OUT':
                        self.state.outs += 1
                    self.state.homeLineupIndex = (self.state.homeLineupIndex + 1) % 9
                    
                self.state.clearBases()
            
            self.state.inning += 1
            
        self.state.isComplete = True
