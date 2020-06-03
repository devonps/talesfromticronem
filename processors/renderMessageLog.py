import esper
from bearlibterminal import terminal
from loguru import logger

from utilities import configUtilities, common
from utilities.mobileHelp import MobileUtilities
from utilities.common import CommonUtils


class RenderMessageLog(esper.Processor):
    def __init__(self, gameworld):
        self.gameworld = gameworld

    def process(self, game_config):
        self.render_message_panel(self, game_config=game_config)

    @staticmethod
    def render_message_panel(self, game_config):

        unicode_string_to_print = '[font=dungeon][color=MSGPANEL_FRAME_COLOUR]['
        ascii_prefix = 'ASCII_SINGLE_'

        # get message log entity id
        player_entity = MobileUtilities.get_player_entity(self.gameworld, game_config)
        message_panel_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='messagePanel',
                                                                            parameter='MSG_PANEL_WIDTH')
        message_panel_depth = configUtilities.get_config_value_as_integer(configfile=game_config, section='messagePanel',
                                                                            parameter='MSG_PANEL_DEPTH')

        message_panel_start_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='messagePanel',
                                                                            parameter='MSG_PANEL_START_X')

        message_panel_start_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='messagePanel',
                                                                            parameter='MSG_PANEL_START_Y')

        message_panel_top_left_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'TOP_LEFT')

        message_panel_bottom_left_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'BOTTOM_LEFT')

        message_panel_top_right_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'TOP_RIGHT')

        message_panel_bottom_right_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'BOTTOM_RIGHT')

        message_panel_horizontal = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'HORIZONTAL')
        message_panel_vertical = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'VERTICAL')
        message_panel_left_junction = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'LEFT_T_JUNCTION')
        message_panel_right_junction = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'RIGHT_T_JUNCTION')
        message_panel_top_junction = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'TOP_T_JUNCTION')
        message_panel_bottom_junction = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'BOTTOM_T_JUNCTION')

        # draw message panel boundary
        # top left
        terminal.printf(x=message_panel_start_x, y=message_panel_start_y, s=unicode_string_to_print + message_panel_top_left_corner + ']')

        # horizontals
        for z in range(message_panel_start_x + 1, (message_panel_start_x + message_panel_width)):
            terminal.printf(x=z, y=message_panel_start_y, s=unicode_string_to_print + message_panel_horizontal + ']')
            terminal.printf(x=z, y=message_panel_start_y + 2, s=unicode_string_to_print + message_panel_horizontal + ']')
            terminal.printf(x=z, y=(message_panel_start_y + message_panel_depth), s=unicode_string_to_print + message_panel_horizontal + ']')
        # top right
        terminal.printf(x=message_panel_start_x + message_panel_width, y=message_panel_start_y, s=unicode_string_to_print + message_panel_top_right_corner + ']')

        # verticals
        for z in range(message_panel_start_y + message_panel_depth):
            terminal.printf(x=message_panel_start_x, y=(message_panel_start_y + z) + 1, s=unicode_string_to_print + message_panel_vertical + ']')
            terminal.printf(x=message_panel_start_x + message_panel_width, y=(message_panel_start_y + z) + 1, s=unicode_string_to_print + message_panel_vertical + ']')

        # left junction for tab bar
        terminal.printf(x=message_panel_start_x, y=message_panel_start_y + 2, s=unicode_string_to_print + message_panel_left_junction + ']')

        # right junction for tab bar
        terminal.printf(x=message_panel_start_x + message_panel_width, y=message_panel_start_y + 2, s=unicode_string_to_print + message_panel_right_junction + ']')

        # bottom left
        terminal.printf(x=message_panel_start_x, y=(message_panel_start_y + message_panel_depth), s=unicode_string_to_print + message_panel_bottom_left_corner + ']')

        # bottom right
        terminal.printf(x=message_panel_start_x + message_panel_width, y=(message_panel_start_y + message_panel_depth), s=unicode_string_to_print + message_panel_bottom_right_corner + ']')

        message_log_entity = MobileUtilities.get_MessageLog_id(gameworld=self.gameworld, entity=player_entity)

        # build the tabs
        visible_log = CommonUtils.get_current_log_id(gameworld=self.gameworld, log_entity=message_log_entity)
        logger.info('Visible log is {}', visible_log)

        tabs_to_display = configUtilities.get_config_value_as_list(configfile=game_config, section='messagePanel', parameter='MSG_PANEL_TABS')
        not_selected_tab_colour = '[color=white]'
        selected_tab_color = '[color=blue]'
        tab_pos_x = 1
        tab_length = 8
        for tab in range(len(tabs_to_display)):
            if tab != visible_log:
                str_to_print = not_selected_tab_colour + tabs_to_display[tab]
            else:
                str_to_print = selected_tab_color + tabs_to_display[tab]

            terminal.printf(x=tab_pos_x, y=message_panel_start_y + 1, s=str_to_print)
            if tab > 0:
                terminal.printf(x=tab_pos_x - 1, y=message_panel_start_y + 1, s=unicode_string_to_print + message_panel_vertical + ']')
                terminal.printf(x=tab_pos_x - 1, y=message_panel_start_y, s=unicode_string_to_print + message_panel_top_junction + ']')
                terminal.printf(x=tab_pos_x - 1, y=message_panel_start_y + 2, s=unicode_string_to_print + message_panel_bottom_junction + ']')

            tab_pos_x += tab_length
        terminal.printf(x=tab_pos_x - 1, y=message_panel_start_y + 1, s=unicode_string_to_print + message_panel_vertical + ']')
        terminal.printf(x=tab_pos_x - 1, y=message_panel_start_y, s=unicode_string_to_print + message_panel_top_junction + ']')
        terminal.printf(x=tab_pos_x - 1, y=message_panel_start_y + 2, s=unicode_string_to_print + message_panel_bottom_junction + ']')

        RenderMessageLog.log_tab_display(visible_log=visible_log, unicode_string_to_print=unicode_string_to_print, message_panel_vertical=message_panel_vertical, message_panel_bottom_left_corner=message_panel_bottom_left_corner, message_panel_bottom_right_corner=message_panel_bottom_right_corner)

        # now show the messages
        visible_messages, display_messages_from, display_messages_to, display_messages_count = CommonUtils.get_messages_for_visible_message_log(gameworld=self.gameworld, log_entity=message_log_entity)
        display_line = 4
        msg_log_display_x = 1
        if display_messages_count > 0:
            for msg in range(display_messages_from, display_messages_to):
                message = visible_messages[msg]
                str_to_print = CommonUtils.build_message_to_be_displayed(gameworld=self.gameworld, log_entity=message_log_entity, message=message)
                if str_to_print != "":
                    terminal.printf(x=msg_log_display_x, y=message_panel_start_y + display_line, s=str_to_print)
                    display_line += 1

    @staticmethod
    def log_tab_display(visible_log, unicode_string_to_print, message_panel_vertical, message_panel_bottom_left_corner, message_panel_bottom_right_corner):
        if visible_log == 0:
            terminal.clear_area(1, 2, 7, 1)
            terminal.printf(x=0, y=2, s=unicode_string_to_print + message_panel_vertical + ']')
            terminal.printf(x=8, y=2, s=unicode_string_to_print + message_panel_bottom_left_corner + ']')

        if visible_log == 1:
            terminal.clear_area(9, 2, 7, 1)
            terminal.printf(x=8, y=2, s=unicode_string_to_print + message_panel_bottom_right_corner + ']')
            terminal.printf(x=16, y=2, s=unicode_string_to_print + message_panel_bottom_left_corner + ']')

        if visible_log == 2:
            terminal.clear_area(17, 2, 7, 1)
            terminal.printf(x=16, y=2, s=unicode_string_to_print + message_panel_bottom_right_corner + ']')
            terminal.printf(x=24, y=2, s=unicode_string_to_print + message_panel_bottom_left_corner + ']')

        if visible_log == 3:
            terminal.clear_area(25, 2, 7, 1)
            terminal.printf(x=24, y=2, s=unicode_string_to_print + message_panel_bottom_right_corner + ']')
            terminal.printf(x=32, y=2, s=unicode_string_to_print + message_panel_bottom_left_corner + ']')
