from bearlibterminal import terminal
from loguru import logger

from mapRelated.gameMap import RenderLayer
from utilities import colourUtilities, configUtilities
from utilities.common import CommonUtils
from utilities.display import draw_simple_frame, draw_colourful_frame
from utilities.input_handlers import handle_game_keys
from utilities.itemsHelp import ItemUtilities
from utilities.jsonUtilities import read_json_file
from utilities.mobileHelp import MobileUtilities


class Debug:

    @staticmethod
    def populate_es_lists(entity_spy_file):
        section_title = []
        section_heading = []
        section_lines = []
        section_width = []
        section_posx = []
        section_posy = []

        for section in entity_spy_file['es']:
            section_title.append(section['title'])
            section_heading.append(section['heading'])
            section_lines.append(section['lines'])
            section_width.append(section['width'])
            section_posx.append(section['posx'])
            section_posy.append(section['posy'])

        return section_title, section_heading, section_lines, section_width, section_posx, section_posy

    @staticmethod
    def clear_terminal_area_es(game_config):
        start_panel_frame_x = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                          'START_PANEL_FRAME_X')
        start_panel_frame_y = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                          'START_PANEL_FRAME_Y')
        start_panel_frame_width = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                              'START_PANEL_FRAME_WIDTH')
        start_panel_frame_height = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                               'START_PANEL_FRAME_HEIGHT')

        terminal.clear_area(start_panel_frame_x, start_panel_frame_y, start_panel_frame_width + 20,
                            start_panel_frame_height)

    @staticmethod
    def entity_spy(gameworld, game_config, coords):
        # get entity id at position coords
        entity_id = CommonUtils.get_entity_at_location(gameworld=gameworld, coords=coords)

        if entity_id == 0:
            logger.debug('Entity not found at location')
        else:
            # read Json file for on-screen placement
            es_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                 parameter='ENTITYSPYFILE')
            entity_spy_file = read_json_file(es_file)

            section_title, section_heading, section_lines, section_width, section_posx, section_posy = Debug.populate_es_lists(entity_spy_file)


            # display entity information
            Debug.clear_terminal_area_es(game_config=game_config)

            draw_colourful_frame(title=' Entity Spy ', title_decorator=True, title_loc='centre',
                                 corner_decorator='', corner_studs='square',
                                 msg=4)

            end_string = "[/color]"
            instruction_start_string = "[color=yellow]"
            string_to_print = instruction_start_string + "Press tab for next page" + end_string
            terminal.print_(x=6, y=3, s=string_to_print)



            Debug.display_page_one_entity_spy(gameworld=gameworld, entity_id=entity_id, section_posx=section_posx,
                                              section_posy=section_posy, section_width=section_width,
                                              section_lines=section_lines, section_heading=section_heading)

            # blit the terminal
            terminal.refresh()
            page_to_display = 1

            # wait for user key press
            # validTargets[ent, name.first, desc.glyph, desc.foreground, desc.background]
            player_not_pressed_a_key = True
            while player_not_pressed_a_key:
                event_to_be_processed, event_action = handle_game_keys()
                if event_to_be_processed == 'keypress':
                    if event_action == 'quit':
                        player_not_pressed_a_key = False
                    if event_action == 'tab':
                        Debug.clear_terminal_area_es(game_config=game_config)
                        page_to_display += 1
                        if page_to_display > 2:
                            page_to_display = 1
                        if page_to_display == 1:
                            Debug.display_page_one_entity_spy(gameworld=gameworld, entity_id=entity_id,
                                                              section_posx=section_posx,
                                                              section_posy=section_posy, section_width=section_width,
                                                              section_lines=section_lines, section_heading=section_heading)
                        else:

                            Debug.display_page_two_entity_spy(gameworld=gameworld, entity_id=entity_id,
                                                              section_posx=section_posx,
                                                              section_posy=section_posy, section_width=section_width,
                                                              section_lines=section_lines, section_heading=section_heading)
                        # blit the terminal
                        terminal.refresh()

    @staticmethod
    def display_page_one_entity_spy(section_posx, section_posy, section_width, section_lines, section_heading,
                                    gameworld, entity_id):
        section = 0
        start_string = "[color=orange]"
        end_string = "[/color]"

        draw_colourful_frame(title=" Entity Spy ", title_decorator=True, title_loc='centre',
                             corner_decorator='', corner_studs='square', msg=4)

        draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                          start_panel_frame_width=section_width[section],
                          start_panel_frame_height=section_lines[section], title=section_heading[section],
                          fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))
        race_details = MobileUtilities.get_mobile_race_details(gameworld=gameworld, entity=entity_id)
        string_to_print = start_string + "Race:" + end_string + race_details[0]
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 2, s=string_to_print)
        class_print = start_string + "Class:" + end_string + MobileUtilities.get_character_class(
            gameworld=gameworld, entity=entity_id)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 3, s=class_print)
        glyph_print = start_string + "Glyph:" + end_string + MobileUtilities.get_mobile_glyph(
            gameworld=gameworld, entity=entity_id)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 4, s=glyph_print)

        section = 1
        draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                          start_panel_frame_width=section_width[section],
                          start_panel_frame_height=section_lines[section], title=section_heading[section],
                          fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))
        entity_names = MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=entity_id)
        first_name_string = start_string + "First Name:" + end_string + entity_names[0]
        gender_string = start_string + "Gender:" + end_string + MobileUtilities.get_player_gender(
            gameworld=gameworld, entity=entity_id)
        personality_string = start_string + "Personality:" + end_string + MobileUtilities.get_mobile_personality_title(
            gameworld=gameworld, entity=entity_id)
        ai_level_string = start_string + "AI level:" + end_string + str(
            MobileUtilities.get_mobile_ai_level(gameworld=gameworld, entity_id=entity_id))
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 2, s=first_name_string)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 4, s=personality_string)
        terminal.print_(x=section_posx[section] + len("First Name:" + entity_names[0]) + 2, y=section_posy[section] + 2,
                        s=gender_string)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 3, s=ai_level_string)

        section = 2
        no_item = "[color=gray]"
        draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                          start_panel_frame_width=section_width[section],
                          start_panel_frame_height=section_lines[section], title=section_heading[section],
                          fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))
        weapons_list = MobileUtilities.get_weapons_equipped(gameworld=gameworld, entity=entity_id)
        main_weapon = weapons_list[0]
        off_weapon = weapons_list[1]
        both_weapon = weapons_list[2]

        both_hands_weapon_name = no_item + "none" + end_string
        main_hand_weapon_name = no_item + "none" + end_string
        off_hand_weapon_name = no_item + "none" + end_string
        main_hand = start_string + "Main Hand:" + end_string
        both_hands = start_string + "Both Hands:" + end_string
        off_hand = start_string + "Off Hand:" + end_string

        if both_weapon > 0:
            both_hands_weapon_name = ItemUtilities.get_item_name(gameworld=gameworld, entity=both_weapon)
        else:
            main_hand_weapon_name = ItemUtilities.get_item_name(gameworld=gameworld, entity=main_weapon)
            off_hand_weapon_name = ItemUtilities.get_item_name(gameworld=gameworld, entity=off_weapon)

        if both_hands_weapon_name != '':
            both_hands += both_hands_weapon_name + end_string

        if main_hand_weapon_name != '':
            main_hand += main_hand_weapon_name + end_string

        if off_hand_weapon_name != '':
            off_hand += off_hand_weapon_name + end_string

        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 2, s=both_hands)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 3, s=main_hand)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 4, s=off_hand)

        section = 3
        draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                          start_panel_frame_width=section_width[section],
                          start_panel_frame_height=section_lines[section], title=section_heading[section],
                          fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))
        no_left_ear = no_item + "none" + end_string
        no_right_ear = no_item + "none" + end_string
        no_left_hand = no_item + "none" + end_string
        no_right_hand = no_item + "none" + end_string
        no_neck = no_item + "none" + end_string

        equipped_jewellery = MobileUtilities.get_jewellery_already_equipped(gameworld=gameworld, mobile=entity_id)


        # section = 0
            # draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section], start_panel_frame_width=section_width[section], start_panel_frame_height=section_lines[section], title=section_heading[section], fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))
            #
            # section = 0
            # draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section], start_panel_frame_width=section_width[section], start_panel_frame_height=section_lines[section], title=section_heading[section], fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))
            #
            # section = 0
            # draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section], start_panel_frame_width=section_width[section], start_panel_frame_height=section_lines[section], title=section_heading[section], fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))
            #
            # section = 0
            # draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section], start_panel_frame_width=section_width[section], start_panel_frame_height=section_lines[section], title=section_heading[section], fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))
            #



    @staticmethod
    def display_page_two_entity_spy(section_posx, section_posy, section_width, section_lines, section_heading,
                                    gameworld, entity_id):

        section = 8
        start_string = "[color=orange]"
        end_string = "[/color]"

        draw_colourful_frame(title=' Entity Spy ', title_decorator=True, title_loc='centre',
                             corner_decorator='', corner_studs='square', msg=4)

        draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                          start_panel_frame_width=section_width[section],
                          start_panel_frame_height=section_lines[section], title=section_heading[section],
                          fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))

    # section = 0
    # draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section], start_panel_frame_width=section_width[section], start_panel_frame_height=section_lines[section], title=section_heading[section], fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))
    #
    # section = 0
    # draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section], start_panel_frame_width=section_width[section], start_panel_frame_height=section_lines[section], title=section_heading[section], fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))
    #
    # section = 0
    # draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section], start_panel_frame_width=section_width[section], start_panel_frame_height=section_lines[section], title=section_heading[section], fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))
    #
    # section = 0
    # draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section], start_panel_frame_width=section_width[section], start_panel_frame_height=section_lines[section], title=section_heading[section], fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))
    #
    # section = 0
    # draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section], start_panel_frame_width=section_width[section], start_panel_frame_height=section_lines[section], title=section_heading[section], fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))
    #
