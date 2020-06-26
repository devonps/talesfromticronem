import textwrap

from bearlibterminal import terminal

from loguru import logger

from newGame.CreateSpells import AsEntities
from utilities import configUtilities, colourUtilities
from utilities.display import draw_colourful_frame, pointy_menu
from utilities.input_handlers import handle_game_keys
from utilities.jsonUtilities import read_json_file
from utilities.mobileHelp import MobileUtilities
from newGame.initialiseNewGame import create_world
from utilities.common import CommonUtils

from ticronem import game_loop


class CharacterCreation:

    @staticmethod
    def create_new_character():
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
        selected_class = ''
        selected_gender = ''

        show_character_options = True
        create_character_selected_choice = 0

        player_race_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                      parameter='RACESFILE')
        player_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                       parameter='CLASSESFILE')
        attribute_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                      parameter='ATTRIBUTES')

        menu_start_x = configUtilities.get_config_value_as_integer(game_config, 'newCharacter', 'MENU_START_X')
        menu_start_y = configUtilities.get_config_value_as_integer(game_config, 'newCharacter', 'MENU_START_Y')
        race_flavour_x = configUtilities.get_config_value_as_integer(game_config, 'newCharacter', 'RACE_CONSOLE_FLAVOR_X')
        original_race_flavour_y = configUtilities.get_config_value_as_integer(game_config, 'newCharacter', 'RACE_CONSOLE_FLAVOR_Y')
        race_benefits_x = configUtilities.get_config_value_as_integer(game_config, 'newCharacter', 'RACE_CONSOLE_BENEFITS_X')
        race_benefits_y = configUtilities.get_config_value_as_integer(game_config, 'newCharacter', 'RACE_CONSOLE_BENEFITS_Y')

        #
        # LOAD PLAYABLE RACES FROM DISK
        #
        race_file = read_json_file(player_race_file)

        race_name = []
        race_flavour = []
        race_prefix = []
        race_bg_colour = []
        race_size = []
        race_benefits = []
        race_name_desc = []
        race_count = 0

        for option in race_file['races']:
            if option['playable']:
                race_name.append(option['name'])
                race_flavour.append(option['flavour'])
                race_prefix.append(option['prefix'])
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

        attribute_file = read_json_file(attribute_file)

        attribute_name = []
        attribute_flavour = []

        for attribute in attribute_file['attributes']:
            attribute_name.append(attribute['name'])
            attribute_flavour.append(attribute['flavour'])

        #
        # LOAD PLAYABLE CLASSES FROM DISK
        #

        class_file = read_json_file(player_class_file)

        character_class_name = []
        character_class_flavour = []
        class_health = []
        class_weapons = []
        class_defense_benefits = []
        class_balanced_benefits = []
        class_offense_benefits = []
        class_spell_file = []

        for option in class_file['classes']:
            character_class_name.append(option['name'])
            character_class_flavour.append(option['flavour'])
            class_health.append(option['health'])
            class_spell_file.append(option['spellfile'])
            class_weapons.append(option['weapons'])
            class_defense_benefits.append(option['defensive'])
            class_balanced_benefits.append(option['balanced'])
            class_offense_benefits.append(option['offensive'])



        selected_menu_option = 0
        max_menu_option = len(race_name) - 1

        dungeon_font = "[font=dungeon]"
        unicode_attribute_names = dungeon_font + '[color=CREATE_CHARACTER_ATTRIBUTE_NAME]'
        unicode_attribute_flavour = dungeon_font + '[color=CREATE_CHARACTER_ATTRIBUTE_FLAVOUR]'
        unicode_benefit_title = dungeon_font + '[color=CREATE_CHARACTER_BENEFITS_TITLE]'
        race_selected = 0
        race_name_selected = ''

        while show_character_options:
            this_row = configUtilities.get_config_value_as_integer(configfile=game_config, section='newCharacter',
                                                                   parameter='START_LIST_Y')
            CommonUtils.render_ui_framework(game_config=game_config)
            terminal.printf(x=start_list_x, y=this_row, s='Your Choices')
            this_row += 2
            terminal.printf(x=start_list_x, y=this_row, s='Race ' + selected_race)
            this_row += 1
            terminal.printf(x=start_list_x, y=this_row, s='Class ' + selected_class)
            this_row += 1
            terminal.printf(x=start_list_x, y=this_row, s='Gender ' + selected_gender)

            if create_character_selected_choice == 0:
                # display race options
                pointy_menu(header='',
                            menu_options=race_name, menu_id_format=True, menu_start_x=menu_start_x,
                            menu_start_y=menu_start_y,
                            blank_line=True, selected_option=selected_menu_option)

                # racial flavour text
                strings_list = textwrap.wrap(race_flavour[selected_menu_option], width=33)
                flavour_text_length = len(strings_list) - 1
                race_flavour_y = original_race_flavour_y
                terminal.clear_area(x=race_flavour_x, y=race_flavour_y, w=33, h=height)

                for line in strings_list:
                    terminal.print_(x=race_flavour_x, y=race_flavour_y, s=line, width=spell_infobox_width, height=1)
                    race_flavour_y += 1

                race_benefits_y = flavour_text_length + race_flavour_y + 1

                # racial benefits
                posy = 0
                terminal.print_(x=race_benefits_x, y=race_benefits_y, s=unicode_benefit_title + 'Benefits')
                for benefit in race_benefits:
                    if benefit[0] == selected_menu_option + 1:
                        string_to_print = unicode_attribute_names + benefit[1]
                        terminal.printf(x=race_benefits_x, y=(race_benefits_y + 2) + posy, s=string_to_print)
                        posy += 1
                        for attribute in range(len(attribute_name)):
                            attr_name = attribute_name[attribute]
                            benefit_name = benefit[1]
                            if attr_name.lower() == benefit_name:
                                attr_strings_list = textwrap.wrap(attribute_flavour[attribute], width=33)
                                for line in attr_strings_list:
                                    terminal.print_(x=race_benefits_x, y=(race_benefits_y + 2) + posy, s=unicode_attribute_flavour + line, width=spell_infobox_width,
                                                    height=1)
                                    posy += 1
                        posy += 1
            else:
                # display character class options
                logger.info('Selected menu set at {}', selected_menu_option)
                max_menu_option = len(character_class_name) - 1
                pointy_menu(header='',
                            menu_options=character_class_name, menu_id_format=True, menu_start_x=menu_start_x,
                            menu_start_y=menu_start_y,
                            blank_line=True, selected_option=selected_menu_option)
                # class flavour text
                strings_list = textwrap.wrap(character_class_flavour[selected_menu_option], width=33)
                class_flavour_y = original_race_flavour_y
                for line in range(5):
                    for wd in range(33):
                        terminal.printf(x=race_flavour_x + wd, y=class_flavour_y + line, s=' ')

                for line in strings_list:
                    terminal.print_(x=race_flavour_x, y=class_flavour_y, s=line, width=spell_infobox_width, height=1)
                    class_flavour_y += 1
                # class benefits
            terminal.refresh()
            event_to_be_processed, event_action = handle_game_keys()
            if event_to_be_processed != '' and event_to_be_processed == 'keypress':
                if event_action == 'quit':
                    show_character_options = False

                if event_action == 'up':
                    selected_menu_option -= 1
                    if selected_menu_option < 0:
                        selected_menu_option = max_menu_option
                if event_action == 'down':
                    selected_menu_option += 1
                    if selected_menu_option > max_menu_option:
                        selected_menu_option = 0
                if event_action == 'enter':
                    if create_character_selected_choice == 0:
                        race_name_selected = race_name[selected_menu_option]
                        race_selected = selected_menu_option
                        create_character_selected_choice += 1
                        selected_menu_option = 0
                    else:
                        show_character_options = False
            terminal.clear()

        # it's a brave new world
        gameworld = create_world()
        # setup base player entity
        class_selected = character_class_name[selected_menu_option]
        logger.debug('Creating the player character entity')
        player = MobileUtilities.get_next_entity_id(gameworld=gameworld)
        MobileUtilities.create_base_mobile(gameworld=gameworld, game_config=game_config, entity_id=player)
        MobileUtilities.create_player_character(gameworld=gameworld, game_config=game_config,
                                                player_entity=player)
        logger.info('Player character stored as entity {}', player)

        # setup racial stuff
        MobileUtilities.setup_racial_attributes(gameworld=gameworld, player=player, selected_race=race_name_selected,
            race_size=race_size[race_selected], bg=race_bg_colour[race_selected],
            race_names=race_name_desc[race_selected])

        # create class

        MobileUtilities.setup_class_attributes(gameworld=gameworld, player=player,
                                               selected_class=class_selected,
                                               health=int(class_health[selected_menu_option]),
                                               spellfile=class_spell_file[selected_menu_option])

        CharacterCreation.generate_player_character_from_choices(gameworld=gameworld)

        messagelog_entity = MobileUtilities.get_next_entity_id(gameworld=gameworld)
        CommonUtils.create_message_log_as_entity(gameworld=gameworld, log_entity=messagelog_entity)
        MobileUtilities.set_MessageLog_for_player(gameworld=gameworld, entity=player,
                                                  logid=messagelog_entity)
        logger.info('Mesage log stored as entity {}', messagelog_entity)
        game_loop(gameworld=gameworld)

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

        # generate spells for this playable class
        spellfile = MobileUtilities.get_character_class_spellfilename(gameworld, player)
        class_component = MobileUtilities.get_character_class(gameworld, player)
        if spellfile == '':
            logger.warning('Spell file name not set')

        AsEntities.generate_spells_as_entities_for_class(gameworld=gameworld, game_config=game_config, spell_file=spellfile, playable_class=class_component)

        #
        # calculate derived stats
        #

        MobileUtilities.set_mobile_derived_derived_attributes(gameworld=gameworld, entity=player)

        racial_details = MobileUtilities.get_mobile_race_details(gameworld=gameworld, entity=player)
        player_race_component = racial_details[0]
        terminal.clear()
        CharacterCreation.name_your_character(gameworld=gameworld, player_race_component=player_race_component)

    @staticmethod
    def name_your_character(gameworld, player_race_component):

        # get config items
        game_config = configUtilities.load_config()
        name_menu_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'NAME_MENU_X')
        name_menu_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'NAME_MENU_Y')
        mx = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'NAME_MALE_TAG_X')
        fx = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'NAME_FEMALE_TAG_X')
        gy = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'NAME_MALE_TAG_Y')
        txt_panel_write_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                        parameter='TXT_PANEL_WRITE_X')
        txt_panel_write_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                        parameter='TXT_PANEL_WRITE_Y')
        txt_panel_cursor = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                       parameter='TXT_PANEL_CURSOR')
        txt_panel_cursor_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                         parameter='TXT_PANEL_CURSOR_X')
        txt_panel_cursor_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                         parameter='TXT_PANEL_CURSOR_Y')
        txt_panel_letters_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                          parameter='TXT_PANEL_LETTERS_LEFT_X')
        menu_options = ['Choose Gender', 'Enter a Name', 'Choose Name From List', 'Random Name']
        letter_count = 0
        my_word = ""
        max_letters = 15
        character_not_named = True
        selected_menu_option = 0
        max_menu_option = len(menu_options) - 1
        gender_choice = 1
        gender_selector = chr(62)
        selected_name = ''
        cxoffset = 2

        player_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)

        terminal.print_(x=mx, y=gy, s='Male')
        terminal.print_(x=fx, y=gy, s='Female')

        draw_colourful_frame(title=' Character Creation - Name Your Character ', title_decorator=False,
                             title_loc='centre', corner_decorator='', msg=1)
        while character_not_named:

            if gender_choice == 1:
                terminal.put(x=fx - cxoffset, y=gy, c=32)
                terminal.put(x=mx - cxoffset, y=gy, c=gender_selector)
            else:
                terminal.put(x=mx - cxoffset, y=gy, c=32)
                terminal.put(x=fx - cxoffset, y=gy, c=gender_selector)

            if selected_name != '':
                terminal.clear_area(x=name_menu_x, y=30, width=35, height=1)
                string_to_print = 'color=[' + colourUtilities.get(
                    'MEDIUMSLATEBLUE') + ']' + 'Selected Name: ' + selected_name
                terminal.print(x=name_menu_x, y=30, s=string_to_print)

            # blit changes to root console
            terminal.refresh()

            pointy_menu(header='',
                        menu_options=menu_options, menu_id_format=True, menu_start_x=name_menu_x,
                        menu_start_y=name_menu_y, blank_line=True, selected_option=selected_menu_option)

            event_to_be_processed, event_action = handle_game_keys()
            if event_to_be_processed != '' and event_to_be_processed == 'keypress':
                    if event_action == 'quit':
                        character_not_named = False
                    if event_action == 'up':
                        selected_menu_option -= 1
                        if selected_menu_option < 0:
                            selected_menu_option = max_menu_option
                    if event_action == 'down':
                        selected_menu_option += 1
                        if selected_menu_option > max_menu_option:
                            selected_menu_option = 0
                    if event_action == 'left' and selected_menu_option == 0:
                            gender_choice -= 1
                            if gender_choice < 1:
                                gender_choice = 2
                    if event_action == 'right' and selected_menu_option == 0:
                            gender_choice += 1
                            if gender_choice > 2:
                                gender_choice = 1
                    if event_action == 'enter':
                        if gender_choice == 1:
                            MobileUtilities.set_player_gender(gameworld=gameworld, entity=player_entity, gender='male')
                        else:
                            MobileUtilities.set_player_gender(gameworld=gameworld, entity=player_entity,
                                                              gender='female')

                        if selected_menu_option == 1:
                            enter_name = True
                            if my_word != '':
                                terminal.clear_area(x=txt_panel_write_x, y=txt_panel_write_y, width=35, height=1)

                            if selected_name != '':
                                terminal.clear_area(x=mx, y=(name_menu_y + 3) + max_menu_option, width=35, height=1)
                            while enter_name:
                                terminal.put(x=txt_panel_cursor_x + letter_count, y=txt_panel_cursor_y,
                                             c=txt_panel_cursor)
                                terminal.refresh()
                                event_to_be_processed, event_action = handle_game_keys()
                                if event_to_be_processed == 'textinput' and letter_count < max_letters and ((64 < ord(event_action) < 91) or (96 < ord(event_action) < 123)):

                                        terminal.put(x=txt_panel_write_x + letter_count, y=txt_panel_write_y,
                                                     c=ord(event_action))
                                        my_word += event_action
                                        letter_count += 1
                                if event_to_be_processed == 'keypress':
                                    if event_action == 'quit':
                                        enter_name = False
                                        my_word = ''
                                        letter_count = 0
                                        terminal.clear_area(x=txt_panel_write_x, y=txt_panel_write_y, width=35,
                                                            height=1)
                                    if event_action == 'delete' and letter_count > 0:
                                            terminal.put(x=(txt_panel_write_x + letter_count) - 1, y=txt_panel_write_y,
                                                         c=32)
                                            terminal.put(x=txt_panel_cursor_x + letter_count, y=txt_panel_cursor_y,
                                                         c=32)
                                            my_word = my_word[:-1]
                                            letter_count -= 1

                                    if event_action == 'enter':
                                        selected_name = my_word
                                        my_word = ''
                                        enter_name = False
                                        character_not_named = False
                                        terminal.put(x=txt_panel_cursor_x + letter_count, y=txt_panel_cursor_y, c=32)
                                        letter_count = 0
                                        terminal.clear_area(x=txt_panel_letters_x, y=txt_panel_write_y, width=18,
                                                            height=1)
                                        MobileUtilities.set_mobile_first_name(gameworld=gameworld, entity=player_entity,
                                                                              name=selected_name)
                                # display letters remaining
                                if enter_name:
                                    letters_remaining = max_letters - letter_count
                                    letters_left = ' ' + str(letters_remaining) + ' letters left '
                                    string_to_print = '[color=' + colourUtilities.get('RAWSIENNA') + ']' + letters_left
                                    terminal.print(x=txt_panel_letters_x, y=txt_panel_write_y, s=string_to_print)

                        if selected_menu_option == 3:
                            if selected_name != '':
                                terminal.clear_area(x=txt_panel_write_x, y=txt_panel_write_y, width=35, height=1)
                            selected_name = MobileUtilities.choose_random_name(gameworld=gameworld,
                                                                               game_config=game_config,
                                                                               entity=player_entity,
                                                                               gender=gender_choice,
                                                                               race=player_race_component)
                            terminal.clear_area(x=mx, y=(name_menu_y + 3) + max_menu_option, width=35, height=1)

                            string_to_print = '[color=' + colourUtilities.get('WHITE') + ']' + selected_name
                            terminal.print(x=mx, y=(name_menu_y + 3) + max_menu_option, s=string_to_print)
                            character_not_named = False

                            MobileUtilities.set_mobile_first_name(gameworld=gameworld, entity=player_entity,
                                                                  name=selected_name)

