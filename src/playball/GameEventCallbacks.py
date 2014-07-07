__author__ = 'Sam'

from playball.GameEvent import Play


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

        print "Batter:", event.batter.full_name()
        print "Batting Result:", Play.PlayTypes.reverse_mapping[event.battingResult]

        if event.batterDestination >= 4:
            print " * %s scores." % (event.batter.full_name())
        elif event.batterDestination > 0:
            print " * %s goes to %s." % (event.batter.full_name(), event.batterDestination)
        for i in range(1, len(pre_state.bases)):
            if pre_state.bases[i] is not None and i != event.runnerDestinations[i]:
                if event.runnerDestinations[i] >= 4:
                    print " * %s scores." % (pre_state.bases[i].full_name())
                else:
                    print " * %s goes to %s." % (pre_state.bases[i].full_name(),
                                                 event.runnerDestinations[i])
        print ''



    @staticmethod
    def print_game_end(state):
        print "--------------    FINAL   --------------"
        print "Away: %s: %d" % (state.awayTeam.full_name(), state.awayRuns)
        print "Home: %s: %d" % (state.homeTeam.full_name(), state.homeRuns)