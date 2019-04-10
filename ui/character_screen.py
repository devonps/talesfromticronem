import tcod.event

from newGame import constants
from utilities.mobileHelp import MobileUtilities
from utilities.display import display_coloured_box
from utilities.weaponHelp import WeaponUtilities
from utilities.armourHelp import ArmourUtilities
from components import bags


def display_hero_panel(con, key, mouse, gameworld):

    bg = tcod.grey
    hero_panel_displayed = True

    # gather player entity
    player_entity = MobileUtilities.get_player_entity(gameworld=gameworld)
    # update player derived attributes - do that here to allow for mid-turn changes
    MobileUtilities.calculate_derived_attributes(gameworld=gameworld, entity=player_entity)
    # generate new tcod.console
    hero_panel = tcod.console_new(constants.HERO_PANEL_WIDTH, constants.HERO_PANEL_HEIGHT)

    # get the length of the longest word used for the tabs
    maxtablength = 0
    tab_count = 0
    for mytab in constants.HERO_PANEL_TABS:
        tab_count += 1
        if len(mytab) > maxtablength:
            maxtablength = len(mytab)
    selected_tab = 1
    x_offset = 11
    y_offset = 9

    # main loop whilst hero panel is displayed
    while hero_panel_displayed:
        hero_panel.draw_frame(x=0, y=0,
                              width=constants.HERO_PANEL_WIDTH,
                              height=constants.HERO_PANEL_HEIGHT,
                              clear=False,
                              bg_blend=tcod.BKGND_DEFAULT,
                              title='Hero Panel')
        draw_hero_panel_tabs(hero_panel, maxtablength, selected_tab,
                             gameworld=gameworld, player_entity=player_entity)

        hero_panel.print_box(x=maxtablength + 15, y=hero_panel.height - 2,
                      width=40,
                      height=1, string='Mouse to select, ESC to exit')

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
                    # y_down = (y_offset + tab_count)
                    if x_offset <= x <= (x_offset + maxtablength):
                        ret_value = constants.HERO_PANEL_TAB_OFFSETS.index(y)
                        selected_tab = ret_value

        hero_panel.clear(ch=ord(' '), fg=tcod.white, bg=tcod.grey)


def draw_hero_panel_tabs(hero_panel, maxtablength, selected_tab, gameworld, player_entity):
    tab_down = 3
    tab_pos = 4
    def_fg = tcod.white

    # full length line
    hero_panel.draw_rect(x=maxtablength + 1, y=1, width=1, height=hero_panel.height - 2, ch=179, fg=def_fg, bg=tcod.grey)
    # top bar decoration
    hero_panel.put_char(x=maxtablength + 1, y=0, ch=194)
    # bottom bar decoration
    hero_panel.put_char(x=maxtablength + 1, y=hero_panel.height - 1, ch=193)
    for tab_count, tab in enumerate(constants.HERO_PANEL_TABS):
        if tab_down == 3:
            # tab cross bar
            hero_panel.draw_rect(x=1, y=tab_down, width=maxtablength, height=1, ch=196, fg=def_fg, bg=tcod.grey)
            # tab cross bar top decoration
            hero_panel.put_char(x=maxtablength + 1, y=tab_down, ch=180)
            hero_panel.put_char(x=0, y=tab_down, ch=195)
            tab_down += 1
        if selected_tab != tab_count:

            hero_panel.print_box(x=1, y=tab_down, width=maxtablength, height=1, string=tab)
            hero_panel.draw_rect(x=1, y=tab_down, width=maxtablength, height=1, ch=0, fg=tcod.white, bg=tcod.grey)
            tab_down += 1
            # tab cross bar
            hero_panel.draw_rect(x=1, y=tab_down, width=maxtablength, height=1, ch=196, fg=def_fg, bg=tcod.grey)
            # tab cross bar top decoration
            hero_panel.put_char(x=maxtablength + 1, y=tab_down, ch=180)
            # left side tab cross bar decoration
            hero_panel.put_char(x=0, y=tab_down, ch=195)
            tab_down += 1

        else:
            hero_panel.print_box(x=1, y=tab_down, width=maxtablength, height=1, string=tab)
            hero_panel.draw_rect(x=1, y=tab_down, width=maxtablength, height=1, ch=0, fg=tcod.white, bg=tcod.black)
            # draws the 'space' at the end of the tab
            hero_panel.put_char(x=maxtablength + 1, y=tab_down, ch=32)
            tab_down += 1
            # tab cross bar
            hero_panel.draw_rect(x=1, y=tab_down, width=maxtablength, height=1, ch=196, fg=def_fg, bg=tcod.grey)
            # tab cross bar bottom right decoration
            hero_panel.put_char(x=maxtablength + 1, y=tab_down, ch=191)
            # tab cross bar top right decoration
            hero_panel.put_char(x=maxtablength + 1, y=tab_down - 2, ch=217)
            # left side tab cross bar decoration
            hero_panel.put_char(x=0, y=tab_down, ch=195)

            tab_down += 1

        draw_hero_information(hero_panel=hero_panel, selected_tab=selected_tab, gameworld=gameworld, player=player_entity)


def draw_hero_information(hero_panel, selected_tab, gameworld, player):
    if selected_tab == 0:
        equipment_tab(console=hero_panel, gameworld=gameworld, player=player)
    elif selected_tab == 1:
        personal_tab(console=hero_panel, gameworld=gameworld, player=player)
    elif selected_tab == 2:
        current_build_tab(console=hero_panel, gameworld=gameworld, player=player)
    elif selected_tab == 3:
        weapons_tab(console=hero_panel, gameworld=gameworld, player=player)
    else:
        inventory_tab(console=hero_panel, gameworld=gameworld, player=player)


def equipment_tab(console, gameworld, player):

    console.print_box(x=constants.HERO_PANEL_INFO_DEF_X, y=constants.HERO_PANEL_INFO_DEF_Y, width=constants.HERO_PANEL_INFO_WIDTH, height=1, string="Equipment:")


def personal_tab(console, gameworld, player):

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

    console.print_box(x=constants.HERO_PANEL_LEFT_COL, y=constants.HERO_PANEL_INFO_DEF_Y,
                      width=len(player_description), height=1, string=player_description)
    console.print_box(x=constants.HERO_PANEL_LEFT_COL, y=constants.HERO_PANEL_INFO_DEF_Y + 1,
                      width=len("who is known for being " + player_personality_title + "."), height=1,
                      string="who is known for being " + player_personality_title.lower() + ".")

    display_coloured_box(console=console, title="Primary Attributes",
                         posx=constants.HERO_PANEL_LEFT_COL,
                         posy=constants.HERO_PANEL_INFO_DEF_Y + 4,
                         width=24,
                         height=8,
                         fg=tcod.white,
                         bg=tcod.darker_gray)

    console.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 6,
                      width=len("Power:" + str(player_power)), height=1,
                      string="Power:" + str(player_power))

    console.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 7,
                      width=len("Precision:" + str(player_precision)), height=1,
                      string="Precision:" + str(player_precision))
    console.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 8,
                      width=len("Toughness:" + str(player_toughness)), height=1,
                      string="Toughness:" + str(player_toughness))
    console.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 9,
                      width=len("Vitality:" + str(player_vitality)), height=1,
                      string="Vitality:" + str(player_vitality))

    display_coloured_box(console=console, title="Secondary Attributes",
                         posx=constants.HERO_PANEL_LEFT_COL,
                         posy=constants.HERO_PANEL_INFO_DEF_Y + 12,
                         width=24,
                         height=10,
                         fg=tcod.white,
                         bg=tcod.dark_gray)

    console.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 14,
                      width=constants.HERO_PANEL_INFO_WIDTH, height=1,
                      string="Concentration:" + str(player_concentration))
    console.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 15,
                      width=constants.HERO_PANEL_INFO_WIDTH, height=1,
                      string="Condition Damage:" + str(player_condi_damage))
    console.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 16,
                      width=constants.HERO_PANEL_INFO_WIDTH, height=1,
                      string="Expertise:" + str(player_expertise))
    console.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 17,
                      width=constants.HERO_PANEL_INFO_WIDTH, height=1,
                      string="Ferocity:" + str(player_ferocity))
    console.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 18,
                      width=constants.HERO_PANEL_INFO_WIDTH, height=1,
                      string="Healing Power:" + str(player_healing_power))

    display_coloured_box(console=console, title="Derived Attributes",
                         posx=constants.HERO_PANEL_LEFT_COL,
                         posy=constants.HERO_PANEL_INFO_DEF_Y + 22,
                         width=24,
                         height=9,
                         fg=tcod.white,
                         bg=tcod.grey)

    console.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 24,
                      width=constants.HERO_PANEL_INFO_WIDTH,
                      height=1, string="Armour:" + str(player_armour))
    console.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 25,
                      width=constants.HERO_PANEL_INFO_WIDTH, height=1,
                      string="Boon Duration:" + str(player_boon_duration))
    console.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 26,
                      width=constants.HERO_PANEL_INFO_WIDTH, height=1,
                      string="Critical Chance:" + str(player_critical_chance) + '%')
    console.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 27,
                      width=constants.HERO_PANEL_INFO_WIDTH, height=1,
                      string="Critical Damage:" + str(player_critical_damage) + '%')
    console.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 28,
                      width=constants.HERO_PANEL_INFO_WIDTH,
                      height=1, string="Condition Duration:" + str(player_condi_duration))

    health_percent = MobileUtilities.get_number_as_a_percentage(player_current_health, player_max_health)
    health_string = 'Health at ' + str(health_percent) + '%'

    console.print_box(x=constants.HERO_PANEL_RIGHT_COL + 7, y=constants.HERO_PANEL_INFO_DEF_Y + 4,
                      width=len(health_string), height=1,
                      string=health_string)

    health_bar_count = int(health_percent / 10)
    for a in range(10):
        if a <= health_bar_count:
            console.print(x=constants.HERO_PANEL_RIGHT_COL + 7 + a, y=constants.HERO_PANEL_INFO_DEF_Y + 5,
                          string=chr(175), fg=tcod.white, bg=tcod.lighter_green)
        else:
            console.print(x=constants.HERO_PANEL_RIGHT_COL + 7 + a, y=constants.HERO_PANEL_INFO_DEF_Y + 5,
                          string=chr(175), fg=tcod.white, bg=tcod.dark_green)

    mana_percent = MobileUtilities.get_number_as_a_percentage(player_current_mana, player_maximum_mana)
    mana_string = 'Mana at ' + str(mana_percent) + '%'

    console.print_box(x=constants.HERO_PANEL_RIGHT_COL + 7, y=constants.HERO_PANEL_INFO_DEF_Y +7,
                      width=len(mana_string), height=1,
                      string=mana_string)
    mana_bar_count = int(mana_percent / 10)
    for a in range(10):
        if a <= mana_bar_count:
            console.print(x=constants.HERO_PANEL_RIGHT_COL + 7 + a, y=constants.HERO_PANEL_INFO_DEF_Y + 8,
                          string=chr(175), fg=tcod.white, bg=tcod.lighter_blue)
        else:
            console.print(x=constants.HERO_PANEL_RIGHT_COL + 7 + a, y=constants.HERO_PANEL_INFO_DEF_Y + 8,
                          string=chr(175), fg=tcod.white, bg=tcod.dark_blue)


def current_build_tab(console, gameworld, player):

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
        am_set_name = ArmourUtilities.get_armour_set_name(gameworld=gameworld, entity=head_armour)
        am_quality_level = ArmourUtilities.get_armour_quality_level(gameworld=gameworld, entity=head_armour)
        am_weight = ArmourUtilities.get_armour_piece_weight(gameworld=gameworld, entity=head_armour)
        am_defense_value = ArmourUtilities.get_armour_defense_value(gameworld=gameworld, body_location=head_armour)

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
        both_weapon_display_name = WeaponUtilities.get_weapon_display_name(gameworld=gameworld, entity=both_hands_weapon_entity)
        weapon_display_string.append(both_weapon_display_name + ' is in both hands.')
    if main_hand_weapon_entity != 0:
        main_weapon_display_name = WeaponUtilities.get_weapon_display_name(gameworld=gameworld, entity=main_hand_weapon_entity)
        box_height = 6
        weapon_display_string.append(main_weapon_display_name + ' is in the main hand')
    if off_hand_weapon_entity != 0:
        off_weapon_display_name = WeaponUtilities.get_weapon_display_name(gameworld=gameworld, entity=off_hand_weapon_entity)
        weapon_display_string.append(off_weapon_display_name + ' is in the off hand')
        if box_height == 6:
            box_height = 7
        else:
            box_height = 6

    display_coloured_box(console=console, title="Equipped Weapons",
                         posx=constants.HERO_PANEL_LEFT_COL,
                         posy=constants.HERO_PANEL_INFO_DEF_Y,
                         width=30,
                         height=box_height,
                         fg=tcod.white,
                         bg=tcod.dark_gray)
    cnt = 2
    for wpn in weapon_display_string:
        console.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + cnt,
                      width=40,
                      height=1, string=wpn)
        cnt += 1

    # display equipped armour
    armcnt = cnt + 3
    display_coloured_box(console=console, title="Equipped Armour",
                         posx=constants.HERO_PANEL_LEFT_COL,
                         posy=constants.HERO_PANEL_INFO_DEF_Y + armcnt,
                         width=30,
                         height=10,
                         fg=tcod.white,
                         bg=tcod.dark_gray)

    console.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + armcnt + 2,
                      width=40,
                      height=1, string='Head ' + head_armour_display)
    console.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + armcnt + 3,
                      width=40,
                      height=1, string='Chest')
    console.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + armcnt + 4,
                      width=40,
                      height=1, string='Hands')
    console.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + armcnt + 5,
                      width=40,
                      height=1, string='Legs')
    console.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + armcnt + 6,
                      width=40,
                      height=1, string='Feet')

    # display current set of equipped Jewellery
    jcnt = armcnt + 10
    display_coloured_box(console=console, title="Equipped Jewellery",
                         posx=constants.HERO_PANEL_LEFT_COL,
                         posy=constants.HERO_PANEL_INFO_DEF_Y + jcnt,
                         width=30,
                         height=10,
                         fg=tcod.white,
                         bg=tcod.dark_gray)

    console.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + jcnt + 2,
                      width=40,
                      height=1, string='Left Ear')
    console.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + jcnt + 3,
                      width=40,
                      height=1, string='Right Ear')
    console.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + jcnt + 4,
                      width=40,
                      height=1, string='Left Hand')
    console.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + jcnt + 5,
                      width=40,
                      height=1, string='Right Hand')

    console.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + jcnt + 6,
                      width=40,
                      height=1, string='Neck')

    # display current set of stats


def weapons_tab(console, gameworld, player):

    console.print_box(x=constants.HERO_PANEL_INFO_DEF_X, y=constants.HERO_PANEL_INFO_DEF_Y, width=constants.HERO_PANEL_INFO_WIDTH, height=1, string="Weapons:" )


def inventory_tab(console, gameworld, player):
    start_y = 3
    ac = 10
    w = 6
    def_fg = tcod.white
    selected_inv_bag = 0
    # cross bar
    console.draw_rect(x=ac, y=start_y, width=w, height=1, ch=196, fg=def_fg, bg=tcod.grey)
    console.put_char(x=ac, y=start_y, ch=197)
    console.put_char(x=ac + 5, y=start_y, ch=191)
    console.print_box(x=ac + 1, y=start_y + 1, width=4, height=1, string="Bags")
    console.put_char(x=ac + 5, y=start_y + 1, ch=179)
    # cross bar
    console.draw_rect(x=ac, y=start_y + 2, width=w, height=1, ch=196, fg=def_fg, bg=tcod.grey)
    console.put_char(x=ac, y=start_y + 2, ch=197)
    console.put_char(x=ac + 5, y=start_y + 2, ch=180)

    bg_dwn = start_y + 3
    for bag_id in range(4):
        # bg id
        console.put_char(x=ac + 2, y=bg_dwn + bag_id, ch=49 + bag_id)
        console.put_char(x=ac + 5, y=bg_dwn + bag_id, ch=179)
        bg_dwn += 1
        # cross bar
        console.draw_rect(x=ac, y=bg_dwn + bag_id, width=w, height=1, ch=196, fg=def_fg, bg=tcod.grey)
        console.put_char(x=ac, y=bg_dwn + bag_id, ch=197)
        console.put_char(x=ac + 5, y=bg_dwn + bag_id, ch=180)
    console.put_char(x=ac + 5, y=bg_dwn + 3, ch=217)

# next up display the selected inventory bag slots
    inv_bag_max_slots = gameworld.component_for_entity(selected_inv_bag, bags.SlotSize).maxSize

    for slot_id in range(inv_bag_max_slots):



# then make the inventory numbers clickable
