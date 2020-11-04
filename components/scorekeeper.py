class ScoreKeeperFlag:
    def __init__(self, sc_flag):
        self.sc_flag = sc_flag


class MetaEvents:
    def __init__(self, map_of_events=None):
        if map_of_events is None:
            map_of_events = {}
        self.map_of_events = map_of_events


class AreasVisited:
    def __init__(self, current_area='', all_areas=None):
        self.current_area = current_area
        if all_areas is None:
            all_areas = []
        self.all_areas = all_areas
