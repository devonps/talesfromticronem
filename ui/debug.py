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
from utilities.spellHelp import SpellUtilities


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
        logger.debug('Entity id at this location {}', entity_id)

        if entity_id > 0:
            # read Json file for on-screen placement
            es_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                 parameter='ENTITYSPYFILE')
            entity_spy_file = read_json_file(es_file)

            section_title, section_heading, section_lines, section_width, section_posx, section_posy = Debug.populate_es_lists(
                entity_spy_file)

            # clear the underlying terminal
            Debug.clear_terminal_area_es(game_config=game_config)

            # draw a frame around the components
            draw_colourful_frame(title=' Entity Spy ', title_decorator=True, title_loc='centre',
                                 corner_decorator='', corner_studs='square',
                                 msg=4)

            # display page one of entity components
            Debug.display_page_one_entity_spy(gameworld=gameworld, entity_id=entity_id, section_posx=section_posx,
                                              section_posy=section_posy, section_width=section_width,
                                              section_lines=section_lines, section_heading=section_heading)

            # display instructions
            page_to_display = 1
            Debug.display_es_instructions(page=page_to_display)

            # blit the terminal
            terminal.refresh()

            # wait for user key press
            player_not_pressed_quit = True
            while player_not_pressed_quit:
                event_to_be_processed, event_action = handle_game_keys()
                # if event_to_be_processed == 'keypress':
                if event_action == 'quit':
                    player_not_pressed_quit = False
                if event_action == 'tab':
                    Debug.clear_terminal_area_es(game_config=game_config)
                    page_to_display += 1
                    if page_to_display > 2:
                        page_to_display = 1
                    if page_to_display == 1:
                        Debug.display_page_one_entity_spy(gameworld=gameworld, entity_id=entity_id,
                                                          section_posx=section_posx,
                                                          section_posy=section_posy, section_width=section_width,
                                                          section_lines=section_lines,
                                                          section_heading=section_heading)
                    else:

                        Debug.display_page_two_entity_spy(gameworld=gameworld, entity_id=entity_id,
                                                          section_posx=section_posx,
                                                          section_posy=section_posy, section_width=section_width,
                                                          section_lines=section_lines,
                                                          section_heading=section_heading)
                    # display instructions
                    Debug.display_es_instructions(page=page_to_display)

                    # blit the terminal
                    terminal.refresh()

    @staticmethod
    def display_es_instructions(page):
        instruction_start_string = "[color=ENTITY_SPY_INSTRUCTIONS]"
        string_to_print = instruction_start_string + "Press tab for next page"
        terminal.print_(x=6, y=3, s=string_to_print)

        string_to_print = instruction_start_string + "Page:" + str(page) + "/2"
        terminal.print_(x=70, y=3, s=string_to_print)

    @staticmethod
    def display_page_one_entity_spy(section_posx, section_posy, section_width, section_lines, section_heading,
                                    gameworld, entity_id):
        section = 0
        start_string = "[color=ENTITY_SPY_COMPONENT]"
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
        ai_level = int(MobileUtilities.get_mobile_ai_level(gameworld=gameworld, entity_id=entity_id))

        if ai_level == 1:
            ai_string = "Player"
        else:
            ai_string = "Monster"

        ai_level_string = start_string + "AI level:" + end_string + ai_string
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 2, s=first_name_string)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 4, s=personality_string)
        terminal.print_(x=section_posx[section] + len("First Name:" + entity_names[0]) + 2, y=section_posy[section] + 2,
                        s=gender_string)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 3, s=ai_level_string)

        section = 2
        draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                          start_panel_frame_width=section_width[section],
                          start_panel_frame_height=section_lines[section], title=section_heading[section],
                          fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))
        weapons_list = MobileUtilities.get_weapons_equipped(gameworld=gameworld, entity=entity_id)
        main_weapon = weapons_list[0]
        off_weapon = weapons_list[1]
        both_weapon = weapons_list[2]

        both_hands = Debug.set_both_hands_weapon_string_es(gameworld=gameworld, both_weapon=both_weapon)
        main_hand = Debug.set_main_hand_weapon_string_es(main_weapon=main_weapon, gameworld=gameworld)
        off_hand = Debug.set_off_hand_weapon_string_es(off_weapon=off_weapon, gameworld=gameworld)

        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 2, s=both_hands)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 3, s=main_hand)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 4, s=off_hand)

        section = 3
        draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                          start_panel_frame_width=section_width[section],
                          start_panel_frame_height=section_lines[section], title=section_heading[section],
                          fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))

        equipped_jewellery = MobileUtilities.get_jewellery_already_equipped(gameworld=gameworld, mobile=entity_id)
        left_ear = Debug.set_jewellery_left_ear_string(gameworld=gameworld, left_ear=equipped_jewellery[0])
        right_ear = Debug.set_jewellery_right_ear_string(gameworld=gameworld, right_ear=equipped_jewellery[1])
        left_hand = Debug.set_jewellery_left_hand_string(gameworld=gameworld, left_hand=equipped_jewellery[2])
        right_hand = Debug.set_jewellery_right_hand_string(gameworld=gameworld, right_hand=equipped_jewellery[3])
        neck = Debug.set_jewellery_neck_string(gameworld=gameworld, neck=equipped_jewellery[4])

        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 2, s=left_ear)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 3, s=right_ear)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 4, s=left_hand)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 5, s=right_hand)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 6, s=neck)

        section = 4
        draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                          start_panel_frame_width=section_width[section],
                          start_panel_frame_height=section_lines[section], title=section_heading[section],
                          fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))

        slot_one = Debug.set_spellbar_slot_one_string(gameworld=gameworld, entity_id=entity_id)
        slot_two = Debug.set_spellbar_slot_two_string(gameworld=gameworld, entity_id=entity_id)
        slot_three = Debug.set_spellbar_slot_three_string(gameworld=gameworld, entity_id=entity_id)
        slot_four = Debug.set_spellbar_slot_four_string(gameworld=gameworld, entity_id=entity_id)
        slot_five = Debug.set_spellbar_slot_five_string(gameworld=gameworld, entity_id=entity_id)

        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 2, s=slot_one)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 3, s=slot_two)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 4, s=slot_three)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 5, s=slot_four)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 6, s=slot_five)

        section = 5
        draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                          start_panel_frame_width=section_width[section],
                          start_panel_frame_height=section_lines[section], title=section_heading[section],
                          fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))

        slot_six = Debug.set_spellbar_slot_six_string(gameworld=gameworld, entity_id=entity_id)
        slot_seven = Debug.set_spellbar_slot_seven_string(gameworld=gameworld, entity_id=entity_id)
        slot_eight = Debug.set_spellbar_slot_eight_string(gameworld=gameworld, entity_id=entity_id)
        slot_nine = Debug.set_spellbar_slot_nine_string(gameworld=gameworld, entity_id=entity_id)

        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 2, s=slot_six)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 3, s=slot_seven)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 4, s=slot_eight)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 5, s=slot_nine)

        section = 6
        draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                          start_panel_frame_width=section_width[section],
                          start_panel_frame_height=section_lines[section], title=section_heading[section],
                          fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))
        current_health_value = MobileUtilities.get_mobile_derived_current_health(gameworld=gameworld, entity=entity_id)
        max_health_value = MobileUtilities.get_mobile_derived_maximum_health(gameworld=gameworld, entity=entity_id)

        current_mana_value = MobileUtilities.get_mobile_derived_current_mana(gameworld=gameworld, entity=entity_id)
        max_mana_value = MobileUtilities.get_mobile_derived_maximum_mana(gameworld=gameworld, entity=entity_id)

        current_f1_value = MobileUtilities.get_mobile_derived_special_bar_current_value(gameworld=gameworld,
                                                                                        entity=entity_id)
        max_f1_value = MobileUtilities.get_mobile_derived_special_bar_max_value(gameworld=gameworld, entity=entity_id)

        health_string = start_string + "Health:" + end_string + str(current_health_value) + " of " + str(
            max_health_value)
        mana_string = start_string + "Mana:" + end_string + str(current_mana_value) + " of " + str(max_mana_value)
        f1_string = start_string + "Special:" + end_string + str(current_f1_value) + " of " + str(max_f1_value)

        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 2, s=health_string)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 3, s=mana_string)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 4, s=f1_string)

        if ai_level > 1:
            section = 7
            draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                              start_panel_frame_width=section_width[section],
                              start_panel_frame_height=section_lines[section], title=section_heading[section],
                              fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))

    @staticmethod
    def display_page_two_entity_spy(section_posx, section_posy, section_width, section_lines, section_heading,
                                    gameworld, entity_id):

        # display armour
        section = 8

        draw_colourful_frame(title=' Entity Spy ', title_decorator=True, title_loc='centre',
                             corner_decorator='', corner_studs='square', msg=4)

        draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                          start_panel_frame_width=section_width[section],
                          start_panel_frame_height=section_lines[section], title=section_heading[section],
                          fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))

        str_to_print = "[color=blue]Location Material Display Defense  Major        Minor[/color]"
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 2, s=str_to_print)

        str_to_print = Debug.get_head_armour_details(gameworld=gameworld, entity_id=entity_id)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 4, s=str_to_print)

        str_to_print = Debug.get_chest_armour_details(gameworld=gameworld, entity_id=entity_id)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 5, s=str_to_print)

        str_to_print = Debug.get_hands_armour_details(gameworld=gameworld, entity_id=entity_id)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 6, s=str_to_print)

        str_to_print = Debug.get_legs_armour_details(gameworld=gameworld, entity_id=entity_id)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 7, s=str_to_print)

        str_to_print = Debug.get_feet_armour_details(gameworld=gameworld, entity_id=entity_id)
        terminal.print_(x=section_posx[section] + 1, y=section_posy[section] + 8, s=str_to_print)

        # display primary attributes
        section = 9
        draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                          start_panel_frame_width=section_width[section],
                          start_panel_frame_height=section_lines[section], title=section_heading[section],
                          fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))

        # display secondary attributes
        section = 10
        draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                          start_panel_frame_width=section_width[section],
                          start_panel_frame_height=section_lines[section], title=section_heading[section],
                          fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))

        # display derived attributes
        section = 11
        draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                          start_panel_frame_width=section_width[section],
                          start_panel_frame_height=section_lines[section], title=section_heading[section],
                          fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))

        # display applied status effects
        section = 12
        draw_simple_frame(start_panel_frame_x=section_posx[section], start_panel_frame_y=section_posy[section],
                          start_panel_frame_width=section_width[section],
                          start_panel_frame_height=section_lines[section], title=section_heading[section],
                          fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))

    @staticmethod
    def set_spellbar_slot_one_string(gameworld, entity_id):
        slot_one_string = "[color=ENTITY_SPY_NO_COMPONENT]Slot 1:None[/color]"
        slot_one_spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=gameworld, slot=1,
                                                                                   player_entity=entity_id)
        if slot_one_spell_entity > 0:
            spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=slot_one_spell_entity)
            slot_one_string = "[color=ENTITY_SPY_COMPONENT]Slot 1:[/color]" + spell_name

        return slot_one_string

    @staticmethod
    def set_spellbar_slot_two_string(gameworld, entity_id):
        slot_two_string = "[color=ENTITY_SPY_NO_COMPONENT]Slot 2:None[/color]"
        slot_two_spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=gameworld, slot=2,
                                                                                   player_entity=entity_id)
        if slot_two_spell_entity > 0:
            spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=slot_two_spell_entity)
            slot_two_string = "[color=ENTITY_SPY_COMPONENT]Slot 2:[/color]" + spell_name

        return slot_two_string

    @staticmethod
    def set_spellbar_slot_three_string(gameworld, entity_id):
        slot_three_string = "[color=ENTITY_SPY_NO_COMPONENT]Slot 3:None[/color]"
        slot_three_spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=gameworld, slot=3,
                                                                                     player_entity=entity_id)
        if slot_three_spell_entity > 0:
            spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=slot_three_spell_entity)
            slot_three_string = "[color=ENTITY_SPY_COMPONENT]Slot 3:[/color]" + spell_name

        return slot_three_string

    @staticmethod
    def set_spellbar_slot_four_string(gameworld, entity_id):
        slot_four_string = "[color=ENTITY_SPY_NO_COMPONENT]Slot 4:None[/color]"
        slot_four_spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=gameworld, slot=4,
                                                                                   player_entity=entity_id)
        if slot_four_spell_entity > 0:
            spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=slot_four_spell_entity)
            slot_four_string = "[color=ENTITY_SPY_COMPONENT]Slot 4:[/color]" + spell_name

        return slot_four_string

    @staticmethod
    def set_spellbar_slot_five_string(gameworld, entity_id):
        slot_five_string = "[color=ENTITY_SPY_NO_COMPONENT]Slot 5:None[/color]"
        slot_five_spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=gameworld, slot=5,
                                                                                   player_entity=entity_id)
        if slot_five_spell_entity > 0:
            spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=slot_five_spell_entity)
            slot_five_string = "[color=ENTITY_SPY_COMPONENT]Slot 5:[/color]" + spell_name

        return slot_five_string

    @staticmethod
    def set_spellbar_slot_six_string(gameworld, entity_id):
        slot_six_string = "[color=ENTITY_SPY_NO_COMPONENT]Slot 6:None[/color]"
        slot_six_spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=gameworld, slot=6,
                                                                                   player_entity=entity_id)
        if slot_six_spell_entity > 0:
            spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=slot_six_spell_entity)
            slot_six_string = "[color=ENTITY_SPY_COMPONENT]Slot 6:[/color]" + spell_name

        return slot_six_string

    @staticmethod
    def set_spellbar_slot_seven_string(gameworld, entity_id):
        slot_seven_string = "[color=ENTITY_SPY_NO_COMPONENT]Slot 7:None[/color]"
        slot_seven_spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=gameworld, slot=7,
                                                                                   player_entity=entity_id)
        if slot_seven_spell_entity > 0:
            spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=slot_seven_spell_entity)
            slot_seven_string = "[color=ENTITY_SPY_COMPONENT]Slot 7:[/color]" + spell_name

        return slot_seven_string

    @staticmethod
    def set_spellbar_slot_eight_string(gameworld, entity_id):
        slot_eight_string = "[color=ENTITY_SPY_NO_COMPONENT]Slot 8:None[/color]"
        slot_eight_spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=gameworld, slot=8,
                                                                                   player_entity=entity_id)
        if slot_eight_spell_entity > 0:
            spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=slot_eight_spell_entity)
            slot_eight_string = "[color=ENTITY_SPY_COMPONENT]Slot 8:[/color]" + spell_name

        return slot_eight_string

    @staticmethod
    def set_spellbar_slot_nine_string(gameworld, entity_id):
        slot_nine_string = "[color=ENTITY_SPY_NO_COMPONENT]Slot 9:None[/color]"
        slot_nine_spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=gameworld, slot=9,
                                                                                   player_entity=entity_id)
        if slot_nine_spell_entity > 0:
            spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=slot_nine_spell_entity)
            slot_nine_string = "[color=ENTITY_SPY_COMPONENT]Slot 9:[/color]" + spell_name

        return slot_nine_string


    @staticmethod
    def set_jewellery_left_ear_string(gameworld, left_ear):
        left_ear_string = "[color=ENTITY_SPY_NO_COMPONENT]Left Ear:None[/color]"
        if left_ear != 0:
            activator = ItemUtilities.get_jewellery_activator(gameworld=gameworld, entity=left_ear)
            item_name = ItemUtilities.get_item_name(gameworld=gameworld, entity=left_ear)
            left_ear_string = "[color=ENTITY_SPY_COMPONENT]Left Ear:[/color]" + activator + ' ' + item_name
        return left_ear_string

    @staticmethod
    def set_jewellery_right_ear_string(gameworld, right_ear):
        right_ear_string = "[color=ENTITY_SPY_NO_COMPONENT]Right Ear:None[/color]"
        if right_ear != 0:
            activator = ItemUtilities.get_jewellery_activator(gameworld=gameworld, entity=right_ear)
            item_name = ItemUtilities.get_item_name(gameworld=gameworld, entity=right_ear)
            right_ear_string = "[color=ENTITY_SPY_COMPONENT]Right Ear:[/color]" + activator + ' ' + item_name
        return right_ear_string

    @staticmethod
    def set_jewellery_left_hand_string(gameworld, left_hand):
        left_hand_string = "[color=ENTITY_SPY_NO_COMPONENT]Left Hand:None[/color]"
        if left_hand != 0:
            activator = ItemUtilities.get_jewellery_activator(gameworld=gameworld, entity=left_hand)
            item_name = ItemUtilities.get_item_name(gameworld=gameworld, entity=left_hand)
            left_hand_string = "[color=ENTITY_SPY_COMPONENT]Left Hand:[/color]" + activator + ' ' + item_name
        return left_hand_string

    @staticmethod
    def set_jewellery_right_hand_string(gameworld, right_hand):
        right_hand_string = "[color=ENTITY_SPY_NO_COMPONENT]Right Hand:None[/color]"
        if right_hand != 0:
            activator = ItemUtilities.get_jewellery_activator(gameworld=gameworld, entity=right_hand)
            item_name = ItemUtilities.get_item_name(gameworld=gameworld, entity=right_hand)
            right_hand_string = "[color=ENTITY_SPY_COMPONENT]Right Hand:[/color]" + activator + ' ' + item_name
        return right_hand_string

    @staticmethod
    def set_jewellery_neck_string(gameworld, neck):
        neck_string = "[color=ENTITY_SPY_NO_COMPONENT]Neck:None[/color]"
        if neck != 0:
            activator = ItemUtilities.get_jewellery_activator(gameworld=gameworld, entity=neck)
            item_name = ItemUtilities.get_item_name(gameworld=gameworld, entity=neck)
            neck_string = "[color=ENTITY_SPY_COMPONENT]Neck:[/color]" + activator + ' ' + item_name
        return neck_string

    @staticmethod
    def get_head_armour_details(gameworld, entity_id):
        str_to_print = "[color=ENTITY_SPY_NO_COMPONENT]Head:None[/color]"
        head_armour_id = MobileUtilities.is_entity_wearing_head_armour(gameworld=gameworld, entity=entity_id)
        if head_armour_id > 0:
            armour_material = ItemUtilities.get_item_material(gameworld=gameworld, entity=head_armour_id)
            armour_displayname = ItemUtilities.get_item_displayname(gameworld=gameworld, entity=head_armour_id)
            def_head_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, entity=head_armour_id)
            major_attributes = ItemUtilities.get_armour_major_attributes(gameworld=gameworld, entity=head_armour_id)
            minor_attributes = ItemUtilities.get_armour_minor_attributes(gameworld=gameworld, entity=head_armour_id)

            str_to_print = "[color=ENTITY_SPY_COMPONENT]Head:[/color]    " + armour_material + '  ' + armour_displayname + '         ' + str(
                def_head_value) + '   ' + major_attributes[0] + '     ' + str(major_attributes[1])
        return str_to_print

    @staticmethod
    def get_chest_armour_details(gameworld, entity_id):
        str_to_print = "[color=ENTITY_SPY_NO_COMPONENT]Chest:None[/color]"
        chest_armour_id = MobileUtilities.is_entity_wearing_chest_armour(gameworld=gameworld, entity=entity_id)
        if chest_armour_id > 0:
            armour_material = ItemUtilities.get_item_material(gameworld=gameworld, entity=chest_armour_id)
            armour_displayname = ItemUtilities.get_item_displayname(gameworld=gameworld, entity=chest_armour_id)
            def_chest_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, entity=chest_armour_id)
            major_attributes = ItemUtilities.get_armour_major_attributes(gameworld=gameworld, entity=chest_armour_id)
            minor_attributes = ItemUtilities.get_armour_minor_attributes(gameworld=gameworld, entity=chest_armour_id)

            str_to_print = "[color=ENTITY_SPY_COMPONENT]Chest:[/color]   " + armour_material + '  ' + armour_displayname + '        ' + str(
                def_chest_value) + '   ' + major_attributes[0] + '     ' + str(major_attributes[1])

        return str_to_print

    @staticmethod
    def get_hands_armour_details(gameworld, entity_id):
        str_to_print = "[color=ENTITY_SPY_NO_COMPONENT]Hands:None[/color]"
        hands_armour_id = MobileUtilities.is_entity_wearing_hands_armour(gameworld=gameworld, entity=entity_id)
        if hands_armour_id > 0:
            armour_material = ItemUtilities.get_item_material(gameworld=gameworld, entity=hands_armour_id)
            armour_displayname = ItemUtilities.get_item_displayname(gameworld=gameworld, entity=hands_armour_id)
            def_hands_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, entity=hands_armour_id)
            major_attributes = ItemUtilities.get_armour_major_attributes(gameworld=gameworld, entity=hands_armour_id)
            minor_attributes = ItemUtilities.get_armour_minor_attributes(gameworld=gameworld, entity=hands_armour_id)

            str_to_print = "[color=ENTITY_SPY_COMPONENT]Hands:[/color]   " + armour_material + '  ' + armour_displayname + ' ' + str(
                def_hands_value) + '   ' + major_attributes[0] + '     ' + str(major_attributes[1])

        return str_to_print

    @staticmethod
    def get_legs_armour_details(gameworld, entity_id):
        str_to_print = "[color=ENTITY_SPY_NO_COMPONENT]Legs:None[/color]"
        legs_armour_id = MobileUtilities.is_entity_wearing_legs_armour(gameworld=gameworld, entity=entity_id)
        if legs_armour_id > 0:
            armour_material = ItemUtilities.get_item_material(gameworld=gameworld, entity=legs_armour_id)
            armour_displayname = ItemUtilities.get_item_displayname(gameworld=gameworld, entity=legs_armour_id)
            def_legs_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, entity=legs_armour_id)
            major_attributes = ItemUtilities.get_armour_major_attributes(gameworld=gameworld, entity=legs_armour_id)
            minor_attributes = ItemUtilities.get_armour_minor_attributes(gameworld=gameworld, entity=legs_armour_id)

            str_to_print = "[color=ENTITY_SPY_COMPONENT]Legs:[/color]    " + armour_material + '  ' + armour_displayname + '    ' + str(
                def_legs_value) + '   ' + major_attributes[0] + '     ' + str(major_attributes[1])

        return str_to_print

    @staticmethod
    def get_feet_armour_details(gameworld, entity_id):
        str_to_print = "[color=ENTITY_SPY_NO_COMPONENT]Feet:None[/color]"
        feet_armour_id = MobileUtilities.is_entity_wearing_feet_armour(gameworld=gameworld, entity=entity_id)
        if feet_armour_id > 0:
            armour_material = ItemUtilities.get_item_material(gameworld=gameworld, entity=feet_armour_id)
            armour_displayname = ItemUtilities.get_item_displayname(gameworld=gameworld, entity=feet_armour_id)
            def_feet_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, entity=feet_armour_id)
            major_attributes = ItemUtilities.get_armour_major_attributes(gameworld=gameworld, entity=feet_armour_id)
            minor_attributes = ItemUtilities.get_armour_minor_attributes(gameworld=gameworld, entity=feet_armour_id)

            str_to_print = "[color=ENTITY_SPY_COMPONENT]Feet:[/color]    " + armour_material + '  ' + armour_displayname + '     ' + str(
                def_feet_value) + '   ' + major_attributes[0] + '     ' + str(major_attributes[1])

        return str_to_print

    @staticmethod
    def get_armour_major_attributes(gameworld, entity_id):
        str_to_print = "[color=ENTITY_SPY_NO_COMPONENT]Major:None[/color]"
        major_attributes = ItemUtilities.get_armour_major_attributes(gameworld=gameworld, entity=entity_id)
        if len(major_attributes) > 0:
            str_to_print = "[color=ENTITY_SPY_COMPONENT]Major:[/color]" + major_attributes

        return str_to_print

    @staticmethod
    def get_armour_minor_attributes(gameworld, entity_id):
        str_to_print = "[color=ENTITY_SPY_NO_COMPONENT]Minor:None[/color]"
        minor_attributes = ItemUtilities.get_armour_minor_attributes(gameworld=gameworld, entity=entity_id)
        if len(minor_attributes) > 0:
            str_to_print = "[color=ENTITY_SPY_COMPONENT]Minor:[/color]" + minor_attributes

        return str_to_print

    @staticmethod
    def set_both_hands_weapon_string_es(both_weapon, gameworld):
        start_string = "[color=ENTITY_SPY_COMPONENT]Both Hands:[/color]"
        both_hands_weapon_name = start_string + '[color=ENTITY_SPY_NO_COMPONENT]none[/color]'
        if both_weapon > 0:
            both_hands_weapon_name = start_string + ItemUtilities.get_item_name(gameworld=gameworld, entity=both_weapon)
        return both_hands_weapon_name

    @staticmethod
    def set_main_hand_weapon_string_es(main_weapon, gameworld):
        start_string = "[color=ENTITY_SPY_COMPONENT]Main Hand:[/color]"
        main_hand_weapon_name = start_string + '[color=ENTITY_SPY_NO_COMPONENT]none[/color]'
        if main_weapon > 0:
            main_hand_weapon_name = start_string + ItemUtilities.get_item_name(gameworld=gameworld, entity=main_weapon)
        return main_hand_weapon_name

    @staticmethod
    def set_off_hand_weapon_string_es(off_weapon, gameworld):
        start_string = "[color=ENTITY_SPY_COMPONENT]Off Hand:[/color]"
        off_hand_weapon_name = start_string + "[color=ENTITY_SPY_NO_COMPONENT]none[/color]"
        if off_weapon > 0:
            off_hand_weapon_name = start_string + ItemUtilities.get_item_name(gameworld=gameworld, entity=off_weapon)
        return off_hand_weapon_name
