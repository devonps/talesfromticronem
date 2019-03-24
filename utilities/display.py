import tcod
import tcod.console, tcod.event
from utilities.input_handlers import get_user_input_entity, handle_mouse_in_menus, handle_menus
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
    #height = len(options) + header_height
    height = constants.MENU_MAX_HEIGHT

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


def display_hero_panel(con, key, mouse, gameworld):

    bg = tcod.grey
    hero_panel_displayed = True

    # generate new tcod.console
    hero_panel = tcod.console_new(constants.HERO_PANEL_WIDTH, constants.HERO_PANEL_HEIGHT)
    # hero_panel = tcod.console.Console(width=constants.HERO_PANEL_WIDTH, height=constants.HERO_PANEL_HEIGHT, order='F')

    # prettify the console
    # tcod.console_set_default_background(hero_panel, bg)
    # tcod.console_clear(hero_panel)
    hero_panel.clear(ch=ord(' '), fg=tcod.white, bg=tcod.grey)
    hero_panel.draw_frame(x=0,y=0,
                          width=constants.HERO_PANEL_WIDTH,
                          height=constants.HERO_PANEL_HEIGHT,
                          clear=False,
                          bg_blend=tcod.BKGND_DEFAULT,
                          title='Hero Panel')
    # display the various elements
    # draw the tabs
    tabs_list = ['Equipment', 'Personal', 'Build', 'Story']
    # get the length of the longest word used for the tabs
    maxtablength = 0
    tab_count = 0
    for mytab in tabs_list:
        tab_count += 1
        if len(mytab) > maxtablength:
            maxtablength = len(mytab)
    selected_tab = 1
    x_offset = 11
    y_offset = 8
    # main loop whilst hero panel is displayed
    while hero_panel_displayed:

        tcod.console_blit(hero_panel, 0, 0,
                          constants.HERO_PANEL_WIDTH,
                          constants.HERO_PANEL_HEIGHT,
                          0,
                          constants.HERO_PANEL_LEFT_X,
                          constants.HERO_PANEL_LEFT_Y)
        draw_hero_panel_tabs(hero_panel, tabs_list, maxtablength, selected_tab, y_offset)
        tcod.console_flush()
        for event in tcod.event.wait():
            if event.type == 'KEYDOWN':
                if event.sym == tcod.event.K_ESCAPE:
                    hero_panel_displayed = False
            elif event.type == "MOUSEBUTTONDOWN":
                x = event.tile.x
                y = event.tile.y
                if (x >= x_offset and x <= (x_offset + maxtablength)) and (y >= y_offset and y < (y_offset + tab_count)):
                    ret_value = y - 8
                    selected_tab = ret_value
                logger.info('Tile x/y: {}/{}', x,y)
                logger.info('Menu option: {}', selected_tab)




def draw_hero_panel_tabs(hero_panel, tab_list, maxtablength, selected_tab, y_offset):
    tab_down = 3
    for tab_count, tab in enumerate(tab_list):
        if selected_tab == tab_count:
            hero_panel.print_box(x=1, y=tab_down, width=maxtablength, height=1, string=tab)
            # hero_panel.print_box(x=maxtablength + 1, y=tab_down, width= 1, height=1, string='>')
            # hero_panel.draw_rect(x=maxtablength + 1, y=tab_down, width=1, height=1, ch=ord(">"), fg=tcod.black, bg=tcod.grey)
            hero_panel.draw_rect(x=1, y=tab_down, width=maxtablength, height=1, ch=0, fg=tcod.black, bg=tcod.grey)
        else:
            hero_panel.print_box(x=1, y=tab_down, width=maxtablength, height=1, string=tab)
            hero_panel.draw_rect(x=1, y=tab_down, width=maxtablength, height=1, ch=0, fg=tcod.white, bg=tcod.grey)
        tab_down += 1
        draw_hero_information(hero_panel=hero_panel, selected_tab=selected_tab)

    tab_draw_pos = (3 + selected_tab)
    hero_panel.draw_rect(x=maxtablength + 1, y=1, width=1, height=hero_panel.height - 2, ch=ord("|"), fg=tcod.white, bg=tcod.grey)
    hero_panel.draw_rect(x=maxtablength + 1, y=tab_draw_pos, width=1, height=1, ch=ord(">"), fg=tcod.black, bg=tcod.grey)


def draw_hero_information(hero_panel, selected_tab):
    if selected_tab == 0:
        equipment_tab(console=hero_panel)
    elif selected_tab == 1:
        personal_tab(console=hero_panel)
    elif selected_tab == 2:
        current_build_tab(console=hero_panel)
    else:
        story_tab(console=hero_panel)


def equipment_tab(console):
    console.print_box(x=30, y=5, width=30, height=1, string='EQUIPMNT INFORMATION', fg=tcod.blue, bg=tcod.grey)


def personal_tab(console):
    console.print_box(x=30, y=5, width=30, height=1, string='PERSONAL INFORMATION', fg=tcod.blue, bg=tcod.grey)


def current_build_tab(console):
    console.print_box(x=30, y=5, width=30, height=1, string='BUILD    INFORMATION', fg=tcod.blue, bg=tcod.grey)


def story_tab(console):
    console.print_box(x=30, y=5, width=30, height=1, string='STORY    INFORMATION', fg=tcod.blue, bg=tcod.grey)
