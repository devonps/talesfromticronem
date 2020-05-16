from utilities import configUtilities, colourUtilities
from loguru import logger
from bearlibterminal import terminal


# the selected option is the choice from list_options that will be highlighted
# so if list_options were  [apple, orange, grape] and selected_option were 'grape' then grape would be highlighted
def coloured_list(list_options, list_x, list_y, selected_option, blank_line, fg):
    list_count = 0
    start_print_string = "[color="
    end_print_string = ']'

    for option in list_options:
        if selected_option.lower() == option.lower():
            fg_color = colourUtilities.get('YELLOW1')
        else:
            fg_color = fg
        string_to_print = start_print_string + fg_color + end_print_string + option
        terminal.printf(x=list_x, y=list_y + list_count, s=string_to_print)

        list_count += 1
        if blank_line:
            list_count += 1


def pointy_menu(header, menu_options, menu_id_format, menu_start_x, menu_start_y, blank_line, selected_option):
    if len(menu_options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')

    # print the header, with auto-wrap
    if header != '':
        terminal.print_(x=menu_start_x, y=10, s=header)

    # print the menu options
    menu_count = 0
    mnu = 0
    start_print_string = "[color="
    end_print_string = ']'

    for option_text in menu_options:
        if selected_option == mnu:
            fg_color = colourUtilities.get('YELLOW1')
            mnu_pointer = '>'
        else:
            fg_color = colourUtilities.get('WHITE')
            mnu_pointer = ' '
        men_text = start_print_string + fg_color + end_print_string + mnu_pointer + ' ' + option_text

        terminal.print_(x=menu_start_x, y=menu_start_y + menu_count, s=men_text)
        menu_count += 1
        mnu += 1
        if blank_line:
            menu_count += 1


def display_coloured_box(title, posx, posy, width, height, fg, bg):
    draw_simple_frame(start_panel_frame_x=posx, start_panel_frame_y=posy, start_panel_frame_width=width,
                      start_panel_frame_height=height, title=title, fg=fg, bg=bg)

    draw_coloured_rectangle(start_panel_frame_x=posx, start_panel_frame_y=posy, start_panel_frame_width=width,
                            start_panel_frame_height=height, ch=u'\u0020', fg=fg, bg=bg)


def draw_coloured_rectangle(start_panel_frame_x, start_panel_frame_y, start_panel_frame_width, start_panel_frame_height,
                            ch, fg, bg):
    string_to_print = "[color=" + fg + '][/color][bkcolor=' + bg + '][/bkcolor]' + ch
    for posx in range(start_panel_frame_width):
        for posy in range(start_panel_frame_height):
            terminal.print_(x=(start_panel_frame_x + 1) + posx, y=(start_panel_frame_y + 1) + posy, s=string_to_print)


def draw_simple_frame(start_panel_frame_x, start_panel_frame_y, start_panel_frame_width, start_panel_frame_height,
                      title, fg, bg):
    # unicode frame tiles
    top_left = u'\u250c'
    top_right = u'\u2510'
    bottom_left = u'\u2514'
    bottom_right = u'\u2518'
    across_pipe = u'\u2500'
    down_pipe = u'\u2502'

    # top left
    terminal.put(x=start_panel_frame_x, y=start_panel_frame_y, c=top_left)
    # top left --> top right
    pipe_across = start_panel_frame_width
    for posx in range(pipe_across):
        terminal.put(x=(start_panel_frame_x + 1) + posx, y=start_panel_frame_y, c=across_pipe)
    # top right
    terminal.put(x=(start_panel_frame_x + 1) + pipe_across, y=start_panel_frame_y, c=top_right)
    # right side down
    pipe_down = start_panel_frame_height
    for posy in range(pipe_down):
        terminal.put(x=(start_panel_frame_x + 1) + pipe_across, y=(start_panel_frame_y + 1) + posy, c=down_pipe)
    # right corner
    terminal.put(x=(start_panel_frame_x + 1) + pipe_across, y=(start_panel_frame_y + 1) + start_panel_frame_height,
                 c=bottom_right)
    # bottom left --> bottom right
    for posx in range(pipe_across):
        terminal.put(x=(start_panel_frame_x + 1) + posx, y=(start_panel_frame_y + 1) + start_panel_frame_height,
                     c=across_pipe)
    # bottom left
    terminal.put(x=start_panel_frame_x, y=(start_panel_frame_y + 1) + start_panel_frame_height, c=bottom_left)
    # left side down
    for posy in range(pipe_down):
        terminal.put(x=start_panel_frame_x, y=(start_panel_frame_y + 1) + posy, c=down_pipe)

    if title != '':
        titlestring = '[color=' + fg + ']' + title
        titlelen = len(title)
        titleminuspanel = start_panel_frame_width - titlelen
        pwx = int(titleminuspanel / 2)
        terminal.print_(x=start_panel_frame_x + pwx, y=start_panel_frame_y, s=titlestring)


def draw_colourful_frame(title, title_decorator, title_loc, corner_decorator, corner_studs, msg):
    # get config items
    game_config = configUtilities.load_config()

    stored_messages = ['ESC to go back, up & down Enter to accept',
                       'ESC to go back, up & down, left & right arrows to select, Enter to accept',
                       'ESC to go back, Enter to accept',
                       'ESC to go back, mouse to select',
                       'ESC to return to the game']

    msg = stored_messages[msg]

    start_panel_frame_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_X')
    start_panel_frame_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_Y')
    start_panel_frame_width = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                          'START_PANEL_FRAME_WIDTH')
    start_panel_frame_height = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                           'START_PANEL_FRAME_HEIGHT')

    root_con_width = configUtilities.get_config_value_as_integer(game_config, 'gui', 'SCREEN_WIDTH')
    root_con_height = configUtilities.get_config_value_as_integer(game_config, 'gui', 'SCREEN_HEIGHT')

    # check inbound values
    if (start_panel_frame_x + start_panel_frame_width >= root_con_width) or (
            start_panel_frame_y + start_panel_frame_height >= root_con_height):
        logger.warning('Frame for panel will not fit inside root console - frame aborted')
        return

    # load glyphs for frames
    msg_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='newgame',
                                                        parameter='PRETTY_FRAME_MSG_X')
    msg_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='newgame',
                                                        parameter='PRETTY_FRAME_MSG_Y')

    bg = colourUtilities.get('BLACK')

    # draw basic frame
    #  top left corner
    # terminal.color(fg)
    terminal.bkcolor(bg)

    # unicode frame tiles
    top_left = u'\u250c'
    top_right = u'\u2510'
    bottom_left = u'\u2514'
    bottom_right = u'\u2518'
    across_pipe = u'\u2500'
    down_pipe = u'\u2502'

    # top left
    terminal.put(x=start_panel_frame_x, y=start_panel_frame_y, c=top_left)
    # top left --> top right
    pipe_across = (start_panel_frame_x + 1) + start_panel_frame_width
    for posx in range(pipe_across):
        terminal.put(x=(start_panel_frame_x + 1) + posx, y=start_panel_frame_y, c=across_pipe)
    # top right
    terminal.put(x=(start_panel_frame_x + 1) + pipe_across, y=start_panel_frame_y, c=top_right)
    # right side down
    pipe_down = start_panel_frame_height - start_panel_frame_y - 2
    for posy in range(pipe_down):
        terminal.put(x=(start_panel_frame_x + 1) + pipe_across, y=(start_panel_frame_y + 1) + posy, c=down_pipe)
    # right corner
    terminal.put(x=(start_panel_frame_x + 1) + pipe_across, y=start_panel_frame_height - 1, c=bottom_right)
    # bottom left --> bottom right
    for posx in range(pipe_across):
        terminal.put(x=(start_panel_frame_x + 1) + posx, y=start_panel_frame_height - 1, c=across_pipe)
    # bottom left
    terminal.put(x=start_panel_frame_x, y=start_panel_frame_height - 1, c=bottom_left)
    # left side down
    for posy in range(pipe_down):
        terminal.put(x=start_panel_frame_x, y=(start_panel_frame_y + 1) + posy, c=down_pipe)
    title_edging = ''
    # draw string title + decorator if needed
    if title != '':
        if title_decorator == '':
            title_edging = u'\u2502'  # vertical pipe
        pwx = 0
        titlestring = title_edging + title + title_edging
        titlelen = len(titlestring)

        if title_loc == 'left':
            pwx = start_panel_frame_x + 3
        if title_loc == 'centre':
            titleminuspanel = start_panel_frame_width - titlelen
            pwx = int(titleminuspanel / 2)

        if title_loc == 'right':
            pwx = (start_panel_frame_width - titlelen) - 4

        terminal.print_(x=pwx, y=start_panel_frame_y, s=titlestring)

    if msg != '':
        terminal.print_(x=msg_x, y=msg_y, s=msg)

    # You can only draw corner decorators or studs
    if corner_decorator != '':
        # unicode frame tiles
        arc_top_left = u'\u25DC'
        arc_top_right = u'\u256E'
        arc_bottom_left = u'\u2570'
        arc_bottom_right = u'\u256F'

        # top left corner
        terminal.put(x=start_panel_frame_x, y=start_panel_frame_y, c=arc_top_left)
        # # top right corner
        terminal.put(x=start_panel_frame_width - 1, y=start_panel_frame_y, c=arc_top_right)
        # # bottom left corner
        terminal.put(x=start_panel_frame_x, y=start_panel_frame_height - 1, c=arc_bottom_left)
        # # right corner corner
        terminal.put(x=start_panel_frame_width - 1, y=start_panel_frame_height - 1, c=arc_bottom_right)


def draw_pipes_across(start_panel_frame_x, start_panel_frame_width, start_panel_frame_y, across_pipe):
    pipe_across = (start_panel_frame_x + 1) + start_panel_frame_width
    for posx in range(pipe_across):
        terminal.put(x=(start_panel_frame_x + 1) + posx, y=start_panel_frame_y, c=across_pipe)


def draw_clear_text_box(posx, posy, width, height, text, fg, bg):
    terminal.clear_area(x=posx, y=posy, width=width, height=height)

    string_to_print = '[color=' + fg + '][/color][bkcolor=' + bg + '][/bkcolor]' + text
    terminal.print_(x=posx, y=posy - 2, width=60, height=5, align=terminal.TK_ALIGN_LEFT, s=string_to_print)
