"""
Created on Jul 31, 2013

@author: mejones
"""

import random
import sys

import names

from playball.GameEventCallbacks import GameEventCallbacks
from playball.GameManager import GameManager


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
    p = Player(None, names.get_first_name(gender='male'), names.get_last_name())
    p.rate1B = random.gauss(0.154, 0.051)
    p.rate2B = random.gauss(0.044, 0.015)
    p.rate3B = random.gauss(0.004, 0.001)
    p.rateHR = random.gauss(0.025, 0.008)
    p.rateBB = random.gauss(0.079, 0.026)
    p.rateHBP = random.gauss(0.008, 0.003)
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
        while BA(p) < .2:
            p = randomPlayer()
        away.offensiveLineup[i] = p

    for i in range(9):
        p = randomPlayer()
        while BA(p) < .2:
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
    games = []
    for i in range(GAMES):
        game = Game(home_team=home, away_team=away)
        games.append(game)

    manager = GameManager(games)
    manager.subscribe_event_callback(GameEventCallbacks.print_event)
    manager.subscribe_game_end_callback(GameEventCallbacks.print_game_end)
    manager.play_games()

#     end = time()

#     print 'Time Elapsed:', (end - start)
#     print 'Games/Second:', GAMES / (end - start)
print "\nseed =", seed
