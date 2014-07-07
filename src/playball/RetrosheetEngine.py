from collections import deque
import csv
import sys

from playball import GameEvent, Game, Player
from playball.GameEngine import GameEngine
from playball.GameEventCallbacks import GameEventCallbacks
from playball.GameManager import GameManager


__author__ = 'Sam'


class RetrosheetEngine(GameEngine):
    def __init__(self):
        self.records = deque()

    def append_record(self, event):
        self.records.append(event)

    def next_event(self, state):
        if len(self.records) > 0:
            record = self.records.popleft()
            return record.to_event()


class RetrosheetParser():
    def __init__(self, filename):
        self.games = deque()
        with open(filename, 'rb') as f:
            reader = csv.reader(f)
            engine = None
            try:
                for row in reader:
                    record = RetrosheetParser.Record.parse_row(row)
                    if isinstance(record, RetrosheetParser.Id):
                        engine = RetrosheetEngine()
                        game = Game(engine)
                        self.games.append(game)
                    engine.append_record(record)
            except csv.Error as e:
                sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

    def simulate_games(self):
        manager = GameManager(self.games)
        manager.subscribe_event_callback(GameEventCallbacks.print_event)
        manager.subscribe_game_end_callback(GameEventCallbacks.print_game_end)
        manager.play_games()

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
            # TODO - parse the play string

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