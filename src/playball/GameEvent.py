'''
Created on Aug 5, 2013

@author: mejones
'''

class GameEvent(object):
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
