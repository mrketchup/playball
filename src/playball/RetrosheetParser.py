import csv
import sys
from GameEngine import GameEngine
from collections import deque
from playball import Game
from playball import GameEvent

__author__ = 'sam'


class RetrosheetParser():
    def __init__(self, filename):
        self.games = deque()
        with open(filename, 'rb') as f:
            reader = csv.reader(f)
            engine = None
            try:
                for row in reader:
                    if row[0] == 'info':
                        engine = RetrosheetEngine()
                        game = Game(engine)
                        self.games.append(game)
                    else:
                        record = self.parseRow(row)
                        if engine is not None:
                            engine.appendRecord(record)
            except csv.Error as e:
                sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

    def simulateGames(self):
        for game in self.games:
            game.play()

    def parseRow(self, row):
        eventType = row[0]
        if eventType == 'play':
            print Play(row)
            return Play(row)
        elif eventType == 'sub':
            print Sub(row)
            return Sub(row)


class RetrosheetEngine(GameEngine):
    def __init__(self):
        self.records = deque()

    def appendRecord(self, event):
        self.records.append(event)

    def nextEvent(self, state):
        if len(self.records) > 0:
            record = self.records.popleft()
            if record is Play:
                return GameEvent.Play()
            elif record is Sub:
                return GameEvent.Substitution()


class Record():
    pass


class Play(Record):
    def __init__(self, record):
        self.inning = int(record[1])
        self.inningHalf = int(record[2])
        self.batterId = record[3]
        self.balls = int(record[4][0])
        self.strikes = int(record[4][1])
        self.pitchSequence = record[5]
        self.playString = record[6]

    def __str__(self):
        return "play, {0}, {1}, {2}, {3}{4}, {5}, {6}".format(
            self.inning, self.inningHalf, self.batterId, self.balls, self.strikes, self.pitchSequence, self.playString
        )


class Sub(Record):
    def __init__(self, record):
        self.playerId = record[1]
        self.playerName = record[2]
        self.team = int(record[3])
        self.battingOrder = int(record[4])
        self.position = int(record[5])

    def __str__(self):
        return "sub, {0}, {1}, {2}, {3}, {4}".format(
            self.playerId, self.playerName, self.team, self.battingOrder, self.position
        )