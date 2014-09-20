from collections import deque
import csv
import sys
from playball.RetrosheetRecord import RetrosheetRecord
from playball.RetrosheetGame import RetrosheetGame


class RetrosheetScorebook():
    def __init__(self, filename):
        self.games = deque()
        with open(filename, 'rb') as f:
            reader = csv.reader(f)
            game = None
            try:
                for row in reader:
                    record = RetrosheetRecord.parse_row(row)
                    if record.record_type == 'id':
                        game = RetrosheetGame(record.gameid)
                        self.games.append(game)
                    elif record.record_type == 'version':
                        game.version = record.version
                    elif record.record_type == 'info':
                        game.info[record.name] = record.value
                    elif record.record_type == 'start':
                        game.add_starter(record)
                    elif record.record_type == 'data':
                        game.add_data(record)
                    else:
                        game.add_event(record)
            except csv.Error as e:
                sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
