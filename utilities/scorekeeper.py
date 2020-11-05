from loguru import logger

from components import scorekeeper
from utilities import externalfileutilities
import datetime


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

    # scorecard methods
    @staticmethod
    def create_scorecard_file():
        current_date_time = datetime.datetime.now()
        formatted_date_time = current_date_time.strftime("%d%m%y%H%M%S")
        formatted_time_as_string = str(formatted_date_time)
        scorecard_filename = formatted_time_as_string + '_scorecard.txt'

        externalfileutilities.Externalfiles.create_new_scorecard_file(filename=scorecard_filename)

        return scorecard_filename

    @staticmethod
    def add_last_run_information(filename, game_version):
        start_date_time_of_run = datetime.datetime.now()
        start_date_time_of_run_formatted = str(start_date_time_of_run.strftime("%x at %X"))
        end_date_time_of_run = datetime.datetime.now()
        end_date_time_of_run_formatted = str(end_date_time_of_run.strftime("%x at %X"))
        blank_line_string = '\n'
        game_title_string = 'Tales From Ticronem Scorecard'
        game_version_string = 'Game Version is ' + game_version
        run_start_time_string = 'This run started on ' + start_date_time_of_run_formatted + ' and ended on ' + end_date_time_of_run_formatted
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=game_title_string)
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=blank_line_string)
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=game_version_string)
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=blank_line_string)
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=run_start_time_string)
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=blank_line_string)

    @staticmethod
    def add_spells_cast_information(gameworld, filename):
        all_areas_visited = ScorekeeperUtilities.get_all_areas_visited(gameworld=gameworld)
        events_split_by_area = ScorekeeperUtilities.unpack_meta_events_to_list(gameworld=gameworld)
        blank_line_string = '\n'
        total_count_of_spells_cast = 0
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=blank_line_string)

        for area in all_areas_visited:
            area_string = "Areas ".ljust(30) + area
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=area_string)
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=blank_line_string)

        for area in all_areas_visited:
            area_events = events_split_by_area[area]
            for key, value in area_events.items():
                if key.endswith('_cast'):
                    raw_spell_name = key[:-5]
                    spell_cast_count = value
                    spell_name = raw_spell_name.replace("_", " ")
                    logger.info('spell name is {} and it has been cast {} times', spell_name, spell_cast_count)
                    spell_cast_count_string = str(spell_cast_count)
                    total_count_of_spells_cast += spell_cast_count
                    spell_cast_string = spell_name.ljust(30) + spell_cast_count_string.zfill(5 - len(spell_cast_count_string))
                    externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=spell_cast_string)
                    externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=blank_line_string)
            spells_cast_count_string = str(total_count_of_spells_cast)
            total_spells_cast_string = 'Total Spell Cast:'.ljust(29) + spells_cast_count_string.zfill(6 - len(spells_cast_count_string))
            externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=blank_line_string)
            externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=total_spells_cast_string)
    # areas of the game
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

    # Get scorekeeper entity methods
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

    # meta event value transformations
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
