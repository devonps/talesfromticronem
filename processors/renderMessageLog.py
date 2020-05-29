import esper
from bearlibterminal import terminal

from utilities import configUtilities
from utilities.mobileHelp import MobileUtilities
from utilities.common import CommonUtils


class RenderMessageLog(esper.Processor):
    def __init__(self, gameworld):
        self.gameworld = gameworld

    def process(self, game_config):
        self.render_message_panel(self, game_config)

    @staticmethod
    def render_message_panel(self, game_config):

        # get message log entity id
        player_entity = MobileUtilities.get_player_entity(self.gameworld, game_config)
        log_id = MobileUtilities.get_MessageLog_id(gameworld=self.gameworld, entity=player_entity)
        message_panel_width = CommonUtils.get_message_log_width(gameworld=self.gameworld, logid=log_id)
        message_panel_depth = CommonUtils.get_message_log_depth(gameworld=self.gameworld, logid=log_id)
        message_panel_height = CommonUtils.get_message_log_height(gameworld=self.gameworld, logid=log_id)

        message_panel_start_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                            parameter='MSG_PANEL_START_X')
        image_x_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='map_Xscale')
        image_y_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='map_Yscale')

        # top left
        terminal.put(x=(message_panel_start_x * image_x_scale), y=message_panel_height * image_y_scale, c=0xE700 + 0)

        # left edge
        for d in range(message_panel_depth):
            terminal.put(x=(message_panel_start_x * image_x_scale), y=(message_panel_height + d) * image_y_scale,
                         c=0xE700 + 4)

        # bottom left
        terminal.put(x=(message_panel_start_x * image_x_scale), y=(message_panel_height + 5) * image_y_scale,
                     c=0xE700 + 2)

        # top right
        terminal.put(x=(message_panel_start_x * image_x_scale) + message_panel_width,
                     y=message_panel_height * image_y_scale, c=0xE700 + 1)

        # bottom right
        terminal.put(x=(message_panel_start_x * image_x_scale) + message_panel_width,
                     y=(message_panel_height + 5) * image_y_scale, c=0xE700 + 3)

        # top edge
        for a in range(message_panel_width):
            terminal.put(x=a + (message_panel_start_x * image_x_scale), y=message_panel_height * image_y_scale,
                         c=0xE700 + 6)
        # right edge
        for d in range(message_panel_depth):
            terminal.put(x=message_panel_start_x * image_x_scale + message_panel_width,
                         y=(message_panel_height + d) * image_y_scale, c=0xE700 + 5)

        # bottom edge
        for a in range(message_panel_width):
            terminal.put(x=a + (message_panel_start_x * image_x_scale), y=(message_panel_height + 5) * image_y_scale,
                         c=0xE700 + 7)
        # message tabs
        terminal.printf(x=(message_panel_start_x * image_x_scale), y=(message_panel_height * image_y_scale) + 1,
                        s="Combat")
        # now show the messages
        #
        visible_messages, display_messages_from, display_messages_to, display_messages_count = CommonUtils.get_messages_for_visible_message_log(gameworld=self.gameworld, log_id=log_id)
        display_line = 2
        if display_messages_count > 0:
            for msg in range(display_messages_from, display_messages_to):
                message = visible_messages[msg]
                str_to_print = CommonUtils.build_message_to_be_displayed(gameworld=self.gameworld, logid=log_id, message=message)
                if str_to_print != "":
                    terminal.printf(x=(message_panel_start_x * image_x_scale), y=(message_panel_height * image_y_scale) + display_line,
                                    s=str_to_print)
                    display_line += 1
