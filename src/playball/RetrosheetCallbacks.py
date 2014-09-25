from playball import GameEvent
from playball.GameEvent import Enum
from playball.RetrosheetRecord import Play, Sub

__author__ = 'Sam'


class RetrosheetCallbacks:
    def __init__(self, game):
        self.game = game

    def record_event(self, pre_state, post_state, event):
        if isinstance(event, GameEvent.Play):
            retrosheet_event = Play()
            retrosheet_event.inning = pre_state.inning
            retrosheet_event.inningHalf = 1 if pre_state.inningBottom else 0
            retrosheet_event.batterId = event.batter.retrosheet_id
            retrosheet_event.balls = event.balls
            retrosheet_event.strikes = event.strikes
            retrosheet_event.pitchSequence = event.pitchSequence

            if event.playType == GameEvent.Play.PlayTypes.GENERIC_OUT:
                retrosheet_event.playString = ''.join(event.fielders)
            elif event.playType == GameEvent.Play.PlayTypes.STRIKEOUT:
                retrosheet_event.playString = 'K'
            elif event.playType == GameEvent.Play.PlayTypes.WALK:
                retrosheet_event.playString = 'W'
            elif event.playType == GameEvent.Play.PlayTypes.SINGLE:
                retrosheet_event.playString = 'S'
            elif event.playType == GameEvent.Play.PlayTypes.DOUBLE:
                retrosheet_event.playString = 'D'
            elif event.playType == GameEvent.Play.PlayTypes.TRIPLE:
                retrosheet_event.playString = 'T'
            elif event.playType == GameEvent.Play.PlayTypes.HOMERUN:
                retrosheet_event.playString = 'HR'
            elif event.playType == GameEvent.Play.PlayTypes.NO_PLAY:
                retrosheet_event.playString = 'NP'
            else:
                raise Exception("Unsupported play type " + str(event.playType))

        elif isinstance(event, GameEvent.Substitution):
            retrosheet_event = Sub()
            retrosheet_event.playerId = event.player.retrosheet_id
            retrosheet_event.playerName = event.player.full_name()
            retrosheet_event.team = event.team
            retrosheet_event.battingOrder = event.offensiveLineupIndex
            retrosheet_event.position = event.defensiveLineupIndex

        else:
            raise Exception("Unsupported event type", type(event))

        self.game.event_records.append(retrosheet_event)

    def record_game_end(self, state):
        pass