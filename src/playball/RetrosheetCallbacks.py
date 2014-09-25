from playball import GameEvent
from playball.RetrosheetRecord import Play

__author__ = 'Sam'


class RetrosheetCallbacks:
    def __init__(self, game):
        self.game = game

    def record_event(self, pre_state, post_state, event):
        if isinstance(event, GameEvent.Play):
            play = Play()
            play.inning = pre_state.inning
            play.inningHalf = 1 if pre_state.inningBottom else 0
            play.batterId = event.batter.retrosheet_id
            play.balls = event.balls
            play.strikes = event.strikes
            play.pitchSequence = event.pitchSequence

            if event.playType == GameEvent.Play.PlayTypes.GENERIC_OUT:
                play.playString = ''.join(event.fielders)

            self.game.event_records.append(play)

        else:
            raise Exception("Unsupported event type")

    def record_game_end(self):
        pass