import tcod
from utilities.input_handlers import get_user_input_entity
from components import userInput


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

    # blit the contents of 'window' to the root console
    tcod.console_blit(window, 0, 0, width, height, 0, posx, posy, 1.0, 0.7)
    # compute x and y offsets
    x_offset = posx
    y_offset = posy + header_height
    player_input_entity = get_user_input_entity(gameworld)

    while True:
        tcod.console_flush()
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse)

        if mouse.lbutton_pressed:
            (menu_x, menu_y) = (mouse.cx - x_offset, mouse.cy - y_offset)
            if (menu_x >= 0 and menu_x < width) and (menu_y >= 0 and menu_y < height - header_height):
                gameworld.component_for_entity(player_input_entity, userInput.Keyboard).keypressed = chr(97 + menu_y)
                gameworld.component_for_entity(player_input_entity, userInput.Mouse).lbutton = True
                print('console set to ' + str(con))
                print('menu option ' + str(menu_y))
                return menu_y

        if mouse.rbutton_pressed or key.vk == tcod.KEY_ESCAPE:
            return None

        # convert the ASCII code to a menu option
        index = key.c - ord('a')
        key_char = chr(key.c)

        if 0 <= index <= len(options):
            print('console set to ' + str(con))
            return key_char

        if 0 <= index <= 26:
            return None
