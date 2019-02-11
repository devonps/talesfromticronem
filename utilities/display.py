import tcod
from utilities.input_handlers import get_user_input_entity, handle_mouse_in_menus
from components import userInput
from newGame import constants

from loguru import logger


def menu(con, header, options, width, screen_width, screen_height, posx, posy, foreground, key, mouse, gameworld):

    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate the total height for the menu header with one line per option
    header_height = tcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    if header == '':
        header_height = 0
    height = len(options) + header_height

    # create an off-screen window - this is where the menu options will be displayed
    window = tcod.console_new(width, height)

    # print the header, with auto-wrap
    tcod.console_set_default_foreground(window, foreground)
    tcod.console_print_rect_ex(window, 0, 0, width, height, tcod.BKGND_NONE, tcod.LEFT, header)

    # print the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        tcod.console_print_ex(window, 0, y, tcod.BKGND_NONE, tcod.LEFT, text)
        y += 1
        letter_index += 1

    # compute x and y offsets
    x_offset = posx
    y_offset = posy + header_height
    player_input_entity = get_user_input_entity(gameworld)

    while True:
        tcod.console_blit(window, 0, 0, width, height, 0, posx, posy, 1.0, 0.7)
        tcod.console_flush()
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse)

        ret_value = handle_mouse_in_menus(mouse=mouse, width=width, height=height, header_height=header_height, x_offset=x_offset, y_offset=y_offset)

        if ret_value > -1:
            logger.info('Mouse button menu option {}', ret_value)
            gameworld.component_for_entity(player_input_entity, userInput.Keyboard).keypressed = chr(97 + ret_value)
            gameworld.component_for_entity(player_input_entity, userInput.Mouse).lbutton = True
            keyboard_component = gameworld.component_for_entity(player_input_entity, userInput.Keyboard)
            logger.info('keypress stored as {}', keyboard_component.keypressed)
            return ret_value

        # convert the ASCII code to a menu option
        index = key.c - ord('a')
        key_char = chr(key.c)

        if 0 <= index <= len(options):
            logger.info('at least one key has been pressed {}', key_char)
            return key_char

        if 0 <= index <= 26:
            return None
