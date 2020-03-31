from components.messages import Message
from utilities import configUtilities
from components import viewport, messages


class CommonUtils:

    @staticmethod
    def calculate_percentage(lowNumber, maxNumber):
        return int((lowNumber / maxNumber) * 100)

    @staticmethod
    def format_combat_log_message(gameworld, target, damage_done_to_target, spell_name, message_log_id):
        turnNumber = 1
        msgStart = str(turnNumber) + ': You hit '
        target_name = target
        tempMessage = msgStart + target_name + " for " + str(damage_done_to_target) + " using [" + spell_name + "]"

        if len(tempMessage) <= 25:
            msg = Message(text=msgStart + target_name + " for " + "[color=orange]" + str(
                damage_done_to_target) + "[/color] using [[" + spell_name + "]]", msgclass="combat", fg="white",
                          bg="black", fnt="")
            CommonUtils.add_message(gameworld=gameworld, message=msg, logid=message_log_id)
        else:
            temp2Message = Message(
                msgStart + target_name + " for " + "[color=orange]" + str(damage_done_to_target) + " pts",
                msgclass="combat", fg="white", bg="black", fnt="")
            temp3Message = Message("[/color] using [color=yellow][[" + spell_name + "]]", msgclass="combat",
                                   fg="yellow", bg="black", fnt="")
            CommonUtils.add_message(gameworld=gameworld, message=temp2Message, logid=message_log_id)
            CommonUtils.add_message(gameworld=gameworld, message=temp3Message, logid=message_log_id)

    @staticmethod
    def create_message_log_as_entity(gameworld, logid):
        game_config = configUtilities.load_config()
        message_panel_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                          parameter='MSG_PANEL_WIDTH')
        message_panel_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                           parameter='MSG_PANEL_START_Y')
        message_panel_depth = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                          parameter='MSG_PANEL_DEPTH')
        # need to add data to the components next
        gameworld.add_component(logid, messages.MessageLog(width=message_panel_width,
                                                           height=message_panel_height, depth=message_panel_depth,
                                                           display_from_message=0, display_to_message=10, visibleLog='all'))

    @staticmethod
    def add_message(gameworld, message, logid):
        storedMsgs = CommonUtils.get_message_log_all_messages(gameworld=gameworld, logid=logid)
        storedMsgs.append(message)
        messaage_component = gameworld.component_for_entity(logid, messages.MessageLog)
        messaage_component.storedMessages = storedMsgs

    @staticmethod
    def set_visible_log(gameworld, logid, logToDisplay):

        messaageLog_component = gameworld.component_for_entity(logid, messages.MessageLog)
        messaageLog_component.visibleLog = logToDisplay

    @staticmethod
    def get_visible_log(gameworld, logid):

        messaageLog_component = gameworld.component_for_entity(logid, messages.MessageLog)
        return messaageLog_component.visibleLog

    @staticmethod
    def build_message_to_be_displayed(gameworld, logid, message):
        str_to_print = ""
        if message.msgclass == CommonUtils.get_visible_log(gameworld=gameworld, logid=logid):
            fg_color = "white" if message.fg == "" else message.fg
            bg_color = "red" if message.bg == "" else message.bg
            fnt = "" if message.fnt == "" else message.fnt
            str_to_print += "[color=" + fg_color + "]"
            str_to_print += "[bkcolor=" + bg_color + "]"
            str_to_print += "[font=" + fnt + "]"
            str_to_print += message.text

        return str_to_print

    @staticmethod
    def get_message_log_width(gameworld, logid):
        log_component = gameworld.component_for_entity(logid, messages.MessageLog)
        return log_component.width

    @staticmethod
    def get_message_log_height(gameworld, logid):
        log_component = gameworld.component_for_entity(logid, messages.MessageLog)
        return log_component.height

    @staticmethod
    def get_message_log_depth(gameworld, logid):
        log_component = gameworld.component_for_entity(logid, messages.MessageLog)
        return log_component.depth

    @staticmethod
    def get_message_log_all_messages(gameworld, logid):
        log_component = gameworld.component_for_entity(logid, messages.MessageLog)
        return log_component.storedMessages

    @staticmethod
    def get_message_log_first_dispay_message(gameworld, logid):
        log_component = gameworld.component_for_entity(logid, messages.MessageLog)
        return log_component.display_from_message

    @staticmethod
    def get_message_log_last_display_message(gameworld, logid):
        log_component = gameworld.component_for_entity(logid, messages.MessageLog)
        return log_component.display_to_message

    @staticmethod
    def create_viewport_as_entity(gameworld, vwp):
        game_config = configUtilities.load_config()

        viewport_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                     parameter='VIEWPORT_WIDTH')
        viewport_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='VIEWPORT_HEIGHT')

        gameworld.add_component(vwp, viewport.Dimensions(width=viewport_width, height=viewport_height))
        gameworld.add_component(vwp,
                                viewport.DisplayRange(min_x=0, max_x=viewport_width, min_y=0, max_y=viewport_height))
        gameworld.add_component(vwp, viewport.PlayerViewportPosition(viewport_x=0, viewport_y=0))
        gameworld.add_component(vwp, viewport.Information())

    @staticmethod
    def get_viewport_width(gameworld, viewport_id):
        viewport_component = gameworld.component_for_entity(viewport_id, viewport.Dimensions)

        return viewport_component.width

    @staticmethod
    def get_viewport_height(gameworld, viewport_id):
        viewport_component = gameworld.component_for_entity(viewport_id, viewport.Dimensions)

        return viewport_component.height

    @staticmethod
    def get_viewport_x_axis_min_value(gameworld, viewport_id):
        viewport_component = gameworld.component_for_entity(viewport_id, viewport.DisplayRange)
        return viewport_component.min_x

    @staticmethod
    def get_viewport_x_axis_max_value(gameworld, viewport_id):
        viewport_component = gameworld.component_for_entity(viewport_id, viewport.DisplayRange)
        return viewport_component.max_x

    @staticmethod
    def get_viewport_y_axis_min_value(gameworld, viewport_id):
        viewport_component = gameworld.component_for_entity(viewport_id, viewport.DisplayRange)
        return viewport_component.min_y

    @staticmethod
    def get_viewport_y_axis_max_value(gameworld, viewport_id):
        viewport_component = gameworld.component_for_entity(viewport_id, viewport.DisplayRange)
        return viewport_component.max_y

    @staticmethod
    def set_viewport_x_axis_min_value(gameworld, viewport_id, value):
        viewport_component = gameworld.component_for_entity(viewport_id, viewport.DisplayRange)
        viewport_component.min_x = value

    @staticmethod
    def set_viewport_x_axis_max_value(gameworld, viewport_id, value):
        viewport_component = gameworld.component_for_entity(viewport_id, viewport.DisplayRange)
        viewport_component.max_x = value

    @staticmethod
    def set_viewport_y_axis_min_value(gameworld, viewport_id, value):
        viewport_component = gameworld.component_for_entity(viewport_id, viewport.DisplayRange)
        viewport_component.min_y = value

    @staticmethod
    def set_viewport_y_axis_max_value(gameworld, viewport_id, value):
        viewport_component = gameworld.component_for_entity(viewport_id, viewport.DisplayRange)
        viewport_component.max_y = value

    @staticmethod
    def get_player_viewport_position_info(gameworld, viewport_id):
        viewport_component = gameworld.component_for_entity(viewport_id, viewport.PlayerViewportPosition)

        return [viewport_component.viewport_x, viewport_component.viewport_y]

    @staticmethod
    def set_player_viewport_position_x(gameworld, viewport_id, posx):
        viewport_component = gameworld.component_for_entity(viewport_id, viewport.PlayerViewportPosition)

        viewport_component.viewport_x = posx

    @staticmethod
    def set_player_viewport_position_y(gameworld, viewport_id, posy):
        viewport_component = gameworld.component_for_entity(viewport_id, viewport.PlayerViewportPosition)

        viewport_component.viewport_y = posy

    @staticmethod
    def set_viewport_right_boundary_visited_true(gameworld, viewport_id):
        viewport_component = gameworld.component_for_entity(viewport_id, viewport.Information)
        viewport_component.boundaryRight = True

    @staticmethod
    def set_viewport_right_boundary_visited_false(gameworld, viewport_id):
        viewport_component = gameworld.component_for_entity(viewport_id, viewport.Information)
        viewport_component.boundaryRight = False

    @staticmethod
    def get_viewport_right_boundary(gameworld, viewport_id):
        viewport_component = gameworld.component_for_entity(viewport_id, viewport.Information)
        return viewport_component.boundaryRight

    @staticmethod
    def set_viewport_left_boundary_visited_true(gameworld, viewport_id):
        viewport_component = gameworld.component_for_entity(viewport_id, viewport.Information)
        viewport_component.boundaryLeft = True

    @staticmethod
    def set_viewport_left_boundary_visited_false(gameworld, viewport_id):
        viewport_component = gameworld.component_for_entity(viewport_id, viewport.Information)
        viewport_component.boundaryLeft = False

    @staticmethod
    def get_viewport_left_boundary(gameworld, viewport_id):
        viewport_component = gameworld.component_for_entity(viewport_id, viewport.Information)
        return viewport_component.boundaryLeft
