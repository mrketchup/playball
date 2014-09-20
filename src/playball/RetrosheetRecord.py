import re
import string

from playball import GameEvent, Player


__author__ = 'sam'


class RetrosheetRecord():
    def __init__(self, record_type):
        self.record_type = record_type

    @staticmethod
    def parse_row(row):
        row_type = row[0]
        if row_type == 'id':
            return Id(row)
        elif row_type == 'version':
            return Version(row)
        elif row_type == 'info':
            return Info(row)
        elif row_type == 'start':
            return Start(row)
        elif row_type == 'play':
            return Play(row)
        elif row_type == 'sub':
            return Sub(row)
        elif row_type == 'com':
            return Com(row)
        elif row_type == 'data':
            return Data(row)
        else:
            raise Exception("Cannot parse row: %s" % row)


class Id(RetrosheetRecord):
    def __init__(self, row):
        RetrosheetRecord.__init__(self, row[0])
        self.gameid = row[1]

    def __str__(self):
        return "id,{0}".format(self.gameid)


class Version(RetrosheetRecord):
    def __init__(self, row):
        RetrosheetRecord.__init__(self, row[0])
        self.version = row[1]

    def __str__(self):
        return "version,{0}".format(self.version)


class Info(RetrosheetRecord):
    def __init__(self, row):
        RetrosheetRecord.__init__(self, row[0])
        self.name = row[1]
        self.value = row[2]

    def __str__(self):
        return "info,{0},{1}".format(self.name, self.value)


class Start(RetrosheetRecord):
    def __init__(self, row):
        RetrosheetRecord.__init__(self, row[0])
        self.retrosheet_id = row[1]
        self.player_name = row[2]
        self.team = row[3]
        self.batting_position = row[4]
        self.fielding_position = row[5]

    def __str__(self):
        return 'start,{0},"{1}",{2},{3},{4}'.format(self.retrosheet_id, self.player_name, self.team,
                                                    self.batting_position, self.fielding_position)


class Play(RetrosheetRecord):
    def __init__(self, row):
        RetrosheetRecord.__init__(self, row[0])
        self.inning = int(row[1])
        self.inningHalf = int(row[2])
        self.batterId = row[3]
        self.balls = int(row[4][0])
        self.strikes = int(row[4][1])
        self.pitchSequence = row[5]
        self.playString = row[6]

    def __str__(self):
        return "play,{0},{1},{2},{3}{4},{5},{6}".format(
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


class Sub(RetrosheetRecord):
    def __init__(self, row):
        RetrosheetRecord.__init__(self, row[0])
        self.playerId = row[1]
        self.playerName = row[2]
        self.team = int(row[3])
        self.battingOrder = int(row[4])
        self.position = int(row[5])

    def __str__(self):
        return 'sub,{0},"{1}",{2},{3},{4}'.format(
            self.playerId, self.playerName, self.team, self.battingOrder, self.position
        )


class Com(RetrosheetRecord):
    def __init__(self, row):
        RetrosheetRecord.__init__(self, row[0])
        self.comment = row[1]

    def __str__(self):
        return 'com,"{0}"'.format(self.comment)


class Data(RetrosheetRecord):
    def __init__(self, row):
        RetrosheetRecord.__init__(self, row[0])
        self.name = row[1]
        self.retrosheet_id = row[2]
        self.value = row[3]

    def __str__(self):
        return "data,{0},{1},{2}".format(self.name, self.retrosheet_id, self.value)
