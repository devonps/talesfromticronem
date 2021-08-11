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

        return meta_events_per_area_list

    @staticmethod
    def strip_area_tag_from_meta_event(meta_event):
        new_string = meta_event[4:]
        return new_string

    # scorecard methods
    @staticmethod
    def report_create_scorecard_file():
        current_date_time = datetime.datetime.now()
        formatted_date_time = current_date_time.strftime("%d%m%y%H%M%S")
        formatted_time_as_string = str(formatted_date_time)
        scorecard_filename = formatted_time_as_string + '_scorecard.txt'

        externalfileutilities.Externalfiles.create_new_scorecard_file(filename=scorecard_filename)

        return scorecard_filename

    @staticmethod
    def report_add_last_run_information(filename, game_version):
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
    def report_add_player_info(filename, player_class):
        blank_line_string = '\n'
        string_to_print = 'You played this game as a ' + player_class
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=blank_line_string)
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=string_to_print)
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=blank_line_string)

    @staticmethod
    def report_add_game_turns_info(filename, gameworld):
        game_turns = ScorekeeperUtilities.get_meta_event_value(gameworld=gameworld, event_name='game_turn')
        blank_line_string = '\n'
        string_to_print = 'You took ' + str(game_turns) + ' turns, see below for highlights.'
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=string_to_print)
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=blank_line_string)

    @staticmethod
    def build_scorecard(gameworld, game_version, player_class, dump_scores):
        all_areas_visited = ScorekeeperUtilities.get_all_areas_visited(gameworld=gameworld)

        if dump_scores == 1:
            externalfileutilities.Externalfiles.create_new_directory(directory_name='scores')
            score_card_file = ScorekeeperUtilities.report_create_scorecard_file()

            ScorekeeperUtilities.report_add_last_run_information(filename=score_card_file, game_version=game_version)
            ScorekeeperUtilities.report_add_player_info(filename=score_card_file, player_class=player_class)
            ScorekeeperUtilities.report_add_game_turns_info(filename=score_card_file, gameworld=gameworld)

            for area in all_areas_visited:
                # print area information - might be just their name
                ScorekeeperUtilities.report_add_game_area_info(filename=score_card_file, area_name=area)
                # print out spell cast information
                ScorekeeperUtilities.report_add_spells_cast_information(gameworld=gameworld, filename=score_card_file,
                                                                        visited_area=area)
                # print out different damage types
                ScorekeeperUtilities.report_add_types_of_damage_per_area(gameworld=gameworld, filename=score_card_file,
                                                                         visited_area=area)
                # print out enemy kills
                ScorekeeperUtilities.report_add_enemy_kills_per_area(gameworld=gameworld, filename=score_card_file,
                                                                     visited_area=area)

    @staticmethod
    def report_add_game_area_info(filename, area_name):
        blank_line_string = '\n'
        string_to_print = area_name
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=blank_line_string)
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=string_to_print)
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=blank_line_string)
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=blank_line_string)

    @staticmethod
    def report_add_spells_cast_information(gameworld, filename, visited_area):
        events_split_to_list_by_area = ScorekeeperUtilities.unpack_meta_events_to_list(gameworld=gameworld)
        event_list = events_split_to_list_by_area[visited_area]
        blank_line_string = '\n'
        total_count_of_spells_cast = 0
        string_to_print = ' '.ljust(5) + 'Spells Cast'.ljust(34) + 'Count'
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=string_to_print)
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=blank_line_string)

        # gather spells cast per area within a list
        for key, value in event_list.items():
            if key.endswith('_cast'):
                raw_spell_name = key[:-5]
                spell_cast_count = value
                spell_name = raw_spell_name.replace("_", " ")
                spell_cast_count_string = str(spell_cast_count)
                total_count_of_spells_cast += spell_cast_count
                spell_cast_string = ' '.ljust(10) + spell_name.ljust(30) + spell_cast_count_string.zfill(4)
                externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=spell_cast_string)
                externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=blank_line_string)
        # total spells for this area
        spells_cast_count_string = str(total_count_of_spells_cast)
        total_spells_cast_string = ' '.ljust(10) + 'Total Spells Cast:'.ljust(29) + spells_cast_count_string.zfill(5)
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=total_spells_cast_string)

    @staticmethod
    def has_event_already_been_added(gameworld, event_name):
        event_dict = ScorekeeperUtilities.get_list_of_meta_events(gameworld=gameworld)
        event_found = False
        if event_name in event_dict:
            event_found = True
        return event_found

    @staticmethod
    def report_add_types_of_damage_per_area(gameworld, filename, visited_area):
        events_split_to_list_by_area = ScorekeeperUtilities.unpack_meta_events_to_list(gameworld=gameworld)
        event_list = events_split_to_list_by_area[visited_area]
        blank_line_string = '\n'
        total_damage_caused = 0
        string_to_print = ' '.ljust(5) + 'Types of Damage Inflicted'.ljust(34) + 'Total'
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=blank_line_string)
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=blank_line_string)
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=string_to_print)
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=blank_line_string)
        for key, value in event_list.items():
            if key.endswith('_damage'):
                total_damage_caused += int(value)
                raw_damage_name = key[:-7]
                damage_total_count = int(value)
                damage_total_count_string = str(damage_total_count)
                final_damage_string = damage_total_count_string.zfill(4)
                damage_name = raw_damage_name.replace("_", " ")
                damage_cast_string = ' '.ljust(10) + damage_name.ljust(30) + final_damage_string
                externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=damage_cast_string)
                externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=blank_line_string)
        # total damage for this area
        total_damage_string = str(total_damage_caused)
        total_damage_caused_string = ' '.ljust(10) + 'Total Damage Caused:'.ljust(29) + total_damage_string.zfill(5)
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=total_damage_caused_string)

    @staticmethod
    def report_add_enemy_kills_per_area(gameworld, filename, visited_area):
        events_split_to_list_by_area = ScorekeeperUtilities.unpack_meta_events_to_list(gameworld=gameworld)
        event_list = events_split_to_list_by_area[visited_area]
        blank_line_string = '\n'
        total_enemies_killed = 0
        string_to_print = ' '.ljust(5) + 'Enemy Types Killed'.ljust(34) + 'Total'
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=blank_line_string)
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=blank_line_string)
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=string_to_print)
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=blank_line_string)
        for key, value in event_list.items():
            if key.endswith('_kill'):
                total_enemies_killed += value
                raw_enemy_type_name = key[:-5]
                enemy_type_total_count = int(value)
                enemy_total_count_string = str(enemy_type_total_count)
                final_enemy_string = enemy_total_count_string.zfill(4)
                enemy_type_name = raw_enemy_type_name.replace("_", " ")
                enemy_type_string = ' '.ljust(10) + enemy_type_name.ljust(30) + final_enemy_string
                externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=enemy_type_string)
                externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=blank_line_string)
        # total enemies killed for this area
        total_enemy_string = str(total_enemies_killed)
        total_enemy_type_string = ' '.ljust(10) + 'Total Enemies Killed:'.ljust(29) + total_enemy_string.zfill(5)
        externalfileutilities.Externalfiles.write_to_existing_file(filename=filename, value=total_enemy_type_string)

    # areas of the game
    @staticmethod
    def set_current_area(gameworld, current_area_tag):
        scorekeeper_entity = ScorekeeperUtilities.get_scorekeeper_entity(gameworld=gameworld)
        scorekeeper_component = gameworld.component_for_entity(scorekeeper_entity, scorekeeper.AreasVisited)
        all_areas_list = scorekeeper_component.all_areas
        all_areas_list.append(current_area_tag)

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
        # hack for testing purposes
        meta_events.update({'dg1_necrotic_grasp_cast': 0})
        meta_events.update({'dg1_mark_of_blood_cast': 0})
        meta_events.update({'dg2_life_blood_cast': 0})
        meta_events.update({'dg2_putrid_mark_cast': 0})
        meta_events.update({"dg3_reaper's_mark_cast": 0})
        meta_events.update({'dg3_your_soul_is_mine_cast': 0})
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
    def increase_meta_event_by_value(gameworld, event_name, value):
        all_meta_events = ScorekeeperUtilities.get_list_of_meta_events(gameworld=gameworld)
        meta_event_value = all_meta_events.get(event_name)
        meta_event_value += value
        all_meta_events.update({event_name: meta_event_value})
        ScorekeeperUtilities.update_scorekeeper_all_meta_events(gameworld=gameworld, meta_events=all_meta_events)

    @staticmethod
    def decrease_meta_event_by_value(gameworld, event_name, value):
        all_meta_events = ScorekeeperUtilities.get_list_of_meta_events(gameworld=gameworld)
        meta_event_value = all_meta_events.get(event_name)
        meta_event_value -= value
        if meta_event_value < 0:
            meta_event_value = 0
        all_meta_events.update({event_name: meta_event_value})
        ScorekeeperUtilities.update_scorekeeper_all_meta_events(gameworld=gameworld, meta_events=all_meta_events)

    @staticmethod
    def register_damage_types_for_current_area(current_area_tag, gameworld):
        ScorekeeperUtilities.register_scorekeeper_meta_event(gameworld=gameworld,
                                                             event_name=current_area_tag + '_bleeding_damage',
                                                             event_starting_value=0)
        ScorekeeperUtilities.register_scorekeeper_meta_event(gameworld=gameworld,
                                                             event_name=current_area_tag + '_burning_damage',
                                                             event_starting_value=0)

        ScorekeeperUtilities.register_scorekeeper_meta_event(gameworld=gameworld,
                                                             event_name=current_area_tag + '_confusion_damage',
                                                             event_starting_value=0)

        ScorekeeperUtilities.register_scorekeeper_meta_event(gameworld=gameworld,
                                                             event_name=current_area_tag + '_poison_damage',
                                                             event_starting_value=0)

        ScorekeeperUtilities.register_scorekeeper_meta_event(gameworld=gameworld,
                                                             event_name=current_area_tag + '_torment_damage',
                                                             event_starting_value=0)

        ScorekeeperUtilities.register_scorekeeper_meta_event(gameworld=gameworld,
                                                             event_name=current_area_tag + '_direct_damage',
                                                             event_starting_value=0)
