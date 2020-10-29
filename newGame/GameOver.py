from bearlibterminal import terminal
from loguru import logger

from utilities import configUtilities
from utilities.common import CommonUtils
from utilities.input_handlers import handle_game_keys
from utilities.itemsHelp import ItemUtilities
from utilities.mobileHelp import MobileUtilities
from utilities.scorekeeper import ScorekeeperUtilities


class GameOver:

    @staticmethod
    def process_game_over(player_died, gameworld):
        game_config = configUtilities.load_config()
        player_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
        visible_panel = 0
        terminal.clear()
        GameOver.display_game_over_screen(game_config=game_config)

        if player_died:
            logger.debug('Player Died - display Game Over Screen')
            GameOver.display_killed_by_information(game_config=game_config, gameworld=gameworld, player_entity=player_entity, visible_panel=visible_panel)
            GameOver.display_end_game_key_statistics(gameworld=gameworld, game_config=game_config)
        else:
            logger.debug('Player Quit - display something else')
            meta_events = ScorekeeperUtilities.get_list_of_meta_events(gameworld=gameworld)
            logger.warning('list of meta events:{}', meta_events)

        terminal.refresh()
        valid_event = False
        while not valid_event:
            event_to_be_processed, event_action = handle_game_keys()
            if event_action == 'quit':
                valid_event = True
            if event_action == 'A':
                visible_panel = 0
            if event_action == 'J':
                visible_panel = 1
            if event_action == 'W':
                visible_panel = 2

            GameOver.display_killed_by_information(game_config=game_config, gameworld=gameworld,
                                                   player_entity=player_entity, visible_panel=visible_panel)
            terminal.refresh()

    @staticmethod
    def display_end_game_key_statistics(gameworld, game_config):
        turn_killed_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_STATS_POS_X')
        turn_killed_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_STATS_POS_Y')

        current_turn = ScorekeeperUtilities.get_meta_event_value(gameworld=gameworld, event_name='game_turn')
        terminal.print_(x=turn_killed_x, y=turn_killed_y, s='You died on turn ' + str(current_turn))

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
    def display_killed_by_information(game_config, gameworld, player_entity, visible_panel):
        killed_by_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_KILLED_BY_X')
        killed_by_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_KILLED_BY_Y')
        died_when_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_WHEN_DIED_X')
        died_when_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_WHEN_DIED_Y')
        condi_print_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_CONDI_X')
        condi_print_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_CONDI_Y')
        boon_print_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_BOON_X')
        boon_print_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_BOON_Y')

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

        equipment_panel_top_left_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                         parameter=ascii_prefix + 'TOP_LEFT')

        equipment_panel_bottom_left_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                            parameter=ascii_prefix + 'BOTTOM_LEFT')

        equipment_panel_top_right_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                          parameter=ascii_prefix + 'TOP_RIGHT')

        equipment_panel_bottom_right_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                             parameter=ascii_prefix + 'BOTTOM_RIGHT')

        equipment_panel_horizontal = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                    parameter=ascii_prefix + 'HORIZONTAL')
        equipment_panel_vertical = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                  parameter=ascii_prefix + 'VERTICAL')
        equipment_panel_left_junction = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                       parameter=ascii_prefix + 'LEFT_T_JUNCTION')
        equipment_panel_right_junction = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                        parameter=ascii_prefix + 'RIGHT_T_JUNCTION')
        equipment_panel_top_junction = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                      parameter=ascii_prefix + 'TOP_T_JUNCTION')
        equipment_panel_bottom_junction = CommonUtils.get_ascii_to_unicode(game_config=game_config,
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

        equipped_armour = MobileUtilities.get_full_armourset_ids_from_entity(gameworld=gameworld, entity=player_entity)
        equipped_jewellery = MobileUtilities.get_jewellery_already_equipped(gameworld=gameworld, mobile=player_entity)
        equipped_weapons = MobileUtilities.get_weapons_equipped(gameworld=gameworld, entity=player_entity)

        # the thing that killed the player
        terminal.printf(x=killed_by_x, y=killed_by_y, s='You died of poisoning!')

        # at the time of your death
        terminal.printf(x=died_when_x, y=died_when_y, s='At the time of your death...')

        # condis attached
        condi_string = GameOver.format_condi_string(gameworld=gameworld, player_entity=player_entity)
        terminal.printf(x=condi_print_x, y=condi_print_y, s=condi_string)

        # boons attached
        boon_string = GameOver.format_boon_string(gameworld=gameworld, player_entity=player_entity)

        terminal.printf(x=boon_print_x, y=boon_print_y, s=boon_string)

        # when you died

        # Armour / Jewellery / Weapons panel

        # draw message panel boundary
        # top left
        terminal.printf(x=equipment_panel_start_x, y=equipment_panel_start_y,
                        s=unicode_string_to_print + equipment_panel_top_left_corner + ']')

        # horizontals
        for z in range(equipment_panel_start_x + 1, (equipment_panel_start_x + equipment_panel_width)):
            terminal.printf(x=z, y=equipment_panel_start_y, s=unicode_string_to_print + equipment_panel_horizontal + ']')
            terminal.printf(x=z, y=equipment_panel_start_y + 2,
                            s=unicode_string_to_print + equipment_panel_horizontal + ']')
            terminal.printf(x=z, y=(equipment_panel_start_y + equipment_panel_depth),
                            s=unicode_string_to_print + equipment_panel_horizontal + ']')
        # top right
        terminal.printf(x=equipment_panel_start_x + equipment_panel_width, y=equipment_panel_start_y,
                        s=unicode_string_to_print + equipment_panel_top_right_corner + ']')

        # verticals
        for z in range(equipment_panel_depth):
            terminal.printf(x=equipment_panel_start_x, y=(equipment_panel_start_y + z )+ 1, s=unicode_string_to_print + equipment_panel_vertical + ']')
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
        terminal.printf(x=equipment_panel_start_x + equipment_panel_width, y=(equipment_panel_start_y + equipment_panel_depth),
                        s=unicode_string_to_print + equipment_panel_bottom_right_corner + ']')

        # build the tabs
        not_selected_tab_colour = '[color=white]'
        selected_tab_color = '[color=blue]'
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
        GameOver.ep_tab_display(visible_panel=visible_panel, unicode_string_to_print=unicode_string_to_print, message_panel_vertical=equipment_panel_vertical, message_panel_bottom_left_corner=equipment_panel_bottom_left_corner, message_panel_bottom_right_corner=equipment_panel_bottom_right_corner)

        # display items
        GameOver.display_equipment(visible_panel=visible_panel, equipment_panel_item_x=equipment_panel_item_x, equipment_panel_item_y=equipment_panel_item_y, equipped_armour=equipped_armour, equipped_jewellery=equipped_jewellery, equipped_weapons=equipped_weapons, gameworld=gameworld)


    @staticmethod
    def format_condi_string(gameworld, player_entity):
        current_condis = MobileUtilities.get_current_condis_applied_to_mobile(gameworld=gameworld, entity=player_entity)
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
        current_boons = MobileUtilities.get_current_boons_applied_to_mobile(gameworld=gameworld, entity=player_entity)
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
        if len(equipped_armour) > 0:
            for armour_entity in range(len(equipped_armour)):
                armour_piece_name = ItemUtilities.get_item_displayname(gameworld=gameworld, entity=equipped_armour[armour_entity])
                terminal.print_(x=posx, y=posy, s=armour_piece_name)
                posy += 1
        else:
            terminal.print_(x=posx, y=posy, s='No armour equipped')

    @staticmethod
    def display_equipped_jewellery(posx, posy, equipped_jewellery, gameworld):
        if len(equipped_jewellery) > 0:
            for jewellery_entity in range(len(equipped_jewellery)):
                jewellery_piece_name = ItemUtilities.get_item_displayname(gameworld=gameworld,
                                                                       entity=equipped_jewellery[jewellery_entity])
                terminal.print_(x=posx, y=posy, s=jewellery_piece_name)
                posy += 1
        else:
            terminal.print_(x=posx, y=posy, s='No jewellery equipped')

    @staticmethod
    def display_equipped_weapons(posx, posy, equipped_weapons, gameworld):
        if len(equipped_weapons) > 0:
            for weapon_entity in range(len(equipped_weapons)):
                if equipped_weapons[weapon_entity] > 0:
                    weapon_piece_name = ItemUtilities.get_item_displayname(gameworld=gameworld,
                                                                           entity=equipped_weapons[weapon_entity])

                    terminal.print_(x=posx, y=posy, s=weapon_piece_name)
                    posy += 1
        else:
            terminal.print_(x=posx, y=posy, s='No weapons equipped')

    @staticmethod
    def ep_tab_display(visible_panel, unicode_string_to_print, message_panel_vertical, message_panel_bottom_left_corner, message_panel_bottom_right_corner):
        if visible_panel == 0:
            terminal.clear_area(21, 22, 11, 1)
            terminal.printf(x=20, y=22, s=unicode_string_to_print + message_panel_vertical + ']')
            terminal.printf(x=32, y=22, s=unicode_string_to_print + message_panel_bottom_left_corner + ']')

        if visible_panel == 1:
            terminal.clear_area(33, 22, 11, 1)
            terminal.printf(x=32, y=22, s=unicode_string_to_print + message_panel_bottom_right_corner + ']')
            terminal.printf(x=44, y=22, s=unicode_string_to_print + message_panel_bottom_left_corner + ']')

        if visible_panel == 2:
            terminal.clear_area(45, 22, 11, 1)
            terminal.printf(x=44, y=22, s=unicode_string_to_print + message_panel_bottom_right_corner + ']')
            terminal.printf(x=56, y=22, s=unicode_string_to_print + message_panel_bottom_left_corner + ']')


