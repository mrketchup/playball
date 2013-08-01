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
            print batter.fullName, 'is out.'
            
        elif result == '1B':
            print batter.fullName, 'singles.'
            
            rand = random()
            if self.third is not None:
                runs += 1
                print ' *', self.third.fullName, 'scores.'
                self.third = None
            if self.second is not None:
                if rand < 0.5:
                    runs += 1
                    print ' *', self.second.fullName, 'scores.'
                else:
                    self.third = self.second
                    print ' *', self.second.fullName, 'goes to third.'
                self.second = None
            if self.first is not None:
                if rand < 0.2:
                    self.third = self.first
                    print ' *', self.first.fullName, 'goes to third.'
                else:
                    self.second = self.first
                    print ' *', self.first.fullName, 'goes to second.'
                self.first = None
            
            self.first = batter
            
        elif result == '2B':
            print batter.fullName, 'doubles.'
            
            if self.third is not None:
                runs += 1
                print ' *', self.third.fullName, 'scores.'
                self.third = None
            if self.second is not None:
                runs += 1
                print ' *', self.second.fullName, 'scores.'
                self.second = None
            if self.first is not None:
                if random() < 0.2:
                    runs += 1
                    print ' *', self.first.fullName, 'scores.'
                else:
                    self.third = self.first
                    print ' *', self.first.fullName, 'goes to third.'
                self.first = None
                
            self.second = batter
            
        elif result == '3B':
            print batter.fullName, 'triples.'
            
            if self.third is not None:
                runs += 1
                print ' *', self.third.fullName, 'scores.'
                self.third = None
            if self.second is not None:
                runs += 1
                print ' *', self.second.fullName, 'scores.'
                self.second = None
            if self.first is not None:
                runs += 1
                print ' *', self.first.fullName, 'scores.'
                self.first = None
                
            self.third = batter
            
        elif result == 'HR':
            print batter.fullName, 'homers.'
            runs += 1
            
            if self.third is not None:
                runs += 1
                print ' *', self.third.fullName, 'scores.'
                self.third = None
            if self.second is not None:
                runs += 1
                print ' *', self.second.fullName, 'scores.'
                self.second = None
            if self.first is not None:
                runs += 1
                print ' *', self.first.fullName, 'scores.'
                self.first = None
                
        elif result == 'BB':
            print batter.fullName, 'walks.'
            
            if self.third is not None and self.second is not None and self.first is not None:
                runs += 1
                print ' *', self.third.fullName, 'scores.'
                print ' *', self.second.fullName, 'goes to third.'
                print ' *', self.first.fullName, 'goes to second.'
                self.third = self.second
                self.second = self.first
            elif self.second is not None and self.first is not None:
                print ' *', self.second.fullName, 'goes to third.'
                print ' *', self.first.fullName, 'goes to second.'
                self.third = self.second
                self.second = self.first
            elif self.first is not None:
                print ' *', self.first.fullName, 'goes to second.'
                self.second = self.first
                
            self.first = batter
            
        elif result == 'HBP':
            print batter.fullName, 'is hit by pitch.'
            
            if self.third is not None and self.second is not None and self.first is not None:
                runs += 1
                print ' *', self.third.fullName, 'scores.'
                print ' *', self.second.fullName, 'goes to third.'
                print ' *', self.first.fullName, 'goes to second.'
                self.third = self.second
                self.second = self.first
            elif self.second is not None and self.first is not None:
                print ' *', self.second.fullName, 'goes to third.'
                print ' *', self.first.fullName, 'goes to second.'
                self.third = self.second
                self.second = self.first
            elif self.first is not None:
                print ' *', self.first.fullName, 'goes to second.'
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
        
    def play(self):
        diamond = Diamond()
        inning = 1
        homeSpot = 0 # lineup spot
        awaySpot = 0
        
        while inning <= 9 or self.homeRuns == self.awayRuns:
            print '----  TOP  ', str(inning), ' ----'
            
            outs = 0
            while outs < 3:
                batter = self.awayTeam.lineup[awaySpot]
                result = simulatePA(batter)
                runs = diamond.advanceRunners(batter, result)
                self.awayRuns += runs
                if result == 'OUT':
                    outs += 1
                awaySpot = awaySpot + 1 if awaySpot < 8 else 0
                
            diamond.clear()
            
            if self.homeRuns <= self.awayRuns or inning < 9:
                print '---- BOTTOM', str(inning), ' ----'
                
                outs = 0
                while outs < 3:
                    if self.homeRuns > self.awayRuns and inning >= 9:
                        break
                    batter = self.homeTeam.lineup[awaySpot]
                    result = simulatePA(batter)
                    runs = diamond.advanceRunners(batter, result)
                    self.homeRuns += runs
                    if result == 'OUT':
                        outs += 1
                    homeSpot = homeSpot + 1 if homeSpot < 8 else 0
                    
                diamond.clear()
                inning += 1
