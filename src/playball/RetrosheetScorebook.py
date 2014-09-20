import csv
import sys
from playball.RetrosheetRecord import RetrosheetRecord
from playball.RetrosheetGame import RetrosheetGame


class RetrosheetScorebook():
    def __init__(self,):
        self.games = []

    def read(self, filename):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            game = None
            try:
                for row in reader:
                    record = RetrosheetRecord.parse_row(row)
                    if record.record_type == 'id':
                        game = RetrosheetGame()
                        game.id_record = record
                        self.games.append(game)
                    elif record.record_type == 'version':
                        game.version_record = record
                    elif record.record_type == 'info':
                        game.info_records.append(record)
                    elif record.record_type == 'start':
                        game.start_records.append(record)
                    elif record.record_type == 'data':
                        game.data_records.append(record)
                    else:
                        game.event_records.append(record)
            except csv.Error as e:
                sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
            f.close()

    def write(self, filename):
        with open(filename, 'w') as f:
            for game in self.games:
                f.write(str(game.id_record) + '\n')
                f.write(str(game.version_record) + '\n')
                for record in game.info_records:
                    f.write(str(record) + '\n')
                for record in game.start_records:
                    f.write(str(record) + '\n')
                for record in game.event_records:
                    f.write(str(record) + '\n')
                for record in game.data_records:
                    f.write(str(record) + '\n')
            f.close()
