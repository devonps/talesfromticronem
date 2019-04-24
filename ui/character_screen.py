import tcod.event

from newGame import constants
from utilities.mobileHelp import MobileUtilities
from utilities.display import display_coloured_box
from utilities.itemsHelp import ItemUtilities
from components import mobiles


def display_hero_panel(gameworld):

    hero_panel_displayed = True

    hp_def_fg = tcod.white
    hp_def_bg = tcod.dark_gray

    # gather player entity
    player_entity = MobileUtilities.get_player_entity(gameworld=gameworld)
    # update player derived attributes - do that here to allow for mid-turn changes
    MobileUtilities.calculate_derived_attributes(gameworld=gameworld, entity=player_entity)
    # generate new tcod.console
    hero_panel = tcod.console_new(constants.HERO_PANEL_WIDTH, constants.HERO_PANEL_HEIGHT)

    # get the length of the longest word used for the tabs
    maxtablength = calculate_max_tab_length()

    x_offset = 11

    # main loop whilst hero panel is displayed
    while hero_panel_displayed:
        draw_hero_panel_frame(hero_panel, maxtablength)
        draw_hero_panel_tabs(hero_panel, maxtablength, hp_def_fg, hp_def_bg)
        draw_hero_information(hero_panel=hero_panel, gameworld=gameworld, player=player_entity)

        tcod.console_blit(hero_panel, 0, 0,
                          constants.HERO_PANEL_WIDTH,
                          constants.HERO_PANEL_HEIGHT,
                          0,
                          constants.HERO_PANEL_LEFT_X,
                          constants.HERO_PANEL_LEFT_Y)
        tcod.console_flush()
        for event in tcod.event.wait():
            if event.type == 'KEYDOWN':
                if event.sym == tcod.event.K_ESCAPE:
                    hero_panel_displayed = False
            elif event.type == "MOUSEBUTTONDOWN":
                x = event.tile.x
                y = event.tile.y
                if y in constants.HERO_PANEL_TAB_OFFSETS:
                    if x_offset <= x <= (x_offset + maxtablength):
                        ret_value = constants.HERO_PANEL_TAB_OFFSETS.index(y)
                        constants.HERO_PANEL_SELECTED_TAB = ret_value

        hero_panel.clear(ch=ord(' '), fg=hp_def_fg, bg=hp_def_bg)


def calculate_max_tab_length():
    maxtablength = 0
    tab_count = 0
    for mytab in constants.HERO_PANEL_TABS:
        tab_count += 1
        if len(mytab) > maxtablength:
            maxtablength = len(mytab)

    return maxtablength


def draw_hero_panel_frame(hero_panel, maxtablength):
    hero_panel.draw_frame(x=0, y=0,
                          width=constants.HERO_PANEL_WIDTH,
                          height=constants.HERO_PANEL_HEIGHT,
                          clear=False,
                          bg_blend=tcod.BKGND_DEFAULT,
                          title='Hero Panel')

    hero_panel.print_box(x=maxtablength + 15, y=hero_panel.height - 2,
                         width=40,
                         height=1, string='Mouse to select, ESC to exit')


def draw_hero_panel_tabs(hero_panel, maxtablength, def_fg, def_bg):
    tab_down = 3
    # def_fg = tcod.white
    # def_bg = tcod.grey

    # full length line
    hero_panel.draw_rect(x=maxtablength + 1, y=1, width=1, height=hero_panel.height - 2, ch=179, fg=def_fg, bg=def_bg)
    # top bar decoration
    hero_panel.put_char(x=maxtablength + 1, y=0, ch=194)
    # bottom bar decoration
    hero_panel.put_char(x=maxtablength + 1, y=hero_panel.height - 1, ch=193)
    for tab_count, tab in enumerate(constants.HERO_PANEL_TABS):
        if tab_down == 3:
            # tab cross bar
            hero_panel.draw_rect(x=1, y=tab_down, width=maxtablength, height=1, ch=196, fg=def_fg, bg=def_bg)
            # tab cross bar top decoration
            hero_panel.put_char(x=maxtablength + 1, y=tab_down, ch=180)
            hero_panel.put_char(x=0, y=tab_down, ch=195)
            tab_down += 1
        if constants.HERO_PANEL_SELECTED_TAB != tab_count:

            hero_panel.print_box(x=1, y=tab_down, width=maxtablength, height=1, string=tab)
            hero_panel.draw_rect(x=1, y=tab_down, width=maxtablength, height=1, ch=0, fg=tcod.white, bg=def_bg)
            tab_down += 1
            # tab cross bar
            hero_panel.draw_rect(x=1, y=tab_down, width=maxtablength, height=1, ch=196, fg=def_fg, bg=def_bg)
            # tab cross bar top decoration
            hero_panel.put_char(x=maxtablength + 1, y=tab_down, ch=180)
            # left side tab cross bar decoration
            hero_panel.put_char(x=0, y=tab_down, ch=195)
            tab_down += 1

        else:
            hero_panel.print_box(x=1, y=tab_down, width=maxtablength, height=1, string=tab)
            hero_panel.draw_rect(x=1, y=tab_down, width=maxtablength, height=1, ch=0, fg=def_fg, bg=tcod.black)
            # draws the 'space' at the end of the tab
            hero_panel.put_char(x=maxtablength + 1, y=tab_down, ch=32)
            tab_down += 1
            # tab cross bar
            hero_panel.draw_rect(x=1, y=tab_down, width=maxtablength, height=1, ch=196, fg=def_fg, bg=def_bg)
            # tab cross bar bottom right decoration
            hero_panel.put_char(x=maxtablength + 1, y=tab_down, ch=191)
            # tab cross bar top right decoration
            hero_panel.put_char(x=maxtablength + 1, y=tab_down - 2, ch=217)
            # left side tab cross bar decoration
            hero_panel.put_char(x=0, y=tab_down, ch=195)

            tab_down += 1


def draw_hero_information(hero_panel, gameworld, player):
    if constants.HERO_PANEL_SELECTED_TAB == 0:
        equipment_tab(hero_panel=hero_panel, gameworld=gameworld, player=player)
    elif constants.HERO_PANEL_SELECTED_TAB == 1:
        personal_tab(hero_panel=hero_panel, gameworld=gameworld, player=player)
    elif constants.HERO_PANEL_SELECTED_TAB == 2:
        current_build_tab(hero_panel=hero_panel, gameworld=gameworld, player=player)
    elif constants.HERO_PANEL_SELECTED_TAB == 3:
        weapons_tab(hero_panel=hero_panel, gameworld=gameworld, player=player)
    else:
        inventory_tab(hero_panel=hero_panel, gameworld=gameworld, player=player)


def equipment_tab(hero_panel, gameworld, player):

    hero_panel.print_box(x=constants.HERO_PANEL_INFO_DEF_X, y=constants.HERO_PANEL_INFO_DEF_Y, width=constants.HERO_PANEL_INFO_WIDTH, height=1, string="Equipment:")


def personal_tab(hero_panel, gameworld, player):

    player_power = MobileUtilities.get_mobile_power(gameworld=gameworld, entity=player)
    player_precision = MobileUtilities.get_mobile_precision(gameworld=gameworld, entity=player)
    player_toughness = MobileUtilities.get_mobile_toughness(gameworld=gameworld, entity=player)
    player_vitality = MobileUtilities.get_mobile_vitality(gameworld=gameworld, entity=player)
    player_concentration = MobileUtilities.get_mobile_concentration(gameworld=gameworld, entity=player)
    player_condi_damage = MobileUtilities.get_mobile_condition_damage(gameworld=gameworld, entity=player)
    player_expertise = MobileUtilities.get_mobile_expertise(gameworld=gameworld, entity=player)
    player_ferocity = MobileUtilities.get_mobile_ferocity(gameworld=gameworld, entity=player)
    player_healing_power = MobileUtilities.get_mobile_healing_power(gameworld=gameworld, entity=player)
    player_armour = MobileUtilities.get_derived_armour_value(gameworld=gameworld, entity=player)
    player_boon_duration = MobileUtilities.get_derived_boon_duration(gameworld=gameworld, entity=player)
    player_description = MobileUtilities.describe_the_mobile(gameworld, player)
    player_personality_title = MobileUtilities.get_mobile_personality_title(gameworld=gameworld, entity=player)

    player_critical_chance = MobileUtilities.get_derived_critical_hit_chance(gameworld=gameworld, entity=player)
    player_critical_damage = MobileUtilities.get_derived_critical_damage(gameworld=gameworld, entity=player)
    player_condi_duration = MobileUtilities.get_derived_condition_duration(gameworld=gameworld, entity=player)
    player_max_health = MobileUtilities.get_derived_maximum_health(gameworld=gameworld, entity=player)
    player_current_health = MobileUtilities.get_derived_current_health(gameworld=gameworld, entity=player)

    player_current_mana = MobileUtilities.get_derived_current_mana(gameworld=gameworld, entity=player)
    player_maximum_mana = MobileUtilities.get_derived_maximum_mana(gameworld=gameworld, entity=player)

    hero_panel.print_box(x=constants.HERO_PANEL_LEFT_COL, y=constants.HERO_PANEL_INFO_DEF_Y,
                      width=len(player_description), height=1, string=player_description)
    hero_panel.print_box(x=constants.HERO_PANEL_LEFT_COL, y=constants.HERO_PANEL_INFO_DEF_Y + 1,
                      width=len("who is known for being " + player_personality_title + "."), height=1,
                      string="who is known for being " + player_personality_title.lower() + ".")

    display_coloured_box(console=hero_panel, title="Primary Attributes",
                         posx=constants.HERO_PANEL_LEFT_COL,
                         posy=constants.HERO_PANEL_INFO_DEF_Y + 4,
                         width=24,
                         height=8,
                         fg=tcod.white,
                         bg=tcod.darker_gray)

    hero_panel.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 6,
                      width=len("Power:" + str(player_power)), height=1,
                      string="Power:" + str(player_power))

    hero_panel.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 7,
                      width=len("Precision:" + str(player_precision)), height=1,
                      string="Precision:" + str(player_precision))
    hero_panel.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 8,
                      width=len("Toughness:" + str(player_toughness)), height=1,
                      string="Toughness:" + str(player_toughness))
    hero_panel.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 9,
                      width=len("Vitality:" + str(player_vitality)), height=1,
                      string="Vitality:" + str(player_vitality))

    display_coloured_box(console=hero_panel, title="Secondary Attributes",
                         posx=constants.HERO_PANEL_LEFT_COL,
                         posy=constants.HERO_PANEL_INFO_DEF_Y + 12,
                         width=24,
                         height=10,
                         fg=tcod.white,
                         bg=tcod.dark_gray)

    hero_panel.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 14,
                      width=constants.HERO_PANEL_INFO_WIDTH, height=1,
                      string="Concentration:" + str(player_concentration))
    hero_panel.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 15,
                      width=constants.HERO_PANEL_INFO_WIDTH, height=1,
                      string="Condition Damage:" + str(player_condi_damage))
    hero_panel.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 16,
                      width=constants.HERO_PANEL_INFO_WIDTH, height=1,
                      string="Expertise:" + str(player_expertise))
    hero_panel.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 17,
                      width=constants.HERO_PANEL_INFO_WIDTH, height=1,
                      string="Ferocity:" + str(player_ferocity))
    hero_panel.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 18,
                      width=constants.HERO_PANEL_INFO_WIDTH, height=1,
                      string="Healing Power:" + str(player_healing_power))

    display_coloured_box(console=hero_panel, title="Derived Attributes",
                         posx=constants.HERO_PANEL_LEFT_COL,
                         posy=constants.HERO_PANEL_INFO_DEF_Y + 22,
                         width=24,
                         height=9,
                         fg=tcod.white,
                         bg=tcod.grey)

    hero_panel.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 24,
                      width=constants.HERO_PANEL_INFO_WIDTH,
                      height=1, string="Armour:" + str(player_armour))
    hero_panel.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 25,
                      width=constants.HERO_PANEL_INFO_WIDTH, height=1,
                      string="Boon Duration:" + str(player_boon_duration))
    hero_panel.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 26,
                      width=constants.HERO_PANEL_INFO_WIDTH, height=1,
                      string="Critical Chance:" + str(player_critical_chance) + '%')
    hero_panel.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 27,
                      width=constants.HERO_PANEL_INFO_WIDTH, height=1,
                      string="Critical Damage:" + str(player_critical_damage) + '%')
    hero_panel.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 28,
                      width=constants.HERO_PANEL_INFO_WIDTH,
                      height=1, string="Condition Duration:" + str(player_condi_duration))

    health_percent = MobileUtilities.get_number_as_a_percentage(player_current_health, player_max_health)
    health_string = 'Health at ' + str(health_percent) + '%'

    hero_panel.print_box(x=constants.HERO_PANEL_RIGHT_COL + 7, y=constants.HERO_PANEL_INFO_DEF_Y + 4,
                      width=len(health_string), height=1,
                      string=health_string)

    health_bar_count = int(health_percent / 10)
    draw_bar(hero_panel, constants.HERO_PANEL_RIGHT_COL + 7, constants.HERO_PANEL_INFO_DEF_Y + 5,
             tcod.white, tcod.lighter_green, tcod.dark_green, health_bar_count)

    mana_percent = MobileUtilities.get_number_as_a_percentage(player_current_mana, player_maximum_mana)
    mana_string = 'Mana at ' + str(mana_percent) + '%'

    hero_panel.print_box(x=constants.HERO_PANEL_RIGHT_COL + 7, y=constants.HERO_PANEL_INFO_DEF_Y +7,
                      width=len(mana_string), height=1,
                      string=mana_string)

    mana_bar_count = int(mana_percent / 10)
    draw_bar(hero_panel, constants.HERO_PANEL_RIGHT_COL + 7, constants.HERO_PANEL_INFO_DEF_Y + 8,
             tcod.white, tcod.lighter_blue, tcod.dark_blue, mana_bar_count)


def draw_bar(hero_panel, posx, posy, fg, bg, bg_break, break_point):
    for a in range(10):
        if a <= break_point:
            hero_panel.print(x=posx + a, y=posy,
                          string=chr(175), fg=fg, bg=bg)
        else:
            hero_panel.print(x=constants.HERO_PANEL_RIGHT_COL + 7 + a, y=constants.HERO_PANEL_INFO_DEF_Y + 8,
                          string=chr(175), fg=fg, bg=bg_break)


def current_build_tab(hero_panel, gameworld, player):

    # gather current set of: spells, equipped armour, weapons, jewellery
    # this creates a list of entities, i.e. weapons that are equipped in main hand, off hand, both hands
    weapons_equipped_list = MobileUtilities.get_weapons_equipped(gameworld=gameworld, entity=player)
    main_hand_weapon_entity = weapons_equipped_list[0]
    off_hand_weapon_entity = weapons_equipped_list[1]
    both_hands_weapon_entity = weapons_equipped_list[2]

    # gather armour being worn
    head_armour = MobileUtilities.is_entity_wearing_head_armour(gameworld=gameworld, entity=player)
    chest_armour = MobileUtilities.is_entity_wearing_chest_armour(gameworld=gameworld, entity=player)
    legs_armour = MobileUtilities.is_entity_wearing_legs_armour(gameworld=gameworld, entity=player)
    feet_armour = MobileUtilities.is_entity_wearing_feet_armour(gameworld=gameworld, entity=player)
    hands_armour= MobileUtilities.is_entity_wearing_hands_armour(gameworld=gameworld, entity=player)

    head_armour_display = ''

    if head_armour == 0:
        head_armour_display = 'None'
    else:
        am_set_name = ItemUtilities.get_armour_set_name(gameworld=gameworld, entity=head_armour)
        am_quality_level = ItemUtilities.get_item_quality(gameworld=gameworld, entity=head_armour)
        am_weight = ItemUtilities.get_armour_piece_weight(gameworld=gameworld, entity=head_armour)
        am_defense_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, body_location=head_armour)

        if am_set_name != '':
            head_armour_display = '(' + am_set_name + ') '

        if am_quality_level != '':
            head_armour_display += am_quality_level + ' '

        if am_weight != '':
            head_armour_display += am_weight + ' '

        if am_defense_value != 0:
            head_armour_display += str(am_defense_value)

    # gather jewellery being worn


    # gather current stats

    # display current set of equipped weapons
    box_height = 5
    weapon_display_string = []

    if both_hands_weapon_entity != 0:
        box_height = 5
        both_weapon_display_name = ItemUtilities.get_item_name(gameworld=gameworld, entity=both_hands_weapon_entity)
        weapon_display_string.append(both_weapon_display_name + ' is in both hands.')
    if main_hand_weapon_entity != 0:
        main_weapon_display_name =ItemUtilities.get_item_name(gameworld=gameworld, entity=main_hand_weapon_entity)
        box_height = 6
        weapon_display_string.append(main_weapon_display_name + ' is in the main hand')
    if off_hand_weapon_entity != 0:
        off_weapon_display_name = ItemUtilities.get_item_name(gameworld=gameworld, entity=off_hand_weapon_entity)
        weapon_display_string.append(off_weapon_display_name + ' is in the off hand')
        if box_height == 6:
            box_height = 7
        else:
            box_height = 6

    display_coloured_box(console=hero_panel, title="Equipped Weapons",
                         posx=constants.HERO_PANEL_LEFT_COL,
                         posy=constants.HERO_PANEL_INFO_DEF_Y,
                         width=30,
                         height=box_height,
                         fg=tcod.white,
                         bg=tcod.dark_gray)
    cnt = 2
    for wpn in weapon_display_string:
        hero_panel.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + cnt,
                      width=40,
                      height=1, string=wpn)
        cnt += 1

    # display equipped armour
    armcnt = cnt + 3
    display_coloured_box(console=hero_panel, title="Equipped Armour",
                         posx=constants.HERO_PANEL_LEFT_COL,
                         posy=constants.HERO_PANEL_INFO_DEF_Y + armcnt,
                         width=30,
                         height=10,
                         fg=tcod.white,
                         bg=tcod.dark_gray)

    hero_panel.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + armcnt + 2,
                      width=40,
                      height=1, string='Head ' + head_armour_display)
    hero_panel.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + armcnt + 3,
                      width=40,
                      height=1, string='Chest')
    hero_panel.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + armcnt + 4,
                      width=40,
                      height=1, string='Hands')
    hero_panel.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + armcnt + 5,
                      width=40,
                      height=1, string='Legs')
    hero_panel.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + armcnt + 6,
                      width=40,
                      height=1, string='Feet')

    # display current set of equipped Jewellery
    jcnt = armcnt + 10
    display_coloured_box(console=hero_panel, title="Equipped Jewellery",
                         posx=constants.HERO_PANEL_LEFT_COL,
                         posy=constants.HERO_PANEL_INFO_DEF_Y + jcnt,
                         width=30,
                         height=10,
                         fg=tcod.white,
                         bg=tcod.dark_gray)

    hero_panel.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + jcnt + 2,
                      width=40,
                      height=1, string='Left Ear')
    hero_panel.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + jcnt + 3,
                      width=40,
                      height=1, string='Right Ear')
    hero_panel.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + jcnt + 4,
                      width=40,
                      height=1, string='Left Hand')
    hero_panel.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + jcnt + 5,
                      width=40,
                      height=1, string='Right Hand')

    hero_panel.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + jcnt + 6,
                      width=40,
                      height=1, string='Neck')

    # display current set of stats


def weapons_tab(hero_panel, gameworld, player):

    hero_panel.print_box(x=constants.HERO_PANEL_INFO_DEF_X, y=constants.HERO_PANEL_INFO_DEF_Y, width=constants.HERO_PANEL_INFO_WIDTH, height=1, string="Weapons:" )


def inventory_tab(hero_panel, gameworld, player):

    # temp solution until I sort out how to store a dictionary of items in bags
    mobile_inventory_component = gameworld.component_for_entity(player, mobiles.Inventory)
    letter_index = 97
    bar_width = 15
    frame_left = 12
    frame_down = 5
    frame_width = 25
    iy = frame_down + 1
    key_pos = frame_left
    glyph_pos = frame_left + 2
    desc_pos = frame_left + 4
    def_fg = tcod.white
    def_bg = tcod.darker_gray
    def_wd = tcod.blue
    across_pipe = 196
    bottom_left = 192
    bottom_right = 217
    bottom_tee = 193
    down_pipe = 179
    left_tee = 195
    right_tee = 180
    top_left = 218
    top_tee = 194
    top_right = 191
    cross_pipe = 197

    inventory_items = mobile_inventory_component.items
    if len(inventory_items) != 0:
        max_lines = len(inventory_items) * 2
        # draw surrounding frame
        # left vertical line
        hero_panel.draw_rect(x=frame_left, y=frame_down, width=1, height=max_lines, ch=down_pipe, fg=def_fg,
                             bg=def_bg)
        # right vertical line
        hero_panel.draw_rect(x=frame_left + frame_width - 1, y=frame_down, width=1, height=max_lines, ch=down_pipe,
                             fg=def_fg, bg=def_bg)
        # top horizontal line
        hero_panel.draw_rect(x=frame_left, y=frame_down, width=frame_width, height=1, ch=across_pipe, fg=def_fg,
                             bg=def_bg)
        # bottom horizontal line
        hero_panel.draw_rect(x=frame_left, y=frame_down + max_lines, width=frame_width, height=1, ch=across_pipe,
                             fg=def_fg, bg=def_bg)
        # top left
        hero_panel.print(x=frame_left, y=frame_down, string=chr(top_left), fg=def_fg, bg=def_bg)
        # hero_panel.put_char(x=frame_left, y=frame_down, ch=top_left)

        # top right
        hero_panel.print(x=frame_left + frame_width - 1, y=frame_down, string=chr(top_right), fg=def_fg, bg=def_bg)
        # hero_panel.put_char(x=frame_left + frame_width - 1, y=frame_down, ch=top_right)

        # bottom left
        hero_panel.print(x=frame_left, y=frame_down + max_lines, string=chr(bottom_left), fg=def_fg, bg=def_bg)
        # hero_panel.put_char(x=frame_left, y=frame_down + max_lines, ch=bottom_left)

        # bottom right
        hero_panel.print(x=frame_left + frame_width - 1, y=frame_down + max_lines, string=chr(bottom_right), fg=def_fg, bg=def_bg)
        # hero_panel.put_char(x=frame_left + frame_width - 1, y=frame_down + max_lines, ch=bottom_right)

        z = frame_down + 2
        cnt = 1
        if max_lines > 2:
            for i in range(len(inventory_items)):
                hero_panel.draw_rect(x=frame_left+1, y=z, width=frame_width - 2, height=1, ch=across_pipe, fg=def_fg, bg=def_bg)

                if cnt < len(inventory_items):
                    hero_panel.print(x=frame_left, y=z, string=chr(left_tee), fg=def_fg, bg=def_bg)
                    # hero_panel.put_char(x=frame_left, y=z, ch=left_tee)
                    hero_panel.print(x=frame_left + frame_width - 1, y=z, string=chr(right_tee), fg=def_fg, bg=def_bg)
                    # hero_panel.put_char(x=frame_left + frame_width - 1, y=z, ch=right_tee)
                else:
                    hero_panel.print(x=frame_left, y=z, string=chr(bottom_left), fg=def_fg, bg=def_bg)
                    # hero_panel.put_char(x=frame_left, y=z, ch=bottom_left)
                    hero_panel.print(x=frame_left + frame_width - 1, y=z, string=chr(bottom_right), fg=def_fg, bg=def_bg)
                    # hero_panel.put_char(x=frame_left + frame_width - 1, y=z, ch=bottom_right)

                z += 2
                cnt += 1
        zz = 1
        for item in inventory_items:

            item_glyph = ItemUtilities.get_item_glyph(gameworld=gameworld, entity=item)
            item_name = ItemUtilities.get_item_displayname(gameworld=gameworld, entity=item)
            item_fg = ItemUtilities.get_item_fg_colour(gameworld=gameworld, entity=item)
            item_bg = ItemUtilities.get_item_bg_colour(gameworld=gameworld, entity=item)
            item_quality = ItemUtilities.get_item_quality(gameworld=gameworld, entity=item)

            # KEY
            hero_panel.print(x=key_pos + 1, y=iy, string=chr(letter_index), fg=def_wd, bg=None)
            # hero_panel.put_char(x=key_pos + 1, y=iy, ch=letter_index)
            hero_panel.print(x=key_pos + 2, y=iy, string=chr(down_pipe), fg=def_fg, bg=def_bg)
            # hero_panel.put_char(x=key_pos + 2, y=iy, ch=down_pipe)
            if zz == 1:
                hero_panel.print(x=key_pos + 2, y=iy - 1, string=chr(top_tee), fg=def_fg, bg=def_bg)
                # hero_panel.put_char(x=key_pos + 2, y=iy - 1, ch=top_tee)

            if zz < len(inventory_items):
                hero_panel.print(x=key_pos + 2, y=iy + 1, string=chr(cross_pipe), fg=def_fg, bg=def_bg)
                # hero_panel.put_char(x=key_pos + 2, y=iy + 1, ch=cross_pipe)
            else:
                hero_panel.print(x=key_pos + 2, y=iy + 1, string=chr(bottom_tee), fg=def_fg, bg=def_bg)
                # hero_panel.put_char(x=key_pos + 2, y=iy + 1, ch=bottom_tee)

            # GLYPH
            hero_panel.print(x=glyph_pos + 1, y=iy, string=item_glyph, fg=item_fg, bg=item_bg)
            # hero_panel.put_char(x=glyph_pos + 1, y=iy, ch=item_glyph)
            hero_panel.print(x=glyph_pos + 2, y=iy, string=chr(down_pipe), fg=def_fg, bg=def_bg)
            # hero_panel.put_char(x=glyph_pos + 2, y=iy, ch=down_pipe)
            if zz == 1:
                hero_panel.print(x=glyph_pos + 2, y=iy - 1, string=chr(top_tee), fg=def_fg, bg=def_bg)
                # hero_panel.put_char(x=glyph_pos + 2, y=iy - 1, ch=top_tee)

            if zz < len(inventory_items):
                hero_panel.print(x=glyph_pos + 2, y=iy + 1, string=chr(cross_pipe), fg=def_fg, bg=def_bg)
                # hero_panel.put_char(x=glyph_pos + 2, y=iy + 1, ch=cross_pipe)
            else:
                hero_panel.print(x=glyph_pos + 2, y=iy + 1, string=chr(bottom_tee), fg=def_fg, bg=def_bg)
                # hero_panel.put_char(x=glyph_pos + 2, y=iy + 1, ch=bottom_tee)

            # DESCRIPTION
            hero_panel.print(x=desc_pos + 1, y=iy, string=item_name, fg=def_wd, bg=None)
            # hero_panel.print_box(x=desc_pos + 1, y=iy, width=bar_width, height=1, string=item_name)
            # QUALITY

            letter_index += 1
            iy += 2
            zz += 1
    else:
        hero_panel.print_box(x=key_pos, y=iy, width=40, height=1, string='Nothing in Inventory')

