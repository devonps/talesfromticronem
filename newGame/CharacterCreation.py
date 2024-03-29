import textwrap

from bearlibterminal import terminal
from loguru import logger
from newGame import Items, initialiseNewGame
from static.data import constants
from utilities import configUtilities, namegenUtilities, armourManagement, display, input_handlers, jsonUtilities, \
    mobileHelp, common, spellHelp, weaponManagement, world, colourUtilities
from ticronem import game_loop


class CharacterCreation:

    @staticmethod
    def create_new_character():
        race_name_selected, race_size, race_bg_colour, race_name_desc = CharacterCreation.choose_race()
        class_selected, class_health, class_spell_file = CharacterCreation.choose_class()

        # it's a brave new world
        gameworld = initialiseNewGame.create_world()
        # setup base player entity
        player = world.get_next_entity_id(gameworld=gameworld)
        mobileHelp.MobileUtilities.create_base_mobile(gameworld=gameworld, entity_id=player)
        mobileHelp.MobileUtilities.create_player_character(gameworld=gameworld, player_entity=player)
        logger.info('Player character stored as entity {}', player)

        # setup racial stuff race_name_selected, race_size, race_bg_colour, race_name_desc
        mobileHelp.MobileUtilities.setup_racial_attributes(gameworld=gameworld, entity=player, selected_race=race_name_selected,
                                                           race_size=race_size, bg=race_bg_colour, race_names=race_name_desc)
        # set player FG colour
        this_colour = colourUtilities.get('white')

        mobileHelp.MobileUtilities.set_mobile_fg_render_colour(gameworld=gameworld, entity=player, value=this_colour)

        # create class
        mobileHelp.MobileUtilities.setup_class_attributes(gameworld=gameworld, player=player, selected_class=class_selected,
                                               health=class_health, spellfile=class_spell_file)

        CharacterCreation.generate_player_character_from_choices(gameworld=gameworld)

        messagelog_entity = mobileHelp.MobileUtilities.get_next_entity_id(gameworld=gameworld)
        common.CommonUtils.create_message_log_as_entity(gameworld=gameworld, log_entity=messagelog_entity)
        mobileHelp.MobileUtilities.set_MessageLog_for_player(gameworld=gameworld, entity=player, logid=messagelog_entity)
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

        race_name, race_flavour, race_bg_colour, race_size, race_benefits, race_name_desc = CharacterCreation.read_playable_races()

        selected_menu_option = 0
        max_menu_option = len(race_name) - 1
        start_row = configUtilities.get_config_value_as_integer(configfile=game_config, section='newCharacter',
                                                                parameter='START_LIST_Y')

        while show_character_options:
            this_row = start_row
            common.CommonUtils.render_ui_framework(game_config=game_config)
            terminal.printf(x=start_list_x, y=this_row, s='Your Choices')
            this_row += 2
            terminal.printf(x=start_list_x, y=this_row, s='Race ' + selected_race)
            this_row += 1
            terminal.printf(x=start_list_x, y=this_row, s='Class')
            this_row += 1
            terminal.printf(x=start_list_x, y=this_row, s='Gender')

            # display race options
            display.pointy_vertical_menu(header='', menu_options=race_name, menu_start_x=menu_start_x, menu_start_y=menu_start_y,
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
            event_to_be_processed, event_action = input_handlers.handle_game_keys()
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
        attribute_name, attribute_flavour = CharacterCreation.read_race_attributes()

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
        character_class_name, character_class_flavour, class_health, class_spell_file = CharacterCreation.read_playable_classes()

        selected_menu_option = 0
        start_row = configUtilities.get_config_value_as_integer(configfile=game_config, section='newCharacter',
                                                                parameter='START_LIST_Y')

        while show_character_options:
            terminal.clear()
            this_row = start_row
            common.CommonUtils.render_ui_framework(game_config=game_config)
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
            event_to_be_processed, event_action = input_handlers.handle_game_keys()
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
    def read_playable_classes():
        player_class_file = constants.FILE_CLASSESFILE
        class_file = jsonUtilities.read_json_file(player_class_file)

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
        display.pointy_vertical_menu(header='', menu_options=character_class_name, menu_start_x=menu_start_x, menu_start_y=menu_start_y,
                             blank_line=True, selected_option=selected_menu_option)
        # class flavour text
        strings_list = textwrap.wrap(character_class_flavour[selected_menu_option], width=33)
        class_flavour_y = original_race_flavour_y

        terminal.clear_area(x=race_flavour_x, y=class_flavour_y, w=33, h=height)

        CharacterCreation.print_array(strings_list=strings_list, startx=race_flavour_x, starty=class_flavour_y,
                                      width=spell_infobox_width)

    @staticmethod
    def read_race_attributes():

        attribute_file = constants.FILE_ATTRIBUTES
        attribute_file = jsonUtilities.read_json_file(attribute_file)

        attribute_name = []
        attribute_flavour = []

        for attribute in attribute_file['attributes']:
            attribute_name.append(attribute['name'])
            attribute_flavour.append(attribute['flavour'])

        return attribute_name, attribute_flavour

    @staticmethod
    def read_playable_races():
        player_race_file = constants.FILE_RACESFILE
        race_file = jsonUtilities.read_json_file(player_race_file)

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
                race_bg_colour.append('black')
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
        player = mobileHelp.MobileUtilities.get_player_entity(gameworld=gameworld)

        # get race details for character
        racial_details = mobileHelp.MobileUtilities.get_mobile_race_details(gameworld=gameworld, entity=player)
        player_race = racial_details[0]

        # create racial bonuses
        if player_race.lower() == 'dilga':

            mobileHelp.MobileUtilities.set_mobile_primary_precision(gameworld=gameworld, entity=player, value=1)
            mobileHelp.MobileUtilities.set_mobile_secondary_condition_damage(gameworld=gameworld, entity=player, value=1)
            mobileHelp.MobileUtilities.set_mobile_secondary_ferocity(gameworld=gameworld, entity=player, value=1)

        if player_race.lower() == 'eskeri':
            mobileHelp.MobileUtilities.set_mobile_primary_power(gameworld=gameworld, entity=player, value=1)
            mobileHelp.MobileUtilities.set_mobile_secondary_concentration(gameworld=gameworld, entity=player, value=1)

        if player_race.lower() == 'jogah':
            mobileHelp.MobileUtilities.set_mobile_primary_vitality(gameworld=gameworld, entity=player, value=1)
            mobileHelp.MobileUtilities.set_mobile_secondary_concentration(gameworld=gameworld, entity=player, value=1)
            mobileHelp.MobileUtilities.set_mobile_secondary_ferocity(gameworld=gameworld, entity=player, value=1)

        if player_race.lower() == 'oshun':
            mobileHelp.MobileUtilities.set_mobile_primary_toughness(gameworld=gameworld, entity=player, value=1)
            mobileHelp.MobileUtilities.set_mobile_secondary_condition_damage(gameworld=gameworld, entity=player, value=1)

        # generate an empty spell bar
        spellHelp.SpellUtilities.setup_mobile_empty_spellbar(gameworld=gameworld, player_entity=player)

        # add heal spell to spellbar
        heal_spell_entity = spellHelp.SpellUtilities.get_class_heal_spell(gameworld=gameworld, player_entity=player)
        spellHelp.SpellUtilities.set_spellbar_slot(gameworld=gameworld, spell_entity=heal_spell_entity, slot=5, player_entity=player)

        # calculate derived stats
        armourManagement.ArmourUtilities.set_mobile_derived_armour_attribute(gameworld=gameworld, entity=player)
        mobileHelp.MobileUtilities.set_mobile_derived_attributes(gameworld=gameworld, entity=player)

        # name the character
        CharacterCreation.character_naming(gameworld=gameworld, game_config=game_config)

        # assign male gender to character
        mobileHelp.MobileUtilities.set_mobile_gender(gameworld=gameworld, entity=player, gender='male')

        # give the player a 2-handed staff with spells fully loaded
        player_class = mobileHelp.MobileUtilities.get_character_class(gameworld=gameworld, entity=player)

        weapon_to_be_created = 'staff'
        if player_class == 'illusionist':
            weapon_to_be_created = 'sword'

        created_weapon_entity = Items.ItemManager.create_weapon(gameworld=gameworld, weapon_type=weapon_to_be_created,
                                                          game_config=game_config)
        mobileHelp.MobileUtilities.equip_weapon(gameworld=gameworld, entity=player, weapon=created_weapon_entity, hand='both')
        spell_list = spellHelp.SpellUtilities.get_list_of_spells_for_enemy(gameworld=gameworld, weapon_type=weapon_to_be_created,
                                                                 mobile_class=player_class)

        # load spellbar with spells from weapon(s)
        weaponManagement.WeaponUtilities.load_player_spellbar_from_weapons(gameworld=gameworld, weapon_type=weapon_to_be_created,
                                                          spell_list=spell_list, player_entity=player)

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

        player_entity = mobileHelp.MobileUtilities.get_player_entity(gameworld=gameworld)
        terminal.clear()
        display.draw_simple_frame(start_panel_frame_x=txt_panel_write_x, start_panel_frame_y=txt_panel_write_y, start_panel_frame_width=35, start_panel_frame_height=6, title='Name Your Character')
        terminal.printf(x=txt_panel_write_x + 1, y=txt_panel_write_y + 4, s=unicode_help_messages + 'valid chars:A-Z and a-z')
        terminal.printf(x=txt_panel_write_x + 1, y=txt_panel_write_y + 5, s=unicode_help_messages + 'leave blank for random name')

        while character_not_named:
            terminal.put(x=txt_panel_cursor_x + letter_count, y=txt_panel_cursor_y, c=txt_panel_cursor)
            terminal.refresh()
            event_to_be_processed, event_action = input_handlers.handle_game_keys()
            if event_to_be_processed is not None and event_to_be_processed == 'keypress' and (letter_count < max_letters):
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
                        key_pressed = event_action
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
            mobileHelp.MobileUtilities.set_mobile_first_name(gameworld=gameworld, entity=player_entity,
                                                  name=selected_name)
        else:
            random_name = CharacterCreation.generate_random_name_based_on_race(gameworld=gameworld, player_entity=player_entity)
            mobileHelp.MobileUtilities.set_mobile_first_name(gameworld=gameworld, entity=player_entity, name=random_name)

    @staticmethod
    def generate_random_name_based_on_race(gameworld, player_entity):
        # get race details for character
        racial_details = mobileHelp.MobileUtilities.get_mobile_race_details(gameworld=gameworld, entity=player_entity)
        player_race = racial_details[0]
        name_file = player_race.upper() + 'NAMESFILE'
        game_config = configUtilities.load_config()

        # read names file
        racial_names_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                   parameter=name_file)

        name_file = namegenUtilities.read_name_file(file_to_read=racial_names_file)
        name_components = namegenUtilities.process_name_file(name_file=name_file)
        random_name = namegenUtilities.generate_name(name_components=name_components)

        return random_name
