__author__ = 'Sam'

from playball.GameEvent import Play, Substitution, Comment


class GameEventCallbacks:
    def __init__(self):
        pass

    @staticmethod
    def print_event(pre_state, post_state, event):
        tb = "Bottom" if pre_state.inningBottom else "Top"
        print "-------------- %6s  %2d --------------" % (tb, pre_state.inning)
        print "Away: %s: %d" % (pre_state.awayTeam.full_name(), pre_state.awayRuns)
        print "Home: %s: %d" % (pre_state.homeTeam.full_name(), pre_state.homeRuns)
        print "Outs:", pre_state.outs
        print "-" * 40

        if isinstance(event, Play):
            GameEventCallbacks.print_play(pre_state, post_state, event)
        elif isinstance(event, Substitution):
            GameEventCallbacks.print_sub(event)
        elif isinstance(event, Comment):
            GameEventCallbacks.print_com(event)
        else:
            raise Exception("Unsupported event type:", event)

        print ''

    @staticmethod
    def print_play(pre_state, post_state, event):
        print "Batter:", event.batter.retrosheet_id
        print "Batting Result:", Play.PlayTypes.reverse_mapping[event.battingResult]

        print pre_state.bases
        print event.runnerDestinations
        print post_state.bases
        if event.batterDestination >= 4:
            print " * %s scores." % event.batter.retrosheet_id
        elif event.batterDestination > 0:
            print " * %s goes to %s." % (event.batter.retrosheet_id, event.batterDestination)
        for i in range(1, len(event.runnerDestinations)):
            if pre_state.bases[i] is not None and event.runnerDestinations[i] is not None:
                if event.runnerDestinations[i] >= 4:
                    print " * %s scores." % pre_state.bases[i].retrosheet_id
                else:
                    print " * %s goes to %s." % (pre_state.bases[i].retrosheet_id,
                                                 event.runnerDestinations[i])

    @staticmethod
    def print_sub(event):
        print "Substitution"
        print "Player:", event.player.retrosheet_id
        print "Team:", event.team
        print "Batting Order:", event.offensiveLineupIndex
        print "Fielding Position:", event.defensiveLineupIndex

    @staticmethod
    def print_com(event):
        print "Comment:", event.comment

    @staticmethod
    def print_game_end(state):
        print "--------------    FINAL   --------------"
        print "Away: %s: %d" % (state.awayTeam.full_name(), state.awayRuns)
        print "Home: %s: %d" % (state.homeTeam.full_name(), state.homeRuns)