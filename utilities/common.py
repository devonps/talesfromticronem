from bearlibterminal import terminal
from loguru import logger
from utilities import configUtilities, jsonUtilities
from utilities.mobileHelp import MobileUtilities
from utilities.scorekeeper import ScorekeeperUtilities
from components import messages
from utilities.display import draw_simple_frame


class CommonUtils:

    @staticmethod
    def check_if_entity_has_boon_applied(gameworld, target_entity, boon_being_checked):
        found_boon = False
        current_boons = MobileUtilities.get_current_boons_applied_to_mobile(gameworld=gameworld, entity=target_entity)
        for boon in current_boons:
            boon_name = boon['name']
            if boon_name == boon_being_checked:
                found_boon = True

        return found_boon

    @staticmethod
    def check_if_entity_has_condi_applied(gameworld, target_entity, condi_being_checked):
        found_condi = False
        condi_count = 0
        current_condis = MobileUtilities.get_current_condis_applied_to_mobile(gameworld=gameworld,
                                                                              entity=target_entity)
        for condi in current_condis:
            condi_name = condi['name']
            if condi_being_checked == condi_name:
                found_condi = True
                condi_count += 1

        return found_condi, condi_count

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
        current_turn = ScorekeeperUtilities.get_meta_event_value(gameworld=gameworld,
                                                                 event_name='game_turn')
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

        if event_title == 'dialog-general':
            par1 = kwargs.get('dialog', None)
            new_string = CommonUtils.replace_value_in_event(event_string=event_string, par1=par1)

        if event_title == 'story-general':
            par1 = kwargs.get('dialog', None)
            new_string = CommonUtils.replace_value_in_event(event_string=event_string, par1=par1)

        if event_title == 'spell-notarget':
            par1 = kwargs.get('spell_name', None)
            new_string = CommonUtils.replace_value_in_event(event_string=event_string, par1=par1)

        if event_title == 'spell-fizzle':
            par1 = kwargs.get('target', None)
            new_string = CommonUtils.replace_value_in_event(event_string=event_string, par1=par1)

        return new_string

    @staticmethod
    def process_new_string(new_string, event_classes, foreground_colour, background_colour, gameworld,
                           message_log_entity):
        if new_string != '':
            n = 0
            for _ in event_classes:
                if event_classes[n] == 'all':
                    msg = messages.Message(text=new_string, msgclass=0, fg=foreground_colour, bg=background_colour,
                                           fnt="")
                    log_message = new_string
                    CommonUtils.add_message(gameworld=gameworld, message=msg, log_entity=message_log_entity,
                                            message_for_export=log_message)
                elif event_classes[n] == 'combat':
                    msg = messages.Message(text=new_string, msgclass=1, fg=foreground_colour, bg=background_colour,
                                           fnt="")
                    log_message = new_string
                    CommonUtils.add_message(gameworld=gameworld, message=msg, log_entity=message_log_entity,
                                            message_for_export=log_message)
                elif event_classes[n] == 'story':
                    msg = messages.Message(text=new_string, msgclass=2, fg=foreground_colour, bg=background_colour,
                                           fnt="")
                    log_message = new_string
                    CommonUtils.add_message(gameworld=gameworld, message=msg, log_entity=message_log_entity,
                                            message_for_export=log_message)
                else:
                    msg = messages.Message(text=new_string, msgclass=3, fg=foreground_colour, bg=background_colour,
                                           fnt="")
                    log_message = new_string
                    CommonUtils.add_message(gameworld=gameworld, message=msg, log_entity=message_log_entity,
                                            message_for_export=log_message)
                n += 1

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
        frame_components_list = CommonUtils.get_ui_frame_components()
        # frame_components_list breakdown
        # [0] = top_left_corner_char
        # [1] = bottom_left_corner_char
        # [2] = top_right_corner_char
        # [3] = bottom_right_corner_char
        # [4] = horizontal_char
        # [5] = vertical_char
        # [6] = left_t_junction_char
        # [7] = right_t_junction_char

        start_x = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                              section='newCharacter', parameter='NC_START_X')

        start_y = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                              section='newCharacter',
                                                              parameter='NC_START_Y')

        width = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                            section='newCharacter', parameter='NC_WIDTH')
        height = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                             section='newCharacter',
                                                             parameter='NC_DEPTH')

        choices_start_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='newCharacter',
                                                                      parameter='CHOICES_BAR_Y')

        # render horizontal bottom
        for z in range(start_x, (start_x + width)):
            terminal.printf(x=z, y=(start_y + height),
                            s=unicode_string_to_print + frame_components_list[4] + ']')
            terminal.printf(x=z, y=start_y, s=unicode_string_to_print + frame_components_list[4] + ']')

        # render verticals
        for z in range(start_y, (start_y + height) - 1):
            terminal.printf(x=start_x, y=z + 1, s=unicode_string_to_print + frame_components_list[5] + ']')
            terminal.printf(x=(start_x + width), y=z + 1,
                            s=unicode_string_to_print + frame_components_list[5] + ']')

        # top left
        terminal.printf(x=start_x, y=start_y,
                        s=unicode_string_to_print + frame_components_list[0] + ']')
        # bottom left
        terminal.printf(x=start_x, y=(start_y + height),
                        s=unicode_string_to_print + frame_components_list[1] + ']')
        # top right
        terminal.printf(x=(start_x + width), y=start_y,
                        s=unicode_string_to_print + frame_components_list[2] + ']')
        # bottom right
        terminal.printf(x=(start_x + width),
                        y=(start_y + height),
                        s=unicode_string_to_print + frame_components_list[3] + ']')

        # render horizontal splitters
        for z in range(start_x, (start_x + width)):
            terminal.printf(x=z, y=choices_start_y,
                            s=unicode_string_to_print + frame_components_list[4] + ']')

            terminal.printf(x=start_x, y=choices_start_y,
                            s=unicode_string_to_print + frame_components_list[6] + ']')

            terminal.printf(x=(start_x + width), y=choices_start_y,
                            s=unicode_string_to_print + frame_components_list[7] + ']')

    @staticmethod
    def helper_print_valid_targets(gameworld, valid_targets, game_config):
        vp_x_offset = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                  parameter='VIEWPORT_START_X')
        vp_y_offset = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                  parameter='VIEWPORT_START_Y')

        height = 5 + len(valid_targets) + 1

        terminal.clear_area(vp_x_offset + 1, vp_y_offset + 1, 26, height)

        draw_simple_frame(start_panel_frame_x=vp_x_offset, start_panel_frame_y=vp_y_offset,
                          start_panel_frame_width=26, start_panel_frame_height=height, title='| Valid Targets |')

        lft = vp_x_offset + 1

        entity_tag = vp_y_offset + 2
        target_letters = []

        xx = 0
        base_str_to_print = "[color=white][font=dungeon]"
        if len(valid_targets) == 0:
            str_to_print = base_str_to_print + 'No valid targets'
            terminal.printf(x=vp_x_offset + 3, y=entity_tag, s=str_to_print)
        else:
            for x in valid_targets:
                entity_name = MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=x)
                entity_fg = MobileUtilities.get_mobile_fg_render_colour(gameworld=gameworld, entity=x)
                entity_bg = MobileUtilities.get_mobile_bg_render_colour(gameworld=gameworld, entity=x)

                str_to_print = base_str_to_print + chr(
                    97 + xx) + ") [color=" + entity_fg + "][bkcolor=" + entity_bg + "]" + "@" + ' ' + entity_name[0]
                terminal.printf(x=vp_x_offset + 2, y=entity_tag, s=str_to_print)
                entity_tag += 1
                target_letters.append(chr(97 + xx))
                xx += 1
        str_to_print = base_str_to_print + 'Press ESC to cancel'
        terminal.printf(x=vp_x_offset + (lft + 3), y=(vp_y_offset + height), s=str_to_print)

        return target_letters

    @staticmethod
    def get_ui_frame_components():
        game_config = configUtilities.load_config()
        ascii_prefix = 'ASCII_SINGLE_'
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

        frame_components = [top_left_corner_char, bottom_left_corner_char, top_right_corner_char,
                            bottom_right_corner_char, horizontal_char, vertical_char, left_t_junction_char,
                            right_t_junction_char]

        return frame_components

    @staticmethod
    def get_item_ui_common_coords():
        game_config = configUtilities.load_config()
        spell_item_info_item_imp_text_x = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                                      section='spellInfoPopup',
                                                                                      parameter='SP_IMPORTANT_TEXT_X')
        spell_item_info_start_x = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                              section='spellInfoPopup',
                                                                              parameter='SP_START_X')

        spell_item_info_start_y = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                              section='spellInfoPopup',
                                                                              parameter='SP_START_Y')
        spell_item_info_width = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                            section='spellInfoPopup',
                                                                            parameter='SP_WIDTH')
        spell_item_info_item_horz = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                                section='spellInfoPopup',
                                                                                parameter='SP_PORTRAIT_BAR')

        common_coords = [spell_item_info_item_imp_text_x, spell_item_info_start_x, spell_item_info_start_y,
                         spell_item_info_width, spell_item_info_item_horz]

        return common_coords

    @staticmethod
    def move_menu_selection(event_action, selected_menu_option, max_menu_option):
        if event_action in ('up', 'left'):
            selected_menu_option -= 1
            if selected_menu_option < 0:
                selected_menu_option = max_menu_option
        if event_action in ('down', 'right'):
            selected_menu_option += 1
            if selected_menu_option > max_menu_option:
                selected_menu_option = 0
        return selected_menu_option

    # the next 2 methods are used by dialogutilities to draw the scripted dialog box
    @staticmethod
    def draw_horiz_row_of_characters(start_x, start_y, width, height, glyph):
        for z in range(start_x, (start_x + width)):
            terminal.printf(x=z, y=(start_y + height), s=glyph)
            terminal.printf(x=z, y=start_y, s=glyph)

    @staticmethod
    def draw_vert_row_of_characters(start_x, start_y, width, height, glyph):
        for z in range(start_y, (start_y + height) - 1):
            terminal.printf(x=start_x, y=z + 1, s=glyph)
            terminal.printf(x=(start_x + width), y=z + 1, s=glyph)

    @staticmethod
    def draw_dialog_ui(gameworld, game_config, entity_speaking):
        # frame_components_list breakdown
        # [0] = top_left_corner_char
        # [1] = bottom_left_corner_char
        # [2] = top_right_corner_char
        # [3] = bottom_right_corner_char
        # [4] = horizontal_char
        # [5] = vertical_char
        # [6] = left_t_junction_char
        # [7] = right_t_junction_char

        unicode_string_to_print = '[font=dungeon][color=SPELLINFO_FRAME_COLOUR]['
        entity_names = MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=entity_speaking)
        frame_components_list = CommonUtils.get_ui_frame_components()

        dialog_frame_start_x = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                           section='gui',
                                                                           parameter='DIALOG_FRAME_START_X')
        dialog_frame_start_y = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                           section='gui',
                                                                           parameter='DIALOG_FRAME_START_Y')
        dialog_frame_width = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                         section='gui', parameter='DIALOG_FRAME_WIDTH')
        dialog_frame_height = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                          section='gui',
                                                                          parameter='DIALOG_FRAME_HEIGHT')
        # clear dialog space
        terminal.clear_area(dialog_frame_start_x, dialog_frame_start_y, dialog_frame_width, dialog_frame_height)
        # render horizontals
        CommonUtils.draw_horiz_row_of_characters(start_x=dialog_frame_start_x, start_y=dialog_frame_start_y,
                                                 width=dialog_frame_width, height=dialog_frame_height,
                                                 glyph=unicode_string_to_print + frame_components_list[4] + ']')

        # render verticals
        CommonUtils.draw_vert_row_of_characters(start_x=dialog_frame_start_x, start_y=dialog_frame_start_y,
                                                width=dialog_frame_width, height=dialog_frame_height,
                                                glyph=unicode_string_to_print + frame_components_list[5] + ']')

        # top left
        terminal.printf(x=dialog_frame_start_x, y=dialog_frame_start_y,
                        s=unicode_string_to_print + frame_components_list[0] + ']')
        # bottom left
        terminal.printf(x=dialog_frame_start_x, y=(dialog_frame_start_y + dialog_frame_height),
                        s=unicode_string_to_print + frame_components_list[1] + ']')
        # top right
        terminal.printf(x=(dialog_frame_start_x + dialog_frame_width), y=dialog_frame_start_y,
                        s=unicode_string_to_print + frame_components_list[2] + ']')
        # bottom right
        terminal.printf(x=(dialog_frame_start_x + dialog_frame_width),
                        y=(dialog_frame_start_y + dialog_frame_height),
                        s=unicode_string_to_print + frame_components_list[3] + ']')

        # npc/speaker name
        terminal.printf(x=dialog_frame_start_x + 3, y=dialog_frame_start_y, s="[[ " + entity_names[0] + " ]]")

    @staticmethod
    def camera_to_game_map_position(caster_screen_coords, game_config, gameworld, coords_to_check):
        player_entity = MobileUtilities.get_player_entity(gameworld, game_config)
        player_map_x = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=player_entity)
        player_map_y = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=player_entity)

        dist_x = abs(caster_screen_coords[0] - coords_to_check[0])
        dist_y = abs(caster_screen_coords[1] - coords_to_check[1])

        if caster_screen_coords[0] > coords_to_check[0]:
            posx = player_map_x - dist_x
        elif caster_screen_coords[0] < coords_to_check[0]:
            posx = player_map_x + dist_x
        else:
            posx = player_map_x

        if caster_screen_coords[1] > coords_to_check[1]:
            posy = player_map_y - dist_y
        elif caster_screen_coords[1] < coords_to_check[1]:
            posy = player_map_y + dist_y
        else:
            posy = player_map_y

        return posx, posy

    @staticmethod
    def to_camera_coordinates(game_config, game_map, x, y, gameworld):

        player_entity = MobileUtilities.get_player_entity(gameworld, game_config)
        player_map_pos_x = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=player_entity)
        player_map_pos_y = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=player_entity)

        camera_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                   parameter='VIEWPORT_WIDTH')
        camera_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='VIEWPORT_HEIGHT')

        camera_x, camera_y = CommonUtils.calculate_camera_position(camera_width=camera_width,
                                                                   camera_height=camera_height,
                                                                   player_map_pos_x=player_map_pos_x,
                                                                   player_map_pos_y=player_map_pos_y,
                                                                   game_map=game_map)

        (x, y) = (x - camera_x, y - camera_y)

        if x < 0 or y < 0 or x >= camera_width or y >= camera_height:
            return -99, -99  # if it's outside the view, return nothing

        return int(x), int(y)
