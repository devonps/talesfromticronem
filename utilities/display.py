from loguru import logger
from bearlibterminal import terminal
from utilities import configUtilities, colourUtilities, armourManagement, itemsHelp, jewelleryManagement, mobileHelp


def draw_entities_inside_aoe(gameworld, entities_found):
    for a in range(len(entities_found)):
        ent_id = entities_found[a][0]
        ent_x = entities_found[a][1]
        ent_y = entities_found[a][2]
        ent_glyph = mobileHelp.MobileUtilities.get_mobile_glyph(gameworld=gameworld, entity=ent_id)
        ent_fg = mobileHelp.MobileUtilities.get_mobile_fg_render_colour(gameworld=gameworld, entity=ent_id)
        glyph_colour_string = '[font=dungeon][color=' + ent_fg + ']'
        terminal.printf(x=ent_x, y=ent_y, s=glyph_colour_string + ent_glyph)


# the selected option is the choice from list_options that will be highlighted
# so if list_options were  [apple, orange, grape] and selected_option were 'grape' then grape would be highlighted


def coloured_list(list_options, list_x, list_y, selected_option, blank_line, fg):
    list_count = 0

    for option in list_options:
        if selected_option.lower() == option.lower():
            fg_color = "[color=COLOURED_LIST_NOT_SELECTED]"
        else:
            fg_color = fg
        string_to_print = fg_color + option
        terminal.printf(x=list_x, y=list_y + list_count, s=string_to_print)

        list_count += 1
        if blank_line:
            list_count += 1


#
# this is like a single select menu
#
def pointy_vertical_menu(header, menu_options, menu_start_x, menu_start_y, blank_line, selected_option):
    selected_colour = '[color=POINTY_VERTICAL_MENU_SELECTED]'
    non_selected_colour = '[color=POINTY_VERTICAL_MENU_NOT_SELECTED]'

    # print the header, with auto-wrap
    if header != '':
        terminal.print_(x=menu_start_x, y=10, s=header)

    # print the menu options
    menu_count = 0
    mnu = 0

    for option_text in menu_options:
        if selected_option == mnu:
            fg_color = selected_colour
            mnu_pointer = '>'
        else:
            fg_color = non_selected_colour
            mnu_pointer = ' '
        men_text = fg_color + mnu_pointer + ' ' + option_text

        terminal.print_(x=menu_start_x, y=menu_start_y + menu_count, s=men_text)
        menu_count += 1
        mnu += 1
        if blank_line:
            menu_count += 1


def pointy_horizontal_menu(header, menu_options, menu_start_x, menu_start_y, selected_option):
    selected_colour = '[color=POINTY_VERTICAL_MENU_SELECTED]'
    non_selected_colour = '[color=POINTY_VERTICAL_MENU_NOT_SELECTED]'

    # print the header, with auto-wrap
    if header != '':
        terminal.print_(x=menu_start_x, y=10, s=header)

    # print the menu options
    next_pos = 0
    mnu = 0

    for option_text in menu_options:
        if selected_option == mnu:
            fg_color = selected_colour
            mnu_pointer = '>'
        else:
            fg_color = non_selected_colour
            mnu_pointer = ' '
        men_text = fg_color + mnu_pointer + ' ' + option_text

        terminal.print_(x=menu_start_x + next_pos, y=menu_start_y, s=men_text)
        next_pos += len(option_text) + 3
        mnu += 1


def display_coloured_box(title, posx, posy, width, height, fg, bg):
    draw_simple_frame(start_panel_frame_x=posx, start_panel_frame_y=posy, start_panel_frame_width=width,
                      start_panel_frame_height=height, title=title)

    draw_coloured_rectangle(start_panel_frame_x=posx, start_panel_frame_y=posy, start_panel_frame_width=width,
                            start_panel_frame_height=height, ch=u'\u0020', fg=fg, bg=bg)


def draw_coloured_rectangle(start_panel_frame_x, start_panel_frame_y, start_panel_frame_width, start_panel_frame_height,
                            ch, fg, bg):
    string_to_print = "[color=" + fg + '][/color][bkcolor=' + bg + '][/bkcolor]' + ch
    for posx in range(start_panel_frame_width):
        for posy in range(start_panel_frame_height):
            terminal.print_(x=(start_panel_frame_x + 1) + posx, y=(start_panel_frame_y + 1) + posy, s=string_to_print)


def draw_simple_frame(start_panel_frame_x, start_panel_frame_y, start_panel_frame_width, start_panel_frame_height,
                      title):
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
        titlestring = '[color=SIMPLE_FRAME_HEADING_TITLE]' + title
        titlelen = len(title)
        titleminuspanel = start_panel_frame_width - titlelen
        pwx = int(titleminuspanel / 2)
        terminal.print_(x=start_panel_frame_x + pwx, y=start_panel_frame_y, s=titlestring)


def draw_colourful_frame(title, title_decorator, title_loc, corner_decorator, msg):
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
        draw_message(msg_x=msg_x, msg_y=msg_y, msg=msg)

    draw_corner_decorators(start_panel_frame_x=start_panel_frame_x, start_panel_frame_y=start_panel_frame_y,
                           corner_decorator=corner_decorator, start_panel_frame_height=start_panel_frame_height,
                           start_panel_frame_width=start_panel_frame_width)


def draw_message(msg_x, msg_y, msg):
    if msg != '':
        terminal.print_(x=msg_x, y=msg_y, s=msg)


def draw_corner_decorators(start_panel_frame_x, start_panel_frame_y, corner_decorator, start_panel_frame_width,
                           start_panel_frame_height):
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


def draw_clear_text_box(posx, posy, width, height, text, fg, bg):
    terminal.clear_area(x=posx, y=posy, width=width, height=height)

    string_to_print = '[color=' + fg + '][/color][bkcolor=' + bg + '][/bkcolor]' + text
    terminal.print_(x=posx, y=posy - 2, width=60, height=5, align=terminal.TK_ALIGN_LEFT, s=string_to_print)


def set_both_hands_weapon_string_es(both_weapon, gameworld):
    no_item_string = "[color=DISPLAY_NO_ITEM_EQUIPPED]none[/color]"
    both_hands_weapon_name = no_item_string
    if both_weapon > 0:
        both_hands_weapon_name = itemsHelp.ItemUtilities.get_item_name(gameworld=gameworld, entity=both_weapon)
    return both_hands_weapon_name


def set_main_hand_weapon_string_es(main_weapon, gameworld):
    no_item_string = "[color=DISPLAY_NO_ITEM_EQUIPPED]none[/color]"
    main_hand_weapon_name = no_item_string
    if main_weapon > 0:
        main_hand_weapon_name = itemsHelp.ItemUtilities.get_item_name(gameworld=gameworld, entity=main_weapon)
    return main_hand_weapon_name


def set_off_hand_weapon_string_es(off_weapon, gameworld):
    no_item_string = "[color=DISPLAY_NO_ITEM_EQUIPPED]none[/color]"
    off_hand_weapon_name = no_item_string
    if off_weapon > 0:
        off_hand_weapon_name = itemsHelp.ItemUtilities.get_item_name(gameworld=gameworld, entity=off_weapon)
    return off_hand_weapon_name


def set_jewellery_left_ear_string(gameworld, left_ear):
    no_item_string = "[color=DISPLAY_NO_ITEM_EQUIPPED]None[/color]"
    left_ear_string = no_item_string
    if left_ear != 0:
        activator = jewelleryManagement.JewelleryUtilities.get_jewellery_activator(gameworld=gameworld, jewellery_entity=left_ear)
        item_name = itemsHelp.ItemUtilities.get_item_name(gameworld=gameworld, entity=left_ear)
        left_ear_string = activator + ' ' + item_name
    return left_ear_string


def set_jewellery_right_ear_string(gameworld, right_ear):
    no_item_string = "[color=DISPLAY_NO_ITEM_EQUIPPED]None[/color]"
    right_ear_string = no_item_string
    if right_ear != 0:
        activator = jewelleryManagement.JewelleryUtilities.get_jewellery_activator(gameworld=gameworld, jewellery_entity=right_ear)
        item_name = itemsHelp.ItemUtilities.get_item_name(gameworld=gameworld, entity=right_ear)
        right_ear_string = activator + ' ' + item_name
    return right_ear_string


def set_jewellery_left_hand_string(gameworld, left_hand):
    no_item_string = "[color=DISPLAY_NO_ITEM_EQUIPPED]None[/color]"
    left_hand_string = no_item_string
    if left_hand != 0:
        activator = jewelleryManagement.JewelleryUtilities.get_jewellery_activator(gameworld=gameworld, jewellery_entity=left_hand)
        item_name = itemsHelp.ItemUtilities.get_item_name(gameworld=gameworld, entity=left_hand)
        left_hand_string = activator + ' ' + item_name
    return left_hand_string


def set_jewellery_right_hand_string(gameworld, right_hand):
    no_item_string = "[color=DISPLAY_NO_ITEM_EQUIPPED]None[/color]"
    right_hand_string = no_item_string
    if right_hand != 0:
        activator = jewelleryManagement.JewelleryUtilities.get_jewellery_activator(gameworld=gameworld, jewellery_entity=right_hand)
        item_name = itemsHelp.ItemUtilities.get_item_name(gameworld=gameworld, entity=right_hand)
        right_hand_string = activator + ' ' + item_name
    return right_hand_string


def set_jewellery_neck_string(gameworld, neck):
    no_item_string = "[color=DISPLAY_NO_ITEM_EQUIPPED]None[/color]"
    neck_string = no_item_string
    if neck != 0:
        activator = jewelleryManagement.JewelleryUtilities.get_jewellery_activator(gameworld=gameworld, jewellery_entity=neck)
        item_name = itemsHelp.ItemUtilities.get_item_name(gameworld=gameworld, entity=neck)
        neck_string = activator + ' ' + item_name
    return neck_string


def get_head_armour_details(gameworld, entity_id):
    no_item = "[color=DISPLAY_NO_ITEM_EQUIPPED]Head :None[/color]"
    item = "[color=DISPLAY_ITEM_EQUIPPED]Head :[/color]"
    item_list = [no_item]
    head_armour_id = mobileHelp.MobileUtilities.is_entity_wearing_head_armour(gameworld=gameworld, entity=entity_id)
    if head_armour_id > 0:
        armour_material = itemsHelp.ItemUtilities.get_item_material(gameworld=gameworld, entity=head_armour_id)
        armour_displayname = itemsHelp.ItemUtilities.get_item_displayname(gameworld=gameworld, entity=head_armour_id)
        def_head_value = armourManagement.ArmourUtilities.get_armour_defense_value(gameworld=gameworld, entity=head_armour_id)

        item_list = [item, armour_material, armour_displayname, str(def_head_value)]
    return item_list


def get_chest_armour_details(gameworld, entity_id):
    no_item = "[color=DISPLAY_NO_ITEM_EQUIPPED]Chest:None[/color]"
    item = "[color=DISPLAY_ITEM_EQUIPPED]Chest:[/color]"
    item_list = [no_item]
    chest_armour_id = mobileHelp.MobileUtilities.is_entity_wearing_chest_armour(gameworld=gameworld, entity=entity_id)
    if chest_armour_id > 0:
        armour_material = itemsHelp.ItemUtilities.get_item_material(gameworld=gameworld, entity=chest_armour_id)
        armour_displayname = itemsHelp.ItemUtilities.get_item_displayname(gameworld=gameworld, entity=chest_armour_id)
        def_chest_value = armourManagement.ArmourUtilities.get_armour_defense_value(gameworld=gameworld, entity=chest_armour_id)

        item_list = [item, armour_material, armour_displayname, str(def_chest_value)]

    return item_list


def get_hands_armour_details(gameworld, entity_id):
    no_item = "[color=DISPLAY_NO_ITEM_EQUIPPED]Hands:None[/color]"
    item = "[color=DISPLAY_ITEM_EQUIPPED]Hands:[/color]"
    item_list = [no_item]
    hands_armour_id = mobileHelp.MobileUtilities.is_entity_wearing_hands_armour(gameworld=gameworld, entity=entity_id)
    if hands_armour_id > 0:
        armour_material = itemsHelp.ItemUtilities.get_item_material(gameworld=gameworld, entity=hands_armour_id)
        armour_displayname = itemsHelp.ItemUtilities.get_item_displayname(gameworld=gameworld, entity=hands_armour_id)
        def_hands_value = armourManagement.ArmourUtilities.get_armour_defense_value(gameworld=gameworld, entity=hands_armour_id)

        item_list = [item, armour_material, armour_displayname, str(def_hands_value)]

    return item_list


def get_legs_armour_details(gameworld, entity_id):
    no_item = "[color=DISPLAY_NO_ITEM_EQUIPPED]Legs :None[/color]"
    item = "[color=DISPLAY_ITEM_EQUIPPED]Legs :[/color]"
    item_list = [no_item]
    legs_armour_id = mobileHelp.MobileUtilities.is_entity_wearing_legs_armour(gameworld=gameworld, entity=entity_id)
    if legs_armour_id > 0:
        armour_material = itemsHelp.ItemUtilities.get_item_material(gameworld=gameworld, entity=legs_armour_id)
        armour_displayname = itemsHelp.ItemUtilities.get_item_displayname(gameworld=gameworld, entity=legs_armour_id)
        def_legs_value = armourManagement.ArmourUtilities.get_armour_defense_value(gameworld=gameworld, entity=legs_armour_id)

        item_list = [item, armour_material, armour_displayname, str(def_legs_value)]

    return item_list


def get_feet_armour_details(gameworld, entity_id):
    no_item = "[color=DISPLAY_NO_ITEM_EQUIPPED]Feet :None[/color]"
    item = "[color=DISPLAY_ITEM_EQUIPPED]Feet :[/color]"
    item_list = [no_item]
    feet_armour_id = mobileHelp.MobileUtilities.is_entity_wearing_feet_armour(gameworld=gameworld, entity=entity_id)
    if feet_armour_id > 0:
        armour_material = itemsHelp.ItemUtilities.get_item_material(gameworld=gameworld, entity=feet_armour_id)
        armour_displayname = itemsHelp.ItemUtilities.get_item_displayname(gameworld=gameworld, entity=feet_armour_id)
        def_feet_value = armourManagement.ArmourUtilities.get_armour_defense_value(gameworld=gameworld, entity=feet_armour_id)

        item_list = [item, armour_material, armour_displayname, str(def_feet_value)]

    return item_list
