'''
Created on Jul 31, 2013

@author: mejones
'''

from random import random
from Team import Team

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





class Diamond(object):
    '''
    Manages the baserunners.
    '''
    
    def __init__(self):
        self.first = None
        self.second = None
        self.third = None
        
    
    def advanceRunners(self, batter, result):
        runs = 0
        
        if result == 'OUT':
            pass
            
        elif result == '1B':            
            rand = random()
            if self.third is not None:
                runs += 1
                self.third = None
            if self.second is not None:
                if rand < 0.5:
                    runs += 1
                else:
                    self.third = self.second
                self.second = None
            if self.first is not None:
                if rand < 0.2:
                    self.third = self.first
                else:
                    self.second = self.first
                self.first = None
            
            self.first = batter
            
        elif result == '2B':            
            if self.third is not None:
                runs += 1
                self.third = None
            if self.second is not None:
                runs += 1
                self.second = None
            if self.first is not None:
                if random() < 0.2:
                    runs += 1
                else:
                    self.third = self.first
                self.first = None
                
            self.second = batter
            
        elif result == '3B':            
            if self.third is not None:
                runs += 1
                self.third = None
            if self.second is not None:
                runs += 1
                self.second = None
            if self.first is not None:
                runs += 1
                self.first = None
                
            self.third = batter
            
        elif result == 'HR':
            runs += 1
            
            if self.third is not None:
                runs += 1
                self.third = None
            if self.second is not None:
                runs += 1
                self.second = None
            if self.first is not None:
                runs += 1
                self.first = None
                
        elif result == 'BB' or result == 'HBP':            
            if self.third is not None and self.second is not None and self.first is not None:
                runs += 1
                self.third = self.second
                self.second = self.first
            elif self.second is not None and self.first is not None:
                self.third = self.second
                self.second = self.first
            elif self.first is not None:
                self.second = self.first
                
            self.first = batter
            
        return runs
    
    def clear(self):
        self.first = None
        self.second = None
        self.third = None





class Game(object):
    '''
    The game to be played. Contains game logic, scores, and teams.
    '''
    
    def __init__(self, homeTeam=None, awayTeam=None):
        self.homeTeam = homeTeam if homeTeam is not None else Team()
        self.awayTeam = awayTeam if awayTeam is not None else Team()
        self.homeRuns = 0
        self.awayRuns = 0
        self._isPlayed = False
        
    def play(self):
        if self._isPlayed:
            return
        
        self._isPlayed = True
        diamond = Diamond()
        inning = 1
        homeSpot = 0 # lineup spot
        awaySpot = 0
        
        while inning <= 9 or self.homeRuns == self.awayRuns:            
            outs = 0
            while outs < 3:
                batter = self.awayTeam.lineup[awaySpot]
                result = simulatePA(batter)
                runs = diamond.advanceRunners(batter, result)
                self.awayRuns += runs
                if result == 'OUT':
                    outs += 1
                awaySpot = (awaySpot + 1) % 9
                
            diamond.clear()
            
            if self.homeRuns <= self.awayRuns or inning < 9:
                
                outs = 0
                while outs < 3:
                    if self.homeRuns > self.awayRuns and inning >= 9:
                        break
                    batter = self.homeTeam.lineup[homeSpot]
                    result = simulatePA(batter)
                    runs = diamond.advanceRunners(batter, result)
                    self.homeRuns += runs
                    if result == 'OUT':
                        outs += 1
                    homeSpot = (homeSpot + 1) % 9
                    
                diamond.clear()
            
            inning += 1
