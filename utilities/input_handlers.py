import tcod
import tcod.event

from components import mobiles, userInput
from loguru import logger


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
                action = ('left', event.tile.x, event.tile.y)
            else:
                action = ('right', event.tile.x, event.tile.y)
        elif event.type == "MOUSEMOTION":
            pass
    return myevent, action
