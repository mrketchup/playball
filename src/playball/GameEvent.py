'''
Created on Aug 5, 2013

@author: mejones
'''

class Enum(object):
    '''Used for putting together an enum.
    TODO: Move to Utils when Sam commits it
    '''
    def __init__(self, *sequential, **named):
        self.__dict__ = dict(zip(sequential, range(len(sequential))), **named)
        self.reverse_mapping = dict((value, key) for key, value in self.__dict__.iteritems())

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
        
        pitchSequence - The sequence list of pitches. All of the possible pitch
            types are:
                B  ball
                C  called strike
                F  foul
                H  hit batter
                I  intentional ball
                K  strike (unknown type)
                L  foul bunt
                M  missed bunt attempt
                N  no pitch (on balks and interference calls)
                O  foul tip on bunt
                P  pitchout
                Q  swinging on pitchout
                R  foul ball on pitchout
                S  swinging strike
                T  foul tip
                U  unknown or missed pitch
                V  called ball because pitcher went to his mouth
                X  ball put into play by batter
                Y  ball put into play on pitchout

                1  pickoff throw to first
                2  pickoff throw to second
                3  pickoff throw to third
                >  Indicates a runner going on the following pitch
                +  indicated the following pickoff throw by the catcher
                *  indicates the following pitch was blocked by the catcher
                .  marker for play not involving the batter
        
        batter - The player batting
        
        pitcher - The player pitching

        fielders - The sequence of all the fielders involved in the play
        
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
                Homerun
            All the play types are enumerated in the static PlayTypes enum. The
            names are in the all caps & underscore format ('Single' = SINGLE,
            'Generic out' = GENERIC_OUT, etc).
            
        isSacHit - If the out was a sacrifice or not
        
        isSacFly - If the out was a sacrifice fly or not
        
        outsOnPlay - The number of outs on the play
        
        battedBallType - The type of batted ball. It is one of four types: fly
            ball, line drive, pop-up, or ground ball. All the batted ball types
            are enumerated in the static BattedBallTypes enum. The names are in
            the all caps & underscore format ('fly ball' = FLY_BALL, 'pop-up' =
            POP_UP, etc).
        
        isBunt - If the play was a bunt or not
        
        isFoul - If the play was a foul or not
        
        hitLocation - Where on the field the ball was hit. See
            http://www.retrosheet.org/location.htm for details.
        
        errors - A list of errors on the play. An entry in the list will be a
            dictionary in the form of { player : errorType }. The error type is
            either a throw or a drop.
            
        batterDestination - The base where the batter wound up. Possibilities
            are defined by the static Destinations enum:
                0: OUT
                1, 2, 3: FIRST, SECOND, THIRD
                4: EARNED_RUN
                5: UNEARNED_RUN
            
        runnerDestinations - A list of the bases where the runners wound up.The
            list ignores the 0th index, so the integer index corresponds with
            the base (1=1st, 2=2nd, 3=3rd). If a base is empty, its value will
            be None. Possible destinations are defined by the static
            Destinations enum:
                0: OUT
                1, 2, 3: FIRST, SECOND, THIRD
                4: EARNED_RUN
                5: UNEARNED_RUN
        
        runsOnPlay - The number of runs scored on the play
    '''
    
    PlayTypes = Enum("GENERIC_OUT", "STRIKEOUT", "STOLEN_BASE",
                     "DEFENSIVE_INDIFFERENCE", "CAUGHT_STEALING",
                     "PICKOFF_ERROR", "PICKOFF", "WILD_PITCH", "PASSED_BALL",
                     "BALK", "FOUL_ERROR", "WALK", "INTENIONAL_WALK",
                     "HIT_BY_PITCH", "INTERFERENCE", "ERROR", "FIELDERS_CHOICE",
                     "SINGLE", "DOUBLE", "TRIPLE", "HOMERUN")
    
    BattedBallTypes = Enum("FLY_BALL","LINE_DRIVE", "POP_UP", "GROUND_BALL")
    
    Destinations = Enum("OUT", "FIRST", "SECOND", "THIRD", "EARNED_RUN",
                        "UNEARNED_RUN")
    
    def __init__(self):
        self.balls = 0
        self.strikes = 0
        self.pitchSequence = []
        self.batter = None
        self.pitcher = None
        self.fielders = []
        self.playType = 0   
        self.isSacHit = False
        self.isSacFly = False
        self.outsOnPlay = 0
        self.battedBallType = 0
        self.isBunt = False
        self.isFoul = False
        self.hitLocation = None
        self.batterDestination = 0
        self.runnerDestinations = [None, None, None, None]
        self.runsOnPlay = 0
        
    
class Substitution(GameEvent):
    '''
    '''
    
    def __init__(self):
        self.player = None
        self.team = None
        self.offensiveLineupIndex = 0
        self.defensiveLineupIndex = 0


class LineupAdjustment(GameEvent):
    '''
    '''

    def __init__(self):
        self.team = None
        self.offensiveLineupIndex = 0


class BattingAdjustment(GameEvent):
    '''
    '''

    def __init__(self):
        self.player = None
        self.hand = None


class PitchingAdjustment(GameEvent):
    '''
    '''

    def __init__(self):
        self.player = None
        self.hand = None


class Comment(GameEvent):
    '''
    '''

    def __init__(self):
        self.comment = None
