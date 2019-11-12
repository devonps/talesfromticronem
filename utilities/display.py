
from utilities import configUtilities, colourUtilities
from loguru import logger

from bearlibterminal import terminal


# the selected option is the choice from list_options that will be highlighted
# so if list_options were  [apple, orange, grape] and selected_option were 'grape' then grape would be highlighted
def coloured_list(list_options, list_x, list_y, selected_option, blank_line, fg):
    lst = 0
    list_count = 0
    bg_color = colourUtilities.get('BLACK')

    for option in list_options:
        if selected_option.lower() == option.lower():
            fg_color = colourUtilities.get('YELLOW1')
        else:
            fg_color = fg
        string_to_print = '[color=' + fg_color + ']' + option
        terminal.print(x=list_x, y=list_y + list_count, s=string_to_print)

        list_count += 1
        lst += 1
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

    letter_index = ord('a')
    for option_text in menu_options:
        if selected_option == mnu:
            fg_color = colourUtilities.get('YELLOW1')
            mnu_pointer = '>'
        else:
            fg_color = colourUtilities.get('WHITE')
            mnu_pointer = ' '
        men_text = '[color=' + fg_color + ']' + mnu_pointer + ' ' + option_text

        terminal.print_(x=menu_start_x, y=menu_start_y + menu_count, s=men_text)
        menu_count += 1
        mnu += 1
        if blank_line:
            menu_count += 1
        letter_index += 1


def display_coloured_box(title, posx, posy, width, height, fg, bg):

    draw_simple_frame(startx=posx, starty=posy, width=width, height=height, title=title, fg=fg, bg=bg)

    draw_coloured_rectangle(startx=posx, starty=posy, width=width, height=height, ch=u'\u0020', fg=fg, bg=bg)


def draw_coloured_rectangle(startx, starty, width, height, ch, fg, bg):
    string_to_print = '[color=' + fg + '][/color][bkcolor=' + bg + '][/bkcolor]' + ch
    for posx in range(width):
        for posy in range(height):
            terminal.print_(x=(startx + 1) + posx, y=(starty + 1) + posy, s=string_to_print)


def draw_simple_frame(startx, starty, width, height, title, fg, bg):
    # unicode frame tiles
    top_left = u'\u250c'
    top_right = u'\u2510'
    bottom_left = u'\u2514'
    bottom_right = u'\u2518'
    across_pipe = u'\u2500'
    down_pipe = u'\u2502'

    # top left
    terminal.put(x=startx, y=starty, c=top_left)
    # top left --> top right
    pipe_across = width
    for posx in range(pipe_across):
        terminal.put(x=(startx + 1) + posx, y=starty, c=across_pipe)
    # top right
    terminal.put(x=(startx + 1) + pipe_across, y=starty, c=top_right)
    # right side down
    pipe_down = height
    for posy in range(pipe_down):
        terminal.put(x=(startx + 1) + pipe_across, y=(starty + 1) + posy, c=down_pipe)
    # right corner
    terminal.put(x=(startx + 1) + pipe_across, y=(starty + 1) + height, c=bottom_right)
    # bottom left --> bottom right
    for posx in range(pipe_across):
        terminal.put(x=(startx + 1) + posx, y=(starty + 1) + height, c=across_pipe)
    # bottom left
    terminal.put(x=startx, y=(starty + 1) + height, c=bottom_left)
    # left side down
    for posy in range(pipe_down):
        terminal.put(x=startx, y=(starty + 1) + posy, c=down_pipe)

    if title != '':
        titlestring = '[color=' + fg + ']' + title
        titlelen = len(title)
        titleminuspanel = width - titlelen
        pwx = int(titleminuspanel / 2)
        terminal.print_(x=startx + pwx, y=starty, s=titlestring)


def draw_colourful_frame(startx, starty, width, height, title, title_decorator, title_loc, corner_decorator,
                         corner_studs, msg):
    # get config items
    game_config = configUtilities.load_config()

    root_con_width = configUtilities.get_config_value_as_integer(game_config, 'tcod', 'SCREEN_WIDTH')
    root_con_height = configUtilities.get_config_value_as_integer(game_config, 'tcod', 'SCREEN_HEIGHT')
    # check inbound values
    if (startx + width >= root_con_width) or (starty + height >= root_con_height):
        logger.warning('Frame for panel will not fit inside root console - frame aborted')
        return

    # load glyphs for frames
    msg_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='newgame',
                                                        parameter='PRETTY_FRAME_MSG_X')
    msg_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='newgame',
                                                        parameter='PRETTY_FRAME_MSG_Y')

    fg = colourUtilities.get('YELLOW2')
    bg = colourUtilities.get('BLACK')

    # draw basic frame
    #  top left corner
    terminal.color(fg)
    terminal.bkcolor(bg)

    # unicode frame tiles
    top_left = u'\u250c'
    top_right = u'\u2510'
    bottom_left = u'\u2514'
    bottom_right = u'\u2518'
    across_pipe = u'\u2500'
    down_pipe = u'\u2502'

    # top left
    terminal.put(x=startx, y=starty, c=top_left)
    # top left --> top right
    pipe_across = (startx + 1) + width
    for posx in range(pipe_across):
        terminal.put(x=(startx + 1) + posx, y=starty, c=across_pipe)
    # top right
    terminal.put(x=(startx + 1) + pipe_across, y=starty, c=top_right)
    # right side down
    pipe_down = height - starty - 2
    for posy in range(pipe_down):
        terminal.put(x=(startx + 1) + pipe_across, y=(starty + 1) + posy, c=down_pipe)
    # right corner
    terminal.put(x=(startx + 1) + pipe_across, y=height - 1, c=bottom_right)
    # bottom left --> bottom right
    for posx in range(pipe_across):
        terminal.put(x=(startx + 1) + posx, y=height - 1, c=across_pipe)
    # bottom left
    terminal.put(x=startx, y=height - 1, c=bottom_left)
    # left side down
    for posy in range(pipe_down):
        terminal.put(x=startx, y=(starty + 1) + posy, c=down_pipe)
    title_edging = ''
    # draw string title + decorator if needed
    if title != '':
        if title_decorator == '':
            title_edging = u'\u2502'  # vertical pipe
        pwx = 0
        titlestring = title_edging + title + title_edging
        titlelen = len(titlestring)

        if title_loc == 'left':
            pwx = startx + 3
        if title_loc == 'centre':
            titleminuspanel = width - titlelen
            pwx = int(titleminuspanel / 2)

        if title_loc == 'right':
            pwx = (width - titlelen) - 4

        terminal.print_(x=pwx, y=starty, s=titlestring)

    if msg != '':
        ss = msg.split('/')
        terminal.print_(x=msg_x, y=msg_y, s=ss[0])
        terminal.print_(x=msg_x + len(ss[0]), y=msg_y, s=ss[1])

    # You can only draw corner decorators or studs
    if corner_decorator != '':

        # unicode frame tiles
        arc_top_left = u'\u25DC'
        arc_top_right = u'\u256E'
        arc_bottom_left = u'\u2570'
        arc_bottom_right = u'\u256F'

        # top left corner
        terminal.put(x=startx, y=starty, c=arc_top_left)
        # # top right corner
        terminal.put(x=width - 1, y=starty, c=arc_top_right)
        # # bottom left corner
        terminal.put(x=startx, y=height - 1, c=arc_bottom_left)
        # # right corner corner
        terminal.put(x=width - 1, y=height - 1, c=arc_bottom_right)

    elif corner_studs != '':
        corner_stud_decorator = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                            parameter='frame_corner_studs_' + corner_studs)
        # # top left
        # console.print(x=startx + 1, y=starty + 1, string=chr(corner_stud_decorator), fg=corner_decorator_fg, bg=corner_decorator_bg)
        # # top right
        # console.print(x=width - 2, y=starty + 1, string=chr(corner_stud_decorator), fg=corner_decorator_fg, bg=corner_decorator_bg)
        # # bottom left
        # console.print(x=startx + 1, y=height - 2, string=chr(corner_stud_decorator), fg=corner_decorator_fg, bg=corner_decorator_bg)
        # # bottom right
        # console.print(x=width - 2, y=height - 2, string=chr(corner_stud_decorator), fg=corner_decorator_fg, bg=corner_decorator_bg)


def draw_clear_text_box(posx, posy, width, height, text, fg, bg):

    terminal.clear_area(x=posx, y=posy, width=width, height=height)

    string_to_print = '[color=' + fg + '][/color][bkcolor=' + bg + '][/bkcolor]' + text
    terminal.print_(x=posx, y=posy - 2, width=60, height=5, align=terminal.TK_ALIGN_LEFT, s=string_to_print )