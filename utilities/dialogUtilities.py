from bearlibterminal import terminal
from loguru import logger

from utilities.common import CommonUtils
from utilities.display import draw_simple_frame
from utilities.gamemap import GameMapUtilities
from utilities.input_handlers import handle_game_keys
from utilities.mobileHelp import MobileUtilities
from utilities import formulas, configUtilities, colourUtilities


def initiate_dialog(gameworld, game_config):

    entity_to_talk_with = check_for_nearby_valid_mobiles_to_speak_with(gameworld=gameworld, game_config=game_config)


def check_for_nearby_valid_mobiles_to_speak_with(gameworld, game_config):
    player_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)

    # check map surrounding player_entity 1x1 square deep
    visible_entities_list = MobileUtilities.get_visible_entities(gameworld=gameworld, target_entity=player_entity)
    target_entity = get_entity_id_to_talk_to(gameworld=gameworld, player_entity=player_entity, entities_list=visible_entities_list)
    if target_entity == 0:
        CommonUtils.fire_event('dialog-general', gameworld=gameworld, dialog='There is no one near enough to speak with.')
    return target_entity


def get_entity_id_to_talk_to(gameworld, player_entity, entities_list, game_config):
    # this will return a single NPC entity id either because it's the only one visible and in range for chat
    # OR the player selects from a given list
    target_entity = 0
    entity_count = 0
    valid_targets = []
    for loop_index in range(len(entities_list)):
        distance_to_target_npc = int(formulas.calculate_distance_to_target(gameworld=gameworld, from_entity=player_entity,
                                                  to_entity=entities_list[loop_index]))
        if distance_to_target_npc == 1:
            target_entity = entities_list[loop_index]
            valid_targets.append(entities_list[loop_index])
            entity_count += 1
    if entity_count == 0:
        return target_entity
    else:
        # display popup
        target_letters = helper_print_valid_targets(gameworld=gameworld, valid_targets=valid_targets, game_config=game_config)

        # blit the terminal
        terminal.refresh()
        # get player input
        # wait for user key press
        player_not_pressed_a_key = True
        while player_not_pressed_a_key:
            event_to_be_processed, event_action = handle_game_keys()
            if event_to_be_processed == 'keypress':
                if event_action == 'quit':
                    player_not_pressed_a_key = False

                if event_action != 'quit':
                    key_pressed = chr(97 + event_action)
                    if key_pressed in target_letters:
                        target = target_letters.index(key_pressed)
                        target_entity = valid_targets[target]
                        player_not_pressed_a_key = False

    return target_entity


def helper_print_valid_targets(gameworld, valid_targets, game_config):
    vp_x_offset = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                              parameter='VIEWPORT_START_X')
    vp_y_offset = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                              parameter='VIEWPORT_START_Y')

    height = 5 + len(valid_targets) + 1

    terminal.clear_area(vp_x_offset + 1, vp_y_offset + 1, 26, height)

    draw_simple_frame(start_panel_frame_x=vp_x_offset, start_panel_frame_y=vp_y_offset, start_panel_frame_width=26,
                      start_panel_frame_height=height, title='| Valid Targets |',
                      fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))

    lft = vp_x_offset + 1

    entity_tag = vp_y_offset + 2
    target_letters = []

    xx = 0
    base_str_to_print = "[color=white][font=dungeon]"
    if len(valid_targets) == 0:
        str_to_print = base_str_to_print + 'No valid targets'
        terminal.printf(x=vp_x_offset + 3, y=entity_tag, s=str_to_print)
    else:
        for x in valid_targets:
            entity_name = MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=x)
            entity_fg = MobileUtilities.get_mobile_fg_render_colour(gameworld=gameworld, entity=x)
            entity_bg = MobileUtilities.get_mobile_bg_render_colour(gameworld=gameworld, entity=x)

            str_to_print = base_str_to_print + chr(
                97 + xx) + ") [color=" + entity_fg + "][bkcolor=" + entity_bg + "]" + "@" + ' ' + entity_name[0]
            terminal.printf(x=vp_x_offset + 2, y=entity_tag, s=str_to_print)
            entity_tag += 1
            target_letters.append(chr(97 + xx))
            xx += 1
    str_to_print = base_str_to_print + 'Press ESC to cancel'
    terminal.printf(x=vp_x_offset + (lft + 3), y=(vp_y_offset + height), s=str_to_print)

    return target_letters
