'''
Created on Aug 5, 2013

@author: mejones
'''

class GameEvent(object):
    '''
    '''
    
    def __init__(self):
        pass
        
        
class Play(GameEvent):
    '''Contains all info regarding a play.
    
    Attributes:
        balls - The number of balls
        
        strikes - The number of strikes
        
        pitchSequence - The sequence of pitches
        
        batter - The player batting
        
        pitcher - The player pitching
        
        playType - The type of play. All the possible types are:
            Generic out
            Strikeout
            Stolen base
            Defensive indifference
            Caught stealing
            Pickoff error
            Pickoff
            Wild pitch
            Passed ball
            Balk
            Foul error
            Walk
            Intentional walk
            Hit by pitch
            Interference
            Error
            Fielder's choice
            Single
            Double
            Triple
            Home run
            
        isSacHit - If the out was a sacrifice or not
        
        isSacFly - If the out was a sacrifice fly or not
        
        outsOnPlay - The number of outs on the play
        
        battedBallType - The type of batted ball. It is one of four types: fly
            ball, line drive, pop-up, or ground ball.
        
        isBunt - If the play was a bunt or not
        
        isFoul - If the play was a foul or not
        
        hitLocation - Where on the field the ball was hit
        errors - A list of errors on the play. An entry in the list will be a
            dictionary in the form of { player : errorType }. The error type is
            either a throw or a drop.
            
        batterDestination - The base where the batter wound up. Possibilities:
            0: Out
            1, 2, 3: 1st, 2nd, 3rd Bases
            4: Earned Run
            5: Unearned Run
            
        runnerDestinations - A list of the bases where the runners wound up.The
            list ignores the 0th index, so the integer index corresponds with
            the base (1=1st, 2=2nd, 3=3rd). If a base is empty, its value will
            be None. Possible destinations are:
                0: Out
                1, 2, 3: 1st, 2nd, 3rd Bases
                4: Earned Run
                5: Unearned Run
        
        runsOnPlay - The number of runs scored on the play
    '''
    
    def __init__(self):
        self.balls = 0
        self.strikes = 0
        self.pitchSequence = None
        self.batter = None
        self.pitcher = None
        self.playType = None   
        self.isSacHit = False
        self.isSacFly = False
        self.outsOnPlay = 0
        self.battedBallType = None
        self.isBunt = False
        self.isFoul = False
        self.hitLocation = None
        self.batterDestination = None
        self.runnerDestinations = [None, None, None, None]
        self.runsOnPlay = 0
