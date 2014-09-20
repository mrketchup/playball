__author__ = 'sam'


class RetrosheetGame():
    def __init__(self, gameid):
        self.gameid = gameid
        self.info = {}
        self.start_visiting_offense = {}
        self.start_visiting_defense = {}
        self.start_home_offense = {}
        self.start_home_defense = {}
        self.data = []
        self.events = []

    def add_starter(self, start_record):
        player = (start_record.retrosheet_id, start_record.player_name)

        if start_record.team == 0:
            self.start_visiting_offense[start_record.batting_position] = player
            self.start_visiting_defense[start_record.fielding_position] = player
        else:
            self.start_home_offense[start_record.batting_position] = player
            self.start_home_defense[start_record.fielding_position] = player

    def add_data(self, data_record):
        data = (data_record.name, data_record.retrosheet_id, data_record.value)
        self.data.append(data)

    def add_event(self, event_record):
        self.events.append(event_record)

    def __str__(self):
        return "{0}".format(self.gameid)
