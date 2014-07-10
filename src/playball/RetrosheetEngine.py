from collections import deque
import csv
import re
import string
import sys

from playball import GameEvent, Player
from playball.GameEngine import GameEngine


__author__ = 'Sam'


class RetrosheetEngine(GameEngine):
    def __init__(self):
        self.records = deque()
        self.events = deque()

    def append_record(self, event):
        self.records.append(event)

    def next_event(self, state):
        if len(self.records) > 0:
            while True:
                record = self.records.popleft()
                if isinstance(record, RetrosheetParser.Play):
                    return record.to_event()


class RetrosheetParser():
    def __init__(self, filename):
        self.engines = deque()
        with open(filename, 'rb') as f:
            reader = csv.reader(f)
            engine = None
            try:
                for row in reader:
                    record = RetrosheetParser.Record.parse_row(row)
                    if isinstance(record, RetrosheetParser.Id):
                        engine = RetrosheetEngine()
                        self.engines.append(engine)
                    engine.append_record(record)
            except csv.Error as e:
                sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

    class Record():
        def __init__(self):
            pass

        @staticmethod
        def parse_row(row):
            row_type = row[0]
            if row_type == 'id':
                return RetrosheetParser.Id(row)
            elif row_type == 'version':
                return RetrosheetParser.Version(row)
            elif row_type == 'info':
                return RetrosheetParser.Info(row)
            elif row_type == 'start':
                return RetrosheetParser.Start(row)
            elif row_type == 'play':
                return RetrosheetParser.Play(row)
            elif row_type == 'sub':
                return RetrosheetParser.Sub(row)
            elif row_type == 'com':
                return RetrosheetParser.Com(row)
            elif row_type == 'data':
                return RetrosheetParser.Data(row)
            else:
                raise Exception("Cannot parse row: %s" % row)

    class Id(Record):
        def __init__(self, record):
            RetrosheetParser.Record.__init__(self)
            self.id = record[1]

        def __str__(self):
            return "id, {0}".format(self.id)

    class Version(Record):
        def __init__(self, record):
            RetrosheetParser.Record.__init__(self)
            self.version = record[1]

        def __str__(self):
            return "version, {0}".format(self.version)

    class Info(Record):
        def __init__(self, record):
            RetrosheetParser.Record.__init__(self)
            self.name = record[1]
            self.value = record[2]

        def __str__(self):
            return "info, {0}, {1}".format(self.name, self.value)

    class Start(Record):
        def __init__(self, record):
            RetrosheetParser.Record.__init__(self)
            self.retrosheet_id = record[1]
            self.player_name = record[2]
            self.team = record[3]
            self.batting_position = record[4]
            self.fielding_position = record[5]

        def __str__(self):
            return "start, {0}, {1}, {2}, {3}, {4}".format(self.retrosheet_id, self.player_name, self.team,
                                                           self.batting_position, self.fielding_position)

    class Play(Record):
        def __init__(self, record):
            RetrosheetParser.Record.__init__(self)
            self.inning = int(record[1])
            self.inningHalf = int(record[2])
            self.batterId = record[3]
            self.balls = int(record[4][0])
            self.strikes = int(record[4][1])
            self.pitchSequence = record[5]
            self.playString = record[6]

        def __str__(self):
            return "play, {0}, {1}, {2}, {3}{4}, {5}, {6}".format(
                self.inning, self.inningHalf, self.batterId, self.balls, self.strikes, self.pitchSequence,
                self.playString
            )

        def to_event(self):
            play = GameEvent.Play()
            play.batter = Player(self.batterId)
            play.balls = self.balls
            play.strikes = self.strikes
            play.pitchSequence = self.pitchSequence
            self.parse_play_string(play)
            return play

        def parse_play_string(self, play):
            p = re.compile('(\w+)(/[A-Z1-9-\+]+)*(\..+)*')
            m = p.match(self.playString)
            if m is not None:
                self.parse_description(m.group(1), play)
                if m.group(2) is not None:
                    self.parse_modifiers(m.group(2), play)
                if m.group(3) is not None:
                    self.parse_advances(m.group(3), play)
            else:
                raise Exception("Cannot parse play string:", self.playString)

        @staticmethod
        def parse_description(group, play):
            play.fielders = group
            if group[0] in string.digits:
                play.battingResult = GameEvent.Play.PlayTypes.GENERIC_OUT
                play.fielders = group
            elif group[0] == 'S':
                play.battingResult = GameEvent.Play.PlayTypes.SINGLE
                play.fielders = group[1:]
            elif group[0] == 'D':
                play.battingResult = GameEvent.Play.PlayTypes.DOUBLE
                play.fielders = group[1:]
            elif group[0] == 'T':
                play.battingResult = GameEvent.Play.PlayTypes.TRIPLE
                play.fielders = group[1:]
            elif group == 'W':
                play.battingResult = GameEvent.Play.PlayTypes.WALK
            elif group == 'HR':
                play.battingResult = GameEvent.Play.PlayTypes.HOMERUN
            elif group == 'K':
                play.battingResult = GameEvent.Play.PlayTypes.STRIKEOUT
            elif group == 'NP':
                play.battingResult = GameEvent.Play.PlayTypes.NO_PLAY
            else:
                raise Exception("Cannot parse play description:", group)

        @staticmethod
        def parse_modifiers(group, play):
            # remove the first /
            group = group[1:]
            modifiers = group.split('/')
            for modifier in modifiers:
                if modifier == 'G':
                    play.battedBallType = GameEvent.Play.BattedBallTypes.GROUND_BALL
                elif modifier == 'G-':
                    play.battedBallType = GameEvent.Play.BattedBallTypes.GROUND_BALL
                    play.hitStrength = '-'
                elif modifier == 'G+':
                    play.battedBallType = GameEvent.Play.BattedBallTypes.GROUND_BALL
                    play.hitStrength = '+'
                elif modifier == 'F':
                    play.battedBallType = GameEvent.Play.BattedBallTypes.FLY_BALL
                elif modifier == 'L':
                    play.battedBallType = GameEvent.Play.BattedBallTypes.LINE_DRIVE
                elif modifier == 'L+':
                    play.battedBallType = GameEvent.Play.BattedBallTypes.LINE_DRIVE
                    play.hitStrength = '+'
                elif modifier == 'P':
                    play.battedBallType = GameEvent.Play.BattedBallTypes.POP_UP
                elif modifier == 'BG':
                    play.battedBallType = GameEvent.Play.BattedBallTypes.GROUND_BALL
                    play.isBunt = True
                elif modifier[0].isdigit():
                    play.hitLocation = modifier
                else:
                    raise Exception("Cannot parse modifier:", modifier)

        @staticmethod
        def parse_advances(group, play):
            # remove the .
            group = group[1:]
            advances = group.split(';')
            for advance in advances:
                if advance[1] == '-':
                    bases = advance.split('-')
                    runner = bases[0]
                    destination = bases[1]
                    if destination == 'H':
                        destination = 4
                    if runner == 'B':
                        play.batterDestination = destination
                    elif runner.isdigit():
                        play.runnerDestinations[int(runner)] = destination
                    else:
                        raise Exception("Cannot parse advance:", group)
                elif advance[1] == 'X':
                    p = re.compile('([B123])X([123H])\((\d+)\)')
                    m = p.match(advance)
                    if m is not None:
                        play.fielders = m.group(3)
                    else:
                        raise Exception("Cannot parse advance:", group)
                else:
                    raise Exception("Cannot parse advance:", group)

    class Sub(Record):
        def __init__(self, record):
            RetrosheetParser.Record.__init__(self)
            self.playerId = record[1]
            self.playerName = record[2]
            self.team = int(record[3])
            self.battingOrder = int(record[4])
            self.position = int(record[5])

        def __str__(self):
            return "sub, {0}, {1}, {2}, {3}, {4}".format(
                self.playerId, self.playerName, self.team, self.battingOrder, self.position
            )

    class Com(Record):
        def __init__(self, record):
            RetrosheetParser.Record.__init__(self)
            self.comment = record[1]

        def __str__(self):
            return "com, {0}".format(self.comment)

    class Data(Record):
        def __init__(self, record):
            RetrosheetParser.Record.__init__(self)
            self.name = record[1]
            self.retrosheet_id = record[2]
            self.value = record[3]

        def __str__(self):
            return "data, {0}, {1}, {2}".format(self.name, self.retrosheet_id, self.value)