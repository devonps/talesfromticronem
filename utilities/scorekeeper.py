from components import scorekeeper


class ScorekeeperUtilities:

    # Get scorekeeper entity id
    @staticmethod
    def get_scorekeeper_entity(gameworld):
        scorekeeper_entity = 0
        for ent, scf in gameworld.get_component(scorekeeper.ScoreKeeperFlag):
            if scf.sc_flag:
                scorekeeper_entity = ent

        return scorekeeper_entity

    # Register meta event to scorekeeper
    @staticmethod
    def register_scorekeeper_meta_event(gameworld, event_name, event_starting_value=0):
        scorekeeper_entity = ScorekeeperUtilities.get_scorekeeper_entity(gameworld=gameworld)

        scorekeeper_existing_meta_events_component = gameworld.component_for_entity(scorekeeper_entity, scorekeeper.MetaEvents)
        current_meta_events = scorekeeper_existing_meta_events_component.map_of_events
        current_meta_events.update({event_name: event_starting_value})

    @staticmethod
    def get_list_of_meta_events(gameworld):
        scorekeeper_entity = ScorekeeperUtilities.get_scorekeeper_entity(gameworld=gameworld)

        scorekeeper_existing_meta_events = gameworld.component_for_entity(scorekeeper_entity, scorekeeper.MetaEvents)

        meta_events = scorekeeper_existing_meta_events.map_of_events

        return meta_events

    @staticmethod
    def get_meta_event_value(gameworld, event_name):
        scorekeeper_entity = ScorekeeperUtilities.get_scorekeeper_entity(gameworld=gameworld)

        scorekeeper_existing_meta_events_component = gameworld.component_for_entity(scorekeeper_entity, scorekeeper.MetaEvents)

        all_meta_events = scorekeeper_existing_meta_events_component.map_of_events

        meta_event_value = all_meta_events.get(event_name)

        return meta_event_value

    @staticmethod
    def add_one_to_meta_event_value(gameworld, event_name):
        scorekeeper_entity = ScorekeeperUtilities.get_scorekeeper_entity(gameworld=gameworld)

        scorekeeper_existing_meta_events_component = gameworld.component_for_entity(scorekeeper_entity, scorekeeper.MetaEvents)

        all_meta_events = scorekeeper_existing_meta_events_component.map_of_events

        meta_event_value = all_meta_events.get(event_name)

        meta_event_value += 1

        all_meta_events.update({event_name: meta_event_value})

        gameworld.component_for_entity(scorekeeper_entity, scorekeeper.MetaEvents).map_of_events = all_meta_events

