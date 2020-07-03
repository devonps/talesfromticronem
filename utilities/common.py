from bearlibterminal import terminal
from loguru import logger

from components.messages import Message
from utilities import configUtilities, jsonUtilities
from components import messages, mobiles
from utilities.mobileHelp import MobileUtilities


class CommonUtils:

    @staticmethod
    def get_entity_at_location(gameworld, posx, posy):
        entity_id = 0
        for ent, pos in gameworld.get_components(mobiles.Position):
            entity_pos_x = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=ent)
            entity_pos_y = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=ent)
            if entity_pos_x == posx and entity_pos_y == posy:
                entity_id = ent
        return entity_id

    @staticmethod
    def calculate_camera_position(camera_width, camera_height, player_map_pos_x, player_map_pos_y, game_map):
        x = int(player_map_pos_x - (camera_width / 2))
        y = int(player_map_pos_y - (camera_height / 2))

        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x > game_map.width - camera_width - 1:
            x = game_map.width - camera_width - 1
        if y > game_map.height - camera_height - 1:
            y = game_map.height - camera_height - 1

        return x, y

    @staticmethod
    def get_unicode_ascii_char(game_config, config_prefix, tile_assignment):
        tile_char = "0x" + configUtilities.get_config_value_as_string(configfile=game_config, section='dungeon',
                                                                      parameter=config_prefix + str(
                                                                          tile_assignment))
        return tile_char

    @staticmethod
    def get_ascii_to_unicode(game_config, parameter):
        tile_char = "0x" + configUtilities.get_config_value_as_string(configfile=game_config, section='gui',
                                                                      parameter=parameter)
        return tile_char

    @staticmethod
    def format_number_as_string(base_number, base_string):
        base_turn_string = base_string
        current_turn_as_string = str(base_number)
        left_string = len(current_turn_as_string)

        turn_as_string = base_turn_string[left_string:] + current_turn_as_string

        return turn_as_string

    @staticmethod
    def create_message_log_as_entity(gameworld, log_entity):
        # need to add data to the components next
        gameworld.add_component(log_entity, messages.MessageLog(visible_log=0))

    @staticmethod
    def fire_event(event_title, gameworld, **kwargs):
        """
        :param event_title: name of the event/message to be generated
        :param gameworld:
        :param kwargs: see method definition
        """
        game_config = configUtilities.load_config()
        player = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
        message_log_entity = MobileUtilities.get_MessageLog_id(gameworld=gameworld, entity=player)
        current_turn = MobileUtilities.get_current_turn(gameworld=gameworld, entity=player)
        formatted_turn_number = CommonUtils.format_number_as_string(base_number=current_turn, base_string='00000')

        new_string = ''
        foreground_colour = kwargs.get('fg', 'white')
        background_colour = kwargs.get('bg', 'black')
        event_classes = []
        events_file_path = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                      parameter='EVENTSFILE')
        # load file as a dictionary
        events = jsonUtilities.read_json_file(events_file_path)
        for event in events['events']:
            if event['event-title'] == event_title:
                event_string = event['event-message']
                event_classes = CommonUtils.convert_string_to_list(event['event-classes'])
                return_string = CommonUtils.process_events(event_title=event_title, event_string=event_string,
                                                           kwargs=kwargs)
                new_string = formatted_turn_number + ":" + return_string

        CommonUtils.process_new_string(new_string=new_string, event_classes=event_classes,
                                       foreground_colour=foreground_colour, background_colour=background_colour,
                                       gameworld=gameworld, message_log_entity=message_log_entity)

    @staticmethod
    def process_events(event_title, event_string, kwargs):
        new_string = ''

        if event_title == 'new-game':
            par1 = kwargs.get('player_name', None)
            par2 = kwargs.get('player_race', None)
            par3 = kwargs.get('player_class', None)
            new_string = CommonUtils.replace_value_in_event(event_string=event_string, par1=par1, par2=par2, par3=par3)
        if event_title == 'spell-causes-damage':
            par1 = kwargs.get('caster', None)
            par2 = kwargs.get('target', None)
            par3 = kwargs.get('damage', None)
            par4 = kwargs.get('spell_name', None)
            new_string = CommonUtils.replace_value_in_event(event_string=event_string, par1=par1, par2=par2, par3=par3,
                                                            par4=par4)

        if event_title == 'spell-cooldown':
            par1 = kwargs.get('spell_name', None)
            new_string = CommonUtils.replace_value_in_event(event_string=event_string, par1=par1)

        if event_title == 'condi-applied':
            par1 = kwargs.get('target', None)
            par2 = kwargs.get('effect_dialogue', None)
            new_string = CommonUtils.replace_value_in_event(event_string=event_string, par1=par1, par2=par2)

        if event_title == 'condi-damage':
            par1 = kwargs.get('target', None)
            par2 = kwargs.get('damage', None)
            par3 = kwargs.get('condi_name', None)
            new_string = CommonUtils.replace_value_in_event(event_string=event_string, par1=par1, par2=par2, par3=par3)

        if event_title == 'boon-benefit':
            par1 = kwargs.get('target', None)
            par2 = kwargs.get('benefit', None)
            par3 = kwargs.get('boon_name', None)
            new_string = CommonUtils.replace_value_in_event(event_string=event_string, par1=par1, par2=par2, par3=par3)

        if event_title == 'boon-removal':
            par1 = kwargs.get('target', None)
            par2 = kwargs.get('boon_name', None)
            new_string = CommonUtils.replace_value_in_event(event_string=event_string, par1=par1, par2=par2)

        return new_string

    @staticmethod
    def process_new_string(new_string, event_classes, foreground_colour, background_colour, gameworld,
                           message_log_entity):
        if new_string != '':
            n = 0
            for _ in event_classes:
                if event_classes[n] == 'all':
                    message_class = 0
                elif event_classes[n] == 'combat':
                    message_class = 1
                elif event_classes[n] == 'story':
                    message_class = 2
                else:
                    message_class = 3
                n += 1

                msg = Message(text=new_string, msgclass=message_class, fg=foreground_colour, bg=background_colour,
                              fnt="")
                log_message = new_string
                CommonUtils.add_message(gameworld=gameworld, message=msg, log_entity=message_log_entity,
                                        message_for_export=log_message)

    @staticmethod
    def convert_string_to_list(the_string):
        return list(the_string.split(","))

    @staticmethod
    def add_message(gameworld, message, log_entity, message_for_export):
        stored_msgs = CommonUtils.get_message_log_all_messages(gameworld=gameworld, log_entity=log_entity)
        if stored_msgs is None:
            stored_msgs = []
        stored_msgs.append(message)
        message_component = gameworld.component_for_entity(log_entity, messages.MessageLog)
        message_component.storedMessages = stored_msgs

        # this next piece of code adds a plain/vanilla message ready to be exported
        stored_export_messages = CommonUtils.get_all_log_messages_for_export(gameworld=gameworld, log_entity=log_entity)
        stored_export_messages.append(message_for_export)
        message_component = gameworld.component_for_entity(log_entity, messages.MessageLog)
        message_component.stored_log_messages = stored_export_messages

    @staticmethod
    def get_current_log_id(gameworld, log_entity):
        messaage_log_component = gameworld.component_for_entity(log_entity, messages.MessageLog)
        return messaage_log_component.log_id

    @staticmethod
    def set_current_log(gameworld, log_entity):
        # get current message log
        current_log_id = CommonUtils.get_current_log_id(gameworld=gameworld, log_entity=log_entity)
        logger.debug('Current log id is {}', current_log_id)

        # increase the id by and check for out of bounds
        current_log_id += 1
        if current_log_id > 3:
            current_log_id = 0

        logger.debug('New log id is {}', current_log_id)
        # set the current message log
        messaage_log_component = gameworld.component_for_entity(log_entity, messages.MessageLog)
        messaage_log_component.log_id = current_log_id

    @staticmethod
    def set_visible_log(gameworld, log_entity, log_to_display):

        messaage_log_component = gameworld.component_for_entity(log_entity, messages.MessageLog)
        messaage_log_component.visible_log = log_to_display

    @staticmethod
    def get_visible_log(gameworld, logid):

        messaage_log_component = gameworld.component_for_entity(logid, messages.MessageLog)
        return messaage_log_component.visible_log

    @staticmethod
    def build_message_to_be_displayed(gameworld, log_entity, message):
        str_to_print = ""
        visible_log = CommonUtils.get_current_log_id(gameworld=gameworld, log_entity=log_entity)
        if message.msgclass == visible_log:
            fg_color = "white" if message.fg == "" else message.fg
            bg_color = "red" if message.bg == "" else message.bg
            fnt = "messageLog" if message.fnt == "" else message.fnt
            str_to_print += "[color=" + fg_color + "]"
            str_to_print += "[bkcolor=" + bg_color + "][/bkcolor]"
            str_to_print += "[font=" + fnt + "]"
            str_to_print += message.text

        return str_to_print

    @staticmethod
    def get_message_log_all_messages(gameworld, log_entity):
        log_component = gameworld.component_for_entity(log_entity, messages.MessageLog)
        return log_component.stored_messages

    @staticmethod
    def get_all_log_messages_for_export(gameworld, log_entity):
        log_component = gameworld.component_for_entity(log_entity, messages.MessageLog)
        return log_component.stored_log_messages

    @staticmethod
    def get_message_log_last_display_message(gameworld, log_entity):
        log_component = gameworld.component_for_entity(log_entity, messages.MessageLog)
        return log_component.display_to_message

    @staticmethod
    def get_messages_for_visible_message_log(gameworld, log_entity):
        stored_msgs = CommonUtils.get_message_log_all_messages(gameworld=gameworld, log_entity=log_entity)
        visible_log = CommonUtils.get_current_log_id(gameworld=gameworld, log_entity=log_entity)
        display_max_number_messages = CommonUtils.get_message_log_last_display_message(gameworld=gameworld,
                                                                                       log_entity=log_entity)

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
    def view_message_log(gameworld, player, log_to_be_displayed):
        logs = log_to_be_displayed.split('_')
        msglog = MobileUtilities.get_MessageLog_id(gameworld=gameworld, entity=player)
        CommonUtils.set_visible_log(gameworld=gameworld, log_entity=msglog, log_to_display=logs[2])
        MobileUtilities.set_view_message_log(gameworld=gameworld, entity=player, view_value=True)

    @staticmethod
    def replace_value_in_event(event_string, **kwargs):
        par1 = kwargs.get('par1', None)
        par2 = kwargs.get('par2', None)
        par3 = kwargs.get('par3', None)
        par4 = kwargs.get('par4', None)
        par1_identifier = kwargs.get('par1_identifier', '$1')
        par2_identifier = kwargs.get('par2_identifier', '$2')
        par3_identifier = kwargs.get('par2_identifier', '$3')
        par4_identifier = kwargs.get('par2_identifier', '$4')

        return_string = event_string.replace(par1_identifier, par1)
        if par2:
            return_string = return_string.replace(par2_identifier, par2)
        if par3:
            return_string = return_string.replace(par3_identifier, par3)
        if par4:
            return_string = return_string.replace(par4_identifier, par4)

        return return_string

    @staticmethod
    def render_ui_framework(game_config):

        unicode_string_to_print = '[font=dungeon][color=SPELLINFO_FRAME_COLOUR]['
        ascii_prefix = 'ASCII_SINGLE_'

        start_x = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                              section='newCharacter',
                                                              parameter='NC_START_X')

        start_y = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                              section='newCharacter',
                                                              parameter='NC_START_Y')

        width = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                            section='newCharacter',
                                                            parameter='NC_WIDTH')
        height = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                             section='newCharacter',
                                                             parameter='NC_DEPTH')

        choices_start_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='newCharacter',
                                                                      parameter='CHOICES_BAR_Y')

        top_left_corner_char = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                parameter=ascii_prefix + 'TOP_LEFT')

        bottom_left_corner_char = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                   parameter=ascii_prefix + 'BOTTOM_LEFT')

        top_right_corner_char = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                 parameter=ascii_prefix + 'TOP_RIGHT')

        bottom_right_corner_char = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                    parameter=ascii_prefix + 'BOTTOM_RIGHT')

        horizontal_char = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                           parameter=ascii_prefix + 'HORIZONTAL')
        vertical_char = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                         parameter=ascii_prefix + 'VERTICAL')

        left_t_junction_char = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                parameter=ascii_prefix + 'LEFT_T_JUNCTION')
        right_t_junction_char = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                 parameter=ascii_prefix + 'RIGHT_T_JUNCTION')

        # render horizontal bottom
        for z in range(start_x, (start_x + width)):
            terminal.printf(x=z, y=(start_y + height),
                            s=unicode_string_to_print + horizontal_char + ']')
            terminal.printf(x=z, y=start_y, s=unicode_string_to_print + horizontal_char + ']')

        # render verticals
        for z in range(start_y, (start_y + height) - 1):
            terminal.printf(x=start_x, y=z + 1, s=unicode_string_to_print + vertical_char + ']')
            terminal.printf(x=(start_x + width), y=z + 1,
                            s=unicode_string_to_print + vertical_char + ']')

        # top left
        terminal.printf(x=start_x, y=start_y,
                        s=unicode_string_to_print + top_left_corner_char + ']')
        # bottom left
        terminal.printf(x=start_x, y=(start_y + height),
                        s=unicode_string_to_print + bottom_left_corner_char + ']')
        # top right
        terminal.printf(x=(start_x + width), y=start_y,
                        s=unicode_string_to_print + top_right_corner_char + ']')
        # bottom right
        terminal.printf(x=(start_x + width),
                        y=(start_y + height),
                        s=unicode_string_to_print + bottom_right_corner_char + ']')

        # render horizontal splitters
        for z in range(start_x, (start_x + width)):
            terminal.printf(x=z, y=choices_start_y,
                            s=unicode_string_to_print + horizontal_char + ']')

            terminal.printf(x=start_x, y=choices_start_y,
                            s=unicode_string_to_print + left_t_junction_char + ']')

            terminal.printf(x=(start_x + width), y=choices_start_y,
                            s=unicode_string_to_print + right_t_junction_char + ']')
