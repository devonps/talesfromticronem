import esper
from bearlibterminal import terminal
from components.messages import MessageLog, Message
from utilities import configUtilities, colourUtilities
from utilities.mobileHelp import MobileUtilities
from loguru import logger
from utilities.common import CommonUtils
from mapRelated.gameMap import RenderLayer


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

        prev_layer = terminal.state(terminal.TK_LAYER)
        terminal.layer(RenderLayer.HUD.value)

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

        terminal.put(x=(message_panel_start_x * image_x_scale) + 3, y=(message_panel_height * image_y_scale), c=0xE880)

        terminal.put(x=(message_panel_start_x * image_x_scale) + 5, y=(message_panel_height * image_y_scale), c=0xE800)

        # right edge
        for d in range(message_panel_depth):
            terminal.put(x=message_panel_start_x * image_x_scale + message_panel_width,
                         y=(message_panel_height + d) * image_y_scale, c=0xE700 + 5)

        # bottom edge
        for a in range(message_panel_width):
            terminal.put(x=a + (message_panel_start_x * image_x_scale), y=(message_panel_height + 5) * image_y_scale,
                         c=0xE700 + 7)

        # now show the messages
        #
        storedMsgs = CommonUtils.get_message_log_all_message(gameworld=self.gameworld, logid=log_id)
        y = 1
        for message in storedMsgs:
            str_to_print = ""
            str_to_print = CommonUtils.build_message_to_be_displayed(gameworld=self.gameworld, logid=log_id, message=message)
            if str_to_print != "":
                terminal.printf(x=(message_panel_start_x * image_x_scale), y=(message_panel_height * image_y_scale) + y, s=str_to_print)
                y += 1