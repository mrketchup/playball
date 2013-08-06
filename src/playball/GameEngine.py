'''
Handles all the logic behind game events.

@author: mejones
'''

from random import random
from GameEvent import GameEvent

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
    event = GameEvent()
    event.batter = batter
    event.battingResult = result
    
    for i in range(1, len(state.bases)):
        event.runners[i] = state.bases[i]
        if event.runners[i] is not None:
            event.runnerDestinations[i] = i
    
    if event.battingResult == 'OUT':
        event.batterDestination = 0
        event.outsOnPlay += 1
        
    elif event.battingResult == '1B':
        event.batterDestination = 1
        rand = random()
        if event.runners[3] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[3] = 4
        if event.runners[2] is not None:
            if rand < 0.5:
                event.runnerDestinations[2] = 4
                event.runsOnPlay += 1
            else:
                event.runnerDestinations[2] = 3
        if event.runners[1] is not None:
            if rand < 0.2:
                event.runnerDestinations[1] = 3
            else:
                event.runnerDestinations[1] = 2
        
    elif event.battingResult == '2B':
        event.batterDestination = 2
        if event.runners[3] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[3] = 4
        if event.runners[2] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[2] = 4
        if event.runners[1] is not None:
            if random() < 0.2:
                event.runsOnPlay += 1
                event.runnerDestinations[1] = 4
            else:
                event.runnerDestinations[1] = 3
        
    elif event.battingResult == '3B':
        event.batterDestination = 3
        if event.runners[3] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[3] = 4
        if event.runners[2] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[2] = 4
        if event.runners[1] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[1] = 4
        
    elif event.battingResult == 'HR':
        event.batterDestination = 4
        event.runsOnPlay += 1
        if event.runners[3] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[3] = 4
        if event.runners[2] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[2] = 4
        if event.runners[1] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[1] = 4
            
    elif event.battingResult == 'BB' or event.battingResult == 'HBP':
        event.batterDestination = 1
        if event.runners[3] is not None and event.runners[2] is not None and event.runners[1] is not None:
            event.runsOnPlay += 1
            event.runnerDestinations[3] = 4
            event.runnerDestinations[2] = 3
            event.runnerDestinations[1] = 2
        elif event.runners[2] is not None and event.runners[1] is not None:
            event.runnerDestinations[2] = 3
            event.runnerDestinations[1] = 2
        elif event.runners[1] is not None:
            event.runnerDestinations[1] = 2
        
    return event

def nextEvent(state):
    batter = None
    if state.inningBottom:
        batter = state.homeTeam.lineup[state.homeLineupIndex]
    else:
        batter = state.awayTeam.lineup[state.awayLineupIndex]
    result = simulatePA(batter)
    return advanceRunners(batter, result, state)
