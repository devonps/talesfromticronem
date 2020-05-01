from components.messages import Message
from utilities import configUtilities
from components import viewport, messages
from utilities.mobileHelp import MobileUtilities


class CommonUtils:

    @staticmethod
    def get_unicode_ascii_char(game_config, config_prefix, tile_assignment):
        tile_char = "0x" + configUtilities.get_config_value_as_string(configfile=game_config, section='dungeon',
                                                                      parameter=config_prefix + str(
                                                                          tile_assignment))
        return tile_char

    @staticmethod
    def calculate_percentage(low_number, max_number):
        return int((low_number / max_number) * 100)

    @staticmethod
    def format_combat_log_message(gameworld, caster_name, target_name, damage_done_to_target, spell_name):

        game_config = configUtilities.load_config()
        player_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
        message_log_id = MobileUtilities.get_MessageLog_id(gameworld=gameworld, entity=player_entity)
        current_turn = MobileUtilities.get_current_turn(gameworld=gameworld, entity=player_entity)
        formatted_turn_number = CommonUtils.format_game_turn_as_string(current_turn=current_turn)

        msg_start = formatted_turn_number + ":" + caster_name + " hits " + target_name + " for "
        message_text = msg_start + "[color=orange]" + str(damage_done_to_target) + " damage[/color] using [[" + spell_name + "]]"
        msg = Message(text=message_text , msgclass="combat", fg="white",bg="black", fnt="")
        log_message = msg_start + str(damage_done_to_target) + " damage using [" + spell_name + "]"

        CommonUtils.add_message(gameworld=gameworld, message=msg, logid=message_log_id, message_for_export=log_message)

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
                                                           display_from_message=0, display_to_message=10, visible_log='all'))

    @staticmethod
    def format_game_turn_as_string(current_turn):
        base_turn_string = '00000'
        current_turn_as_string = str(current_turn)
        left_string = len(current_turn_as_string)

        turn_as_string = base_turn_string[left_string:] + current_turn_as_string

        return turn_as_string


    @staticmethod
    def add_message(gameworld, message, logid, message_for_export):
        stored_msgs = CommonUtils.get_message_log_all_messages(gameworld=gameworld, logid=logid)
        stored_msgs.append(message)
        message_component = gameworld.component_for_entity(logid, messages.MessageLog)
        message_component.storedMessages = stored_msgs

        # this next piece of code adds a plain/vanilla message ready to be exported
        stored_export_messages = CommonUtils.get_all_log_messages_for_export(gameworld=gameworld, logid=logid)
        stored_export_messages.append(message_for_export)
        message_component = gameworld.component_for_entity(logid, messages.MessageLog)
        message_component.stored_log_messages = stored_export_messages

    @staticmethod
    def set_visible_log(gameworld, log_id, log_to_display):

        messaage_log_component = gameworld.component_for_entity(log_id, messages.MessageLog)
        messaage_log_component.visible_log = log_to_display

    @staticmethod
    def get_visible_log(gameworld, logid):

        messaage_log_component = gameworld.component_for_entity(logid, messages.MessageLog)
        return messaage_log_component.visible_log

    @staticmethod
    def build_message_to_be_displayed(gameworld, logid, message):
        str_to_print = ""
        if message.msgclass == CommonUtils.get_visible_log(gameworld=gameworld, logid=logid):
            fg_color = "white" if message.fg == "" else message.fg
            bg_color = "red" if message.bg == "" else message.bg
            fnt = "messageLog" if message.fnt == "" else message.fnt
            str_to_print += "[color=" + fg_color + "]"
            str_to_print += "[bkcolor=" + bg_color + "][/bkcolor]"
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
        return log_component.stored_messages

    @staticmethod
    def get_all_log_messages_for_export(gameworld, logid):
        log_component = gameworld.component_for_entity(logid, messages.MessageLog)
        return log_component.stored_log_messages

    @staticmethod
    def get_message_log_first_dispay_message(gameworld, logid):
        log_component = gameworld.component_for_entity(logid, messages.MessageLog)
        return log_component.display_from_message

    @staticmethod
    def get_message_log_last_display_message(gameworld, logid):
        log_component = gameworld.component_for_entity(logid, messages.MessageLog)
        return log_component.display_to_message

    @staticmethod
    def get_messages_for_visible_message_log(gameworld, log_id):
        stored_msgs = CommonUtils.get_message_log_all_messages(gameworld=gameworld, logid=log_id)
        visible_log = CommonUtils.get_visible_log(gameworld=gameworld, logid=log_id)
        display_max_number_messages = CommonUtils.get_message_log_last_display_message(gameworld=gameworld, logid=log_id)

        visible_messages = [msg for msg in stored_msgs if msg.msgclass == visible_log]

        display_messages_count = len(visible_messages)

        if display_messages_count <= display_max_number_messages:
            display_messages_from = 0
            display_messages_to = display_messages_count
        else:
            display_messages_to = display_messages_count
            display_messages_from = display_messages_to - display_max_number_messages

        return visible_messages, display_messages_from, display_messages_to, display_messages_count

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

    @staticmethod
    def view_message_log(gameworld, player, log_to_be_displayed):
        logs = log_to_be_displayed.split('_')
        msglog = MobileUtilities.get_MessageLog_id(gameworld=gameworld, entity=player)
        CommonUtils.set_visible_log(gameworld=gameworld, log_id=msglog, log_to_display=logs[2])
        MobileUtilities.set_view_message_log(gameworld=gameworld, entity=player, view_value=True)