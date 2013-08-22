'''
Created on Jul 31, 2013

@author: mejones
'''

class Player(object):
    '''
    The Player class. Contains all info on the player.
    '''
    
    def __init__(self, firstName='Dumb', lastName='Dummy'):
        self.firstName = firstName
        self.lastName = lastName
        self.rate1B = 0.000
        self.rate2B = 0.000
        self.rate3B = 0.000
        self.rateHR = 0.000
        self.rateBB = 0.000
        self.rateHBP = 0.000
        
    def fullName(self):
        return self.firstName + ' ' + self.lastName
