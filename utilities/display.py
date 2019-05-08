import tcod
import tcod.console, tcod.event
from utilities.input_handlers import get_user_input_entity, handle_mouse_in_menus

from components import userInput
from utilities import configUtilities


def menu(con, header, options, width, screen_width, screen_height, posx, posy, foreground, key, mouse, gameworld, game_config):

    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate the total height for the menu header with one line per option
    header_height = tcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    if header == '':
        header_height = 0
    height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MENU_MAX_HEIGHT')


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
            gameworld.component_for_entity(player_input_entity, userInput.Keyboard).keypressed = chr(97 + ret_value)
            gameworld.component_for_entity(player_input_entity, userInput.Mouse).lbutton = True
            tcod.console_clear(window)
            return ret_value

        # convert the ASCII code to a menu option
        index = key.c - ord('a')
        key_char = chr(key.c)

        if 0 <= index <= len(options):
            tcod.console_clear(window)
            return key_char

        if 0 <= index <= 26:
            return None


def display_coloured_box(console, title, posx, posy, width, height, fg, bg ):
    console.print_box(x=posx + 1, y=posy,
                      width=len(title), height=1,
                      string=title)

    console.draw_frame(x=posx - 1, y=posy -1, width=width, height=height,
                       clear=False, bg_blend=tcod.BKGND_DEFAULT, title='')

    console.draw_rect(x=posx, y=posy,
                      width=width - 2, height=height - 2, ch=0, fg=fg, bg=bg)


def draw_panel_frame(hero_panel, game_config):
    hp_tab_max_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='HERO_PANEL_TAB_MAX_WIDTH')
    panel_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='HERO_PANEL_WIDTH')
    panel_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='HERO_PANEL_HEIGHT')

    hero_panel.draw_frame(x=0, y=0,
                          width=panel_width,
                          height=panel_height,
                          clear=False,
                          bg_blend=tcod.BKGND_DEFAULT,
                          title='Hero Panel')

    hero_panel.print_box(x=hp_tab_max_width + 15, y=panel_height - 2,
                         width=40,
                         height=1, string='Mouse to select, ESC to exit')
