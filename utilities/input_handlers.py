import tcod

from components import mobiles, userInput
from loguru import logger
from newGame import constants
from utilities.externalfileutilities import Externalfiles
from newGame.game_messages import Message


def handle_keys(mouse, key, gameworld, player, message_log):
    # movement
    player_velocity_component = gameworld.component_for_entity(player, mobiles.Velocity)
    position_component = gameworld.component_for_entity(player, mobiles.Position)
    ev = tcod.sys_wait_for_event(tcod.EVENT_KEY, key, mouse, flush=False)
    if ev & tcod.EVENT_KEY_PRESS:
        key_char = chr(key.c)
        if key.vk == tcod.KEY_UP:
            player_velocity_component.dy = -1
            position_component.hasMoved = True
            value = 'move:' + str(player) + ':0:-1'
            Externalfiles.write_to_existing_file(constants.GAME_ACTIONS_FILE, value)
            return {'player_moved': True}
        elif key.vk == tcod.KEY_DOWN:
            player_velocity_component.dy = 1
            position_component.hasMoved = True
            value = 'move:' + str(player) + ':0:1'
            Externalfiles.write_to_existing_file(constants.GAME_ACTIONS_FILE, value)
            return {'player_moved': True}
        elif key.vk == tcod.KEY_LEFT:
            player_velocity_component.dx = -1
            position_component.hasMoved = True
            value = 'move:' + str(player) + ':-1:0'
            Externalfiles.write_to_existing_file(constants.GAME_ACTIONS_FILE, value)
            return {'player_moved': True}
        elif key.vk == tcod.KEY_RIGHT:
            player_velocity_component.dx = 1
            position_component.hasMoved = True
            value = 'move:' + str(player) + ':1:0'
            Externalfiles.write_to_existing_file(constants.GAME_ACTIONS_FILE, value)
            return {'player_moved': True}

        # non-movement keys
        if key.vk == tcod.KEY_ENTER:
            message_log.add_message(message=Message('123456789012345678901234567890', color=tcod.white))
        if key.vk == tcod.KEY_ENTER and key.lalt:
            # Alt+Enter: toggle full screen
            message_log.add_message(message=Message('Full screen mode activated', color=tcod.white))
            return {'fullscreen': True}

        elif key.vk == tcod.KEY_ESCAPE:
            # Exit the game
            value = 'exit:true'
            Externalfiles.write_to_existing_file(constants.GAME_ACTIONS_FILE, value)
            return {'exit': True}
        # hero action keys
        elif key_char == 'h':
            return {'display_hero_panel': True}

    return {}


def handle_menus(key, mouse, gameworld):
    key_char = chr(key.c)
    if key.vk == tcod.KEY_CHAR:
        return key_char
    player_input_entity = get_user_input_entity(gameworld)
    mouse_component = gameworld.component_for_entity(player_input_entity, userInput.Mouse)
    keyboard_component = gameworld.component_for_entity(player_input_entity, userInput.Keyboard)
    if mouse:
        if mouse_component.lbutton:
            return keyboard_component.keypressed
    return {}


def handle_mouse_in_menus(mouse, width, height, header_height, x_offset, y_offset):
    if mouse.lbutton_pressed:

        (menu_x, menu_y) = (mouse.cx - x_offset, mouse.cy - y_offset)
        logger.info('left mouse button pressed at {}/{}', menu_x, menu_y)
        if (menu_x >= 0 and menu_x < width) and (menu_y >= 0 and menu_y < height - header_height):
            return menu_y
    return -1


def handle_mouse(mouse):
    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}

    return {}


def get_user_input_entity(gameworld):
    for ent, (k, m) in gameworld.get_components(userInput.Mouse, userInput.Keyboard):
        return ent
