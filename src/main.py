'''
Created on Jul 31, 2013

@author: mejones
'''

if __name__ == '__main__':
    from playball import Player
    from playball import Team
    from playball import Game
    from time import time
    
    p = Player()
    p.rate1B = 0.150
    p.rate2B = 0.050
    p.rate3B = 0.005
    p.rateHR = 0.050
    p.rateBB = 0.100
    p.rateHBP = 0.010
    
    home = Team()
    away = Team()
    
    for i in range(9):
        home.lineup[i] = p
        away.lineup[i] = p
    
    GAMES = 1
    
    start = time()
    
    for i in range(GAMES):
        game = Game(home, away)
        game.play()
        
    end = time()
    
    print 'Time Elapsed:', (end - start)
    print 'Games/Second:', GAMES / (end - start)
