'''
Created on Jul 31, 2013

@author: mejones
'''

if __name__ == '__main__':
    from Player import Player
    from Team import Team
    from Game import Game
    
    joe = Player('Regular', 'Joe')
    joe.rate1B = 0.150
    joe.rate2B = 0.050
    joe.rate3B = 0.005
    joe.rateHR = 0.050
    joe.rateBB = 0.100
    joe.rateHBP = 0.010
    
    home = Team('Hometown', 'Heroes')
    home.lineup[0] = joe
    home.lineup[1] = joe
    home.lineup[2] = joe
    home.lineup[3] = joe
    home.lineup[4] = joe
    home.lineup[5] = joe
    home.lineup[6] = joe
    home.lineup[7] = joe
    home.lineup[8] = joe
    
    away = Team('Outtatown', 'Baddies')
    away.lineup[0] = joe
    away.lineup[1] = joe
    away.lineup[2] = joe
    away.lineup[3] = joe
    away.lineup[4] = joe
    away.lineup[5] = joe
    away.lineup[6] = joe
    away.lineup[7] = joe
    away.lineup[8] = joe
    
    game = Game(home, away)
    game.play()
    
    print 'Game Over!'
    print home.fullName + ':' + str(game.homeRuns)
    print away.fullName + ':' + str(game.awayRuns)
