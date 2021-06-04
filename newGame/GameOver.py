from bearlibterminal import terminal
from loguru import logger

from utilities import configUtilities, common, display, input_handlers, itemsHelp, mobileHelp, scorekeeper, externalfileutilities


class GameOver:

    @staticmethod
    def process_game_over(player_died, gameworld):
        game_config = configUtilities.load_config()
        player_entity = mobileHelp.MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
        player_class = mobileHelp.MobileUtilities.get_character_class(gameworld=gameworld, entity=player_entity)
        game_version = configUtilities.get_config_value_as_string(configfile=game_config, section='default',
                                                                  parameter='VERSION')
        dump_meta_data = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_DUMP_META_DATA')

        dump_scores = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_DUMP_SCORES')
        visible_panel = 0
        terminal.clear()

        # temporary code to generate test data
        if dump_meta_data == 1:
            scorekeeper.ScorekeeperUtilities.set_current_area(gameworld=gameworld, current_area_tag='dg1')
            scorekeeper.ScorekeeperUtilities.set_current_area(gameworld=gameworld, current_area_tag='dg2')
            scorekeeper.ScorekeeperUtilities.set_current_area(gameworld=gameworld, current_area_tag='dg3')
            meta_events = scorekeeper.ScorekeeperUtilities.get_list_of_meta_events(gameworld=gameworld)
            logger.warning('list of meta events:{}', meta_events)

        scorekeeper.ScorekeeperUtilities.build_scorecard(gameworld=gameworld, game_version=game_version, player_class=player_class, dump_scores=dump_scores)

        GameOver.display_game_over_screen(game_config=game_config)
        GameOver.display_killed_by_information(game_config=game_config, death_status=player_died)
        GameOver.display_equipment_panels(gameworld=gameworld, game_config=game_config, visible_panel=visible_panel, player_entity=player_entity)
        GameOver.display_applied_status_effects(gameworld=gameworld, game_config=game_config, player_entity=player_entity)
        GameOver.display_end_game_key_statistics(gameworld=gameworld, game_config=game_config)
        terminal.refresh()
        valid_event = False
        while not valid_event:
            event_to_be_processed, event_action = input_handlers.handle_game_keys()
            if event_action == 'quit':
                valid_event = True
            if event_action == 'A':
                visible_panel = 0
            if event_action == 'J':
                visible_panel = 1
            if event_action == 'W':
                visible_panel = 2

            GameOver.display_equipment_panels(gameworld=gameworld, game_config=game_config, visible_panel=visible_panel, player_entity=player_entity)
            terminal.refresh()

    @staticmethod
    def display_end_game_key_statistics(gameworld, game_config):
        stat_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_STATS_POS_X')
        stat_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_STATS_POS_Y')

        stat_value_x = stat_x + 30
        stats_text_colour = '[font=dungeon][color=GO_STATS_TEXT_COLOUR]'
        stats_text_info = '[font=dungeon][color=GO_STATS_TEXT_INFO]'
        stats_text_controls = '[font=dungeon][color=GO_STATS_TEXT_CONTROLS]'
        stats_text_controls_keys= '[font=dungeon][color=GO_STATS_TAB_SELECTED]'

        display.draw_simple_frame(start_panel_frame_x=stat_x - 5, start_panel_frame_y=stat_y - 3, start_panel_frame_width=43, start_panel_frame_height=23, title='[[ Stats Summary ]]')

        current_turn = scorekeeper.ScorekeeperUtilities.get_meta_event_value(gameworld=gameworld, event_name='game_turn')
        terminal.print_(x=stat_x, y=stat_y + 2, s=stats_text_colour + 'Turns Completed')
        terminal.print_(x=stat_value_x, y=stat_y + 2, s=str(current_turn))
        terminal.print_(x=stat_x, y=stat_y + 3, s=stats_text_colour + 'Total Enemies Killed')
        terminal.print_(x=stat_value_x, y=stat_y + 3, s=str(current_turn))
        terminal.print_(x=stat_x, y=stat_y + 4, s=stats_text_colour + 'Total Spells Cast')
        terminal.print_(x=stat_value_x, y=stat_y + 4, s=str(current_turn))
        terminal.print_(x=stat_x, y=stat_y + 5, s=stats_text_colour + 'Highest Spell Damage')
        terminal.print_(x=stat_value_x, y=stat_y + 5, s=str(current_turn))
        terminal.print_(x=stat_x, y=stat_y + 6, s=stats_text_colour + 'Total Damage Inflicted')
        terminal.print_(x=stat_value_x, y=stat_y + 6, s=str(current_turn))
        terminal.print_(x=stat_x, y=stat_y + 7, s=stats_text_colour + 'Total Damage Received')
        terminal.print_(x=stat_value_x, y=stat_y + 7, s=str(current_turn))
        terminal.print_(x=stat_x, y=stat_y + 8, s=stats_text_colour + 'Dungeons Visited')
        terminal.print_(x=stat_value_x, y=stat_y + 8, s=str(current_turn))

        # further direction for the player
        terminal.print_(x=stat_x, y=stat_y + 12, s=stats_text_controls_keys + '[[ESCAPE]] ' + stats_text_controls + 'TO QUIT ' + stats_text_controls_keys + '[[ENTER]] ' + stats_text_controls + 'FOR NEW GAME')
        terminal.print_(x=stat_x, y=stat_y + 15, s=stats_text_info + 'Full stats can be found in /scores')

    @staticmethod
    def display_game_over_screen(game_config):
        banner_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                               parameter='GO_BANNER_POS_X')
        banner_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                               parameter='GO_BANNER_POS_Y')

        terminal.printf(x=banner_x, y=banner_y,
                        s=" ██████╗  █████╗ ███╗   ███╗███████╗   █████╗ ██╗   ██╗███████╗██████╗ ")
        terminal.printf(x=banner_x, y=banner_y + 1,
                        s="██╔════╝ ██╔══██╗████╗ ████║██╔════╝  ██╔══██╗██║   ██║██╔════╝██╔══██╗")
        terminal.printf(x=banner_x, y=banner_y + 2,
                        s="██║  ██╗ ███████║██╔████╔██║█████╗    ██║  ██║╚██╗ ██╔╝█████╗  ██████╔╝")
        terminal.printf(x=banner_x, y=banner_y + 3,
                        s="██║  ╚██╗██╔══██║██║╚██╔╝██║██╔══╝    ██║  ██║ ╚████╔╝ ██╔══╝  ██╔══██╗")
        terminal.printf(x=banner_x, y=banner_y + 4,
                        s="╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗  ╚█████╔╝  ╚██╔╝  ███████╗██║  ██║")
        terminal.printf(x=banner_x, y=banner_y + 5,
                        s=" ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝   ╚════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝")

    @staticmethod
    def display_killed_by_information(game_config, death_status):
        killed_by_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_KILLED_BY_X')
        killed_by_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_KILLED_BY_Y')
        died_when_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_WHEN_DIED_X')
        died_when_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_WHEN_DIED_Y')

        # the thing that killed the player
        if death_status:
            terminal.printf(x=killed_by_x, y=killed_by_y, s='You died of poisoning!')
        else:
            terminal.printf(x=killed_by_x, y=killed_by_y, s='You quit.')

        # at the time of your death
        terminal.printf(x=died_when_x, y=died_when_y, s='At the time of your death...')

    @staticmethod
    def display_applied_status_effects(gameworld, game_config, player_entity):
        condi_print_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_CONDI_X')
        condi_print_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_CONDI_Y')
        boon_print_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_BOON_X')
        boon_print_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_BOON_Y')

        # condis attached
        condi_string = GameOver.format_condi_string(gameworld=gameworld, player_entity=player_entity)
        terminal.printf(x=condi_print_x, y=condi_print_y, s=condi_string)

        # boons attached
        boon_string = GameOver.format_boon_string(gameworld=gameworld, player_entity=player_entity)

        terminal.printf(x=boon_print_x, y=boon_print_y, s=boon_string)

    @staticmethod
    def display_equipment_panels(gameworld, game_config, visible_panel, player_entity):
        unicode_string_to_print = '[font=dungeon][color=MSGPANEL_FRAME_COLOUR]['
        ascii_prefix = 'ASCII_SINGLE_'
        equipment_panel_width = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                            section='gameOver',
                                                                            parameter='GO_EQUIP_PANEL_WIDTH')
        equipment_panel_depth = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                            section='gameOver',
                                                                            parameter='GO_EQUIP_PANEL_DEPTH')

        equipment_panel_start_x = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                              section='gameOver',
                                                                              parameter='GO_EQUIP_PANEL_START_X')

        equipment_panel_start_y = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                              section='gameOver',
                                                                              parameter='GO_EQUIP_PANEL_START_Y')

        equipment_panel_top_left_corner = common.CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                           parameter=ascii_prefix + 'TOP_LEFT')

        equipment_panel_bottom_left_corner = common.CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                              parameter=ascii_prefix + 'BOTTOM_LEFT')

        equipment_panel_top_right_corner = common.CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                            parameter=ascii_prefix + 'TOP_RIGHT')

        equipment_panel_bottom_right_corner = common.CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                               parameter=ascii_prefix + 'BOTTOM_RIGHT')

        equipment_panel_horizontal = common.CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                      parameter=ascii_prefix + 'HORIZONTAL')
        equipment_panel_vertical = common.CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                    parameter=ascii_prefix + 'VERTICAL')
        equipment_panel_left_junction = common.CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                         parameter=ascii_prefix + 'LEFT_T_JUNCTION')
        equipment_panel_right_junction = common.CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                          parameter=ascii_prefix + 'RIGHT_T_JUNCTION')
        equipment_panel_top_junction = common.CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                        parameter=ascii_prefix + 'TOP_T_JUNCTION')
        equipment_panel_bottom_junction = common.CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                           parameter=ascii_prefix + 'BOTTOM_T_JUNCTION')
        tabs_to_display = configUtilities.get_config_value_as_list(configfile=game_config, section='gameOver',
                                                                   parameter='GO_EQUIP_PANEL_TABS')

        equipment_panel_item_x = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                             section='gameOver',
                                                                             parameter='GO_EQUIP_ITEM_X')
        equipment_panel_item_y = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                             section='gameOver',
                                                                             parameter='GO_EQUIP_ITEM_Y')

        tab_pos_x = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                section='gameOver',
                                                                parameter='GO_EQUIP_TAB_X')

        tab_length = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                 section='gameOver',
                                                                 parameter='GO_EQUIP_TAB_WIDTH')

        equipped_armour = mobileHelp.MobileUtilities.get_full_armourset_ids_from_entity(gameworld=gameworld, entity=player_entity)
        equipped_jewellery = mobileHelp.MobileUtilities.get_jewellery_already_equipped(gameworld=gameworld, mobile=player_entity)
        equipped_weapons = mobileHelp.MobileUtilities.get_weapons_equipped(gameworld=gameworld, entity=player_entity)

        # Armour / Jewellery / Weapons panel

        # draw message panel boundary
        # top left
        terminal.printf(x=equipment_panel_start_x, y=equipment_panel_start_y,
                        s=unicode_string_to_print + equipment_panel_top_left_corner + ']')

        # horizontals
        for z in range(equipment_panel_start_x + 1, (equipment_panel_start_x + equipment_panel_width)):
            terminal.printf(x=z, y=equipment_panel_start_y,
                            s=unicode_string_to_print + equipment_panel_horizontal + ']')
            terminal.printf(x=z, y=equipment_panel_start_y + 2,
                            s=unicode_string_to_print + equipment_panel_horizontal + ']')
            terminal.printf(x=z, y=(equipment_panel_start_y + equipment_panel_depth),
                            s=unicode_string_to_print + equipment_panel_horizontal + ']')
        # top right
        terminal.printf(x=equipment_panel_start_x + equipment_panel_width, y=equipment_panel_start_y,
                        s=unicode_string_to_print + equipment_panel_top_right_corner + ']')

        # verticals
        for z in range(equipment_panel_depth):
            terminal.printf(x=equipment_panel_start_x, y=(equipment_panel_start_y + z) + 1,
                            s=unicode_string_to_print + equipment_panel_vertical + ']')
            terminal.printf(x=equipment_panel_start_x + equipment_panel_width, y=(equipment_panel_start_y + z) + 1,
                            s=unicode_string_to_print + equipment_panel_vertical + ']')

        # left junction for tab bar
        terminal.printf(x=equipment_panel_start_x, y=equipment_panel_start_y + 2,
                        s=unicode_string_to_print + equipment_panel_left_junction + ']')

        # right junction for tab bar
        terminal.printf(x=equipment_panel_start_x + equipment_panel_width, y=equipment_panel_start_y + 2,
                        s=unicode_string_to_print + equipment_panel_right_junction + ']')

        # bottom left
        terminal.printf(x=equipment_panel_start_x, y=(equipment_panel_start_y + equipment_panel_depth),
                        s=unicode_string_to_print + equipment_panel_bottom_left_corner + ']')

        # bottom right
        terminal.printf(x=equipment_panel_start_x + equipment_panel_width,
                        y=(equipment_panel_start_y + equipment_panel_depth),
                        s=unicode_string_to_print + equipment_panel_bottom_right_corner + ']')

        # build the tabs
        not_selected_tab_colour = '[font=dungeon][color=GO_STATS_TAB_NOT_SELECTED]'
        selected_tab_color = '[font=dungeon][color=GO_STATS_TAB_SELECTED]'
        for tab in range(len(tabs_to_display)):
            if tab != visible_panel:
                str_to_print = not_selected_tab_colour + tabs_to_display[tab]
            else:
                str_to_print = selected_tab_color + tabs_to_display[tab]

            terminal.printf(x=tab_pos_x, y=equipment_panel_start_y + 1, s=str_to_print)
            if tab > 0:
                terminal.printf(x=tab_pos_x - 1, y=equipment_panel_start_y + 1,
                                s=unicode_string_to_print + equipment_panel_vertical + ']')
                terminal.printf(x=tab_pos_x - 1, y=equipment_panel_start_y,
                                s=unicode_string_to_print + equipment_panel_top_junction + ']')
                terminal.printf(x=tab_pos_x - 1, y=equipment_panel_start_y + 2,
                                s=unicode_string_to_print + equipment_panel_bottom_junction + ']')

            tab_pos_x += tab_length
        terminal.printf(x=tab_pos_x - 1, y=equipment_panel_start_y + 1,
                        s=unicode_string_to_print + equipment_panel_vertical + ']')
        terminal.printf(x=tab_pos_x - 1, y=equipment_panel_start_y,
                        s=unicode_string_to_print + equipment_panel_top_junction + ']')
        terminal.printf(x=tab_pos_x - 1, y=equipment_panel_start_y + 2,
                        s=unicode_string_to_print + equipment_panel_bottom_junction + ']')
        GameOver.ep_tab_display(visible_panel=visible_panel, unicode_string_to_print=unicode_string_to_print,
                                message_panel_vertical=equipment_panel_vertical,
                                message_panel_bottom_left_corner=equipment_panel_bottom_left_corner,
                                message_panel_bottom_right_corner=equipment_panel_bottom_right_corner)

        # display items
        GameOver.display_equipment(visible_panel=visible_panel, equipment_panel_item_x=equipment_panel_item_x,
                                   equipment_panel_item_y=equipment_panel_item_y, equipped_armour=equipped_armour,
                                   equipped_jewellery=equipped_jewellery, equipped_weapons=equipped_weapons,
                                   gameworld=gameworld)

    @staticmethod
    def format_condi_string(gameworld, player_entity):
        current_condis = mobileHelp.MobileUtilities.get_current_condis_applied_to_mobile(gameworld=gameworld, entity=player_entity)
        condi_string = 'You were suffering from '
        if len(current_condis) > 0:
            for condi in range(len(current_condis)):
                if (condi + 1) < len(current_condis):
                    condi_string += current_condis['name'] + ', '
                else:
                    condi_string += 'and ' + current_condis[condi] + '.'
        else:
            condi_string += 'no conditions, lucky you!'

        return condi_string

    @staticmethod
    def format_boon_string(gameworld, player_entity):
        current_boons = mobileHelp.MobileUtilities.get_current_boons_applied_to_mobile(gameworld=gameworld, entity=player_entity)
        boon_string = 'You benefited from '
        if len(current_boons) > 0:
            for boon in range(len(current_boons)):
                if (boon + 1) < len(current_boons):
                    boon_string += current_boons['name'] + ', '
                else:
                    boon_string += 'and ' + current_boons[boon] + '.'
        else:
            boon_string += 'absolutely nothing.'

        return boon_string

    @staticmethod
    def display_equipment(visible_panel, equipment_panel_item_x, equipment_panel_item_y, equipped_armour, equipped_jewellery, equipped_weapons, gameworld):
        posy = equipment_panel_item_y
        string_space = ' ' * 30
        for _ in range(5):
            terminal.print_(x=equipment_panel_item_x, y=posy, s=string_space)
            posy += 1
        if visible_panel == 0:
            GameOver.display_equipped_armour(posx=equipment_panel_item_x, posy=equipment_panel_item_y, equipped_armour=equipped_armour, gameworld=gameworld)
        if visible_panel == 1:
            GameOver.display_equipped_jewellery(posx=equipment_panel_item_x, posy=equipment_panel_item_y, equipped_jewellery=equipped_jewellery, gameworld=gameworld)

        if visible_panel == 2:
            GameOver.display_equipped_weapons(posx=equipment_panel_item_x, posy=equipment_panel_item_y, equipped_weapons=equipped_weapons, gameworld=gameworld)

    @staticmethod
    def display_equipped_armour(posx, posy, equipped_armour, gameworld):
        if equipped_armour.count(0) != 5:
            for armour_entity in range(len(equipped_armour)):
                armour_piece_name = itemsHelp.ItemUtilities.get_item_displayname(gameworld=gameworld, entity=equipped_armour[armour_entity])
                terminal.print_(x=posx, y=posy, s=armour_piece_name)
                posy += 1
        else:
            terminal.print_(x=posx, y=posy, s='No armour equipped')

    @staticmethod
    def display_equipped_jewellery(posx, posy, equipped_jewellery, gameworld):
        if equipped_jewellery.count(0) != 5:
            for jewellery_entity in range(len(equipped_jewellery)):
                jewellery_piece_name = itemsHelp.ItemUtilities.get_item_displayname(gameworld=gameworld,
                                                                       entity=equipped_jewellery[jewellery_entity])
                terminal.print_(x=posx, y=posy, s=jewellery_piece_name)
                posy += 1
        else:
            terminal.print_(x=posx, y=posy, s='No jewellery equipped')

    @staticmethod
    def display_equipped_weapons(posx, posy, equipped_weapons, gameworld):
        if equipped_weapons.count(0) != 3:
            for weapon_entity in range(len(equipped_weapons)):
                if equipped_weapons[weapon_entity] > 0:
                    weapon_piece_name = itemsHelp.ItemUtilities.get_item_displayname(gameworld=gameworld,
                                                                           entity=equipped_weapons[weapon_entity])

                    terminal.print_(x=posx, y=posy, s=weapon_piece_name)
                    posy += 1
        else:
            terminal.print_(x=posx, y=posy, s='No weapons equipped')

    @staticmethod
    def ep_tab_display(visible_panel, unicode_string_to_print, message_panel_vertical, message_panel_bottom_left_corner, message_panel_bottom_right_corner):
        if visible_panel == 0:
            terminal.clear_area(3, 22, 14, 1)
            terminal.printf(x=3, y=22, s=unicode_string_to_print + message_panel_vertical + ']')
            terminal.printf(x=16, y=22, s=unicode_string_to_print + message_panel_bottom_left_corner + ']')

        if visible_panel == 1:
            terminal.clear_area(17, 22, 12, 1)
            terminal.printf(x=16, y=22, s=unicode_string_to_print + message_panel_bottom_right_corner + ']')
            terminal.printf(x=28, y=22, s=unicode_string_to_print + message_panel_bottom_left_corner + ']')

        if visible_panel == 2:
            terminal.clear_area(29, 22, 12, 1)
            terminal.printf(x=28, y=22, s=unicode_string_to_print + message_panel_bottom_right_corner + ']')
            terminal.printf(x=40, y=22, s=unicode_string_to_print + message_panel_bottom_left_corner + ']')


