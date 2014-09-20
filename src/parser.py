from playball.RetrosheetScorebook import RetrosheetScorebook

__author__ = 'sam'

scorebook = RetrosheetScorebook("../data/2012eve/2012BAL.EVA")

for game in scorebook.games:
    print game

print "Games:", len(scorebook.games)