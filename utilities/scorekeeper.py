from components import scorekeeper


class ScorekeeperUtilities:

    @staticmethod
    def unpack_meta_events_to_list(gameworld):
        areas_visited = ScorekeeperUtilities.get_all_areas_visited(gameworld=gameworld)
        all_meta_events = ScorekeeperUtilities.get_list_of_meta_events(gameworld=gameworld)

        meta_events_per_area_list = {}
        for area in areas_visited:
            these_events = {}
            for meta_key, meta_value in all_meta_events.items():
                if meta_key.startswith(area):
                    new_event = ScorekeeperUtilities.strip_area_tag_from_meta_event(meta_event=meta_key)
                    these_events.update({new_event: meta_value})
            meta_events_per_area_list.update({area: these_events})
            meta_events_per_area_list.update({'boo': {'spell 1': 500}})
        return meta_events_per_area_list

    @staticmethod
    def strip_area_tag_from_meta_event(meta_event):
        new_string = meta_event[4:]
        return new_string


    @staticmethod
    def set_current_area(gameworld, current_area_tag):
        scorekeeper_entity = ScorekeeperUtilities.get_scorekeeper_entity(gameworld=gameworld)
        scorekeeper_component = gameworld.component_for_entity(scorekeeper_entity, scorekeeper.AreasVisited)
        current_area = scorekeeper_component.current_area
        all_areas_list = scorekeeper_component.all_areas
        # one off check for start of game
        if len(all_areas_list) == 0:
            all_areas_list.append(current_area_tag)
        else:
            all_areas_list.append(current_area)

        scorekeeper_component.current_area = current_area_tag
        scorekeeper_component.all_areas = all_areas_list

    @staticmethod
    def get_current_area(gameworld):
        scorekeeper_entity = ScorekeeperUtilities.get_scorekeeper_entity(gameworld=gameworld)
        scorekeeper_component = gameworld.component_for_entity(scorekeeper_entity, scorekeeper.AreasVisited)
        return scorekeeper_component.current_area

    @staticmethod
    def get_all_areas_visited(gameworld):
        scorekeeper_entity = ScorekeeperUtilities.get_scorekeeper_entity(gameworld=gameworld)
        scorekeeper_component = gameworld.component_for_entity(scorekeeper_entity, scorekeeper.AreasVisited)
        return scorekeeper_component.all_areas

    # Get scorekeeper entity id
    @staticmethod
    def get_scorekeeper_entity(gameworld):
        scorekeeper_entity = 0
        for ent, scf in gameworld.get_component(scorekeeper.ScoreKeeperFlag):
            if scf.sc_flag:
                scorekeeper_entity = ent
        return scorekeeper_entity

    @staticmethod
    def update_scorekeeper_all_meta_events(gameworld, meta_events):
        scorekeeper_entity = ScorekeeperUtilities.get_scorekeeper_entity(gameworld=gameworld)
        gameworld.component_for_entity(scorekeeper_entity, scorekeeper.MetaEvents).map_of_events = meta_events

    @staticmethod
    def get_scorekeeper_component(gameworld):
        scorekeeper_entity = ScorekeeperUtilities.get_scorekeeper_entity(gameworld=gameworld)
        scorekeeper_existing_meta_events_component = gameworld.component_for_entity(scorekeeper_entity,
                                                                                    scorekeeper.MetaEvents)
        return scorekeeper_existing_meta_events_component

    # Register meta event to scorekeeper
    @staticmethod
    def register_scorekeeper_meta_event(gameworld, event_name, event_starting_value=0):
        current_meta_events = ScorekeeperUtilities.get_list_of_meta_events(gameworld=gameworld)
        current_meta_events.update({event_name: event_starting_value})

    @staticmethod
    def get_list_of_meta_events(gameworld):
        scorekeeper_existing_meta_events_component = ScorekeeperUtilities.get_scorekeeper_component(gameworld=gameworld)
        meta_events = scorekeeper_existing_meta_events_component.map_of_events
        return meta_events

    @staticmethod
    def does_this_meta_event_exist(gameworld, incoming_meta_event_name):
        meta_events = ScorekeeperUtilities.get_list_of_meta_events(gameworld=gameworld)

        meta_event_found = False
        for meta_event_name in meta_events.keys():
            if incoming_meta_event_name == meta_event_name:
                meta_event_found = True
        return meta_event_found

    @staticmethod
    def get_meta_event_value(gameworld, event_name):
        all_meta_events = ScorekeeperUtilities.get_list_of_meta_events(gameworld=gameworld)
        meta_event_value = all_meta_events.get(event_name)
        return meta_event_value

    @staticmethod
    def add_one_to_meta_event_value(gameworld, event_name):
        all_meta_events = ScorekeeperUtilities.get_list_of_meta_events(gameworld=gameworld)
        meta_event_value = all_meta_events.get(event_name)
        meta_event_value += 1
        all_meta_events.update({event_name: meta_event_value})
        ScorekeeperUtilities.update_scorekeeper_all_meta_events(gameworld=gameworld, meta_events=all_meta_events)

    @staticmethod
    def subtract_one_from_meta_event_value(gameworld, event_name):
        all_meta_events = ScorekeeperUtilities.get_list_of_meta_events(gameworld=gameworld)
        meta_event_value = all_meta_events.get(event_name)
        meta_event_value -= 1
        all_meta_events.update({event_name: meta_event_value})
        ScorekeeperUtilities.update_scorekeeper_all_meta_events(gameworld=gameworld, meta_events=all_meta_events)
