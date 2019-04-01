import tcod.event

from newGame import constants
from utilities.mobileHelp import MobileUtilities
from utilities.display import display_coloured_box
from loguru import logger


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
    y_offset = 8

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
                if (x_offset <= x <= (x_offset + maxtablength)) and (y_offset <= y < (y_offset + tab_count)):
                    ret_value = y - 8
                    selected_tab = ret_value
                logger.info('Tile x/y: {}/{}', x,y)
                logger.info('Menu option: {}', selected_tab)

        hero_panel.clear(ch=ord(' '), fg=tcod.white, bg=tcod.grey)


def draw_hero_panel_tabs(hero_panel, maxtablength, selected_tab, gameworld, player_entity):
    tab_down = 3
    for tab_count, tab in enumerate(constants.HERO_PANEL_TABS):
        if selected_tab == tab_count:
            hero_panel.print_box(x=1, y=tab_down, width=maxtablength, height=1, string=tab)
            hero_panel.draw_rect(x=1, y=tab_down, width=maxtablength, height=1, ch=0, fg=tcod.black, bg=tcod.grey)
        else:
            hero_panel.print_box(x=1, y=tab_down, width=maxtablength, height=1, string=tab)
            hero_panel.draw_rect(x=1, y=tab_down, width=maxtablength, height=1, ch=0, fg=tcod.white, bg=tcod.grey)
        tab_down += 1
        draw_hero_information(hero_panel=hero_panel, selected_tab=selected_tab, gameworld=gameworld, player=player_entity)

    tab_draw_pos = (3 + selected_tab)
    hero_panel.draw_rect(x=maxtablength + 1, y=1, width=1, height=hero_panel.height - 2, ch=ord("|"), fg=tcod.white, bg=tcod.grey)
    hero_panel.draw_rect(x=maxtablength + 1, y=tab_draw_pos, width=1, height=1, ch=ord(">"), fg=tcod.black, bg=tcod.grey)


def draw_hero_information(hero_panel, selected_tab, gameworld, player):
    if selected_tab == 0:
        equipment_tab(console=hero_panel)
    elif selected_tab == 1:
        personal_tab(console=hero_panel, gameworld=gameworld, player=player)
    elif selected_tab == 2:
        current_build_tab(console=hero_panel)
    else:
        story_tab(console=hero_panel)


def equipment_tab(console):
    width = 15

    console.print_box(x=constants.HERO_PANEL_INFO_DEF_X, y=constants.HERO_PANEL_INFO_DEF_Y, width=constants.HERO_PANEL_INFO_WIDTH, height=1, string="Power:")


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
    player_personality_title = MobileUtilities.get_player_personality_title(gameworld=gameworld, entity=player)

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
                      string="who is known for being " + player_personality_title + ".")

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
                         height=12,
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

    console.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 29,
                      width=constants.HERO_PANEL_INFO_WIDTH, height=1,
                      string="Max Health:" + str(player_max_health))
    console.print_box(x=constants.HERO_PANEL_LEFT_COL + 1, y=constants.HERO_PANEL_INFO_DEF_Y + 30,
                      width=constants.HERO_PANEL_INFO_WIDTH, height=1,
                      string="Current Health:" + str(player_current_health))

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


def current_build_tab(console):

    console.print_box(x=constants.HERO_PANEL_INFO_DEF_X, y=constants.HERO_PANEL_INFO_DEF_Y, width=constants.HERO_PANEL_INFO_WIDTH, height=1, string="Power:" )


def story_tab(console):

    console.print_box(x=constants.HERO_PANEL_INFO_DEF_X, y=constants.HERO_PANEL_INFO_DEF_Y, width=constants.HERO_PANEL_INFO_WIDTH, height=1, string="Power:" )
