import difflib
import sys
from playball.RetrosheetScorebook import RetrosheetScorebook

__author__ = 'sam'

scorebook = RetrosheetScorebook()
scorebook.read("../data/2012eve/2012BAL.EVA")
scorebook.write("../data/test.txt")

f1 = open("../data/2012eve/2012BAL.EVA")
f2 = open("../data/test.txt")

for line in difflib.context_diff(f1.readlines(), f2.readlines()):
    sys.stdout.write(line)