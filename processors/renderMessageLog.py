import esper
from bearlibterminal import terminal

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

        unicode_string_to_print = '[font=dungeon]['

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

        message_panel_top_left_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter='ASCII_TOP_LEFT')

        message_panel_bottom_left_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter='ASCII_LEFT_T_JUNCTION')

        message_panel_top_right_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter='ASCII_TOP_RIGHT')

        message_panel_bottom_right_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter='ASCII_BOTTOM_RIGHT')

        message_panel_horizontal = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter='ASCII_HORIZONTAL')
        message_panel_vertical = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter='ASCII_VERTICAL')

        # draw message panel boundary
        # top left
        terminal.printf(x=message_panel_start_x, y=message_panel_start_y, s=unicode_string_to_print + message_panel_top_left_corner + ']')

        # horizontals
        for z in range(message_panel_start_x + 1, (message_panel_start_x + message_panel_width)):
            terminal.printf(x=z, y=message_panel_start_y, s=unicode_string_to_print + message_panel_horizontal + ']')
            terminal.printf(x=z, y=(message_panel_start_y + message_panel_depth), s=unicode_string_to_print + message_panel_horizontal + ']')
        # top right
        terminal.printf(x=message_panel_start_x + message_panel_width, y=message_panel_start_y, s=unicode_string_to_print + message_panel_top_right_corner + ']')

        # verticals
        for z in range(message_panel_start_y + message_panel_depth):
            terminal.printf(x=message_panel_start_x, y=(message_panel_start_y + z) + 1, s=unicode_string_to_print + message_panel_vertical + ']')
            terminal.printf(x=message_panel_start_x + message_panel_width, y=(message_panel_start_y + z) + 1, s=unicode_string_to_print + message_panel_vertical + ']')

        # bottom left
        terminal.printf(x=message_panel_start_x, y=(message_panel_start_y + message_panel_depth), s=unicode_string_to_print + message_panel_bottom_left_corner + ']')

        # bottom right
        terminal.printf(x=message_panel_start_x + message_panel_width, y=(message_panel_start_y + message_panel_depth), s=unicode_string_to_print + message_panel_bottom_right_corner + ']')


        # now show the messages
        #
        # visible_messages, display_messages_from, display_messages_to, display_messages_count = CommonUtils.get_messages_for_visible_message_log(gameworld=self.gameworld, log_id=log_id)
        # display_line = 2
        # if display_messages_count > 0:
        #     for msg in range(display_messages_from, display_messages_to):
        #         message = visible_messages[msg]
        #         str_to_print = CommonUtils.build_message_to_be_displayed(gameworld=self.gameworld, logid=log_id, message=message)
        #         if str_to_print != "":
        #             terminal.printf(x=(message_panel_start_x * image_x_scale), y=(message_panel_height * image_y_scale) + display_line,
        #                             s=str_to_print)
        #             display_line += 1
