from collections import deque

from playball.GameEngine import GameEngine
from playball.RetrosheetRecord import RetrosheetRecord


__author__ = 'Sam'


class RetrosheetEngine(GameEngine):
    def __init__(self):
        self.records = deque()
        self.events = deque()

    def append_record(self, event):
        self.records.append(event)

    def next_event(self, state):
        if len(self.records) > 0:
            while True:
                record = self.records.popleft()
                if isinstance(record, RetrosheetRecord.Play):
                    return record.to_event()
