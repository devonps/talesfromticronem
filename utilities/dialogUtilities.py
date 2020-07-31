from bearlibterminal import terminal

from utilities.common import CommonUtils
from utilities.display import draw_simple_frame
from utilities.input_handlers import handle_game_keys
from utilities.mobileHelp import MobileUtilities
from utilities import formulas, configUtilities, colourUtilities


def initiate_dialog(gameworld, game_config):

    entity_to_talk_with = check_for_nearby_valid_mobiles_to_speak_with(gameworld=gameworld, game_config=game_config)

    return entity_to_talk_with


def check_for_nearby_valid_mobiles_to_speak_with(gameworld, game_config):
    player_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)

    # check map surrounding player_entity 1x1 square deep
    visible_entities_list = MobileUtilities.get_visible_entities(gameworld=gameworld, target_entity=player_entity)
    target_entity = get_entity_id_to_talk_to(gameworld=gameworld, player_entity=player_entity, entities_list=visible_entities_list, game_config=game_config)
    if target_entity == 0:
        CommonUtils.fire_event('dialog-general', gameworld=gameworld, dialog='There is no one near enough to speak with.')
    return target_entity


def get_entity_id_to_talk_to(gameworld, player_entity, entities_list, game_config):
    # this will return a single NPC entity id either because it's the only one visible and in range for chat
    # OR the player selects from a given list
    target_entity = 0
    valid_targets, entity_count = get_list_of_valid_targets(gameworld=gameworld, player_entity=player_entity, entities_list=entities_list)

    if entity_count > 0:
        # display popup
        target_letters = CommonUtils.helper_print_valid_targets(gameworld=gameworld, valid_targets=valid_targets, game_config=game_config)

        # blit the terminal
        terminal.refresh()
        # get player input
        # wait for user key press
        player_not_pressed_a_key = True
        while player_not_pressed_a_key:
            event_to_be_processed, event_action = handle_game_keys()
            if event_action == 'quit':
                player_not_pressed_a_key = False

            if event_action != 'quit':
                key_pressed = chr(97 + event_action)
                if key_pressed in target_letters:
                    target = target_letters.index(key_pressed)
                    target_entity = valid_targets[target]
                    player_not_pressed_a_key = False

    return target_entity


def get_list_of_valid_targets(gameworld, player_entity, entities_list):
    valid_targets = []
    entity_count = 0
    for loop_index in range(len(entities_list)):
        distance_to_target_npc = int(formulas.calculate_distance_to_target(gameworld=gameworld, from_entity=player_entity,
                                                  to_entity=entities_list[loop_index]))
        if distance_to_target_npc == 1:
            valid_targets.append(entities_list[loop_index])
            entity_count += 1

    return valid_targets, entity_count