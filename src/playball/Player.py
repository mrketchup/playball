"""
Created on Jul 31, 2013

@author: mejones
"""


class Player(object):
    """
    The Player class. Contains all info on the player.
    """

    def __init__(self, retrosheet_id, first_name='Dumb', last_name='Dummy'):
        self.retrosheet_id = retrosheet_id
        self.firstName = first_name
        self.lastName = last_name
        self.rate1B = 0.000
        self.rate2B = 0.000
        self.rate3B = 0.000
        self.rateHR = 0.000
        self.rateBB = 0.000
        self.rateHBP = 0.000

    def full_name(self):
        return self.firstName + ' ' + self.lastName
