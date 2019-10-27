import tcod.event
import tcod.console

from utilities.display import display_coloured_box, draw_simple_frame
from utilities.itemsHelp import ItemUtilities
from utilities import configUtilities, colourUtilities
from utilities.mobileHelp import MobileUtilities
from utilities.input_handlers import handle_game_keys
from loguru import logger

from components import mobiles

from bearlibterminal import terminal


def display_hero_panel(gameworld):

    hero_panel_displayed = True
    game_config = configUtilities.load_config()

    hp_def_fg = tcod.white
    hp_def_bg = tcod.dark_gray
    hp_tab_max_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='HERO_PANEL_TAB_MAX_WIDTH')
    hp_tabs = configUtilities.get_config_value_as_list(configfile=game_config, section='gui', parameter='HERO_PANEL_TAB_OFFSETS')

    hp_tabs_offsets = list(map(int, hp_tabs))

    # gather player entity
    player_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
    # update player derived attributes - do that here to allow for mid-turn changes
    MobileUtilities.calculate_derived_attributes(gameworld=gameworld, gameconfig=game_config)

    x_offset = 11

    # main loop whilst hero panel is displayed
    while hero_panel_displayed:
        terminal.clear()
        draw_hero_panel_frame(hero_panel, game_config)
        draw_hero_panel_tabs(hero_panel, game_config, hp_def_fg, hp_def_bg)
        draw_hero_information(hero_panel=hero_panel, gameworld=gameworld, player=player_entity, game_config=game_config)

        terminal.refresh()

        event_to_be_processed, event_action = handle_game_keys()
        if event_to_be_processed != '':
            if event_to_be_processed == 'keypress':
                if event_action == 'quit':
                    hero_panel_displayed = False

            if event_to_be_processed == 'mousebutton':
                if event_action[0] == 'left':
                    x = event_action[1]
                    y = event_action[2]
                    if y in hp_tabs_offsets:
                        if x_offset <= x <= (x_offset + hp_tab_max_width):
                            ret_value = hp_tabs_offsets.index(y)
                            configUtilities.write_config_value(configfile=game_config, section='gui', parameter='HERO_PANEL_SELECTED_TAB', value=str(ret_value))
                if event_action[0] == 'right':
                    logger.info('Right mouse button clicked')
                    logger.info('Tile coords {}/{}', event_action[1], event_action[2])

        terminal.clear()


def draw_hero_panel_frame(game_config):
    hp_tab_max_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='HERO_PANEL_TAB_MAX_WIDTH')
    panel_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='HERO_PANEL_WIDTH')
    panel_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='HERO_PANEL_HEIGHT')

    draw_simple_frame(startx=0, starty=0, width=panel_width,height=panel_height,title='Hero Panel', fg=colourUtilities.get('WHITE'), bg=colourUtilities.get('BLACK'))
    # hero_panel.draw_frame(x=0, y=0,
    #                       width=panel_width,
    #                       height=panel_height,
    #                       clear=False,
    #                       bg_blend=tcod.BKGND_DEFAULT,
    #                       title='Hero Panel')

    terminal.print_(x=hp_tab_max_width + 15, y=panel_height - 2,width=40,height=1, s='Mouse to select, ESC to exit')
    # hero_panel.print_box(x=hp_tab_max_width + 15, y=panel_height- 2,
    #                      width=40,
    #                      height=1, string='Mouse to select, ESC to exit')


def draw_hero_panel_tabs(game_config, def_fg, def_bg):
    hp_tab_max_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='HERO_PANEL_TAB_MAX_WIDTH')
    hp_selected_tab = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='HERO_PANEL_SELECTED_TAB')
    hp_tabs = configUtilities.get_config_value_as_list(configfile=game_config, section='gui', parameter='HERO_PANEL_TABS')
    hp_height = configUtilities.get_config_value_as_list(configfile=game_config, section='gui', parameter='HERO_PANEL_HEIGHT')

    tab_down = 3

    # full length line
    terminal.color(def_fg)
    for i in range(hp_height - 1):
        terminal.put(x=hp_tab_max_width + 1, y=1 + i, c=179)

    # hero_panel.draw_rect(x=hp_tab_max_width + 1, y=1, width=1, height=hero_panel.height - 2, ch=179, fg=def_fg, bg=def_bg)
    # top bar decoration
    terminal.put(x=hp_tab_max_width + 1, y=0, c=194)
    # hero_panel.put_char(x=hp_tab_max_width + 1, y=0, ch=194)
    # bottom bar decoration
    terminal.put(x=hp_tab_max_width + 1, y=hp_height - 1, c=193)
    # hero_panel.put_char(x=hp_tab_max_width + 1, y=hero_panel.height - 1, ch=193)
    # for tab_count, tab in enumerate(hp_tabs):
    #     if tab_down == 3:
    #         # tab cross bar
    #         hero_panel.draw_rect(x=1, y=tab_down, width=hp_tab_max_width, height=1, ch=196, fg=def_fg, bg=def_bg)
    #         # tab cross bar top decoration
    #         hero_panel.put_char(x=hp_tab_max_width + 1, y=tab_down, ch=180)
    #         hero_panel.put_char(x=0, y=tab_down, ch=195)
    #         tab_down += 1
    #     if hp_selected_tab != tab_count:
    #
    #         hero_panel.print_box(x=1, y=tab_down, width=hp_tab_max_width, height=1, string=tab)
    #         hero_panel.draw_rect(x=1, y=tab_down, width=hp_tab_max_width, height=1, ch=0, fg=tcod.white, bg=def_bg)
    #         tab_down += 1
    #         # tab cross bar
    #         hero_panel.draw_rect(x=1, y=tab_down, width=hp_tab_max_width, height=1, ch=196, fg=def_fg, bg=def_bg)
    #         # tab cross bar top decoration
    #         hero_panel.put_char(x=hp_tab_max_width + 1, y=tab_down, ch=180)
    #         # left side tab cross bar decoration
    #         hero_panel.put_char(x=0, y=tab_down, ch=195)
    #         tab_down += 1
    #
    #     else:
    #         hero_panel.print_box(x=1, y=tab_down, width=hp_tab_max_width, height=1, string=tab)
    #         hero_panel.draw_rect(x=1, y=tab_down, width=hp_tab_max_width, height=1, ch=0, fg=def_fg, bg=tcod.black)
    #         # draws the 'space' at the end of the tab
    #         hero_panel.put_char(x=hp_tab_max_width + 1, y=tab_down, ch=32)
    #         tab_down += 1
    #         # tab cross bar
    #         hero_panel.draw_rect(x=1, y=tab_down, width=hp_tab_max_width, height=1, ch=196, fg=def_fg, bg=def_bg)
    #         # tab cross bar bottom right decoration
    #         hero_panel.put_char(x=hp_tab_max_width + 1, y=tab_down, ch=191)
    #         # tab cross bar top right decoration
    #         hero_panel.put_char(x=hp_tab_max_width + 1, y=tab_down - 2, ch=217)
    #         # left side tab cross bar decoration
    #         hero_panel.put_char(x=0, y=tab_down, ch=195)
    #
    #         tab_down += 1


def draw_hero_information(hero_panel, gameworld, player, game_config):
    hp_selected_tab = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='HERO_PANEL_SELECTED_TAB')

    if hp_selected_tab == 0:
        tab_personal(hero_panel=hero_panel, gameworld=gameworld, player=player, game_config=game_config)
    elif hp_selected_tab == 1:
        tab_equipment(hero_panel=hero_panel, gameworld=gameworld, player=player, game_config=game_config)
    elif hp_selected_tab == 2:
        tab_inventory(hero_panel=hero_panel, gameworld=gameworld, player=player, game_config=game_config)
    elif hp_selected_tab == 3:
        tab_weapons(hero_panel=hero_panel, gameworld=gameworld, player=player, game_config=game_config)
    elif hp_selected_tab == 4:
        tab_utilities()
    elif hp_selected_tab == 5:
        tab_traits()
    else:
        tab_stats()


def tab_equipment(hero_panel, gameworld, player, game_config):
    hp_left_col = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='HERO_PANEL_LEFT_COL')
    hp_def_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='HERO_PANEL_INFO_DEF_Y')

    # gather current set of: spells, equipped armour, weapons, jewellery
    # this creates a list of entities, i.e. weapons that are equipped in main hand, off hand, both hands
    weapons_equipped_list = MobileUtilities.get_weapons_equipped(gameworld=gameworld, entity=player)
    main_hand_weapon_entity = weapons_equipped_list[0]
    off_hand_weapon_entity = weapons_equipped_list[1]
    both_hands_weapon_entity = weapons_equipped_list[2]

    # gather armour being worn
    head_armour_id = MobileUtilities.is_entity_wearing_head_armour(gameworld=gameworld, entity=player)
    chest_armour_id = MobileUtilities.is_entity_wearing_chest_armour(gameworld=gameworld, entity=player)
    legs_armour_id = MobileUtilities.is_entity_wearing_legs_armour(gameworld=gameworld, entity=player)
    feet_armour_id = MobileUtilities.is_entity_wearing_feet_armour(gameworld=gameworld, entity=player)
    hands_armour_id = MobileUtilities.is_entity_wearing_hands_armour(gameworld=gameworld, entity=player)

    head_armour_display = ''

    if head_armour_id == 0:
        head_armour_display = 'None'
    else:
        am_set_material = ItemUtilities.get_item_material(gameworld=gameworld, entity=head_armour_id)
        am_set_displayname = ItemUtilities.get_item_displayname(gameworld=gameworld, entity=head_armour_id)
        am_set_name = ItemUtilities.get_armour_set_name(gameworld=gameworld, entity=head_armour_id)
        am_quality_level = ItemUtilities.get_item_quality(gameworld=gameworld, entity=head_armour_id)
        am_weight = ItemUtilities.get_armour_piece_weight(gameworld=gameworld, entity=head_armour_id)
        am_defense_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, entity=head_armour_id)

        if am_set_name != '':
            head_armour_display = '(' + am_set_name + ') '

        if am_quality_level != '':
            head_armour_display += am_quality_level + ' '

        if am_weight != '':
            head_armour_display += am_weight + ' '

        if am_defense_value != 0:
            head_armour_display += str(am_defense_value)

    chest_armour_display = ''

    if chest_armour_id == 0:
        chest_armour_display = 'None'
    else:
        am_set_material = ItemUtilities.get_item_material(gameworld=gameworld, entity=chest_armour_id)
        am_set_displayname = ItemUtilities.get_item_displayname(gameworld=gameworld, entity=chest_armour_id)
        am_set_name = ItemUtilities.get_armour_set_name(gameworld=gameworld, entity=chest_armour_id)
        am_quality_level = ItemUtilities.get_item_quality(gameworld=gameworld, entity=chest_armour_id)
        am_weight = ItemUtilities.get_armour_piece_weight(gameworld=gameworld, entity=chest_armour_id)
        am_defense_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, entity=chest_armour_id)

        if am_set_name != '':
            chest_armour_display = '(' + am_set_name + ') '

        if am_quality_level != '':
            chest_armour_display += am_quality_level + ' '

        if am_weight != '':
            chest_armour_display += am_weight + ' '

        if am_defense_value != 0:
            chest_armour_display += str(am_defense_value)

    legs_armour_display = ''

    if legs_armour_id == 0:
        legs_armour_display = 'None'
    else:
        am_set_material = ItemUtilities.get_item_material(gameworld=gameworld, entity=legs_armour_id)
        am_set_displayname = ItemUtilities.get_item_displayname(gameworld=gameworld, entity=legs_armour_id)
        am_set_name = ItemUtilities.get_armour_set_name(gameworld=gameworld, entity=legs_armour_id)
        am_quality_level = ItemUtilities.get_item_quality(gameworld=gameworld, entity=legs_armour_id)
        am_weight = ItemUtilities.get_armour_piece_weight(gameworld=gameworld, entity=legs_armour_id)
        am_defense_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, entity=legs_armour_id)

        if am_set_name != '':
            legs_armour_display = '(' + am_set_name + ') '

        if am_quality_level != '':
            legs_armour_display += am_quality_level + ' '

        if am_weight != '':
            legs_armour_display += am_weight + ' '

        if am_defense_value != 0:
            legs_armour_display += str(am_defense_value)

    feet_armour_display = ''

    if feet_armour_id == 0:
        feet_armour_display = 'None'
    else:
        am_set_material = ItemUtilities.get_item_material(gameworld=gameworld, entity=feet_armour_id)
        am_set_displayname = ItemUtilities.get_item_displayname(gameworld=gameworld, entity=feet_armour_id)
        am_set_name = ItemUtilities.get_armour_set_name(gameworld=gameworld, entity=feet_armour_id)
        am_quality_level = ItemUtilities.get_item_quality(gameworld=gameworld, entity=feet_armour_id)
        am_weight = ItemUtilities.get_armour_piece_weight(gameworld=gameworld, entity=feet_armour_id)
        am_defense_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, entity=feet_armour_id)

        if am_set_name != '':
            feet_armour_display = '(' + am_set_name + ') '

        if am_quality_level != '':
            feet_armour_display += am_quality_level + ' '

        if am_weight != '':
            feet_armour_display += am_weight + ' '

        if am_defense_value != 0:
            feet_armour_display += str(am_defense_value)

    hands_armour_display = ''

    if hands_armour_id == 0:
        hands_armour_display = 'None'
    else:
        am_set_material = ItemUtilities.get_item_material(gameworld=gameworld, entity=hands_armour_id)
        am_set_displayname = ItemUtilities.get_item_displayname(gameworld=gameworld, entity=hands_armour_id)
        am_set_name = ItemUtilities.get_armour_set_name(gameworld=gameworld, entity=hands_armour_id)
        am_quality_level = ItemUtilities.get_item_quality(gameworld=gameworld, entity=hands_armour_id)
        am_weight = ItemUtilities.get_armour_piece_weight(gameworld=gameworld, entity=hands_armour_id)
        am_defense_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, entity=hands_armour_id)

        if am_set_name != '':
            hands_armour_display = '(' + am_set_name + ') '

        if am_quality_level != '':
            hands_armour_display += am_quality_level + ' '

        if am_weight != '':
            hands_armour_display += am_weight + ' '

        if am_defense_value != 0:
            hands_armour_display += str(am_defense_value)

    # gather jewellery being worn
    equippedJewellery = MobileUtilities.get_jewellery_already_equipped(gameworld=gameworld, mobile=player)
    left_ear = equippedJewellery[0]
    right_ear = equippedJewellery[1]
    left_hand = equippedJewellery[2]
    right_hand = equippedJewellery[3]
    neck = equippedJewellery[4]

    # display current set of equipped weapons
    box_height = 5
    weapon_display_string = []

    if both_hands_weapon_entity != 0:
        box_height = 5
        both_weapon_display_name = ItemUtilities.get_item_name(gameworld=gameworld, entity=both_hands_weapon_entity)
        weapon_display_string.append(both_weapon_display_name + ' is in both hands.')
    if main_hand_weapon_entity != 0:
        main_weapon_display_name = ItemUtilities.get_item_name(gameworld=gameworld, entity=main_hand_weapon_entity)
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
                         posx=hp_left_col,
                         posy=hp_def_y,
                         width=30,
                         height=box_height,
                         fg=tcod.white,
                         bg=tcod.dark_gray)
    cnt = 2
    for wpn in weapon_display_string:
        hero_panel.print_box(x=hp_left_col + 1, y=hp_def_y + cnt,
                      width=40,
                      height=1, string=wpn)
        cnt += 1

    # display equipped armour
    armcnt = cnt + 3
    display_coloured_box(console=hero_panel, title="Equipped Armour",
                         posx=hp_left_col,
                         posy=hp_def_y + armcnt,
                         width=30,
                         height=10,
                         fg=tcod.white,
                         bg=tcod.dark_gray)

    hero_panel.print_box(x=hp_left_col + 1, y=hp_def_y + armcnt + 2,
                      width=40,
                      height=1, string='Head ' + head_armour_display)
    hero_panel.print_box(x=hp_left_col + 1, y=hp_def_y + armcnt + 3,
                      width=40,
                      height=1, string='Chest ' + chest_armour_display)
    hero_panel.print_box(x=hp_left_col + 1, y=hp_def_y + armcnt + 4,
                      width=40,
                      height=1, string='Hands ' + hands_armour_display)
    hero_panel.print_box(x=hp_left_col + 1, y=hp_def_y + armcnt + 5,
                      width=40,
                      height=1, string='Legs ' + legs_armour_display)
    hero_panel.print_box(x=hp_left_col + 1, y=hp_def_y + armcnt + 6,
                      width=40,
                      height=1, string='Feet ' + feet_armour_display)

    # display current set of equipped Jewellery
    jcnt = armcnt + 10
    display_coloured_box(console=hero_panel, title="Equipped Jewellery",
                         posx=hp_left_col,
                         posy=hp_def_y + jcnt,
                         width=30,
                         height=10,
                         fg=tcod.white,
                         bg=tcod.dark_gray)

    hero_panel.print_box(x=hp_left_col + 1, y=hp_def_y + jcnt + 2,
                      width=40,
                      height=1, string='Left Ear ' + ItemUtilities.get_item_description(gameworld=gameworld, entity=left_ear))
    hero_panel.print_box(x=hp_left_col + 1, y=hp_def_y + jcnt + 3,
                      width=40,
                      height=1, string='Right Ear ' + ItemUtilities.get_item_description(gameworld=gameworld, entity=right_ear))
    hero_panel.print_box(x=hp_left_col + 1, y=hp_def_y + jcnt + 4,
                      width=40,
                      height=1, string='Left Hand ' + ItemUtilities.get_item_description(gameworld=gameworld, entity=left_hand))
    hero_panel.print_box(x=hp_left_col + 1, y=hp_def_y + jcnt + 5,
                      width=40,
                      height=1, string='Right Hand ' + ItemUtilities.get_item_description(gameworld=gameworld, entity=right_hand))

    hero_panel.print_box(x=hp_left_col + 1, y=hp_def_y + jcnt + 6,
                      width=40,
                      height=1, string='Neck ' + ItemUtilities.get_item_description(gameworld=gameworld, entity=neck))

    # display current set of stats


def tab_personal(hero_panel, gameworld, player, game_config):

    hp_left_col = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='HERO_PANEL_LEFT_COL')
    hp_right_col = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='HERO_PANEL_RIGHT_COL')
    hp_def_y= configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='HERO_PANEL_INFO_DEF_Y')
    hp_info_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',parameter='HERO_PANEL_INFO_WIDTH')

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

    hero_panel.print_box(x=hp_left_col, y=hp_def_y, width=len(player_description), height=1, string=player_description)
    hero_panel.print_box(x=hp_left_col, y=hp_def_y + 1,
                      width=len("who is known for being " + player_personality_title + "."), height=1,
                      string="who is known for being " + player_personality_title.lower() + ".")

    display_coloured_box(console=hero_panel, title="Primary Attributes",
                         posx=hp_left_col,
                         posy=hp_def_y + 4,
                         width=24,
                         height=8,
                         fg=tcod.white,
                         bg=tcod.darker_gray)

    hero_panel.print_box(x=hp_left_col + 1, y=hp_def_y + 6,width=len("Power:" + str(player_power)), height=1,string="Power:" + str(player_power))

    hero_panel.print_box(x=hp_left_col + 1, y=hp_def_y + 7,width=len("Precision:" + str(player_precision)), height=1,string="Precision:" + str(player_precision))
    hero_panel.print_box(x=hp_left_col + 1, y=hp_def_y + 8,width=len("Toughness:" + str(player_toughness)), height=1,string="Toughness:" + str(player_toughness))
    hero_panel.print_box(x=hp_left_col + 1, y=hp_def_y + 9,width=len("Vitality:" + str(player_vitality)), height=1,string="Vitality:" + str(player_vitality))

    display_coloured_box(console=hero_panel, title="Secondary Attributes",
                         posx=hp_left_col,
                         posy=hp_def_y + 12,
                         width=24,
                         height=10,
                         fg=tcod.white,
                         bg=tcod.dark_gray)

    hero_panel.print_box(x=hp_left_col + 1, y=hp_def_y + 14,width=hp_info_width, height=1,string="Concentration:" + str(player_concentration))
    hero_panel.print_box(x=hp_left_col + 1, y=hp_def_y + 15,width=hp_info_width, height=1,string="Condition Damage:" + str(player_condi_damage))
    hero_panel.print_box(x=hp_left_col + 1, y=hp_def_y + 16,width=hp_info_width, height=1,string="Expertise:" + str(player_expertise))
    hero_panel.print_box(x=hp_left_col + 1, y=hp_def_y + 17,width=hp_info_width, height=1,string="Ferocity:" + str(player_ferocity))
    hero_panel.print_box(x=hp_left_col + 1, y=hp_def_y + 18,width=hp_info_width, height=1,string="Healing Power:" + str(player_healing_power))

    display_coloured_box(console=hero_panel, title="Derived Attributes",
                         posx=hp_left_col,
                         posy=hp_def_y + 22,
                         width=24,
                         height=9,
                         fg=tcod.white,
                         bg=tcod.grey)

    hero_panel.print_box(x=hp_left_col + 1, y=hp_def_y + 24,width=hp_info_width, height=1, string="Armour:" + str(player_armour))
    hero_panel.print_box(x=hp_left_col + 1, y=hp_def_y + 25,width=hp_info_width, height=1, string="Boon Duration:" + str(player_boon_duration))
    hero_panel.print_box(x=hp_left_col + 1, y=hp_def_y + 26,width=hp_info_width, height=1,string="Critical Chance:" + str(player_critical_chance) + '%')
    hero_panel.print_box(x=hp_left_col + 1, y=hp_def_y + 27,width=hp_info_width, height=1,string="Critical Damage:" + str(player_critical_damage) + '%')
    hero_panel.print_box(x=hp_left_col + 1, y=hp_def_y + 28, width=hp_info_width,height=1, string="Condition Duration:" + str(player_condi_duration))

    health_percent = MobileUtilities.get_number_as_a_percentage(player_current_health, player_max_health)
    health_string = 'Health at ' + str(health_percent) + '%'

    hero_panel.print_box(x=hp_right_col + 7, y=hp_def_y + 4,width=len(health_string), height=1,string=health_string)

    health_bar_count = int(health_percent / 10)
    draw_bar(hero_panel, hp_right_col + 7, hp_def_y + 5,
             tcod.white, tcod.lighter_green, tcod.dark_green, health_bar_count, game_config)

    mana_percent = MobileUtilities.get_number_as_a_percentage(player_current_mana, player_maximum_mana)
    mana_string = 'Mana at ' + str(mana_percent) + '%'

    hero_panel.print_box(x=hp_right_col + 7, y=hp_def_y + 7, width=len(mana_string), height=1, string=mana_string)

    mana_bar_count = int(mana_percent / 10)
    draw_bar(hero_panel, hp_right_col + 7, hp_def_y + 8,
             tcod.white, tcod.lighter_blue, tcod.dark_blue, mana_bar_count, game_config)


def draw_bar(hero_panel, posx, posy, fg, bg, bg_break, break_point, game_config):
    hp_right_col = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',parameter='HERO_PANEL_RIGHT_COL')
    hp_def_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',parameter='HERO_PANEL_INFO_DEF_Y')

    for a in range(10):
        if a <= break_point:
            hero_panel.print(x=posx + a, y=posy, string=chr(175), fg=fg, bg=bg)
        else:
            hero_panel.print(x=hp_right_col + 7 + a, y=hp_def_y + 8, string=chr(175), fg=fg, bg=bg_break)


def tab_weapons(hero_panel, gameworld, player, game_config):

    hp_def_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='HERO_PANEL_INFO_DEF_X')
    hp_def_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='HERO_PANEL_INFO_DEF_Y')
    hp_info_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='HERO_PANEL_INFO_WIDTH')
    inv_wpn_list_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='weapons', parameter='HP_WPNS_LIST_X')
    inv_wpn_list_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='weapons', parameter='HP_WPNS_LIST_Y')
    inv_wpn_list_d = configUtilities.get_config_value_as_integer(configfile=game_config, section='weapons', parameter='HP_WPNS_LIST_D')
    inv_wpn_list_w = configUtilities.get_config_value_as_integer(configfile=game_config, section='weapons', parameter='HP_WPNS_LIST_W')

    hero_panel.print_box(x=hp_def_x, y=hp_def_y, width=hp_info_width, height=1, string="Weapons:")

    # list of weapons in inventory - need a call to something
    weapons_list_inventory = []
    mobile_inventory_component = gameworld.component_for_entity(player, mobiles.Inventory)
    inventory_items = mobile_inventory_component.items
    if len(inventory_items) != 0:
        items_weapons, cnt = populate_inv_lists(inventory_items, gameworld, 'weapon')

        if len(items_weapons) != 0:
            for weapon in items_weapons:
                weapons_list_inventory.append(weapon)
    # list of weapons equipped
    weapons_list_equipped = MobileUtilities.get_weapons_equipped(gameworld=gameworld, entity=player)
    main_hand_weapon_entity = weapons_list_equipped[0]
    off_hand_weapon_entity = weapons_list_equipped[1]
    both_hands_weapon_entity = weapons_list_equipped[2]

    click_zones = []
    dwn = inv_wpn_list_y

    if both_hands_weapon_entity != 0:
        both_weapon_display_name = ItemUtilities.get_item_name(gameworld=gameworld, entity=both_hands_weapon_entity)
        hero_panel.print(x=inv_wpn_list_x, y=dwn, string=both_weapon_display_name, fg=tcod.yellow, bg=None)
        click_zones.append((inv_wpn_list_x, inv_wpn_list_x + inv_wpn_list_w, dwn, dwn))
        dwn += 1

    if main_hand_weapon_entity != 0:
        main_weapon_display_name = ItemUtilities.get_item_name(gameworld=gameworld, entity=main_hand_weapon_entity)
        hero_panel.print(x=inv_wpn_list_x, y=dwn, string=main_weapon_display_name, fg=tcod.yellow, bg=None)
        click_zones.append((inv_wpn_list_x, inv_wpn_list_x + inv_wpn_list_w, dwn, dwn))

        dwn += 1

    if off_hand_weapon_entity != 0:
        off_weapon_display_name = ItemUtilities.get_item_name(gameworld=gameworld, entity=off_hand_weapon_entity)
        hero_panel.print(x=inv_wpn_list_x, y=dwn, string=off_weapon_display_name, fg=tcod.yellow, bg=None)
        click_zones.append((inv_wpn_list_x, inv_wpn_list_x + inv_wpn_list_w, dwn, dwn))

        dwn += 1

    for wpn in weapons_list_inventory:
        weapon_display_name = ItemUtilities.get_item_name(gameworld=gameworld, entity=wpn)
        hero_panel.print(x=inv_wpn_list_x, y=dwn, string=weapon_display_name, fg=tcod.yellow, bg=None)
        dwn += 1


def tab_inventory(hero_panel, gameworld, player, game_config):

    gui_frame = configUtilities.get_config_value_as_string(configfile=game_config, section='gui', parameter='frame_border_pipe_type')

    hp_def_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='HERO_PANEL_INFO_DEF_X')
    hp_def_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='HERO_PANEL_INFO_DEF_Y')
    hp_info_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='HERO_PANEL_INFO_WIDTH')
    left_tee = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',parameter='frame_' + gui_frame + '_left_tee')
    right_tee = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='frame_' + gui_frame + '_right_tee')
    bottom_tee = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='frame_' + gui_frame + '_bottom_tee')
    top_tee = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='frame_' + gui_frame + '_top_tee')
    cross_pipe = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='frame_' + gui_frame + '_cross_pipe')

    across_pipe = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='frame_' + gui_frame + '_across_pipe')
    bottom_left = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='frame_' + gui_frame + '_bottom_left')
    bottom_right = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='frame_' + gui_frame + '_bottom_right')
    down_pipe = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='frame_' + gui_frame + '_down_pipe')
    top_left = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='frame_' + gui_frame + '_top_left')
    top_right = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='frame_' + gui_frame + '_top_right')
    frame_left = configUtilities.get_config_value_as_integer(configfile=game_config, section='inv', parameter='INV_FRAME_LEFT')
    frame_down = configUtilities.get_config_value_as_integer(configfile=game_config, section='inv', parameter='inv_frame_down')
    frame_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='inv', parameter='inv_frame_width')
    inv_key_pos = configUtilities.get_config_value_as_integer(configfile=game_config, section='inv', parameter='inv_key_pos')
    inv_glyph_pos = configUtilities.get_config_value_as_integer(configfile=game_config, section='inv', parameter='inv_glyph_pos')
    inv_desc_pos = configUtilities.get_config_value_as_integer(configfile=game_config, section='inv', parameter='inv_desc_pos')
    inv_section_pos = configUtilities.get_config_value_as_integer(configfile=game_config, section='inv', parameter='inv_section_pos')
    # inv_actions = configUtilities.get_config_value_as_list(configfile=game_config, section='game', parameter='ITEM_INV_ACTIONS')

    # temp solution until I sort out how to store a dictionary of items in bags
    mobile_inventory_component = gameworld.component_for_entity(player, mobiles.Inventory)
    letter_index = 97
    iy = frame_down + 1
    def_fg = colourUtilities.WHITE  # tcod.white
    def_bg = colourUtilities.DARKGRAY  # tcod.darker_gray
    def_wd = colourUtilities.WHITE  # tcod.white

    inventory_items = mobile_inventory_component.items
    if len(inventory_items) != 0:
        max_lines = 2

        items_armour, cnt = populate_inv_lists(inventory_items, gameworld, 'armour')
        max_lines += cnt
        items_weapons, cnt = populate_inv_lists(inventory_items, gameworld, 'weapon')
        max_lines += cnt
        items_jewellery, cnt = populate_inv_lists(inventory_items, gameworld, 'jewellery')
        max_lines += cnt
        items_bags, cnt = populate_inv_lists(inventory_items, gameworld, 'bag')
        max_lines += cnt
        items_gemstones, cnt = populate_inv_lists(inventory_items, gameworld, 'gemstone')
        max_lines += cnt

        if len(items_armour) != 0:
            hero_panel.print_box(x=inv_section_pos, y=iy, width=15, height=1, string='Armour')
            iy += 1

            for armour in items_armour:
                item_glyph = ItemUtilities.get_item_glyph(gameworld=gameworld, entity=armour)
                item_name = ItemUtilities.get_item_displayname(gameworld=gameworld, entity=armour)
                item_fg = ItemUtilities.get_item_fg_colour(gameworld=gameworld, entity=armour)
                item_bg = ItemUtilities.get_item_bg_colour(gameworld=gameworld, entity=armour)

                # KEY
                hero_panel.print(x=inv_key_pos, y=iy, string=chr(letter_index), fg=def_wd, bg=None)
                # GLYPH
                hero_panel.print(x=inv_glyph_pos , y=iy, string=item_glyph, fg=item_fg, bg=item_bg)
                # DESCRIPTION
                hero_panel.print(x=inv_desc_pos, y=iy, string=item_name, fg=def_wd, bg=None)

                letter_index += 1
                iy += 1

        if len(items_weapons) != 0:
            hero_panel.print_box(x=inv_section_pos, y=iy, width=15, height=1, string='Weapons')
            iy += 1

            for weapon in items_weapons:
                item_glyph = ItemUtilities.get_item_glyph(gameworld=gameworld, entity=weapon)
                item_name = ItemUtilities.get_item_displayname(gameworld=gameworld, entity=weapon)
                item_fg = ItemUtilities.get_item_fg_colour(gameworld=gameworld, entity=weapon)
                item_bg = ItemUtilities.get_item_bg_colour(gameworld=gameworld, entity=weapon)

                # KEY
                hero_panel.print(x=inv_key_pos, y=iy, string=chr(letter_index), fg=def_wd, bg=None)
                # GLYPH
                hero_panel.print(x=inv_glyph_pos, y=iy, string=item_glyph, fg=item_fg, bg=item_bg)
                # DESCRIPTION
                hero_panel.print(x=inv_desc_pos, y=iy, string=item_name, fg=def_wd, bg=None)

                letter_index += 1
                iy += 1

        if len(items_jewellery) != 0:
            hero_panel.print_box(x=inv_section_pos, y=iy, width=15, height=1, string='Jewellery')
            iy += 1

            for jewellery in items_jewellery:
                item_glyph = ItemUtilities.get_item_glyph(gameworld=gameworld, entity=jewellery)
                item_name = ItemUtilities.get_item_displayname(gameworld=gameworld, entity=jewellery)
                item_fg = ItemUtilities.get_item_fg_colour(gameworld=gameworld, entity=jewellery)
                item_bg = ItemUtilities.get_item_bg_colour(gameworld=gameworld, entity=jewellery)

                # KEY
                hero_panel.print(x=inv_key_pos, y=iy, string=chr(letter_index), fg=def_wd, bg=None)
                # GLYPH
                hero_panel.print(x=inv_glyph_pos, y=iy, string=item_glyph, fg=item_fg, bg=item_bg)
                # DESCRIPTION
                hero_panel.print(x=inv_desc_pos, y=iy, string=item_name, fg=def_wd, bg=None)

                letter_index += 1
                iy += 1

        # draw surrounding frame
        # left vertical line
        hero_panel.draw_rect(x=frame_left, y=frame_down, width=1, height=max_lines, ch=down_pipe, fg=def_fg, bg=def_bg)
        # right vertical line
        hero_panel.draw_rect(x=frame_left + frame_width - 1, y=frame_down, width=1, height=max_lines, ch=down_pipe, fg=def_fg, bg=def_bg)
        # top horizontal line
        hero_panel.draw_rect(x=frame_left, y=frame_down, width=frame_width, height=1, ch=across_pipe, fg=def_fg, bg=def_bg)
        # top left
        hero_panel.print(x=frame_left, y=frame_down, string=chr(top_left), fg=def_fg, bg=def_bg)
        # top right
        hero_panel.print(x=frame_left + frame_width - 1, y=frame_down, string=chr(top_right), fg=def_fg, bg=def_bg)
        # bottom horizontal line
        hero_panel.draw_rect(x=frame_left, y=iy, width=frame_width, height=1, ch=across_pipe,fg=def_fg, bg=def_bg)
        # bottom left
        hero_panel.print(x=frame_left, y=iy, string=chr(bottom_left), fg=def_fg, bg=def_bg)
        # bottom right
        hero_panel.print(x=frame_left + frame_width - 1, y=iy, string=chr(bottom_right), fg=def_fg, bg=def_bg)
    else:
        hero_panel.print_box(x=inv_key_pos, y=iy, width=40, height=1, string='Nothing in Inventory')


def tab_utilities():
    pass


def tab_traits():
    pass


def tab_stats():
    pass


def populate_inv_lists(inventory_items, gameworld, item_type_in_inv):

    inv_items = []
    cnt = 0

    for item in inventory_items:
        item_type = ItemUtilities.get_item_type(gameworld=gameworld, entity=item)

        if item_type == item_type_in_inv:
            inv_items.append(item)
            if cnt == 0:
                cnt = 2
            else:
                cnt += 1

    return inv_items, cnt
