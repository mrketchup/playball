'''
Handles all the logic behind game events.

@author: mejones
'''

from random import random
from GameEvent import Play

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
    
    result = Play.PlayTypes.GENERIC_OUT
    rand = random()
    if rand < n1B:
        result = Play.PlayTypes.SINGLE
    elif rand < n2B:
        result = Play.PlayTypes.DOUBLE
    elif rand < n3B:
        result = Play.PlayTypes.TRIPLE
    elif rand < nHR:
        result = Play.PlayTypes.HOMERUN
    elif rand < nBB:
        result = Play.PlayTypes.WALK
    elif rand < nHBP:
        result = Play.PlayTypes.HIT_BY_PITCH
        
    return result


def advanceRunners(batter, result, state):
    event = Play()
    event.batter = batter
    event.battingResult = result
    
    for i in range(1, len(state.bases)):
        if state.bases[i] is not None:
            event.runnerDestinations[i] = i
    
    if event.battingResult == Play.PlayTypes.GENERIC_OUT:
        event.batterDestination = Play.Destinations.OUT
        event.outsOnPlay += 1
        
    elif event.battingResult == Play.PlayTypes.SINGLE:
        event.batterDestination = Play.Destinations.FIRST
        rand = random()
        if state.bases[3] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[3] = Play.Destinations.EARNED_RUN
        if state.bases[2] is not None:
            if rand < 0.5:
                event.runnerDestinations[2] = Play.Destinations.EARNED_RUN
                event.runsOnPlay += 1
            else:
                event.runnerDestinations[2] = Play.Destinations.THIRD
        if state.bases[1] is not None:
            if rand < 0.2:
                event.runnerDestinations[1] = Play.Destinations.THIRD
            else:
                event.runnerDestinations[1] = Play.Destinations.SECOND
        
    elif event.battingResult == Play.PlayTypes.DOUBLE:
        event.batterDestination = Play.Destinations.SECOND
        if state.bases[3] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[3] = Play.Destinations.EARNED_RUN
        if state.bases[2] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[2] = Play.Destinations.EARNED_RUN
        if state.bases[1] is not None:
            if random() < 0.2:
                event.runsOnPlay += 1
                event.runnerDestinations[1] = Play.Destinations.EARNED_RUN
            else:
                event.runnerDestinations[1] = Play.Destinations.THIRD
        
    elif event.battingResult == Play.PlayTypes.TRIPLE:
        event.batterDestination = Play.Destinations.THIRD
        if state.bases[3] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[3] = Play.Destinations.EARNED_RUN
        if state.bases[2] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[2] = Play.Destinations.EARNED_RUN
        if state.bases[1] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[1] = Play.Destinations.EARNED_RUN
        
    elif event.battingResult == Play.PlayTypes.HOMERUN:
        event.batterDestination = Play.Destinations.EARNED_RUN
        event.runsOnPlay += 1
        if state.bases[3] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[3] = Play.Destinations.EARNED_RUN
        if state.bases[2] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[2] = Play.Destinations.EARNED_RUN
        if state.bases[1] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[1] = Play.Destinations.EARNED_RUN
            
    elif event.battingResult == Play.PlayTypes.WALK or event.battingResult == Play.PlayTypes.HIT_BY_PITCH:
        event.batterDestination = Play.Destinations.FIRST
        if state.bases[3] is not None and state.bases[2] is not None and state.bases[1] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[3] = Play.Destinations.EARNED_RUN
            event.runnerDestinations[2] = Play.Destinations.THIRD
            event.runnerDestinations[1] = Play.Destinations.SECOND
        elif state.bases[2] is not None and state.bases[1] is not None:
            event.runnerDestinations[2] = Play.Destinations.THIRD
            event.runnerDestinations[1] = Play.Destinations.SECOND
        elif state.bases[1] is not None:
            event.runnerDestinations[1] = Play.Destinations.SECOND
        
    return event

def nextEvent(state):
    batter = None
    if state.inningBottom:
        batter = state.homeTeam.lineup[state.homeLineupIndex]
    else:
        batter = state.awayTeam.lineup[state.awayLineupIndex]
    return advanceRunners(batter, simulatePA(batter), state)
