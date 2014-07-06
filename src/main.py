"""
Created on Jul 31, 2013

@author: mejones
"""

from random import random as rand
from playball.GameEvent import Play
import names


def notify(preState, postState, event):
    tb = "Bottom" if preState.inningBottom else "Top"
    print "-------------- %6s  %2d --------------" % (tb, preState.inning)
    print "Away: %s: %d" % (preState.awayTeam.full_name(), preState.awayRuns)
    print "Home: %s: %d" % (preState.homeTeam.full_name(), preState.homeRuns)
    print "Outs:", preState.outs
    print "-" * 40

    print "Batter:", event.batter.full_name()
    print "Batting Result:", Play.PlayTypes.reverse_mapping[event.battingResult]

    for i in range(1, len(preState.bases)):
        if preState.bases[i] is not None and i != event.runnerDestinations[i]:
            if event.runnerDestinations[i] >= 4:
                print " * %s scores." % (preState.bases[i].full_name())
            else:
                print " * %s goes to %s." % (preState.bases[i].full_name(),
                                             event.runnerDestinations[i])
    print ''


import random
import sys
seed = random.randint(0, sys.maxint)
random.seed(seed)

def AB(p):
    return (1 - p.rateBB - p.rateHBP)

def BA(p):
    return (p.rate1B + p.rate2B + p.rate3B + p.rateHR) / AB(p)

def OBP(p):
    return p.rate1B + p.rate2B + p.rate3B + p.rateHR + p.rateBB + p.rateHBP

def SLG(p):
    return (p.rate1B + 2 * p.rate2B + 3 * p.rate3B + 4 * p.rateHR) / AB(p)

def OPS(p):
    return OBP(p) + SLG(p)

def orderLineup(lineup):
    lineup = sorted(lineup, key=lambda p: OPS(p))
    lineup = sorted(lineup[:-2], key=lambda p: OBP(p), reverse=True) + lineup[-2:]
    lineup = lineup[:2] + sorted(lineup[2:], key=lambda p: OPS(p), reverse=True)
    lineup = lineup[:4] + sorted(lineup[4:], key=lambda p: SLG(p), reverse=True)
    lineup = lineup[:5] + sorted(lineup[5:], key=lambda p: OPS(p), reverse=True)
    return lineup

def playerString(p):
    ba = ('%.3f' % (BA(p))).lstrip('0')
    obp = ('%.3f' % (OBP(p))).lstrip('0')
    slg = ('%.3f' % (SLG(p))).lstrip('0')
    ops = ('%.3f' % (OPS(p))).lstrip('0')
    
    return '%20s (%s/%s/%s/%s)' % (p.full_name(), ba, obp, slg, ops)

def randomPlayer():
    p = Player(names.get_first_name(gender='male'), names.get_last_name())
    p.rate1B = rand() * 0.075 + 0.100
    p.rate2B = rand() * 0.030 + 0.030
    p.rate3B = rand() * 0.014 + 0.001
    p.rateHR = rand() * 0.045 + 0.005
    p.rateBB = rand() * 0.160 + 0.015
    p.rateHBP = rand() * 0.012 + 0.003
    return p

if __name__ == '__main__':
    from playball import Player
    from playball import Team
    from playball import Game
#     from time import time
    
    home = Team('Hometown', 'Heroes')
    away = Team('Outtatown', 'Villains')
    
    for i in range(9):
        p = randomPlayer()
        away.offensiveLineup[i] = p
    
    for i in range(9):
        p = randomPlayer()
        home.offensiveLineup[i] = p
        
    away.offensiveLineup = orderLineup(away.offensiveLineup)
    home.offensiveLineup = orderLineup(home.offensiveLineup)
    
    print 'AWAY:'
    for i in range(9):
        print str(i+1) + ": " + playerString(away.offensiveLineup[i])
    
    print 'HOME:'
    for i in range(9):
        print str(i+1) + ": " + playerString(home.offensiveLineup[i])
    
    GAMES = 1
    
#     start = time()
    print
    for i in range(GAMES):
        game = Game(home_team=home, away_team=away)
        for preState, postState, event in game.play():
            notify(preState, postState, event)

        print "--------------    FINAL   --------------"
        print "Away: %s: %d" % (away.full_name(), game.state.awayRuns)
        print "Home: %s: %d" % (home.full_name(), game.state.homeRuns)
        
#     end = time()
    
#     print 'Time Elapsed:', (end - start)
#     print 'Games/Second:', GAMES / (end - start)
print "\nseed =", seed
