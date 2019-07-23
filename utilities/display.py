import tcod
import tcod.console, tcod.event
from utilities.input_handlers import get_user_input_entity, handle_mouse_in_menus, handle_game_keys

from components import userInput
from utilities import configUtilities, colourUtilities
from loguru import logger


def menu(con, header, options, width, screen_width, screen_height, posx, posy, foreground, key, mouse, gameworld, game_config):

    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate the total height for the menu header with one line per option
    # header_height = tcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    header_height = con.get_height_rect(x=0, y=0, width=width, height=screen_height, string=header)
    if header == '':
        header_height = 0
    height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MENU_MAX_HEIGHT')


    # create an off-screen window - this is where the menu options will be displayed
    window = tcod.console.Console(width, height)

    # print the header, with auto-wrap
    window.print(x=0, y=0, string=header, bg_blend=tcod.BKGND_NONE, alignment=tcod.LEFT)

    # print the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        # tcod.console_print_ex(window, 0, y, tcod.BKGND_NONE, tcod.LEFT, text)
        window.print(x=0, y=y, string=text, bg_blend=tcod.BKGND_NONE, alignment=tcod.LEFT)
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
            window.clear()
            # tcod.console_clear(window)
            return key_char

        if 0 <= index <= 26:
            return None


def better_menu(console, header, menu_options, menu_id_format, menu_start_x, blank_line):
    if len(menu_options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')

    # print the header, with auto-wrap
    if header != '':
        console.print(x=menu_start_x, y=10, string=header, bg_blend=tcod.BKGND_NONE, alignment=tcod.LEFT)

    # print the menu options
    menu_count = len(menu_options) + 15
    letter_index = ord('a')
    for option_text in menu_options:
        menu_id = chr(letter_index)
        menu_text = ')' + option_text
        bg_color = tcod.black
        fg_color = tcod.white

        if menu_id_format:
            fg_color = tcod.light_blue
        console.print(x=menu_start_x, y=menu_count, string=menu_id, fg=fg_color, bg=bg_color, bg_blend=tcod.BKGND_NONE,
                      alignment=tcod.LEFT)
        fg_color = tcod.white
        console.print(x=menu_start_x + 1, y=menu_count, string=menu_text, fg=fg_color, bg=bg_color,
                      bg_blend=tcod.BKGND_NONE,
                      alignment=tcod.LEFT)
        menu_count += 1
        if blank_line:
            menu_count += 1
        letter_index += 1


def pointy_menu(console, header, menu_options, menu_id_format, menu_start_x, menu_start_y, blank_line, selected_option):
    if len(menu_options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')

    # print the header, with auto-wrap
    if header != '':
        console.print(x=menu_start_x, y=10, string=header, bg_blend=tcod.BKGND_NONE, alignment=tcod.LEFT)

    # print the menu options
    menu_count = len(menu_options) + 15
    mnu = 0
    letter_index = ord('a')
    for option_text in menu_options:
        menu_id = chr(letter_index)
        menu_text = ')' + option_text
        if selected_option == mnu:
            bg_color = tcod.black
            fg_color = tcod.yellow
            mnu_pointer = '>'
        else:
            bg_color = tcod.black
            fg_color = tcod.white
            mnu_pointer = ' '
        men_text = mnu_pointer + ' ' + option_text
        console.print(x=menu_start_x, y=menu_count, string=men_text, fg=fg_color, bg=bg_color, bg_blend=tcod.BKGND_NONE,
                      alignment=tcod.LEFT)
        menu_count += 1
        mnu += 1
        if blank_line:
            menu_count += 1
        letter_index += 1


def display_coloured_box(console, title, posx, posy, width, height, fg, bg ):
    console.print_box(x=posx + 1, y=posy,
                      width=len(title), height=1,
                      string=title)

    console.draw_frame(x=posx - 1, y=posy -1, width=width, height=height,
                       clear=False, bg_blend=tcod.BKGND_DEFAULT, title='')

    console.draw_rect(x=posx, y=posy,
                      width=width - 2, height=height - 2, ch=0, fg=fg, bg=bg)


def draw_colourful_frame(console, game_config, startx, starty, width, height, title, title_decorator, title_loc, corner_decorator, corner_studs, msg):
    # get config items
    root_con_width = configUtilities.get_config_value_as_integer(game_config, 'tcod', 'SCREEN_WIDTH')
    root_con_height = configUtilities.get_config_value_as_integer(game_config, 'tcod', 'SCREEN_HEIGHT')
    # check inbound values
    if (startx + width >= root_con_width) or (starty + height >= root_con_height):
        logger.warning('Frame for panel will not fit inside root console - frame aborted')
        return

    # load glyphs for frames
    gui_frame = configUtilities.get_config_value_as_string(configfile=game_config, section='gui',
                                                           parameter='frame_border_pipe_type')
    across_pipe = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                              parameter='frame_' + gui_frame + '_across_pipe')
    bottom_left = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                              parameter='frame_' + gui_frame + '_bottom_left')
    bottom_right = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                               parameter='frame_' + gui_frame + '_bottom_right')
    down_pipe = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                            parameter='frame_' + gui_frame + '_down_pipe')
    top_left = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                           parameter='frame_' + gui_frame + '_top_left')
    top_right = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='frame_' + gui_frame + '_top_right')
    msg_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='newgame', parameter='PRETTY_FRAME_MSG_X')
    msg_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='newgame', parameter='PRETTY_FRAME_MSG_Y')

    fg = colourUtilities.WHITE
    bg = colourUtilities.BLACK
    corner_decorator_fg = colourUtilities.YELLOW1
    corner_decorator_bg = colourUtilities.BLACK

    # draw basic frame
    #  top left corner
    console.print(x=startx, y=starty, string=chr(top_left), fg=fg, bg=bg)
    # top left --> top right
    console.draw_rect(x=startx + 1, y=starty, width=width - 7, height=1, ch=across_pipe, fg=fg, bg=bg)
    # top right
    console.print(x=width-1, y=starty, string=chr(top_right), fg=fg, bg=bg)
    # right side down
    console.draw_rect(x=width - 1, y=starty + 1, width=1, height=height - 4, ch=down_pipe, fg=fg, bg=bg)
    # # right corner
    console.print(x=width - 1, y=height - 1, string=chr(bottom_right), fg=fg, bg=bg)
    # # bottom left --> bottom right
    console.draw_rect(x=startx + 1, y=height - 1, width=width - 7, height=1, ch=across_pipe, fg=fg, bg=bg)
    # # bottom left
    console.print(x=startx, y=height - 1, string=chr(bottom_left), fg=fg, bg=bg)
    # # left side down
    console.draw_rect(x=startx, y=starty + 1, width=1, height=height - 4, ch=down_pipe, fg=fg, bg=bg)

    # draw string title + decorator if needed

    if title:
        if title_decorator:
            title_decorator = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='frame_title_decorator')
        pwx = 0
        titlelen = len(title)

        if title_loc == 'left':
            pwx = startx + 3
        if title_loc == 'centre':
            titleminuspanel = width - titlelen
            pwx = int(titleminuspanel / 2)
        if title_loc == 'right':
            pwx = (width - titlelen) - 4

        titlestring = chr(title_decorator) + title + chr(title_decorator)

        console.print_box(x=pwx, y=starty, width=len(titlestring), height=1, string=titlestring)

    if msg != '':
        s = msg.split('/')
        console.print(x=msg_x, y=msg_y, fg=tcod.yellow, string=s[0])
        console.print(x=msg_x + len(s[0]), y=msg_y, fg=tcod.white, string=s[1])

    # You can only draw corner decorators or studs
    if corner_decorator != '':
        cd = configUtilities.get_config_value_as_list(configfile=game_config, section='gui',
                                                      parameter='frame_corner_decorator_' + corner_decorator)

        corner_decorator = list(map(int, cd))
        # top left corner
        console.print(x=startx, y=starty, string=chr(corner_decorator[0]), fg=fg, bg=bg)
        # top right corner
        console.print(x=width-1, y=starty, string=chr(corner_decorator[1]), fg=fg, bg=bg)
        # bottom left corner
        console.print(x=startx, y=height - 1, string=chr(corner_decorator[2]), fg=fg, bg=bg)
        # right corner corner
        console.print(x=width - 1, y=height - 1, string=chr(corner_decorator[3]), fg=fg, bg=bg)

    elif corner_studs != '':
            corner_stud_decorator = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                                parameter='frame_corner_studs_' + corner_studs)
            # top left
            console.print(x=startx + 1, y=starty + 1, string=chr(corner_stud_decorator), fg=corner_decorator_fg, bg=corner_decorator_bg)
            # top right
            console.print(x=width - 2, y=starty + 1, string=chr(corner_stud_decorator), fg=corner_decorator_fg, bg=corner_decorator_bg)
            # bottom left
            console.print(x=startx + 1, y=height - 2, string=chr(corner_stud_decorator), fg=corner_decorator_fg, bg=corner_decorator_bg)
            # bottom right
            console.print(x=width - 2, y=height - 2, string=chr(corner_stud_decorator), fg=corner_decorator_fg, bg=corner_decorator_bg)
