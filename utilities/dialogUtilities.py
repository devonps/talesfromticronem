from bearlibterminal import terminal
from loguru import logger
from components import mobiles
from newGame.CreateSpells import AsEntities
from static.data import constants
from ui import shopkeeper_armour, shopkeeper_jewellery
from utilities import common, display, input_handlers, jsonUtilities, mobileHelp, formulas, configUtilities
from utilities.mobileHelp import MobileUtilities
from utilities.spellHelp import SpellUtilities


def initiate_dialog(gameworld, game_config):
    entity_to_talk_with = check_for_nearby_valid_mobiles_to_speak_with(gameworld=gameworld, game_config=game_config)

    if entity_to_talk_with > 0:
        name_details = mobileHelp.MobileUtilities.get_mobile_name_details(gameworld=gameworld,
                                                                          entity=entity_to_talk_with)
        common.CommonUtils.fire_event('dialog-general', gameworld=gameworld,
                                      dialog='Going to speak with...' + name_details[0])

        am_i_a_shopkeeper = mobileHelp.MobileUtilities.is_mobile_a_shopkeeper(gameworld=gameworld,
                                                                              target_entity=entity_to_talk_with)
        if am_i_a_shopkeeper:
            what_type_of_shopkeeper = mobileHelp.MobileUtilities.get_type_of_shopkeeper(gameworld=gameworld,
                                                                                        target_entity=entity_to_talk_with)
            open_the_shop(gameworld=gameworld, type_of_shopkeeper=what_type_of_shopkeeper,
                          shopkeeper_id=entity_to_talk_with)
        am_i_a_tutor = mobileHelp.MobileUtilities.is_mobile_a_tutor(gameworld=gameworld,
                                                                    target_entity=entity_to_talk_with)
        if am_i_a_tutor:
            what_type_of_tutor = mobileHelp.MobileUtilities.get_type_of_tutor(gameworld=gameworld,
                                                                              target_entity=entity_to_talk_with)
            open_the_shop(gameworld=gameworld, type_of_shopkeeper=what_type_of_tutor, shopkeeper_id=entity_to_talk_with)
        if not am_i_a_shopkeeper and not am_i_a_tutor:
            mobileHelp.MobileUtilities.set_dialog_welcome_flag_to_false(gameworld=gameworld,
                                                                        target_entity=entity_to_talk_with)
            spoken_to_before = mobileHelp.MobileUtilities.get_spoken_to_before_flag(gameworld=gameworld,
                                                                                    target_entity=entity_to_talk_with)

            speak = mobileHelp.MobileUtilities.get_spoken_to_before_flag(gameworld=gameworld,
                                                                         target_entity=entity_to_talk_with)
            logger.debug('Speaking with{}', entity_to_talk_with)
            logger.debug('spoken to flag is {}', speak)

            if spoken_to_before:
                chain_id = 1
            else:
                chain_id = 0

            dialog_chain = load_entity_dialog_chains(gameworld=gameworld, entity_id=entity_to_talk_with,
                                                     chain_id=chain_id)
            logger.info(dialog_chain)
            handle_chained_dialog(dialog_chain=dialog_chain, game_config=game_config, speaker_name=name_details[0],
                                  gameworld=gameworld, speaker_id=entity_to_talk_with)


def open_the_shop(type_of_shopkeeper, gameworld, shopkeeper_id):
    if type_of_shopkeeper == 'armour':
        shopkeeper_armour.shopkeeper_armour(gameworld=gameworld, shopkeeper_id=shopkeeper_id)

    if type_of_shopkeeper == 'jewellery':
        shopkeeper_jewellery.shopkeeper_jewellery(gameworld=gameworld, shopkeeper_id=shopkeeper_id)


def handle_chained_dialog(dialog_chain, game_config, speaker_name, gameworld, speaker_id):
    player_entity = mobileHelp.MobileUtilities.get_player_entity(gameworld=gameworld)
    player_names = mobileHelp.MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=player_entity)
    player_first_name = player_names[0]
    response_text = 0
    response_option = 1

    dialog_frame_start_x = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                       section='gui', parameter='DIALOG_FRAME_START_X')
    dialog_frame_start_y = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                       section='gui', parameter='DIALOG_FRAME_START_Y')

    mobileHelp.MobileUtilities.clear_talk_to_me_flag(gameworld=gameworld, target_entity=speaker_id)
    mobileHelp.MobileUtilities.set_spoken_to_before_flag_to_true(gameworld=gameworld, target_entity=speaker_id)

    selected_response_option = 0
    while dialog_chain != '':
        # get dialog chain details
        this_dialog_chain = process_rules_tag(current_dialog_chain=dialog_chain, npc_name=speaker_name)
        dialog_chain = this_dialog_chain
        number_responses = len(dialog_chain) - 4
        intro_text = dialog_chain[2]
        responses = build_responses(number_responses=number_responses, dialog_chain=dialog_chain)

        # display dialog UI - starting top left, ending bottom right
        common.CommonUtils.draw_dialog_ui(gameworld=gameworld, game_config=game_config, entity_speaking=speaker_id)

        # intro text
        return_text = common.CommonUtils.replace_value_in_event(event_string=intro_text, par1=player_first_name)
        terminal.printf(x=dialog_frame_start_x + 2, y=dialog_frame_start_y + 2, s=return_text)

        # valid responses
        menu_response = build_menu_responses(number_responses=number_responses, responses=responses,
                                             response_text=response_text)
        display.pointy_vertical_menu(header='', menu_options=menu_response, menu_start_x=dialog_frame_start_x + 3,
                                     menu_start_y=dialog_frame_start_y + 5, blank_line=True,
                                     selected_option=selected_response_option)

        # blit the console
        terminal.refresh()
        # add individual UI elements (speaker, intro text, response choices)
        # wait for player to press a key
        valid_event = False
        while not valid_event:
            event_to_be_processed, event_action = input_handlers.handle_game_keys()
            # if event_to_be_processed == 'keypress':
            if event_action == 'quit':
                dialog_chain = ''
                valid_event = True
            if event_action in ('up', 'down'):
                selected_response_option = common.CommonUtils.move_menu_selection(event_action=event_action,
                                                                                  selected_menu_option=selected_response_option,
                                                                                  max_menu_option=2)
                valid_event = True
            if event_action == 'enter':
                valid_event = True
                dialog_chain, selected_response_option = process_dialog_options_after_player_presses_enter(
                    gameworld=gameworld, game_config=game_config, responses=responses,
                    selected_response_option=selected_response_option, response_option=response_option,
                    speaker_id=speaker_id)


def process_dialog_options_after_player_presses_enter(responses, selected_response_option, response_option, gameworld,
                                                      speaker_id, game_config):
    next_step = responses[selected_response_option][response_option]
    if next_step.isalnum():
        next_step_id = int(next_step)
        dialog_chain = load_entity_dialog_chains(gameworld=gameworld, entity_id=speaker_id,
                                                 dialog_steps_id=next_step_id)
        selected_response_option = 0
    else:
        process_end_of_dialog(gameworld=gameworld, dialogue_action=next_step, entity_just_spoken=speaker_id)
        dialog_chain = ''

    return dialog_chain, selected_response_option


def process_end_of_dialog(gameworld, dialogue_action, entity_just_spoken):
    if dialogue_action == 'open_portal_step':
        # cast "open portal to new area/scene spell
        target_map_x = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=entity_just_spoken)
        target_map_y = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=entity_just_spoken)
        spell_cast_at = [target_map_x, target_map_y]
        spell_entity = AsEntities.generate_portal_transition_spell(gameworld=gameworld, cast_at=spell_cast_at)

        SpellUtilities.set_spell_to_cast_this_turn(gameworld=gameworld, mobile_entity=entity_just_spoken,
                                                   spell_entity=spell_entity,
                                                   spell_target_entity=[entity_just_spoken], slot=0,
                                                   map_coords_list=spell_cast_at)

    if dialogue_action == 'shopkeeper_intro':
        # set shopkeeper mobiles want to talk to player
        for ent, (npc, typ) in gameworld.get_components(mobiles.NpcType, mobiles.NpcType):
            if npc.shopkeeper:
                mobileHelp.MobileUtilities.set_talk_to_me_flag(gameworld=gameworld, target_entity=ent)


def build_responses(number_responses, dialog_chain):
    rsp = []
    for i in range(number_responses):
        rsp.append(dialog_chain[3 + i])
    return rsp


def build_menu_responses(number_responses, responses, response_text):
    mnu = []
    for i in range(number_responses):
        mnu.append(responses[i][response_text])
    return mnu


def load_entity_dialog_chains(gameworld, entity_id, dialog_steps_id=0, chain_id=0):
    dialog_chains_file = constants.FILE_DIALOGFILE
    name_details = mobileHelp.MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=entity_id)
    npc_first_name = name_details[0]
    dialog_chain = []
    intro_text = []
    response_text = []
    rules_tag = []

    dialog_file = jsonUtilities.read_json_file(dialog_chains_file)

    top_level_dialog_chain = dialog_file['dialogue_chains'][chain_id]
    dialog_chain.append(top_level_dialog_chain['chain_name'])

    if top_level_dialog_chain['npc_id'] == npc_first_name:
        dialog_chain.append(top_level_dialog_chain['chain_id'])
        dialog_steps = top_level_dialog_chain['dialogue_steps'][dialog_steps_id]
        intro_text.append(dialog_steps['intro_text'])
        response_choices = dialog_steps['choices']
        rules_tag.append(dialog_steps['rules_tag'])
        resp_length = len(response_choices)
        for n in range(resp_length):
            response = response_choices[n]
            response_pair = (response['response_text'], response['response_option'])
            response_text.append(response_pair)

    merged_list = dialog_chain + intro_text + response_text + rules_tag
    return merged_list


def check_for_nearby_valid_mobiles_to_speak_with(gameworld, game_config):
    player_entity = mobileHelp.MobileUtilities.get_player_entity(gameworld=gameworld)

    # check map surrounding player_entity 1x1 square deep
    visible_entities_list = mobileHelp.MobileUtilities.get_ai_visible_entities(gameworld=gameworld,
                                                                               target_entity=player_entity)
    target_entity = get_entity_id_to_talk_to(gameworld=gameworld, player_entity=player_entity,
                                             entities_list=visible_entities_list, game_config=game_config)
    if target_entity == 0:
        common.CommonUtils.fire_event('dialog-general', gameworld=gameworld,
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
            target_letters = common.CommonUtils.helper_print_valid_targets(gameworld=gameworld,
                                                                           valid_targets=valid_targets,
                                                                           game_config=game_config)
            # blit the terminal
            terminal.refresh()
            # get player input
            # wait for user key press
            player_not_pressed_a_key = True
            while player_not_pressed_a_key:
                event_to_be_processed, event_action = input_handlers.handle_game_keys()
                if event_action == 'quit':
                    player_not_pressed_a_key = False
                if event_action in target_letters:
                    target_entity = get_target_entity_id(event_action=event_action, target_letters=target_letters,
                                                         valid_targets=valid_targets)
                    player_not_pressed_a_key = False

    return target_entity


def get_target_entity_id(event_action, target_letters, valid_targets):
    target = target_letters.index(event_action)
    target_entity = valid_targets[target]

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


def process_rules_tag(current_dialog_chain, npc_name):
    new_dialogue_chain = 'nothing'
    # get dialog chain details
    rules_tag = current_dialog_chain[-1]
    if rules_tag != '':
        logger.warning('dialog chain {}', current_dialog_chain)
        logger.warning('rules tag {}', rules_tag)
        dialog_rules_file = constants.FILE_DIALOGUERULESFULE

        rules_file = jsonUtilities.read_json_file(dialog_rules_file)

        for npc_rules in rules_file['dialogue_rules']:
            if npc_rules['npc_id'] == npc_name:
                rules = npc_rules['rules'][0]
                this_tag = rules['rule']
                if this_tag == rules_tag:
                    rules_options = rules['options']
                    new_dialogue_chain = evaluate_dialog_rules(rules_to_evaluate=rules_options,
                                                               current_dialog_chain=current_dialog_chain)
    if new_dialogue_chain == 'nothing':
        new_dialogue_chain = current_dialog_chain

    return new_dialogue_chain


def evaluate_dialog_rules(rules_to_evaluate, current_dialog_chain):
    new_dialog_chain = ''
    # need to replace these hard-coded values with proper game metadata variables
    won = 0
    lost = 0

    for rule in rules_to_evaluate:

        evaluation_test = rule.get("evaluation")
        has_this_rule_evaluated_true = eval(evaluation_test)
        if has_this_rule_evaluated_true:
            message = rule.get("intro_text")
            responses = rule.get("choices")
            dialog_chain_name = current_dialog_chain[0]
            new_dialog_chain = [dialog_chain_name, '001', message]
            for a in range(len(responses)):
                response_dict = responses[a]
                response_text = response_dict.get('response_text')
                response_response = response_dict.get('response_option')
                response_set = (response_text, response_response)
                new_dialog_chain.append(response_set)
            new_dialog_chain.append('none')
            logger.debug(new_dialog_chain)
    return new_dialog_chain
