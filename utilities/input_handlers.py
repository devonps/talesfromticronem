import tcod
import tcod.event

from components import mobiles, userInput
from loguru import logger
from utilities.game_messages import Message


def handle_keys(mouse, key, gameworld, player, message_log, game_config):

    # movement
    player_velocity_component = gameworld.component_for_entity(player, mobiles.Velocity)
    for event in tcod.event.wait():
        if event.type == 'KEYDOWN':
            if event.sym == tcod.event.K_UP:
                player_velocity_component.dy = -1
                return {'player_moved': True}
            if event.sym == tcod.event.K_DOWN:
                player_velocity_component.dy = 1
                return {'player_moved': True}
            if event.sym == tcod.event.K_LEFT:
                player_velocity_component.dx = -1
                return {'player_moved': True}
            if event.sym == tcod.event.K_RIGHT:
                player_velocity_component.dx = 1
                return {'player_moved': True}

            if event.sym == tcod.event.K_ESCAPE:
                # Exit the game
                return {'exit': True}
        if event.type == "TEXTINPUT":
        # hero action keys
            if event.text == 'i':
                return {'display_inv_panel': True}
            if event.text == 'g':
                return {'pickup': True}

    #
    #     # non-movement keys
    #     if key.vk == tcod.KEY_ENTER:
    #         message_log.add_message(message=Message('123456789012345678901234567890', color=tcod.white), game_config=game_config)
    #     if key.vk == tcod.KEY_ENTER and key.lalt:
    #         # Alt+Enter: toggle full screen
    #         message_log.add_message(message=Message('Full screen mode activated', color=tcod.white), game_config=game_config)
    #         return {'fullscreen': True}



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
        if (0 <= menu_x < width) and (0 <= menu_y < height - header_height):
            return menu_y
    return -1


def get_user_input_entity(gameworld):
    for ent, (k, m) in gameworld.get_components(userInput.Mouse, userInput.Keyboard):
        return ent


def handle_game_keys():
    action = ''
    myevent = ''
    for event in tcod.event.wait():
        if event.type == 'KEYDOWN':
            if event.sym == tcod.event.K_ESCAPE:
                myevent = 'keypress'
                action = 'quit'
            if event.sym == tcod.event.K_LEFT:
                myevent = 'keypress'
                action = 'left'
            if event.sym == tcod.event.K_RIGHT:
                myevent = 'keypress'
                action = 'right'
            if event.sym == tcod.event.K_UP:
                myevent = 'keypress'
                action = 'up'
            if event.sym == tcod.event.K_DOWN:
                myevent = 'keypress'
                action = 'down'
            if event.sym == tcod.event.K_RETURN:
                myevent = 'keypress'
                action = 'enter'
            if event.sym == tcod.event.K_BACKSPACE:
                myevent = 'keypress'
                action = 'delete'
        if event.type == "TEXTINPUT":
            myevent = 'textinput'
            action = event.text
        elif event.type == "MOUSEBUTTONDOWN":
            myevent = 'mousebutton'
            if event.button == tcod.event.BUTTON_LEFT:
                action = 'left'
            else:
                action = 'right'
        elif event.type == "MOUSEMOTION":
            pass
    return myevent, action
