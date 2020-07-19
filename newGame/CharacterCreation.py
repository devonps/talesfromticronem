import textwrap

from bearlibterminal import terminal

from loguru import logger

from newGame.CreateSpells import AsEntities
from newGame.Items import ItemManager
from utilities import configUtilities, colourUtilities
from utilities.display import draw_colourful_frame, pointy_menu, draw_simple_frame
from utilities.input_handlers import handle_game_keys
from utilities.itemsHelp import ItemUtilities
from utilities.jsonUtilities import read_json_file
from utilities.mobileHelp import MobileUtilities
from newGame.initialiseNewGame import create_world
from utilities.common import CommonUtils

from ticronem import game_loop
from utilities.spellHelp import SpellUtilities


class CharacterCreation:

    @staticmethod
    def create_new_character():
        race_name_selected, race_size, race_bg_colour, race_name_desc = CharacterCreation.choose_race()
        class_selected, class_health, class_spell_file = CharacterCreation.choose_class()

        game_config = configUtilities.load_config()

        # it's a brave new world
        gameworld = create_world()
        # setup base player entity
        logger.debug('Creating the player character entity')
        player = MobileUtilities.get_next_entity_id(gameworld=gameworld)
        MobileUtilities.create_base_mobile(gameworld=gameworld, game_config=game_config, entity_id=player)
        MobileUtilities.create_player_character(gameworld=gameworld, game_config=game_config,
                                                player_entity=player)
        logger.info('Player character stored as entity {}', player)

        # setup racial stuff race_name_selected, race_size, race_bg_colour, race_name_desc
        MobileUtilities.setup_racial_attributes(gameworld=gameworld, player=player, selected_race=race_name_selected,
            race_size=race_size, bg=race_bg_colour, race_names=race_name_desc)

        # create class

        MobileUtilities.setup_class_attributes(gameworld=gameworld, player=player, selected_class=class_selected,
                                               health=class_health, spellfile=class_spell_file)

        CharacterCreation.generate_player_character_from_choices(gameworld=gameworld)

        messagelog_entity = MobileUtilities.get_next_entity_id(gameworld=gameworld)
        CommonUtils.create_message_log_as_entity(gameworld=gameworld, log_entity=messagelog_entity)
        MobileUtilities.set_MessageLog_for_player(gameworld=gameworld, entity=player, logid=messagelog_entity)
        logger.info('Mesage log stored as entity {}', messagelog_entity)
        game_loop(gameworld=gameworld)

    @staticmethod
    def choose_race():
        game_config = configUtilities.load_config()
        spell_infobox_width = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                          section='newCharacter',
                                                                          parameter='NC_WIDTH')
        height = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                             section='newCharacter',
                                                             parameter='NC_DEPTH')

        # choices already made
        start_list_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='newCharacter',
                                                                   parameter='START_LIST_X')
        selected_race = ''

        show_character_options = True

        menu_start_x = configUtilities.get_config_value_as_integer(game_config, 'newCharacter', 'MENU_START_X')
        menu_start_y = configUtilities.get_config_value_as_integer(game_config, 'newCharacter', 'MENU_START_Y')
        race_flavour_x = configUtilities.get_config_value_as_integer(game_config, 'newCharacter',
                                                                     'RACE_CONSOLE_FLAVOR_X')
        original_race_flavour_y = configUtilities.get_config_value_as_integer(game_config, 'newCharacter',
                                                                              'RACE_CONSOLE_FLAVOR_Y')

        #
        # LOAD PLAYABLE RACES FROM DISK
        #

        race_name, race_flavour, race_bg_colour, race_size, race_benefits, race_name_desc = CharacterCreation.read_playable_races(game_config=game_config)

        selected_menu_option = 0
        max_menu_option = len(race_name) - 1
        start_row = configUtilities.get_config_value_as_integer(configfile=game_config, section='newCharacter',
                                                                parameter='START_LIST_Y')

        while show_character_options:
            this_row = start_row
            CommonUtils.render_ui_framework(game_config=game_config)
            terminal.printf(x=start_list_x, y=this_row, s='Your Choices')
            this_row += 2
            terminal.printf(x=start_list_x, y=this_row, s='Race ' + selected_race)
            this_row += 1
            terminal.printf(x=start_list_x, y=this_row, s='Class')
            this_row += 1
            terminal.printf(x=start_list_x, y=this_row, s='Gender')

            # display race options
            pointy_menu(header='',
                        menu_options=race_name, menu_id_format=True, menu_start_x=menu_start_x,
                        menu_start_y=menu_start_y,
                        blank_line=True, selected_option=selected_menu_option)

            # racial flavour text
            strings_list = textwrap.wrap(race_flavour[selected_menu_option], width=33)
            flavour_text_length = len(strings_list) - 1
            terminal.clear_area(x=race_flavour_x, y=original_race_flavour_y, w=33, h=height)

            CharacterCreation.print_array(strings_list=strings_list, startx=race_flavour_x, starty=original_race_flavour_y,
                                          width=spell_infobox_width)

            # racial benefits
            race_benefits_y = flavour_text_length + original_race_flavour_y + 2
            CharacterCreation.render_race_benefits(game_config=game_config, race_benefits=race_benefits, selected_menu_option=selected_menu_option, race_benefits_y=race_benefits_y)
            terminal.refresh()
            event_to_be_processed, event_action = handle_game_keys()
            if event_to_be_processed != '':
                if event_action == 'quit':
                    show_character_options = False
                if event_action in ('up', 'down'):
                    selected_menu_option = CharacterCreation.move_menu_selection(event_action=event_action,
                                                                                 selected_menu_option=selected_menu_option,
                                                                                 max_menu_option=max_menu_option)
                if event_action == 'enter':
                    show_character_options = False
            terminal.clear()
        return race_name[selected_menu_option], race_size[selected_menu_option], race_bg_colour[selected_menu_option], race_name_desc[selected_menu_option]

    @staticmethod
    def render_race_benefits(game_config, race_benefits, selected_menu_option, race_benefits_y):
        race_benefits_x = configUtilities.get_config_value_as_integer(game_config, 'newCharacter',
                                                                      'RACE_CONSOLE_BENEFITS_X')
        dungeon_font = "[font=dungeon]"
        unicode_benefit_title = dungeon_font + '[color=CREATE_CHARACTER_BENEFITS_TITLE]'

        # racial benefits
        terminal.print_(x=race_benefits_x, y=race_benefits_y, s=unicode_benefit_title + 'Benefits')
        unicode_attribute_names = dungeon_font + '[color=CREATE_CHARACTER_ATTRIBUTE_NAME]'
        unicode_attribute_flavour = dungeon_font + '[color=CREATE_CHARACTER_ATTRIBUTE_FLAVOUR]'
        posy = 0
        # read race attributes from disk
        attribute_name, attribute_flavour = CharacterCreation.read_race_attributes(game_config=game_config)

        for benefit in race_benefits:
            if benefit[0] == selected_menu_option + 1:
                string_to_print = unicode_attribute_names + benefit[1]
                terminal.printf(x=race_benefits_x, y=(race_benefits_y + 2) + posy, s=string_to_print)
                posy += 1
                posy = CharacterCreation.render_race_attributes(attribute_name=attribute_name, benefit=benefit,
                                                                attribute_flavour=attribute_flavour,
                                                                game_config=game_config, starty=race_benefits_y,
                                                                posy=posy,
                                                                unicode_attribute_flavour=unicode_attribute_flavour)
                posy += 1

    @staticmethod
    def choose_class():
        game_config = configUtilities.load_config()

        # choices already made
        start_list_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='newCharacter',
                                                                   parameter='START_LIST_X')
        selected_race = ''
        selected_class = ''
        selected_gender = ''

        show_character_options = True


        #
        # LOAD PLAYABLE CLASSES FROM DISK
        #
        character_class_name, character_class_flavour, class_health, class_spell_file = CharacterCreation.read_playable_classes(
            game_config=game_config)

        selected_menu_option = 0
        start_row = configUtilities.get_config_value_as_integer(configfile=game_config, section='newCharacter',
                                                                parameter='START_LIST_Y')

        while show_character_options:
            terminal.clear()
            this_row = start_row
            CommonUtils.render_ui_framework(game_config=game_config)
            terminal.printf(x=start_list_x, y=this_row, s='Your Choices')
            this_row += 2
            terminal.printf(x=start_list_x, y=this_row, s='Race ' + selected_race)
            this_row += 1
            terminal.printf(x=start_list_x, y=this_row, s='Class ' + selected_class)
            this_row += 1
            terminal.printf(x=start_list_x, y=this_row, s='Gender ' + selected_gender)

            # display character class options
            max_menu_option = len(character_class_name) - 1
            CharacterCreation.render_playable_classes(character_class_name=character_class_name,
                                                      selected_menu_option=selected_menu_option,
                                                      game_config=game_config,
                                                      character_class_flavour=character_class_flavour)
            terminal.refresh()
            event_to_be_processed, event_action = handle_game_keys()
            if event_to_be_processed != '':
                if event_action == 'quit':
                    show_character_options = False
                if event_action in ('up', 'down'):
                    selected_menu_option = CharacterCreation.move_menu_selection(event_action=event_action, selected_menu_option=selected_menu_option, max_menu_option=max_menu_option)
                if event_action == 'enter':
                    show_character_options = False
        return character_class_name[selected_menu_option], int(class_health[selected_menu_option]), class_spell_file[selected_menu_option]

    @staticmethod
    def move_menu_selection(event_action, selected_menu_option, max_menu_option):
        if event_action == 'up':
            selected_menu_option -= 1
            if selected_menu_option < 0:
                selected_menu_option = max_menu_option
        if event_action == 'down':
            selected_menu_option += 1
            if selected_menu_option > max_menu_option:
                selected_menu_option = 0
        return selected_menu_option

    @staticmethod
    def read_playable_classes(game_config):
        player_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                       parameter='CLASSESFILE')
        class_file = read_json_file(player_class_file)

        character_class_name = []
        character_class_flavour = []
        class_health = []
        class_spell_file = []

        for option in class_file['classes']:
            character_class_name.append(option['name'])
            character_class_flavour.append(option['flavour'])
            class_health.append(option['health'])
            class_spell_file.append(option['spellfile'])

        return character_class_name, character_class_flavour, class_health, class_spell_file

    @staticmethod
    def render_race_attributes(attribute_name, benefit, attribute_flavour, game_config, starty, posy, unicode_attribute_flavour):
        race_benefits_x = configUtilities.get_config_value_as_integer(game_config, 'newCharacter',
                                                                      'RACE_CONSOLE_BENEFITS_X')
        spell_infobox_width = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                          section='newCharacter',
                                                                          parameter='NC_WIDTH')
        for attribute in range(len(attribute_name)):
            attr_name = attribute_name[attribute]
            benefit_name = benefit[1]
            if attr_name.lower() == benefit_name:
                attr_strings_list = textwrap.wrap(attribute_flavour[attribute], width=33)
                for line in attr_strings_list:
                    terminal.print_(x=race_benefits_x, y=(starty + 2) + posy,
                                    s=unicode_attribute_flavour + line, width=spell_infobox_width,
                                    height=1)
                    posy += 1
        return posy

    @staticmethod
    def render_playable_classes(character_class_name, selected_menu_option, game_config, character_class_flavour):
        menu_start_x = configUtilities.get_config_value_as_integer(game_config, 'newCharacter', 'MENU_START_X')
        menu_start_y = configUtilities.get_config_value_as_integer(game_config, 'newCharacter', 'MENU_START_Y')
        race_flavour_x = configUtilities.get_config_value_as_integer(game_config, 'newCharacter', 'RACE_CONSOLE_FLAVOR_X')

        original_race_flavour_y = configUtilities.get_config_value_as_integer(game_config, 'newCharacter', 'RACE_CONSOLE_FLAVOR_Y')
        spell_infobox_width = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                          section='newCharacter',
                                                                          parameter='NC_WIDTH')
        height = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                           section='newCharacter',
                                                                           parameter='NC_DEPTH')
        pointy_menu(header='',
                    menu_options=character_class_name, menu_id_format=True, menu_start_x=menu_start_x,
                    menu_start_y=menu_start_y,
                    blank_line=True, selected_option=selected_menu_option)
        # class flavour text
        strings_list = textwrap.wrap(character_class_flavour[selected_menu_option], width=33)
        class_flavour_y = original_race_flavour_y

        terminal.clear_area(x=race_flavour_x, y=class_flavour_y, w=33, h=height)

        CharacterCreation.print_array(strings_list=strings_list, startx=race_flavour_x, starty=class_flavour_y,
                                      width=spell_infobox_width)

    @staticmethod
    def read_race_attributes(game_config):

        attribute_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                    parameter='ATTRIBUTES')
        attribute_file = read_json_file(attribute_file)

        attribute_name = []
        attribute_flavour = []

        for attribute in attribute_file['attributes']:
            attribute_name.append(attribute['name'])
            attribute_flavour.append(attribute['flavour'])

        return attribute_name, attribute_flavour

    @staticmethod
    def read_playable_races(game_config):
        player_race_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                      parameter='RACESFILE')
        race_file = read_json_file(player_race_file)

        race_name = []
        race_flavour = []
        race_bg_colour = []
        race_size = []
        race_benefits = []
        race_name_desc = []
        race_count = 0

        for option in race_file['races']:
            if option['playable']:
                race_name.append(option['name'])
                race_flavour.append(option['flavour'])
                race_bg_colour.append(colourUtilities.get('BLACK'))
                race_size.append(option['size'])
                racial_bonus_count = option['attribute_count']
                race_name_desc.append(option['singular_plural_adjective'])
                race_count += 1
                for attribute_bonus in range(racial_bonus_count):
                    race_attr_name = 'attribute_' + str(attribute_bonus + 1) + '_name'
                    race_attr_value = 'attribute_' + str(attribute_bonus + 1) + '_value'
                    attribute_benefit_and_amount = (option[race_attr_name], option[race_attr_value])
                    rb = [race_count]
                    rb.extend(list(attribute_benefit_and_amount))
                    race_benefits.append(rb)
        return race_name, race_flavour, race_bg_colour, race_size, race_benefits, race_name_desc

    @staticmethod
    def print_array(strings_list, startx, starty, width):
        for line in strings_list:
            terminal.print_(x=startx, y=starty, s=line, width=width, height=1)
            starty += 1

    @staticmethod
    def generate_player_character_from_choices(gameworld):
        # get config items
        game_config = configUtilities.load_config()

        # get player entity
        player = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)

        # get race details for character
        racial_details = MobileUtilities.get_mobile_race_details(gameworld=gameworld, entity=player)
        player_race = racial_details[0]

        # create racial bonuses
        if player_race.lower() == 'dilga':
            cur_precision = MobileUtilities.get_mobile_primary_precision(gameworld=gameworld, entity=player)
            cur_condi_damage = MobileUtilities.get_mobile_secondary_condition_damage(gameworld=gameworld, entity=player)
            cur_ferocity = MobileUtilities.get_mobile_secondary_ferocity(gameworld=gameworld, entity=player)

            cur_precision += 1
            MobileUtilities.set_mobile_primary_precision(gameworld=gameworld, entity=player, value=cur_precision)
            cur_condi_damage += 1
            MobileUtilities.set_mobile_secondary_condition_damage(gameworld=gameworld, entity=player, value=cur_condi_damage)
            cur_ferocity += 1
            MobileUtilities.set_mobile_secondary_ferocity(gameworld=gameworld, entity=player, value=cur_ferocity)

        if player_race.lower() == 'eskeri':
            cur_power = MobileUtilities.get_mobile_primary_power(gameworld=gameworld, entity=player)
            cur_concentration = MobileUtilities.get_mobile_secondary_concentration(gameworld=gameworld, entity=player)

            cur_power += 1
            MobileUtilities.set_mobile_primary_power(gameworld=gameworld, entity=player, value=cur_power)
            cur_concentration += 1
            MobileUtilities.set_mobile_secondary_concentration(gameworld=gameworld, entity=player, value=cur_concentration)

        if player_race.lower() == 'jogah':
            cur_vitality = MobileUtilities.get_mobile_primary_vitality(gameworld=gameworld, entity=player)
            cur_concentration = MobileUtilities.get_mobile_secondary_concentration(gameworld=gameworld, entity=player)
            cur_ferocity = MobileUtilities.get_mobile_secondary_ferocity(gameworld=gameworld, entity=player)

            cur_vitality += 1
            MobileUtilities.set_mobile_primary_vitality(gameworld=gameworld, entity=player, value=cur_vitality)
            cur_concentration += 1
            MobileUtilities.set_mobile_secondary_concentration(gameworld=gameworld, entity=player, value=cur_concentration)
            cur_ferocity += 1
            MobileUtilities.set_mobile_secondary_ferocity(gameworld=gameworld, entity=player, value=cur_ferocity)

        if player_race.lower() == 'oshun':
            cur_toughness = MobileUtilities.get_mobile_primary_toughness(gameworld=gameworld, entity=player)
            cur_condi_damage = MobileUtilities.get_mobile_secondary_condition_damage(gameworld=gameworld, entity=player)

            cur_toughness += 1
            MobileUtilities.set_mobile_primary_toughness(gameworld=gameworld, entity=player, value=cur_toughness)
            cur_condi_damage += 1
            MobileUtilities.set_mobile_secondary_condition_damage(gameworld=gameworld, entity=player, value=cur_condi_damage)

        # generate an empty spell bar
        SpellUtilities.setup_mobile_empty_spellbar(gameworld=gameworld, player_entity=player)

        # add heal spell to spellbar
        heal_spell_entity = SpellUtilities.get_class_heal_spell(gameworld=gameworld, player_entity=player)
        SpellUtilities.set_spellbar_slot(gameworld=gameworld, spell_entity=heal_spell_entity, slot=6, player_entity=player)

        # calculate derived stats
        MobileUtilities.set_mobile_derived_derived_attributes(gameworld=gameworld, entity=player)

        # name the character
        CharacterCreation.character_naming(gameworld=gameworld, game_config=game_config)

        # assign male gender to character
        MobileUtilities.set_player_gender(gameworld=gameworld, entity=player, gender='male')

        # create jewellery set based on the balanced package
        # this is a temp approach being used for utility spells
        ItemManager.create_jewellery_for_utility_spells(gameworld=gameworld, game_config=game_config)

        pendent_entity = ItemUtilities.get_jewellery_entity_from_body_location(gameworld=gameworld, entity=player, bodylocation='neck')
        left_ear_entity = ItemUtilities.get_jewellery_entity_from_body_location(gameworld=gameworld, entity=player, bodylocation='lear')
        right_ear_entity = ItemUtilities.get_jewellery_entity_from_body_location(gameworld=gameworld, entity=player, bodylocation='rear')
        left_hand_entity = ItemUtilities.get_jewellery_entity_from_body_location(gameworld=gameworld, entity=player, bodylocation='lhand')
        right_hand_entity = ItemUtilities.get_jewellery_entity_from_body_location(gameworld=gameworld, entity=player, bodylocation='rhand')

        if pendent_entity > 0:
            sp1 = ItemUtilities.get_spell_from_item(gameworld=gameworld, item_entity=pendent_entity)
            SpellUtilities.set_spellbar_slot(gameworld=gameworld, spell_entity=sp1, slot=7, player_entity=player)

        if left_ear_entity > 0:
            sp2 = ItemUtilities.get_spell_from_item(gameworld=gameworld, item_entity=left_ear_entity)
            SpellUtilities.set_spellbar_slot(gameworld=gameworld, spell_entity=sp2, slot=8, player_entity=player)

        if right_ear_entity > 0:
            sp3 = ItemUtilities.get_spell_from_item(gameworld=gameworld, item_entity=right_ear_entity)
            SpellUtilities.set_spellbar_slot(gameworld=gameworld, spell_entity=sp3, slot=9, player_entity=player)

        # end of temporary code for setting utility slots

        # create some armour for our hero - another temporary crutch
        # order is: heads, hands, chest, legs, feet
        armour_set = ItemManager.create_full_armour_set(gameworld=gameworld, game_config=game_config, prefix='resilient', armourset='Embroided')
        ItemUtilities.equip_full_set_of_armour(gameworld=gameworld, entity=player, armourset=armour_set)

        # until NPC interactions has been completed



    @staticmethod
    def character_naming(gameworld, game_config):
        txt_panel_cursor = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                       parameter='TXT_PANEL_CURSOR')
        txt_panel_cursor_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                         parameter='TXT_PANEL_CURSOR_X')
        txt_panel_cursor_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                         parameter='TXT_PANEL_CURSOR_Y')
        txt_panel_write_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                        parameter='TXT_PANEL_WRITE_X')
        txt_panel_write_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                        parameter='TXT_PANEL_WRITE_Y')
        txt_panel_letters_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                          parameter='TXT_PANEL_LETTERS_LEFT_X')
        max_letters = 15
        character_not_named = True
        letter_count = 0
        my_word = ''
        dungeon_font = "[font=dungeon]"
        unicode_help_messages = dungeon_font + '[color=NAME_CHAR_HELP_MESSAGE]'
        unicode_name_letters_left = dungeon_font + '[color=NAME_CHAR_LETTERS_LEFT]'

        player_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
        terminal.clear()
        draw_simple_frame(start_panel_frame_x=txt_panel_write_x, start_panel_frame_y=txt_panel_write_y, start_panel_frame_width=35, start_panel_frame_height=6, title='Name Your Character', fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))
        terminal.printf(x=txt_panel_write_x + 1, y=txt_panel_write_y + 4, s=unicode_help_messages + 'valid chars:A-Z and a-z')
        terminal.printf(x=txt_panel_write_x + 1, y=txt_panel_write_y + 5, s=unicode_help_messages + 'leave blank for random name')

        while character_not_named:
            terminal.put(x=txt_panel_cursor_x + letter_count, y=txt_panel_cursor_y, c=txt_panel_cursor)
            terminal.refresh()
            event_to_be_processed, event_action = handle_game_keys()
            if event_to_be_processed == 'keypress' and (letter_count < max_letters):
                if event_action == 'quit':
                    character_not_named = False
                    terminal.clear_area(x=txt_panel_cursor_x, y=txt_panel_cursor_y, width=35,
                                        height=1)
                elif event_action == 'delete' and letter_count > 0:
                    terminal.put(x=(txt_panel_cursor_x + letter_count) - 1, y=txt_panel_cursor_y, c=32)
                    terminal.put(x=txt_panel_cursor_x + letter_count, y=txt_panel_cursor_y, c=32)
                    my_word = my_word[:-1]
                    letter_count -= 1

                elif event_action == 'enter':
                    character_not_named = False
                    terminal.put(x=txt_panel_cursor_x + letter_count, y=txt_panel_cursor_y, c=32)
                    terminal.clear_area(x=txt_panel_letters_x, y=txt_panel_write_y, width=18,
                                        height=1)
                    CharacterCreation.assign_name_to_character(gameworld=gameworld, player_entity=player_entity, selected_name=my_word)
                else:
                    key_pressed = 65 + event_action
                    my_word, letter_count = CharacterCreation.add_letter_to_word(key_pressed=key_pressed, txt_panel_cursor_x=txt_panel_cursor_x, letter_count=letter_count, txt_panel_cursor_y=txt_panel_cursor_y, my_word=my_word)

            # display letters remaining
            letters_remaining = max_letters - letter_count
            letters_left = ' ' + str(letters_remaining) + ' letters left '
            terminal.printf(x=txt_panel_letters_x, y=txt_panel_cursor_y, s=unicode_name_letters_left + letters_left)

    @staticmethod
    def add_letter_to_word(key_pressed, txt_panel_cursor_x, letter_count, txt_panel_cursor_y, my_word):
        if (64 < key_pressed < 91) or (96 < key_pressed < 123):
            terminal.put(x=txt_panel_cursor_x + letter_count, y=txt_panel_cursor_y, c=chr(key_pressed))
            my_word += chr(key_pressed)
            letter_count += 1
        return my_word, letter_count

    @staticmethod
    def assign_name_to_character(gameworld, player_entity, selected_name):
        if selected_name != '':
            MobileUtilities.set_mobile_first_name(gameworld=gameworld, entity=player_entity,
                                                  name=selected_name)
        else:
            MobileUtilities.set_mobile_first_name(gameworld=gameworld, entity=player_entity,
                                                  name="Random")
