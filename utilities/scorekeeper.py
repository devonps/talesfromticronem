from components import scorekeeper


class ScorekeeperUtilities:

    @staticmethod
    def set_current_area(gameworld, current_area_tag):
        scorekeeper_entity = ScorekeeperUtilities.get_scorekeeper_entity(gameworld=gameworld)
        scorekeeper_component = gameworld.component_for_entity(scorekeeper_entity, scorekeeper.AreasVisited)
        current_area = scorekeeper_component.current_area
        all_areas_list = scorekeeper_component.all_areas
        # one off check for start of game
        if len(all_areas_list) == 0:
            scorekeeper_component.current_area = current_area_tag
            scorekeeper_component.all_areas = current_area_tag
        else:
            scorekeeper_component.current_area = current_area_tag
            all_areas_list.append(current_area)
            scorekeeper_component.all_areas = all_areas_list


    @staticmethod
    def get_current_area(gameworld):
        scorekeeper_entity = ScorekeeperUtilities.get_scorekeeper_entity(gameworld=gameworld)
        scorekeeper_component = gameworld.component_for_entity(scorekeeper_entity, scorekeeper.AreasVisited)
        return scorekeeper_component.current_area

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
        scorekeeper_existing_meta_events_component = gameworld.component_for_entity(scorekeeper_entity, scorekeeper.MetaEvents)
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