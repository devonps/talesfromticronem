from bearlibterminal import terminal
from loguru import logger

from components import mobiles, items
from utilities import configUtilities, common, display, gamemap, input_handlers, itemsHelp, jsonUtilities, mobileHelp, \
    spellHelp


class Debug:

    @staticmethod
    def helper_populate_es_lists(entity_spy_file):
        section_title = []
        section_heading = []
        section_lines = []
        section_width = []
        section_posx = []
        section_posy = []

        for section in entity_spy_file['es']:
            if section['title'] != 'frame':
                section_title.append(section['title'])
                section_heading.append(section['heading'])
                section_lines.append(section['lines'])
                section_width.append(section['width'])
                section_posx.append(section['posx'])
                section_posy.append(section['posy'])

        return section_title, section_heading, section_lines, section_width, section_posx, section_posy

    @staticmethod
    def helper_generate_es_click_zones(entity_spy_file):
        click_zones = []
        for section in entity_spy_file['es']:
            if section['title'] != 'frame':
                click_zones.append((section['posx'], section['posy'], section['width'], section['lines']))
        return click_zones

    @staticmethod
    def helper_clear_terminal_area_es(coords):
        start_panel_frame_x = coords[0]
        start_panel_frame_y = coords[1]
        start_panel_frame_width = coords[2]
        start_panel_frame_height = coords[3]

        terminal.clear_area(start_panel_frame_x, start_panel_frame_y, start_panel_frame_width + 1,
                            start_panel_frame_height)

    @staticmethod
    def helper_get_entity_map_position(gameworld, game_config, game_map, coords_clicked):
        player_entity = mobileHelp.MobileUtilities.get_player_entity(gameworld, game_config)
        player_map_x = mobileHelp.MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=player_entity)
        player_map_y = mobileHelp.MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=player_entity)
        camera_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                   parameter='VIEWPORT_WIDTH')
        camera_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='VIEWPORT_HEIGHT')

        screen_offset_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='SCREEN_OFFSET_X')
        screen_offset_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='SCREEN_OFFSET_Y')

        camera_x, camera_y = common.CommonUtils.calculate_camera_position(camera_width=camera_width,
                                                                          camera_height=camera_height,
                                                                          player_map_pos_x=player_map_x,
                                                                          player_map_pos_y=player_map_y,
                                                                          game_map=game_map)

        posx = coords_clicked[0] + camera_x - screen_offset_x
        posy = coords_clicked[1] + camera_y - screen_offset_y

        return posx, posy

    @staticmethod
    def helper_get_entity_type(gameworld, entity_id):
        entity_type = 'undefined'
        if gameworld.has_component(entity_id, mobiles.Name):
            entity_type = 'mobile'
        if gameworld.has_component(entity_id, items.Name):
            entity_type = itemsHelp.ItemUtilities.get_item_type(gameworld=gameworld, item_entity=entity_id)

        return entity_type

    @staticmethod
    def entity_spy(gameworld, game_config, coords_clicked, game_map):

        posx, posy = Debug.helper_get_entity_map_position(gameworld=gameworld, game_config=game_config, game_map=game_map,
                                                          coords_clicked=coords_clicked)
        entity_id = gamemap.GameMapUtilities.get_mobile_entity_at_this_location(game_map=game_map, x=posx, y=posy)

        if entity_id > 0:
            # get outerframe coords from json file
            es_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                 parameter='ENTITYSPYFILE')
            entity_spy_file = jsonUtilities.read_json_file(es_file)
            frame_coords_list = []
            for section in entity_spy_file['es']:
                if section['title'] == 'frame':
                    frame_coords_list.append(section['posx'])
                    frame_coords_list.append(section['posy'])
                    frame_coords_list.append(section['width'])
                    frame_coords_list.append(section['height'])

            # clear the underlying terminal
            Debug.helper_clear_terminal_area_es(coords=frame_coords_list)

            # draw a frame around the components
            display.draw_colourful_frame(title=' Entity Spy ', title_decorator=True, title_loc='centre',
                                         corner_decorator='',
                                         msg=4)

            # display page one of entity components
            Debug.display_page_one_entity_spy(gameworld=gameworld, entity_id=entity_id, game_config=game_config)

            # generate entity spy click zones
            click_zones = Debug.helper_generate_es_click_zones(entity_spy_file=entity_spy_file)

            # display instructions
            page_to_display = 1
            Debug.display_es_instructions(page=page_to_display)

            # blit the terminal
            terminal.refresh()

            # wait for user key press
            player_not_pressed_quit = True
            while player_not_pressed_quit:
                event_to_be_processed, event_action = input_handlers.handle_game_keys()
                player_not_pressed_quit, page_to_display = Debug.es_process_keyboard_actions(
                    event_to_be_processed=event_to_be_processed, event_action=event_action, game_config=game_config,
                    gameworld=gameworld, entity_id=entity_id, page_to_display=page_to_display, coords=frame_coords_list)

                # display instructions
                Debug.display_es_instructions(page=page_to_display)
                Debug.es_process_mouse_actions(event_to_be_processed=event_to_be_processed, event_action=event_action,
                                               click_zones=click_zones, page_to_display=page_to_display)

                # blit the terminal
                terminal.refresh()
        else:
            logger.info('No entity at location {}', coords_clicked)

    @staticmethod
    def es_process_keyboard_actions(event_to_be_processed, event_action, game_config, gameworld, entity_id,
                                    page_to_display, coords):
        player_not_pressed_quit = True
        if event_to_be_processed == 'keypress':
            if event_action == 'quit':
                player_not_pressed_quit = False
            if event_action == 'tab':
                Debug.helper_clear_terminal_area_es(coords=coords)
                page_to_display = Debug.helper_display_entity_spy_page(gameworld=gameworld, entity_id=entity_id,
                                                                       game_config=game_config,
                                                                       page_to_display=page_to_display)
        return player_not_pressed_quit, page_to_display

    @staticmethod
    def es_process_mouse_actions(event_to_be_processed, event_action, click_zones, page_to_display):
        if event_to_be_processed == 'mouseleftbutton':
            zone_clicked, item_selected = Debug.helper_get_zone_clicked(event_action, click_zones, page_to_display)
            Debug.process_zone_action(zone_clicked=zone_clicked, line_item=item_selected)

    @staticmethod
    def process_zone_action(zone_clicked, line_item):

        # if an invalid zone_clicked is passed then my Switch statement will come here
        def default(line):
            logger.info('No component zone found.')

        def es_amendment_racial(line):
            logger.info('Racial zone activated and line {}', line)

            manual_input = terminal.read_str(x=10, y=10, max=10, s=5)
            logger.info('What was typed: {}', manual_input)

        def es_amendment_names(line):
            logger.info('Names zone activated and line {}', line)

        def es_amendment_weapons(line):
            logger.info('Weapons zone activated and line {}', line)

        def es_amendment_jewellery(line):
            logger.info('Jewellery zone activated and line {}', line)

        def es_amendment_spellbarcombat(line):
            logger.info('Combat spells zone activated and line {}', line)

        def es_amendment_spellbarutils(line):
            logger.info('Utility spells zone activated and line {}', line)

        def es_amendment_energy(line):
            logger.info('energy zone activated and line {}', line)

        def es_amendment_monster(line):
            logger.info('Monster zone activated and line {}', line)

        def es_amendment_armour(line):
            logger.info('armour zone activated and line {}', line)

        def es_amendment_primary(line):
            logger.info('primary stats zone activated and line {}', line)

        def es_amendment_secondary(line):
            logger.info('secondary stats zone activated and line {}', line)

        def es_amendment_derived(line):
            logger.info('derived zone activated and line {}', line)

        def es_amendment_statuseffects(line):
            logger.info('status effects zone activated and line {}', line)

        switcher = {0: es_amendment_racial,
                    1: es_amendment_names,
                    2: es_amendment_weapons,
                    3: es_amendment_jewellery,
                    4: es_amendment_spellbarcombat,
                    5: es_amendment_spellbarutils,
                    6: es_amendment_energy,
                    7: es_amendment_monster,
                    8: es_amendment_armour,
                    9: es_amendment_primary,
                    10: es_amendment_secondary,
                    11: es_amendment_derived,
                    12: es_amendment_statuseffects
                    }

        switcher.get(zone_clicked, default)(line=line_item)

    @staticmethod
    def helper_display_entity_spy_page(gameworld, page_to_display, entity_id, game_config):
        page_to_display += 1
        if page_to_display > 2:
            page_to_display = 1
        if page_to_display == 1:
            Debug.display_page_one_entity_spy(gameworld=gameworld, entity_id=entity_id, game_config=game_config)
        else:
            Debug.display_page_two_entity_spy(gameworld=gameworld, entity_id=entity_id, game_config=game_config)

        return page_to_display

    @staticmethod
    def helper_get_zone_clicked(event_action, click_zones, page_to_display):
        mx = event_action[0]
        my = event_action[1]

        click_zone_left = 0
        click_zone_top = 1
        click_zone_width = 2
        click_zone_depth = 3

        zone_clicked = -99
        item_selected = -99

        if page_to_display == 1:
            zone_min = 0
            zone_max = 7
        else:
            zone_min = 7
            zone_max = 13

        for zone in range(zone_min, zone_max):

            mx_in_range = Debug.helper_check_zones(zone=zone, click_zone_one=click_zones[zone][click_zone_left],
                                                   check_point=mx,
                                                   click_zone_two=click_zones[zone][click_zone_left] + click_zones[zone][
                                                click_zone_width])
            my_in_range = Debug.helper_check_zones(zone=zone, click_zone_one=click_zones[zone][click_zone_top], check_point=my,
                                                   click_zone_two=click_zones[zone][click_zone_top] + click_zones[zone][
                                                click_zone_depth])

            if mx_in_range and my_in_range:
                zone_clicked = zone
                item_selected = my - click_zones[zone][click_zone_top]
        return zone_clicked, item_selected

    @staticmethod
    def helper_check_zones(zone, click_zone_one, check_point, click_zone_two):
        check_point_in_range = False
        if click_zone_one <= check_point <= click_zone_two:
            check_point_in_range = True
        return check_point_in_range

    @staticmethod
    def display_es_instructions(page):
        string_to_print = "[color=ENTITY_SPY_INSTRUCTIONS]Press tab for next page"
        terminal.print_(x=6, y=3, s=string_to_print)

        string_to_print = "[color=ENTITY_SPY_INSTRUCTIONS]Page:" + str(page) + "/2"
        terminal.print_(x=70, y=3, s=string_to_print)

    @staticmethod
    def display_page_one_entity_spy(gameworld, game_config, entity_id):
        # read Json file for on-screen placement
        es_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                             parameter='ENTITYSPYFILE')
        entity_spy_file = jsonUtilities.read_json_file(es_file)

        section_title, section_heading, section_lines, section_width, section_posx, section_posy = Debug.helper_populate_es_lists(
            entity_spy_file)

        #
        # DRAW THE UI
        #
        section = 0
        start_string = "[color=ENTITY_SPY_COMPONENT]"
        end_string = "[/color]"

        display.draw_colourful_frame(title=" Entity Spy ", title_decorator=True, title_loc='centre',
                                     corner_decorator='', msg=4)

        display.draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                                  start_panel_frame_width=section_width[section],
                                  start_panel_frame_height=section_lines[section], title=section_heading[section])

        race_details = mobileHelp.MobileUtilities.get_mobile_race_details(gameworld=gameworld, entity=entity_id)
        string_to_print = start_string + "Race:" + end_string + race_details[0]
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 2, s=string_to_print)

        class_print = start_string + "Class:" + end_string + mobileHelp.MobileUtilities.get_character_class(
            gameworld=gameworld, entity=entity_id)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 3, s=class_print)

        glyph_print = start_string + "Glyph:" + end_string + mobileHelp.MobileUtilities.get_mobile_glyph(
            gameworld=gameworld, entity=entity_id)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 4, s=glyph_print)

        #
        # ENTITY PERSONAL DETAILS
        #
        section = 1
        display.draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                                  start_panel_frame_width=section_width[section],
                                  start_panel_frame_height=section_lines[section], title=section_heading[section])

        entity_names = mobileHelp.MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=entity_id)
        first_name_string = start_string + "First Name:" + end_string + entity_names[0]
        gender_string = start_string + "Gender:" + end_string + mobileHelp.MobileUtilities.get_mobile_gender(
            gameworld=gameworld, entity=entity_id)

        personality_string = start_string + "Personality:" + end_string + mobileHelp.MobileUtilities.get_mobile_personality_title(
            gameworld=gameworld, entity=entity_id)

        ai_description = mobileHelp.MobileUtilities.get_mobile_ai_description(gameworld=gameworld, entity_id=entity_id)

        ai_level_string = start_string + "AI level:" + end_string + ai_description
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 2, s=first_name_string)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 3, s=gender_string)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 4, s=ai_level_string)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 5, s=personality_string)

        #
        # WEAPONS
        #
        section = 2
        display.draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                                  start_panel_frame_width=section_width[section],
                                  start_panel_frame_height=section_lines[section], title=section_heading[section])

        weapons_list = mobileHelp.MobileUtilities.get_weapons_equipped(gameworld=gameworld, entity=entity_id)
        main_weapon = weapons_list[0]
        off_weapon = weapons_list[1]
        both_weapon = weapons_list[2]

        both_hands = display.set_both_hands_weapon_string_es(gameworld=gameworld, both_weapon=both_weapon)
        main_hand = display.set_main_hand_weapon_string_es(main_weapon=main_weapon, gameworld=gameworld)
        off_hand = display.set_off_hand_weapon_string_es(off_weapon=off_weapon, gameworld=gameworld)

        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 2, s=both_hands)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 3, s=main_hand)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 4, s=off_hand)

        #
        # JEWELLERY
        #
        section = 3
        display.draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                                  start_panel_frame_width=section_width[section],
                                  start_panel_frame_height=section_lines[section], title=section_heading[section])

        equipped_jewellery = mobileHelp.MobileUtilities.get_jewellery_already_equipped(gameworld=gameworld,
                                                                                       mobile=entity_id)
        if equipped_jewellery[0] > 0:
            left_ear = display.set_jewellery_left_ear_string(gameworld=gameworld, left_ear=equipped_jewellery[0])
            terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 2, s=left_ear)
        if equipped_jewellery[1] > 0:
            right_ear = display.set_jewellery_right_ear_string(gameworld=gameworld, right_ear=equipped_jewellery[1])
            terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 3, s=right_ear)
        if equipped_jewellery[2] > 0:
            left_hand = display.set_jewellery_left_hand_string(gameworld=gameworld, left_hand=equipped_jewellery[2])
            terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 4, s=left_hand)
        if equipped_jewellery[3] > 0:
            right_hand = display.set_jewellery_right_hand_string(gameworld=gameworld, right_hand=equipped_jewellery[3])
            terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 5, s=right_hand)
        if equipped_jewellery[4] > 0:
            neck = display.set_jewellery_neck_string(gameworld=gameworld, neck=equipped_jewellery[4])
            terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 6, s=neck)

        # display armour
        section = 8

        display.draw_colourful_frame(title='-Entity Spy-', title_decorator=True, title_loc='centre',
                                     corner_decorator='', msg=4)

        display.draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                                  start_panel_frame_width=section_width[section],
                                  start_panel_frame_height=section_lines[section],
                                  title=section_heading[section])

        str_to_print = "[color=blue]Location Mat/Disp/Def[/color]"

        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 2, s=str_to_print)

        item_head = display.get_head_armour_details(gameworld=gameworld, entity_id=entity_id)
        if len(item_head) == 1:
            str_to_print = item_head[0]
        else:
            str_to_print = item_head[0] + item_head[1] + '/' + item_head[2] + '/' + item_head[3]
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 4, s=str_to_print)

        item_head = display.get_chest_armour_details(gameworld=gameworld, entity_id=entity_id)
        if len(item_head) == 1:
            str_to_print = item_head[0]
        else:
            str_to_print = item_head[0] + item_head[1] + '/' + item_head[2] + '/' + item_head[3]
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 5, s=str_to_print)

        item_head = display.get_hands_armour_details(gameworld=gameworld, entity_id=entity_id)
        if len(item_head) == 1:
            str_to_print = item_head[0]
        else:
            str_to_print = item_head[0] + item_head[1] + '/' + item_head[2] + '/' + item_head[3]
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 6, s=str_to_print)

        item_head = display.get_legs_armour_details(gameworld=gameworld, entity_id=entity_id)
        if len(item_head) == 1:
            str_to_print = item_head[0]
        else:
            str_to_print = item_head[0] + item_head[1] + '/' + item_head[2] + '/' + item_head[3]
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 7, s=str_to_print)

        item_head = display.get_feet_armour_details(gameworld=gameworld, entity_id=entity_id)
        if len(item_head) == 1:
            str_to_print = item_head[0]
        else:
            str_to_print = item_head[0] + item_head[1] + '/' + item_head[2] + '/' + item_head[3]
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 8, s=str_to_print)

        #
        # SPELL BAR COMBAT
        #
        section = 4
        display.draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                                  start_panel_frame_width=section_width[section],
                                  start_panel_frame_height=section_lines[section], title=section_heading[section])

        slot_one = Debug.set_spellbar_slot_string(gameworld=gameworld, entity_id=entity_id, slotid=0)
        slot_two = Debug.set_spellbar_slot_string(gameworld=gameworld, entity_id=entity_id, slotid=1)
        slot_three = Debug.set_spellbar_slot_string(gameworld=gameworld, entity_id=entity_id, slotid=2)
        slot_four = Debug.set_spellbar_slot_string(gameworld=gameworld, entity_id=entity_id, slotid=3)
        slot_five = Debug.set_spellbar_slot_string(gameworld=gameworld, entity_id=entity_id, slotid=4)

        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 2, s=slot_one)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 3, s=slot_two)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 4, s=slot_three)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 5, s=slot_four)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 6, s=slot_five)

        #
        # SPELL BAR UTILITIES
        #
        section = 5
        display.draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                                  start_panel_frame_width=section_width[section],
                                  start_panel_frame_height=section_lines[section], title=section_heading[section])

        slot_six = Debug.set_spellbar_slot_string(gameworld=gameworld, entity_id=entity_id, slotid=5)
        slot_seven = Debug.set_spellbar_slot_string(gameworld=gameworld, entity_id=entity_id, slotid=6)
        slot_eight = Debug.set_spellbar_slot_string(gameworld=gameworld, entity_id=entity_id, slotid=7)
        slot_nine = Debug.set_spellbar_slot_string(gameworld=gameworld, entity_id=entity_id, slotid=8)

        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 2, s=slot_six)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 3, s=slot_seven)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 4, s=slot_eight)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 5, s=slot_nine)

        #
        # ENERGY BARS
        #
        section = 6
        display.draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                                  start_panel_frame_width=section_width[section],
                                  start_panel_frame_height=section_lines[section], title=section_heading[section])
        current_health_value = mobileHelp.MobileUtilities.get_mobile_derived_current_health(gameworld=gameworld,
                                                                                            entity=entity_id)
        max_health_value = mobileHelp.MobileUtilities.get_mobile_derived_maximum_health(gameworld=gameworld,
                                                                                        entity=entity_id)

        current_f1_value = mobileHelp.MobileUtilities.get_mobile_derived_special_bar_current_value(gameworld=gameworld,
                                                                                                   entity=entity_id)
        max_f1_value = mobileHelp.MobileUtilities.get_mobile_derived_special_bar_max_value(gameworld=gameworld,
                                                                                           entity=entity_id)

        health_string = start_string + "Health:" + end_string + str(current_health_value) + " of " + str(
            max_health_value)
        f1_string = start_string + "Special:" + end_string + str(current_f1_value) + " of " + str(max_f1_value)

        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 2, s=health_string)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 4, s=f1_string)

        #
        # MONSTER SPECIFICS
        #
        # section = 7
        # Debug.draw_monster_specific_components(gameworld=gameworld, entity_id=entity_id, sx=section_posx[section],
        #                                        sy=section_posy[section],
        #                                        sw=section_width[section], sl=section_lines[section],
        #                                        sh=section_heading[section])

    @staticmethod
    def display_page_two_entity_spy(gameworld, entity_id, game_config):

        # read Json file for on-screen placement
        es_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                             parameter='ENTITYSPYFILE')
        entity_spy_file = jsonUtilities.read_json_file(es_file)

        section_title, section_heading, section_lines, section_width, section_posx, section_posy = Debug.helper_populate_es_lists(
            entity_spy_file)

        # display primary attributes
        section = 9
        display.draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                                  start_panel_frame_width=section_width[section],
                                  start_panel_frame_height=section_lines[section], title=section_heading[section])

        entity_power = mobileHelp.MobileUtilities.get_mobile_primary_power(gameworld=gameworld, entity=entity_id)
        entity_precision = mobileHelp.MobileUtilities.get_mobile_primary_precision(gameworld=gameworld,
                                                                                   entity=entity_id)
        entity_toughness = mobileHelp.MobileUtilities.get_mobile_primary_toughness(gameworld=gameworld,
                                                                                   entity=entity_id)
        entity_vitality = mobileHelp.MobileUtilities.get_mobile_primary_vitality(gameworld=gameworld, entity=entity_id)

        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 2,
                        s="[color=ENTITY_SPY_COMPONENT]Power:[/color]" + str(entity_power))
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 3,
                        s="[color=ENTITY_SPY_COMPONENT]Precision:[/color]" + str(entity_precision))
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 4,
                        s="[color=ENTITY_SPY_COMPONENT]Toughness:[/color]" + str(entity_toughness))
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 5,
                        s="[color=ENTITY_SPY_COMPONENT]Vitality:[/color]" + str(entity_vitality))

        # display secondary attributes
        section = 10
        display.draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                                  start_panel_frame_width=section_width[section],
                                  start_panel_frame_height=section_lines[section], title=section_heading[section])

        entity_concentration = mobileHelp.MobileUtilities.get_mobile_secondary_concentration(gameworld=gameworld,
                                                                                             entity=entity_id)
        entity_condi_damage = mobileHelp.MobileUtilities.get_mobile_secondary_condition_damage(gameworld=gameworld,
                                                                                               entity=entity_id)
        entity_expertise = mobileHelp.MobileUtilities.get_mobile_secondary_expertise(gameworld=gameworld,
                                                                                     entity=entity_id)
        entity_ferocity = mobileHelp.MobileUtilities.get_mobile_secondary_ferocity(gameworld=gameworld,
                                                                                   entity=entity_id)
        entity_healing_power = mobileHelp.MobileUtilities.get_mobile_secondary_healing_power(gameworld=gameworld,
                                                                                             entity=entity_id)

        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 2,
                        s="[color=ENTITY_SPY_COMPONENT]Concentration:[/color]" + str(entity_concentration))
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 3,
                        s="[color=ENTITY_SPY_COMPONENT]Condition Damage:[/color]" + str(entity_condi_damage))
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 4,
                        s="[color=ENTITY_SPY_COMPONENT]Expertise:[/color]" + str(entity_expertise))
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 5,
                        s="[color=ENTITY_SPY_COMPONENT]Ferocity:[/color]" + str(entity_ferocity))
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 6,
                        s="[color=ENTITY_SPY_COMPONENT]Healing Power:[/color]" + str(entity_healing_power))

        # display derived attributes
        section = 11
        display.draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                                  start_panel_frame_width=section_width[section],
                                  start_panel_frame_height=section_lines[section], title=section_heading[section])

        entity_boon_duration = mobileHelp.MobileUtilities.get_mobile_derived_boon_duration(gameworld=gameworld,
                                                                                           entity=entity_id)

        entity_critical_chance = mobileHelp.MobileUtilities.get_mobile_derived_critical_hit_chance(gameworld=gameworld,
                                                                                                   entity=entity_id)
        entity_critical_damage = mobileHelp.MobileUtilities.get_mobile_derived_critical_damage(gameworld=gameworld,
                                                                                               entity=entity_id)
        entity_condi_duration = mobileHelp.MobileUtilities.get_mobile_derived_condition_duration(gameworld=gameworld,
                                                                                                 entity=entity_id)
        total_armour = mobileHelp.MobileUtilities.get_mobile_derived_armour_value(gameworld=gameworld, entity=entity_id)

        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 2,
                        s="[color=ENTITY_SPY_COMPONENT]Boon Duration:[/color]+" + str(entity_boon_duration))
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 3,
                        s="[color=ENTITY_SPY_COMPONENT]Critical Chance:[/color]" + str(entity_critical_chance) + "%")
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 4,
                        s="[color=ENTITY_SPY_COMPONENT]Critical Damage:[/color]" + str(entity_critical_damage) + "%")
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 5,
                        s="[color=ENTITY_SPY_COMPONENT]Condition Duration:[/color]+" + str(entity_condi_duration))
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 6,
                        s="[color=ENTITY_SPY_COMPONENT]Defense:[/color]" + str(total_armour))

        # display applied status effects
        section = 12
        display.draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                                  start_panel_frame_width=section_width[section],
                                  start_panel_frame_height=section_lines[section], title=section_heading[section])

        applied_boons = mobileHelp.MobileUtilities.get_current_boons_applied_to_mobile(gameworld=gameworld,
                                                                                       entity=entity_id)
        applied_condis = mobileHelp.MobileUtilities.get_current_condis_applied_to_mobile(gameworld=gameworld,
                                                                                         entity=entity_id)

        boons_to_print = Debug.set_boons_to_print(applied_boons=applied_boons)
        condis_to_print = Debug.set_condis_to_print(applied_condis=applied_condis)

        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 2,
                        s="[color=ENTITY_SPY_COMPONENT]Boons:[/color]" + boons_to_print)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 3,
                        s="[color=ENTITY_SPY_COMPONENT]Conditions:[/color]" + condis_to_print)

    @staticmethod
    def set_boons_to_print(applied_boons):
        boons_to_print = "[color=ENTITY_SPY_NO_COMPONENT]none[/color]"
        if len(applied_boons) > 0:
            boons_to_print = ''.join(applied_boons)
        return boons_to_print

    @staticmethod
    def set_condis_to_print(applied_condis):
        condis_to_print = '[color=ENTITY_SPY_NO_COMPONENT]none[/color]'
        if len(applied_condis) > 0:
            condis_to_print = "".join(applied_condis)
        return condis_to_print

    @staticmethod
    def draw_monster_specific_components(gameworld, entity_id, sx, sy, sw, sl, sh):
        ai_level = int(mobileHelp.MobileUtilities.get_mobile_ai_level(gameworld=gameworld, entity_id=entity_id))
        start_string = "[color=ENTITY_SPY_COMPONENT]"
        end_string = "[/color]"

        if ai_level > 1:
            display.draw_simple_frame(start_panel_frame_x=sx, start_panel_frame_y=sy,
                                      start_panel_frame_width=sw,
                                      start_panel_frame_height=sl, title=sh)

            pref_min_attack_range = mobileHelp.MobileUtilities.get_enemy_preferred_min_range(gameworld=gameworld,
                                                                                             entity=entity_id)
            pre_max_attack_range = mobileHelp.MobileUtilities.get_enemy_preferred_max_range(gameworld=gameworld,
                                                                                            entity=entity_id)
            combat_role = mobileHelp.MobileUtilities.get_enemy_combat_role(gameworld=gameworld, entity=entity_id)

            min_range_string = start_string + "Pref min attack range:" + end_string + str(pref_min_attack_range)
            max_range_string = start_string + "Pref max attack range:" + end_string + str(pre_max_attack_range)
            combat_role_string = start_string + "Combat Role:" + end_string + str(combat_role)

            terminal.print_(x=sx + 1, y=sy + 2, s=min_range_string)
            terminal.print_(x=sx + 1, y=sy + 3, s=str(max_range_string))
            terminal.print_(x=sx + 1, y=sy + 4, s=str(combat_role_string))

    @staticmethod
    def set_spellbar_slot_string(gameworld, entity_id, slotid):
        spell_bar_slot = slotid + 1
        slot_string = "[color=ENTITY_SPY_NO_COMPONENT]Slot " + str(spell_bar_slot) + ":None[/color]"
        slot_spell_entity = spellHelp.SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=gameworld,
                                                                                         slot=slotid,
                                                                                         player_entity=entity_id)
        if slot_spell_entity > 0:
            spell_name = spellHelp.SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=slot_spell_entity)
            slot_string = "[color=ENTITY_SPY_COMPONENT]Slot " + str(spell_bar_slot) + ":[/color]" + spell_name

        return slot_string
