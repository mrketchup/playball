'''
Created on Jul 31, 2013

@author: mejones
'''

from Player import Player

class Team(object):
    '''
    Holds all the info about the team and roster of players.
    '''
    
    def __init__(self, city='Dumb City', name='Dummies'):
        self.city = city
        self.name = name
        
        self.lineup = []
        for i in range(9):
            self.lineup.append(Player())
        
    def fullName(self):
        return self.city + ' ' + self.name
