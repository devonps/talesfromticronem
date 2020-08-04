from bearlibterminal import terminal
from loguru import logger

from components import mobiles
from utilities.common import CommonUtils
from utilities.input_handlers import handle_game_keys
from utilities.jsonUtilities import read_json_file
from utilities.mobileHelp import MobileUtilities
from utilities import formulas, configUtilities


def initiate_dialog(gameworld, game_config):
    entity_to_talk_with = check_for_nearby_valid_mobiles_to_speak_with(gameworld=gameworld, game_config=game_config)

    if entity_to_talk_with > 0:
        name_details = MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=entity_to_talk_with)
        CommonUtils.fire_event('dialog-general', gameworld=gameworld,
                               dialog='Going to speak with...' + name_details[0])
        gameworld.add_component(entity_to_talk_with, mobiles.DialogFlags(welcome=False))

        dialog_chain = load_entity_dialog_chains(gameworld=gameworld, entity_id=entity_to_talk_with,
                                                 game_config=game_config)
        logger.info(dialog_chain)
        handle_chained_dialog(dialog_chain=dialog_chain, game_config=game_config)

    return entity_to_talk_with


def handle_chained_dialog(dialog_chain, game_config):
    while dialog_chain != '':
        # get dialog chain details
        chain_id = dialog_chain[0]
        intro_text = dialog_chain[1]
        responses = [dialog_chain[2], dialog_chain[3], dialog_chain[4]]
        response_text = 0
        response_option = 1
        response_tag = 2

        unicode_string_to_print = '[font=dungeon][color=SPELLINFO_FRAME_COLOUR]['
        ascii_prefix = 'ASCII_SINGLE_'

        top_left_corner_char = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                parameter=ascii_prefix + 'TOP_LEFT')

        bottom_left_corner_char = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                   parameter=ascii_prefix + 'BOTTOM_LEFT')

        top_right_corner_char = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                 parameter=ascii_prefix + 'TOP_RIGHT')

        bottom_right_corner_char = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                    parameter=ascii_prefix + 'BOTTOM_RIGHT')

        horizontal_char = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                           parameter=ascii_prefix + 'HORIZONTAL')
        vertical_char = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                         parameter=ascii_prefix + 'VERTICAL')

        left_t_junction_char = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                parameter=ascii_prefix + 'LEFT_T_JUNCTION')
        right_t_junction_char = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                 parameter=ascii_prefix + 'RIGHT_T_JUNCTION')

        dialog_frame_start_x = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                           section='gui', parameter='DIALOG_FRAME_START_X')
        dialog_frame_start_y = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                           section='gui', parameter='DIALOG_FRAME_START_Y')
        dialog_frame_width = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                           section='gui', parameter='DIALOG_FRAME_WIDTH')
        dialog_frame_height = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                           section='gui', parameter='DIALOG_FRAME_HEIGHT')

        logger.debug('------ BEGIN DIALOG CHAIN -----------')
        logger.info('Chain ID:{}', chain_id)
        logger.info('Intro text:{}', intro_text)
        logger.info('Response 1 text:{}', responses[0][response_text])
        logger.info('Response 1 option:{}', responses[0][response_option])
        logger.info('Response 1 tag:{}', responses[0][response_tag])

        # display dialog UI - starting top left, ending bottom right

        # clear dialog space
        terminal.clear_area(dialog_frame_start_x, dialog_frame_start_y, dialog_frame_width, dialog_frame_height)
        # render horizontals
        for z in range(dialog_frame_start_x, (dialog_frame_start_x + dialog_frame_width)):
            terminal.printf(x=z, y=(dialog_frame_start_y + dialog_frame_height),
                            s=unicode_string_to_print + horizontal_char + ']')
            terminal.printf(x=z, y=dialog_frame_start_y, s=unicode_string_to_print + horizontal_char + ']')

        # render verticals
        for z in range(dialog_frame_start_y, (dialog_frame_start_y + dialog_frame_height) - 1):
            terminal.printf(x=dialog_frame_start_x, y=z + 1, s=unicode_string_to_print + vertical_char + ']')
            terminal.printf(x=(dialog_frame_start_x + dialog_frame_width), y=z + 1,
                            s=unicode_string_to_print + vertical_char + ']')

        # top left
        terminal.printf(x=dialog_frame_start_x, y=dialog_frame_start_y,
                        s=unicode_string_to_print + top_left_corner_char + ']')
        # bottom left
        terminal.printf(x=dialog_frame_start_x, y=(dialog_frame_start_y + dialog_frame_height),
                        s=unicode_string_to_print + bottom_left_corner_char + ']')
        # top right
        terminal.printf(x=(dialog_frame_start_x + dialog_frame_width), y=dialog_frame_start_y,
                        s=unicode_string_to_print + top_right_corner_char + ']')
        # bottom right
        terminal.printf(x=(dialog_frame_start_x + dialog_frame_width),
                        y=(dialog_frame_start_y + dialog_frame_height),
                        s=unicode_string_to_print + bottom_right_corner_char + ']')

        # npc name

        # intro tet
        terminal.printf(x=dialog_frame_start_x + 2, y=dialog_frame_start_y + 2,  s=intro_text)

        # valid responses

        # blit the console
        terminal.refresh()
        # add individual UI elements (speaker, intro text, response choices)
        # wait for player to press a key
        valid_event = False
        while not valid_event:
            event_to_be_processed, event_action = handle_game_keys()
            if event_to_be_processed == 'keypress':
                if event_action == 'quit':
                    dialog_chain = ''
                    valid_event = True
        # if 'next dialog step'



def load_entity_dialog_chains(gameworld, entity_id, game_config, dialog_steps_id=0, chain_id=0):
    dialog_chains_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                    parameter='DIALOGFILE')
    name_details = MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=entity_id)
    npc_first_name = name_details[0]
    dialog_chain = []
    intro_text = []
    response_text = []

    dialog_file = read_json_file(dialog_chains_file)

    top_level_dialog_chain = dialog_file['dialogue_chains'][chain_id]
    dialog_chain.append(top_level_dialog_chain['chain_name'])

    if top_level_dialog_chain['npc_id'] == npc_first_name:
        dialog_steps = top_level_dialog_chain['dialogue_steps'][dialog_steps_id]
        intro_text.append(dialog_steps['intro_text'])
        response_choices = dialog_steps['choices']
        resp_length = dialog_steps['choice_count']
        for n in range(resp_length):
            response = response_choices[n]
            if 'response_tag' in response:
                response_pair = (response['response_text'], response['response_option'], response['response_tag'])
            else:
                response_pair = (response['response_text'], response['response_option'])
            response_text.append(response_pair)

    merged_list = dialog_chain + intro_text + response_text
    return merged_list


def check_for_nearby_valid_mobiles_to_speak_with(gameworld, game_config):
    player_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)

    # check map surrounding player_entity 1x1 square deep
    visible_entities_list = MobileUtilities.get_visible_entities(gameworld=gameworld, target_entity=player_entity)
    target_entity = get_entity_id_to_talk_to(gameworld=gameworld, player_entity=player_entity,
                                             entities_list=visible_entities_list, game_config=game_config)
    if target_entity == 0:
        CommonUtils.fire_event('dialog-general', gameworld=gameworld,
                               dialog='There is no one near enough to speak with.')
    return target_entity


def get_entity_id_to_talk_to(gameworld, player_entity, entities_list, game_config):
    # this will return a single NPC entity id either because it's the only one visible and in range for chat
    # OR the player selects from a given list
    target_entity = 0
    valid_targets, entity_count = get_list_of_valid_targets(gameworld=gameworld, player_entity=player_entity,
                                                            entities_list=entities_list)
    if entity_count > 0:
        if entity_count == 1:
            target_entity = valid_targets[0]
        else:
            # display popup
            target_letters = CommonUtils.helper_print_valid_targets(gameworld=gameworld, valid_targets=valid_targets,
                                                                    game_config=game_config)
            # blit the terminal
            terminal.refresh()
            # get player input
            # wait for user key press
            player_not_pressed_a_key = True
            while player_not_pressed_a_key:
                event_to_be_processed, event_action = handle_game_keys()
                if event_action == 'quit':
                    player_not_pressed_a_key = False
                if event_action is not None and event_action in target_letters:
                    target = target_letters.index(event_action)
                    target_entity = valid_targets[target]
                    player_not_pressed_a_key = False

    return target_entity


def get_list_of_valid_targets(gameworld, player_entity, entities_list):
    valid_targets = []
    entity_count = 0
    for loop_index in range(len(entities_list)):
        distance_to_target_npc = int(
            formulas.calculate_distance_to_target(gameworld=gameworld, from_entity=player_entity,
                                                  to_entity=entities_list[loop_index]))
        if distance_to_target_npc == 1:
            valid_targets.append(entities_list[loop_index])
            entity_count += 1

    return valid_targets, entity_count
