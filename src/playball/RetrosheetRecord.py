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
            return Id(game_id=row[1])
        elif row_type == 'version':
            return Version(version=row[1])
        elif row_type == 'info':
            return Info(name=row[1], value=row[2])
        elif row_type == 'start':
            return Start(retrosheet_id=row[1], player_name=row[2], team=row[3], batting_position=row[4],
                         fielding_position=row[5])
        elif row_type == 'play':
            return Play(inning=row[1], inning_half=row[2], batter_id=row[3], balls=row[4][0], strikes=row[4][1],
                        pitch_sequence=row[5], play_string=row[6])
        elif row_type == 'sub':
            return Sub(player_id=row[1], player_name=row[2], team=row[3], batting_order=row[4], position=row[5])
        elif row_type == 'com':
            return Com(comment=row[1])
        elif row_type == 'data':
            return Data(name=row[1], retrosheet_id=row[2], value=row[3])
        else:
            raise Exception("Cannot parse row: %s" % row)


class Id(RetrosheetRecord):
    def __init__(self, game_id=None):
        RetrosheetRecord.__init__(self, "id")
        self.game_id = game_id

    def __str__(self):
        return "id,{0}".format(self.game_id)


class Version(RetrosheetRecord):
    def __init__(self, version=None):
        RetrosheetRecord.__init__(self, "version")
        self.version = version

    def __str__(self):
        return "version,{0}".format(self.version)


class Info(RetrosheetRecord):
    def __init__(self, name=None, value=None):
        RetrosheetRecord.__init__(self, "info")
        self.name = name
        self.value = value

    def __str__(self):
        return "info,{0},{1}".format(self.name, self.value)


class Start(RetrosheetRecord):
    def __init__(self, retrosheet_id=None, player_name=None, team=None, batting_position=None, fielding_position=None):
        RetrosheetRecord.__init__(self, "start")
        self.retrosheet_id = retrosheet_id
        self.player_name = player_name
        self.team = team
        self.batting_position = batting_position
        self.fielding_position = fielding_position

    def __str__(self):
        return 'start,{0},"{1}",{2},{3},{4}'.format(self.retrosheet_id, self.player_name, self.team,
                                                    self.batting_position, self.fielding_position)


class Play(RetrosheetRecord):
    def __init__(self, inning=None, inning_half=None, batter_id=None, balls=None, strikes=None, pitch_sequence=None,
                 play_string=None):
        RetrosheetRecord.__init__(self, "play")
        self.inning = int(inning)
        self.inningHalf = int(inning_half)
        self.batterId = batter_id
        self.balls = int(balls)
        self.strikes = int(strikes)
        self.pitchSequence = pitch_sequence
        self.playString = play_string

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
        p = re.compile('^([\w\(\)!]+)(/[A-Z1-9-\+]+)*(\..+)*$')
        m = p.match(self.playString)
        if m is not None:
            self.parse_description(m.group(1), play)
            if m.group(2) is not None:
                self.parse_modifiers(m.group(2), play)
            if m.group(3) is not None:
                self.parse_advances(m.group(3), play)
            elif play.groundedDoublePlay:  # default GDP advance
                play.runnerDestinations[1] = 0
        else:
            raise Exception("Cannot parse play string:", self.playString)

    @staticmethod
    def parse_description(group, play):
        play.fielders = group
        if group[0] in string.digits:
            play.battingResult = GameEvent.Play.PlayTypes.GENERIC_OUT
            play.fielders = group
            play.outsOnPlay = 1
        elif group[0] == 'S':
            play.battingResult = GameEvent.Play.PlayTypes.SINGLE
            play.batterDestination = 1
            play.fielders = group[1:]
        elif group[0] == 'D':
            play.battingResult = GameEvent.Play.PlayTypes.DOUBLE
            play.batterDestination = 2
            play.fielders = group[1:]
        elif group[0] == 'T':
            play.battingResult = GameEvent.Play.PlayTypes.TRIPLE
            play.batterDestination = 3
            play.fielders = group[1:]
        elif group == 'W':
            play.battingResult = GameEvent.Play.PlayTypes.WALK
            play.batterDestination = 1
        elif group == 'HR':
            play.battingResult = GameEvent.Play.PlayTypes.HOMERUN
            play.batterDestination = 4
            play.runsOnPlay += 1
        elif group == 'K':
            play.battingResult = GameEvent.Play.PlayTypes.STRIKEOUT
            play.outsOnPlay = 1
        elif group == 'NP':
            play.battingResult = GameEvent.Play.PlayTypes.NO_PLAY
        else:
            raise Exception("Cannot parse play description:", group)

        if "!" in group:
            play.exceptionalPlay = True

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
            elif modifier == 'GDP':
                play.outsOnPlay = 2
                play.groundedDoublePlay = True
            else:
                raise Exception("Cannot parse modifier:", modifier)

    @staticmethod
    def parse_advances(group, play):
        # remove the .
        group = group[1:]
        advances = group.split(';')
        for advance in advances:
            if advance[1] == '-':
                (runner, destination) = advance.split('-')
                if destination == 'H':
                    destination = 4
                    play.runsOnPlay += 1
                if runner == 'B':
                    play.batterDestination = int(destination)
                elif runner.isdigit():
                    play.runnerDestinations[int(runner)] = int(destination)
                else:
                    raise Exception("Cannot parse advance:", group)
            elif advance[1] == 'X':
                p = re.compile('([B123])X([123H])\((\d+)\)')
                m = p.match(advance)
                if m is not None:
                    play.fielders = m.group(3)
                    if m.group(1).isdigit():
                        play.runnerDestinations[int(m.group(1))] = 0
                        play.outsOnPlay += 1
                else:
                    raise Exception("Cannot parse advance:", group)
            else:
                raise Exception("Cannot parse advance:", group)


class Sub(RetrosheetRecord):
    def __init__(self, player_id=None, player_name=None, team=None, batting_order=None, position=None):
        RetrosheetRecord.__init__(self, "sub")
        self.playerId = player_id
        self.playerName = player_name
        self.team = int(team)
        self.battingOrder = int(batting_order)
        self.position = int(position)

    def __str__(self):
        return 'sub,{0},"{1}",{2},{3},{4}'.format(
            self.playerId, self.playerName, self.team, self.battingOrder, self.position
        )

    def to_event(self):
        play = GameEvent.Substitution()
        # TODO - should get the player from a global list
        play.player = Player(self.playerId)
        play.team = self.team
        play.offensiveLineupIndex = self.battingOrder
        play.defensiveLineupIndex = self.position
        return play


class Com(RetrosheetRecord):
    def __init__(self, comment=None):
        RetrosheetRecord.__init__(self, "com")
        self.comment = comment

    def __str__(self):
        return 'com,"{0}"'.format(self.comment)

    def to_event(self):
        play = GameEvent.Comment()
        play.comment = self.comment


class Data(RetrosheetRecord):
    def __init__(self, name=None, retrosheet_id=None, value=None):
        RetrosheetRecord.__init__(self, "data")
        self.name = name
        self.retrosheet_id = retrosheet_id
        self.value = value

    def __str__(self):
        return "data,{0},{1},{2}".format(self.name, self.retrosheet_id, self.value)
