
class NumberOfTurns:
    def __init__(self, count=0):
        self.count = count


class ScoreKeeperFlag:
    def __init__(self, sc_flag):
        self.sc_flag = sc_flag


class MetaEvents:
    def __init__(self, map_of_events=None):
        if map_of_events is None:
            map_of_events = {}
        self.map_of_events = map_of_events
