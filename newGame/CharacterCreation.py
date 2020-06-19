import textwrap

from bearlibterminal import terminal

from loguru import logger

from newGame.CreateSpells import AsEntities
from utilities import configUtilities, colourUtilities, world
from utilities.externalfileutilities import Externalfiles
from utilities.buildLibrary import BuildLibrary
from utilities.display import draw_colourful_frame, pointy_menu, coloured_list, display_coloured_box
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
        unicode_string_to_print = '[font=dungeon][color=SPELLINFO_FRAME_COLOUR]['
        ascii_prefix = 'ASCII_SINGLE_'

        terminal.clear()

        spell_infobox_start_x = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                            section='newCharacter',
                                                                            parameter='NC_START_X')

        spell_infobox_start_y = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                            section='newCharacter',
                                                                            parameter='NC_START_Y')

        spell_infobox_width = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                          section='newCharacter',
                                                                          parameter='NC_WIDTH')
        spell_infobox_height = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                           section='newCharacter',
                                                                           parameter='NC_DEPTH')

        choices_start_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='newCharacter',
                                                                    parameter='CHOICES_BAR_Y')

        spell_info_top_left_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                      parameter=ascii_prefix + 'TOP_LEFT')

        spell_info_bottom_left_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                         parameter=ascii_prefix + 'BOTTOM_LEFT')

        spell_info_top_right_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                       parameter=ascii_prefix + 'TOP_RIGHT')

        spell_info_bottom_right_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                          parameter=ascii_prefix + 'BOTTOM_RIGHT')

        spell_info_horizontal = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                 parameter=ascii_prefix + 'HORIZONTAL')
        spell_info_vertical = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                               parameter=ascii_prefix + 'VERTICAL')

        items_splitter_left_t_junction = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                          parameter=ascii_prefix + 'LEFT_T_JUNCTION')
        items_splitter_right_t_junction = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                           parameter=ascii_prefix + 'RIGHT_T_JUNCTION')


        # set up UI --> options on the left --- flavour text on the right

        # render horizontal bottom
        for z in range(spell_infobox_start_x, (spell_infobox_start_x + spell_infobox_width)):
            terminal.printf(x=z, y=(spell_infobox_start_y + spell_infobox_height),
                            s=unicode_string_to_print + spell_info_horizontal + ']')
            terminal.printf(x=z, y=spell_infobox_start_y, s=unicode_string_to_print + spell_info_horizontal + ']')

        # render verticals
        for z in range(spell_infobox_start_y, (spell_infobox_start_y + spell_infobox_height) - 1):
            terminal.printf(x=spell_infobox_start_x, y=z + 1, s=unicode_string_to_print + spell_info_vertical + ']')
            terminal.printf(x=(spell_infobox_start_x + spell_infobox_width), y=z + 1,
                            s=unicode_string_to_print + spell_info_vertical + ']')

        # top left
        terminal.printf(x=spell_infobox_start_x, y=spell_infobox_start_y,
                        s=unicode_string_to_print + spell_info_top_left_corner + ']')
        # bottom left
        terminal.printf(x=spell_infobox_start_x, y=(spell_infobox_start_y + spell_infobox_height),
                        s=unicode_string_to_print + spell_info_bottom_left_corner + ']')
        # top right
        terminal.printf(x=(spell_infobox_start_x + spell_infobox_width), y=spell_infobox_start_y,
                        s=unicode_string_to_print + spell_info_top_right_corner + ']')
        # bottom right
        terminal.printf(x=(spell_infobox_start_x + spell_infobox_width),
                        y=(spell_infobox_start_y + spell_infobox_height),
                        s=unicode_string_to_print + spell_info_bottom_right_corner + ']')

        # render horizontal splitters
        for z in range(spell_infobox_start_x, (spell_infobox_start_x + spell_infobox_width)):
            terminal.printf(x=z, y=choices_start_y,
                            s=unicode_string_to_print + spell_info_horizontal + ']')

            terminal.printf(x=spell_infobox_start_x, y=choices_start_y,
                            s=unicode_string_to_print + items_splitter_left_t_junction + ']')

            terminal.printf(x=(spell_infobox_start_x + spell_infobox_width), y=choices_start_y,
                            s=unicode_string_to_print + items_splitter_right_t_junction + ']')


        # choices already made
        start_list_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='newCharacter',
                                                                   parameter='START_LIST_X')

        this_row = configUtilities.get_config_value_as_integer(configfile=game_config, section='newCharacter',
                                                                   parameter='START_LIST_Y')

        terminal.printf(x=start_list_x, y=this_row, s='Your Choices')
        this_row += 2
        terminal.printf(x=start_list_x, y=this_row, s='Race')
        this_row += 1
        terminal.printf(x=start_list_x, y=this_row, s='Class')
        this_row += 1
        terminal.printf(x=start_list_x, y=this_row, s='Gender')

        show_character_options = True
        selected_menu_option = 0

        player_race_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                      parameter='RACESFILE')
        menu_start_x = configUtilities.get_config_value_as_integer(game_config, 'newCharacter', 'MENU_START_X')
        menu_start_y = configUtilities.get_config_value_as_integer(game_config, 'newCharacter', 'MENU_START_Y')
        race_flavour_x = configUtilities.get_config_value_as_integer(game_config, 'newCharacter', 'RACE_CONSOLE_FLAVOR_X')
        original_race_flavour_y = configUtilities.get_config_value_as_integer(game_config, 'newCharacter', 'RACE_CONSOLE_FLAVOR_Y')
        race_benefits_x = configUtilities.get_config_value_as_integer(game_config, 'newCharacter', 'RACE_CONSOLE_BENEFITS_X')
        race_benefits_y = configUtilities.get_config_value_as_integer(game_config, 'newCharacter', 'RACE_CONSOLE_BENEFITS_Y')

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

        selected_menu_option = 0
        max_menu_option = len(race_name) - 1
        set_string_colour = "[color="
        set_green_for_racial_benefit = set_string_colour + colourUtilities.get('GREEN') + '][/color]Benefit'
        set_yellow_colour_for_print = set_string_colour + colourUtilities.get('YELLOW1') + "][/color]"

        while show_character_options:

            # display race options
            pointy_menu(header='',
                        menu_options=race_name, menu_id_format=True, menu_start_x=menu_start_x,
                        menu_start_y=menu_start_y,
                        blank_line=True, selected_option=selected_menu_option)

            # racial flavour text
            strings_list = []
            strings_list = textwrap.wrap(race_flavour[selected_menu_option], width=33)
            number_of_lines = len(strings_list)
            string_to_print = ''.join(strings_list)
            race_flavour_y = original_race_flavour_y
            for line in range(5):
                for wd in range(33):
                    terminal.printf(x=race_flavour_x + wd, y=race_flavour_y + line, s=' ')

            for line in strings_list:
                terminal.print_(x=race_flavour_x, y=race_flavour_y, s=line, width=spell_infobox_width, height=1)
                race_flavour_y += 1

            # racial benefits
            terminal.print_(x=race_benefits_x, y=race_benefits_y, s=set_green_for_racial_benefit)
            posy = 0
            for line in range(5):
                for wd in range(33):
                    terminal.printf(x=race_benefits_x + wd, y=race_benefits_y + line, s=' ')
            for benefit in race_benefits:
                if benefit[0] == selected_menu_option + 1:
                    string_to_print = set_yellow_colour_for_print + benefit[1]
                    terminal.printf(x=race_benefits_x, y=(race_benefits_y + 2) + posy, s=string_to_print)
                    posy += 1


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
                    if selected_menu_option == 0:  # something selected
                        gameworld = create_world()
                        terminal.clear()
            terminal.refresh()

    @staticmethod
    def display_character_creation_options():
        logger.info('Character creation options')
        game_config = configUtilities.load_config()
        menu_start_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'MENU_START_X')
        menu_start_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'MENU_START_Y')

        show_character_options = True
        selected_menu_option = 0

        while show_character_options:

            draw_colourful_frame(title=' Character Creation Options ', title_decorator=False, title_loc='centre',
                                 corner_decorator='', msg=0)

            # place game menu options
            pointy_menu(header='',
                        menu_options=['Create New Character', 'Random Character'], menu_id_format=True, menu_start_x=menu_start_x,
                        menu_start_y=menu_start_y, blank_line=True, selected_option=selected_menu_option)

            # blit changes to root console
            terminal.refresh()

            event_to_be_processed, event_action = handle_game_keys()
            if event_to_be_processed != '' and  event_to_be_processed == 'keypress':
                if event_action == 'quit':
                    show_character_options = False

                if event_action == 'up':
                    selected_menu_option -= 1
                    if selected_menu_option < 0:
                        selected_menu_option = 1
                if event_action == 'down':
                    selected_menu_option += 1
                    if selected_menu_option > 1:
                        selected_menu_option = 0
                if event_action == 'enter':
                    if selected_menu_option == 0:  # create new character
                        gameworld = create_world()
                        terminal.clear()
                        CharacterCreation.OLDcreate_new_character(gameworld=gameworld)
                    if selected_menu_option == 1:  # create random character
                        pass

    @staticmethod
    def OLDcreate_new_character(gameworld):

        game_config = configUtilities.load_config()

        logger.debug('Creating the player character entity')
        player_entity = MobileUtilities.get_next_entity_id(gameworld=gameworld)
        MobileUtilities.create_base_mobile(gameworld=gameworld, game_config=game_config, entity_id=player_entity)
        MobileUtilities.create_player_character(gameworld=gameworld, game_config=game_config,
                                                player_entity=player_entity)
        logger.info('Player character stored as entity {}', player_entity)

        CharacterCreation.choose_race(gameworld=gameworld, player=player_entity)

    @staticmethod
    def choose_race(gameworld, player):
        game_config = configUtilities.load_config()

        # get build entity --> build_entity only created here, never used here.
        _ = BuildLibrary.create_build_entity(gameworld=gameworld)

        player_race_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                      parameter='RACESFILE')
        menu_start_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'MENU_START_X')
        menu_start_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'MENU_START_Y')
        race_flavour_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'RACE_CONSOLE_FLAVOR_X')
        race_flavour_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'RACE_CONSOLE_FLAVOR_Y')
        race_benefits_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'RACE_CONSOLE_BENEFITS_X')
        race_benefits_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'RACE_CONSOLE_BENEFITS_Y')

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

        show_race_options = True
        selected_menu_option = 0
        max_menu_option = len(race_name) - 1
        set_string_colour = '[color='
        set_green_for_racial_benefit = set_string_colour + colourUtilities.get('GREEN') + '[/color]Benefit'
        set_yellow_colour_for_print = set_string_colour + colourUtilities.get('YELLOW1') + '[/color]'

        while show_race_options:

            draw_colourful_frame(title=' Character Creation - Select Race ', title_decorator=False, title_loc='centre',
                                 corner_decorator='', msg=0)

            pointy_menu(header='',
                        menu_options=race_name, menu_id_format=True, menu_start_x=menu_start_x,
                        menu_start_y=menu_start_y,
                        blank_line=True, selected_option=selected_menu_option)

            # racial flavour text
            wd = 37
            terminal.clear_area(x=race_flavour_x, y=race_flavour_y, width=wd, height=2)
            terminal.print_(x=race_flavour_x, y=race_flavour_y, s=race_flavour[selected_menu_option], width=wd,
                            height=2)

            # racial benefits
            terminal.print_(x=race_benefits_x, y=race_benefits_y, s=set_green_for_racial_benefit)

            posy = 0
            for benefit in race_benefits:
                if benefit[0] == selected_menu_option + 1:
                    string_to_print = set_yellow_colour_for_print + benefit[1]
                    terminal.printf(x=race_benefits_x, y=(race_benefits_y + 2) + posy, s=string_to_print)
                    posy += 1

            # blit changes to root console
            terminal.refresh()

            event_to_be_processed, event_action = handle_game_keys()
            if event_to_be_processed != '':
                terminal.clear()
                if event_to_be_processed == 'keypress':
                    if event_action == 'quit':
                        show_race_options = False
                    if event_action == 'up':
                        selected_menu_option -= 1
                        if selected_menu_option < 0:
                            selected_menu_option = max_menu_option
                    if event_action == 'down':
                        selected_menu_option += 1
                        if selected_menu_option > max_menu_option:
                            selected_menu_option = 0
                    if event_action == 'enter':
                        MobileUtilities.setup_racial_attributes(
                            gameworld=gameworld, player=player, selected_race=race_name[selected_menu_option],
                            race_size=race_size[selected_menu_option], bg=race_bg_colour[selected_menu_option], race_names=race_name_desc[selected_menu_option])
                        logger.info('Race selected:' + race_name[selected_menu_option])
                        CharacterCreation.choose_class(gameworld)
        terminal.clear()

    @staticmethod
    def choose_class(gameworld):
        game_config = configUtilities.load_config()

        player_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                       parameter='CLASSESFILE')
        build_entity = BuildLibrary.get_build_entity(gameworld=gameworld)
        class_flavour_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'CLASS_CONSOLE_FLAVOR_X')
        class_flavour_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'CLASS_CONSOLE_FLAVOR_Y')
        class_menu_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'CLASS_MENU_X')
        class_menu_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'CLASS_MENU_Y')
        class_package_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'CLASS_PACKAGE_X')
        class_package_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'CLASS_PACKAGE_Y')
        jewellery_packages = configUtilities.get_config_value_as_list(game_config, 'newgame', 'JEWELLERY_PACKAGES')
        jewellery_locations = configUtilities.get_config_value_as_list(game_config, 'newgame', 'JEWELLERY_LOCATIONS')

        logger.info('Selecting character class')
        class_file = read_json_file(player_class_file)

        menu_options = []
        menu_options_flavour = []
        class_health = []
        class_weapons = []
        class_defense_benefits = []
        class_balanced_benefits = []
        class_offense_benefits = []
        class_spell_file = []

        for option in class_file['classes']:
            menu_options.append(option['name'])
            menu_options_flavour.append(option['flavour'])
            class_health.append(option['health'])
            class_spell_file.append(option['spellfile'])
            class_weapons.append(option['weapons'])
            class_defense_benefits.append(option['defensive'])
            class_balanced_benefits.append(option['balanced'])
            class_offense_benefits.append(option['offensive'])

        defensive_class = [['' for _ in range(5)] for _ in range(len(menu_options))]
        balanced_class = [['' for _ in range(5)] for _ in range(len(menu_options))]
        offensive_class = [['' for _ in range(5)] for _ in range(len(menu_options))]

        for class_counter in range(len(menu_options)):
            defensive_class[class_counter][0] = class_defense_benefits[class_counter]['neck']
            defensive_class[class_counter][1] = class_defense_benefits[class_counter]['ring1']
            defensive_class[class_counter][2] = class_defense_benefits[class_counter]['ring2']
            defensive_class[class_counter][3] = class_defense_benefits[class_counter]['earring1']
            defensive_class[class_counter][4] = class_defense_benefits[class_counter]['earring2']

            balanced_class[class_counter][0] = class_balanced_benefits[class_counter]['neck']
            balanced_class[class_counter][1] = class_balanced_benefits[class_counter]['ring1']
            balanced_class[class_counter][2] = class_balanced_benefits[class_counter]['ring2']
            balanced_class[class_counter][3] = class_balanced_benefits[class_counter]['earring1']
            balanced_class[class_counter][4] = class_balanced_benefits[class_counter]['earring2']

            offensive_class[class_counter][0] = class_offense_benefits[class_counter]['neck']
            offensive_class[class_counter][1] = class_offense_benefits[class_counter]['ring1']
            offensive_class[class_counter][2] = class_offense_benefits[class_counter]['ring2']
            offensive_class[class_counter][3] = class_offense_benefits[class_counter]['earring1']
            offensive_class[class_counter][4] = class_offense_benefits[class_counter]['earring2']

        class_not_selected = True
        selected_menu_option = 0
        max_menu_option = len(menu_options) - 1
        package_selected = 1

        set_colour_white_in_print = '[color=' + colourUtilities.get('WHITE') + '][/color]'
        set_colour_blue_in_print = '[color=' + colourUtilities.get('BLUE') + ']'
        set_jewellery_bonus_print = '[color=' + colourUtilities.get('YELLOW1') + ']Jewellery Bonus[/color]'

        while class_not_selected:

            draw_colourful_frame(title='Character Creation - Select Class', title_decorator=False, title_loc='centre',
                                 corner_decorator='', msg=1)

            pointy_menu(header='',
                        menu_options=menu_options, menu_id_format=True, menu_start_x=class_menu_x,
                        menu_start_y=class_menu_y,
                        blank_line=True, selected_option=selected_menu_option)

            # draw class flavour text
            terminal.clear_area(x=class_flavour_x, y=class_flavour_y, width=30, height=10)
            terminal.print_(x=class_flavour_x, y=class_flavour_y, width=30, height=10,
                            s=menu_options_flavour[selected_menu_option])

            # draw jewellery title
            terminal.printf(x=class_package_x + 15, y=class_package_y - 2, s=set_jewellery_bonus_print)

            coloured_list(list_options=jewellery_locations,
                          list_x=class_package_x, list_y=class_package_y + 2,
                          selected_option='nothing',
                          blank_line=False, fg=colourUtilities.get('WHITE'))

            # draw class packages incl jewellery benefits
            pkg_pointer = '>'
            pkg_empty = ' '
            p1 = 9
            p2 = 24
            p3 = 39
            if package_selected == 1:
                string_to_print = set_colour_blue_in_print + pkg_pointer + '[/color]' + jewellery_packages[0]

                terminal.print(x=class_package_x + p1, y=class_package_y, s=string_to_print)
                string_to_print = set_colour_white_in_print + pkg_empty + jewellery_packages[1]
                terminal.print(x=class_package_x + p2, y=class_package_y, s=string_to_print)
                string_to_print = set_colour_white_in_print + pkg_empty + jewellery_packages[2]
                terminal.print(x=class_package_x + p3, y=class_package_y, s=string_to_print)
            if package_selected == 2:
                string_to_print = set_colour_white_in_print + pkg_empty + jewellery_packages[0]
                terminal.print(x=class_package_x + p1, y=class_package_y, s=string_to_print)
                string_to_print = set_colour_blue_in_print + pkg_pointer + '[/color]' + jewellery_packages[1]
                terminal.print(x=class_package_x + p2, y=class_package_y, s=string_to_print)
                string_to_print = set_colour_white_in_print + pkg_empty + jewellery_packages[2]
                terminal.print(x=class_package_x + p3, y=class_package_y, s=string_to_print)
            if package_selected == 3:
                string_to_print = set_colour_white_in_print + pkg_empty + jewellery_packages[0]
                terminal.print(x=class_package_x + p1, y=class_package_y, s=string_to_print)
                string_to_print = set_colour_white_in_print + pkg_empty + jewellery_packages[1]
                terminal.print(x=class_package_x + p2, y=class_package_y, s=string_to_print)
                string_to_print = set_colour_blue_in_print + pkg_pointer + '[/color]' + jewellery_packages[2]
                terminal.print(x=class_package_x + p3, y=class_package_y, s=string_to_print)

            counter = class_package_y + 2
            for loc in range(5):
                terminal.clear_area(x=class_package_x + 10, y=counter, width=20, height=5)
                string_to_print = set_colour_white_in_print + defensive_class[selected_menu_option][loc]
                terminal.print(class_package_x + 10, y=counter, s=string_to_print)

                terminal.clear_area(x=class_package_x + 25, y=counter, width=20, height=5)
                string_to_print = set_colour_white_in_print + balanced_class[selected_menu_option][loc]
                terminal.print(class_package_x + 25, y=counter, s=string_to_print)

                terminal.clear_area(x=class_package_x + 40, y=counter, width=14, height=5)
                string_to_print = set_colour_white_in_print + offensive_class[selected_menu_option][loc]
                terminal.print(class_package_x + 40, y=counter, s=string_to_print)

                counter += 1

            # blit changes to root console
            terminal.refresh()

            event_to_be_processed, event_action = handle_game_keys()
            if event_to_be_processed != '':
                terminal.clear()
                if event_to_be_processed == 'keypress':
                    if event_action == 'quit':
                        class_not_selected = False
                    if event_action == 'up':
                        selected_menu_option -= 1
                        if selected_menu_option < 0:
                            selected_menu_option = max_menu_option
                    if event_action == 'down':
                        selected_menu_option += 1
                        if selected_menu_option > max_menu_option:
                            selected_menu_option = 0
                    if event_action == 'left':
                        package_selected -= 1
                        if package_selected < 1:
                            package_selected = 3
                    if event_action == 'right':
                        package_selected += 1
                        if package_selected > 3:
                            package_selected = 1
                    if event_action == 'enter':
                        if package_selected == 1:
                            BuildLibrary.set_build_jewellery(gameworld=gameworld, entity=build_entity, label='A')

                        if package_selected == 2:
                            BuildLibrary.set_build_jewellery(gameworld=gameworld, entity=build_entity, label='B')

                        if package_selected == 3:
                            BuildLibrary.set_build_jewellery(gameworld=gameworld, entity=build_entity, label='C')

                        player = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
                        MobileUtilities.setup_class_attributes(gameworld=gameworld, player=player,
                                                               selected_class=menu_options[selected_menu_option],
                                                               health=int(class_health[selected_menu_option]),
                                                               spellfile=class_spell_file[selected_menu_option])

                        # CharacterCreation.choose_weapons(gameworld=gameworld,
                        #                                  selected_class=menu_options[selected_menu_option])

                        CharacterCreation.generate_player_character_from_choices(gameworld=gameworld)

        terminal.clear()

    @staticmethod
    def select_personality_choices(con, gameworld, player, game_config):
        # The personality-oriented question affects the conversational options that NPCs provide.
        # there will be 3 options: charm, dignity, ferocity

        MobileUtilities.set_mobile_derived_personality(gameworld=gameworld, game_config=game_config, entity=player)

        personality_component = gameworld.component_for_entity(player, mobiles.Describable)

        logger.debug('Your personality is viewed as {} by other NPCs', personality_component.personality_title)

    @staticmethod
    def choose_weapons(gameworld, selected_class):
        # get config items
        game_config = configUtilities.load_config()
        class_spellfile = ''

        player_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                       parameter='CLASSESFILE')
        start_panel_frame_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_X')
        start_panel_frame_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_Y')
        start_panel_frame_width = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                              'START_PANEL_FRAME_WIDTH')

        logger.info('Selecting weapons')
        class_file = read_json_file(player_class_file)

        available_weapons = []

        # gather list of available weapons for the player class
        for option in class_file['classes']:
            if option['name'] == selected_class:
                class_weapons = option['weapons']
                class_spellfile = option['spellfile']

        if class_weapons['sword'] == 'true':
            available_weapons.append('sword')
        if class_weapons['wand'] == 'true':
            available_weapons.append('wand')
        if class_weapons['scepter'] == 'true':
            available_weapons.append('scepter')
        if class_weapons['staff'] == 'true':
            available_weapons.append('staff')
        if class_weapons['dagger'] == 'true':
            available_weapons.append('dagger')
        if class_weapons['rod'] == 'true':
            available_weapons.append('rod')
        if class_weapons['focus'] == 'true':
            available_weapons.append('focus')

        logger.info('Available weapons for a {} are {}', selected_class, available_weapons)

        # for each available weapon, gather: weapon info & spells associated to it
        weapon_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                       parameter='WEAPONSFILE')

        spellsfile = class_spellfile.upper() + '_SPELLSFILE'

        spell_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                      parameter=spellsfile)

        weapon_file = read_json_file(weapon_class_file)
        spell_file = read_json_file(spell_class_file)

        # initialise blank 2D list (array)
        weapon_info = [['' for _ in range(3)] for _ in range(len(available_weapons))]
        spell_name = [['' for _ in range(6)] for _ in range(len(available_weapons))]
        spell_descripton = [['' for _ in range(6)] for _ in range(len(available_weapons))]
        spell_cast_time = [['' for _ in range(6)] for _ in range(len(available_weapons))]
        spell_cool_down = [['' for _ in range(6)] for _ in range(len(available_weapons))]
        spell_distance = [['' for _ in range(6)] for _ in range(len(available_weapons))]

        weapon_name = 0
        weapon_hands = 1
        weapon_quality = 2

        weapon_counter = 0
        for weapon in available_weapons:
            for wpn in weapon_file['weapons']:
                if wpn['name'] == weapon:
                    weapon_info[weapon_counter][weapon_name] = wpn['display_name']
                    weapon_info[weapon_counter][weapon_hands] = wpn['wielded_hands']
                    weapon_info[weapon_counter][weapon_quality] = wpn['quality_level']

                    for spell in spell_file['spells']:
                        if spell['type_of_spell'] == 'combat' and spell['weapon_type'] == weapon:
                            slot_id = int(spell['weapon_slot'])

                            spell_name[weapon_counter][slot_id] = spell['name']
                            spell_descripton[weapon_counter][slot_id] = spell['short_description']
                            spell_cast_time[weapon_counter][slot_id] = 'Cast time:' + spell['turns_to_cast']
                            spell_cool_down[weapon_counter][slot_id] = 'Cool down:' + spell['cool_down']
                            spell_range = -1
                            range_of_spell = configUtilities.get_config_value_as_string(configfile=game_config,
                                                                                      section='spells',
                                                                                      parameter=spell[
                                                                                          'spell_range'].upper())
                            if range_of_spell != '':
                                spell_range = int(range_of_spell)
                            else:
                                logger.warning('Spell Range is set to zero! file:{} spell name:{}', spellsfile,
                                               spell['name'])
                            spell_distance[weapon_counter][slot_id] = 'Range:' + str(spell_range)
                    weapon_counter += 1

        menu_options = available_weapons

        show_weapons_options = True
        selected_menu_option = 0
        main_hand_selected_weapon = 'nothing'
        off_hand_selected_weapon = 'nothing'
        hand_choice = 1
        hand_selector = chr(62)
        main_hand_color = colourUtilities.get('DARKORANGE4')
        off_hand_color = colourUtilities.get('BLUE')
        spell_name_color = colourUtilities.get('PALEGREEN')
        spell_description_color = colourUtilities.get('BISQUE4')
        spell_cast_time_color = colourUtilities.get('KHAKI3')
        spell_cool_down_color = colourUtilities.get('LIGHTBLUE3')
        spell_range_color = colourUtilities.get('MOCCASIN')
        bg = colourUtilities.get('BLACK')
        back_colour = '[bkcolor=' + bg + '][/bkcolor]'

        spell_name_colour_print = '[color=' + spell_name_color + '][/color]' + back_colour
        spell_description_colour_print = '[color=' + spell_description_color + '][/color]' + back_colour
        spell_cast_time_color_print = '[color=' + spell_cast_time_color + '][/color]' + back_colour
        spell_cool_down_colour_print = '[color=' + spell_cool_down_color + '][/color]' + back_colour
        spell_range_colour_print = '[color=' + spell_range_color + '][/color]' + back_colour


        max_menu_option = len(menu_options) - 1
        off_hand_weapon_id = 0
        main_hand_weapon_id = 0
        set_colour_white_in_print = '[color=' + colourUtilities.get('WHITE') + '][/color]'

        pxx = [10, 23, 36, 52, 65]
        py = start_panel_frame_y + 17
        panell_width = start_panel_frame_width - start_panel_frame_x
        slot_box_gap = int((panell_width / 5))
        wd = slot_box_gap - 2

        while show_weapons_options:
            draw_colourful_frame(title='Character Creation - Select Weapon', title_decorator=False, title_loc='centre',
                                 corner_decorator='', msg=1)

            # list available weapons
            pointy_menu(header='',
                        menu_options=menu_options, menu_id_format=True, menu_start_x=start_panel_frame_x + 3,
                        menu_start_y=start_panel_frame_y + 4, blank_line=True, selected_option=selected_menu_option)

            weapon_info_string = 'This is ' + weapon_info[selected_menu_option][weapon_name] + '\n' + \
                               'Wielded in ' + weapon_info[selected_menu_option][weapon_hands] + ' hand(s) \n' + \
                               'Weapon quality ' + weapon_info[selected_menu_option][weapon_quality]
            # display weapon slot labels
            # display spell slot labels x,y values

            for weapon_slot in range(1, 6):
                if weapon_slot < 4:
                    foreground_colour = main_hand_color
                else:
                    foreground_colour = off_hand_color
                str_to_print = '[color=' + foreground_colour + ']SLOT ' + str(weapon_slot)
                terminal.print_(x=pxx[weapon_slot - 1], y=py - 1, s=str_to_print)

            # display weapon info as a block of information
            str_to_print = set_colour_white_in_print + weapon_info_string
            terminal.print_(x=start_panel_frame_x + 15, y=(start_panel_frame_y + 5), width=30, height=4, s=str_to_print)

            # display spell information for each of the weapon/spell slots
            px = start_panel_frame_x + 5

            if main_hand_selected_weapon != 'nothing':
                string_to_print = spell_name_colour_print + spell_name[main_hand_weapon_id][1]
                terminal.print_(x=px, y=py, width=wd, height=2, s=string_to_print)

                string_to_print = spell_description_colour_print + spell_descripton[main_hand_weapon_id][1]
                terminal.print_(x=px, y=py + 3, width=wd, height=8, s=string_to_print)

                string_to_print = spell_cast_time_color_print + spell_cast_time[main_hand_weapon_id][1]
                terminal.print_(x=px, y=py + 12, width=wd, height=1, s=string_to_print)

                string_to_print = spell_cool_down_colour_print + spell_cool_down[main_hand_weapon_id][1]
                terminal.print_(x=px, y=py + 13, width=wd, height=1, s=string_to_print)

                string_to_print = spell_range_colour_print + spell_distance[main_hand_weapon_id][1]
                terminal.print_(x=px, y=py + 14, width=wd, height=1, s=string_to_print)

                px += slot_box_gap

                string_to_print = spell_name_colour_print + spell_name[main_hand_weapon_id][2]
                terminal.print_(x=px, y=py, width=wd, height=2, s=string_to_print)

                string_to_print = spell_description_colour_print + spell_descripton[main_hand_weapon_id][2]
                terminal.print_(x=px, y=py + 3, width=wd, height=8, s=string_to_print)

                string_to_print = spell_cast_time_color_print + spell_cast_time[main_hand_weapon_id][2]
                terminal.print_(x=px, y=py + 12, width=wd, height=1, s=string_to_print)

                string_to_print = spell_cool_down_colour_print + spell_cool_down[main_hand_weapon_id][2]
                terminal.print_(x=px, y=py + 13, width=wd, height=1, s=string_to_print)

                string_to_print = spell_range_colour_print + spell_distance[main_hand_weapon_id][2]
                terminal.print_(x=px, y=py + 14, width=wd, height=1, s=string_to_print)

                px += slot_box_gap

                string_to_print = spell_name_colour_print + spell_name[main_hand_weapon_id][3]
                terminal.print_(x=px, y=py, width=wd, height=2, s=string_to_print)

                string_to_print = spell_description_colour_print + spell_descripton[main_hand_weapon_id][3]
                terminal.print_(x=px, y=py + 3, width=wd, height=8, s=string_to_print)

                string_to_print = spell_cast_time_color_print + spell_cast_time[main_hand_weapon_id][3]
                terminal.print_(x=px, y=py + 12, width=wd, height=1, s=string_to_print)

                string_to_print = spell_cool_down_colour_print + spell_cool_down[main_hand_weapon_id][3]
                terminal.print_(x=px, y=py + 13, width=wd, height=1, s=string_to_print)

                string_to_print = spell_range_colour_print + spell_distance[main_hand_weapon_id][3]
                terminal.print_(x=px, y=py + 14, width=wd, height=1, s=string_to_print)

                px += slot_box_gap

            if off_hand_selected_weapon != 'nothing':
                px = 52

                string_to_print = spell_name_colour_print + spell_name[main_hand_weapon_id][4]
                terminal.print_(x=px, y=py, width=wd, height=2, s=string_to_print)

                string_to_print = spell_description_colour_print + spell_descripton[main_hand_weapon_id][4]
                terminal.print_(x=px, y=py + 3, width=wd, height=8, s=string_to_print)

                string_to_print = spell_cast_time_color_print + spell_cast_time[main_hand_weapon_id][4]
                terminal.print_(x=px, y=py + 12, width=wd, height=1, s=string_to_print)

                string_to_print = spell_cool_down_colour_print + spell_cool_down[main_hand_weapon_id][4]
                terminal.print_(x=px, y=py + 13, width=wd, height=1, s=string_to_print)

                string_to_print = spell_range_colour_print + spell_distance[main_hand_weapon_id][4]
                terminal.print_(x=px, y=py + 14, width=wd, height=1, s=string_to_print)

                px += slot_box_gap

                string_to_print = spell_name_colour_print + spell_name[main_hand_weapon_id][5]
                terminal.print_(x=px, y=py, width=wd, height=2, s=string_to_print)

                string_to_print = spell_description_colour_print + spell_descripton[main_hand_weapon_id][5]
                terminal.print_(x=px, y=py + 3, width=wd, height=8, s=string_to_print)

                string_to_print = spell_cast_time_color_print + spell_cast_time[main_hand_weapon_id][5]
                terminal.print_(x=px, y=py + 12, width=wd, height=1, s=string_to_print)

                string_to_print = spell_cool_down_colour_print + spell_cool_down[main_hand_weapon_id][5]
                terminal.print_(x=px, y=py + 13, width=wd, height=1, s=string_to_print)

                string_to_print = spell_range_colour_print + spell_distance[main_hand_weapon_id][5]
                terminal.print_(x=px, y=py + 14, width=wd, height=1, s=string_to_print)

            # display main / off hand labels + weapon type selected
            main_hand_weapon = 'MAIN HAND (' + main_hand_selected_weapon + ')    '
            off_hand_weapon = 'OFF HAND (' + off_hand_selected_weapon + ')    '
            if hand_choice == 1:
                terminal.clear_area(x=start_panel_frame_x + 49, y=start_panel_frame_y + 14, width=1, height=1)
                string_to_print = '[color=' + colourUtilities.get('YELLOW1') + ']' + hand_selector
                terminal.print(x=start_panel_frame_x + 19, y=start_panel_frame_y + 14, s=string_to_print)
            else:
                terminal.clear_area(x=start_panel_frame_x + 19, y=start_panel_frame_y + 14, width=1, height=1)
                string_to_print = '[color=' + colourUtilities.get('BLUE') + ']' + hand_selector
                terminal.print(x=start_panel_frame_x + 49, y=start_panel_frame_y + 14, s=string_to_print)

            string_to_print = '[color=' + main_hand_color + '][/color]' + main_hand_weapon
            terminal.print(x=start_panel_frame_x + 20, y=start_panel_frame_y + 14, s=string_to_print)

            string_to_print = '[color=' + off_hand_color + '][/color]' + off_hand_weapon
            terminal.print(x=start_panel_frame_x + 50, y=start_panel_frame_y + 14, s=string_to_print)

            # blit changes to root console
            terminal.refresh()

            event_to_be_processed, event_action = handle_game_keys()
            if event_to_be_processed != '':
                terminal.clear()
                if event_to_be_processed == 'textinput':
                    if event_action == 'z':
                        logger.info('clear weapons')
                        main_hand_weapon_id = 0
                        main_hand_selected_weapon = 'nothing'
                        off_hand_weapon_id = 0
                        off_hand_selected_weapon = 'nothing'

                if event_to_be_processed == 'keypress':
                    if event_action == 'quit':
                        show_weapons_options = False
                    if event_action == 'up':
                        selected_menu_option -= 1
                        if selected_menu_option < 0:
                            selected_menu_option = max_menu_option
                    if event_action == 'down':
                        selected_menu_option += 1
                        if selected_menu_option > max_menu_option:
                            selected_menu_option = 0
                    if event_action == 'left':
                        hand_choice -= 1
                        if hand_choice < 1:
                            hand_choice = 2
                    if event_action == 'right':
                        hand_choice += 1
                        if hand_choice > 2:
                            hand_choice = 1
                    if event_action == 'enter':
                        if main_hand_selected_weapon != 'nothing' and off_hand_selected_weapon != 'nothing':
                            CharacterCreation.choose_armourset(gameworld=gameworld, main_hand=main_hand_selected_weapon,
                                                               off_hand=off_hand_selected_weapon)

                        if weapon_info[selected_menu_option][weapon_hands] == 'off' and hand_choice == 2:
                            if off_hand_weapon_id == main_hand_weapon_id:
                                main_hand_weapon_id = 0
                                main_hand_selected_weapon = 'nothing'
                            off_hand_selected_weapon = available_weapons[selected_menu_option]
                            off_hand_weapon_id = selected_menu_option

                        if weapon_info[selected_menu_option][weapon_hands] == 'main' and hand_choice == 1:
                            if off_hand_weapon_id == main_hand_weapon_id:
                                off_hand_weapon_id = 0
                                off_hand_selected_weapon = 'nothing'
                            main_hand_selected_weapon = available_weapons[selected_menu_option]
                            main_hand_weapon_id = selected_menu_option

                        if weapon_info[selected_menu_option][weapon_hands] == 'both':
                            main_hand_selected_weapon = available_weapons[selected_menu_option]
                            off_hand_selected_weapon = available_weapons[selected_menu_option]
                            off_hand_weapon_id = selected_menu_option
                            main_hand_weapon_id = selected_menu_option

    @staticmethod
    def choose_armourset(gameworld, main_hand, off_hand):
        # get config items
        game_config = configUtilities.load_config()

        armourset_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                    parameter='ARMOURSETFILE')
        armour_menu_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'ARMOUR_MENU_X')
        armour_menu_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'ARMOUR_MENU_Y')
        armour_desc_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'ARMOUR_DESCRIPTION_X')
        armour_desc_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'ARMOUR_DESCRIPTION_Y')

        logger.info('Selecting armourset')
        armour_file = read_json_file(armourset_file)

        as_internal_name = []
        as_display_name = ''
        as_flavour = ''
        as_material = ''
        as_prefix_list = []
        px_flavour = []
        px_att_name = []
        px_att_bonus = []
        pxstring = 'prefix'
        attnamestring = 'attributename'
        attvaluestring = 'attributebonus'

        for armourset in armour_file['armoursets']:
            if armourset['startset'] == 'true':
                as_internal_name.append(armourset['internalsetname'])
                as_display_name = (armourset['displayname'])
                as_flavour = (armourset['flavour'])
                as_material = (armourset['material'])
                as_prefix_list = armourset['prefixlist'].split(",")
                prefix_count = armourset['prefixcount']
                attribute_bonus_count = armourset['attributebonuscount']

                for px in range(1, prefix_count + 1):
                    prefix_string = pxstring + str(px)
                    px_flavour.append(armourset[prefix_string]['flavour'])

                    if attribute_bonus_count > 1:
                        att_bonus_string = attvaluestring + str(px)
                        att_name_string = attnamestring + str(px)
                    else:
                        att_bonus_string = attvaluestring + str(1)
                        att_name_string = attnamestring + str(1)

                    px_att_bonus.append(armourset[prefix_string][att_bonus_string])
                    px_att_name.append(armourset[prefix_string][att_name_string])

        flx = 38
        attx = 20

        show_armour_options = True
        selected_menu_option = 0
        menu_options = as_prefix_list
        max_menu_option = len(menu_options) - 1

        while show_armour_options:

            draw_colourful_frame(title=' Character Creation - Choose Armourset ', title_decorator=False,
                                 title_loc='centre', corner_decorator='', msg=0)

            armour_description = 'You will be wearing ' + as_display_name + ' armour, ' + 'which is made from ' + \
                                 as_material + '. ' + 'Your colleagues would describe it as ' + as_flavour

            string_to_print = '[color=' + colourUtilities.get('PALEGREEN') + ']' + armour_description
            terminal.print_(x=armour_desc_x, y=armour_desc_y, width=50, height=6, s=string_to_print)
            # list available armour
            string_to_print = '[color=' + colourUtilities.get('BLUE') + ']' + 'You can modify your armour thus...'
            terminal.print_(x=23, y=8, s=string_to_print)

            # armour column titles
            string_to_print = '[color=' + colourUtilities.get('LIGHTSLATEGRAY') + ']' + 'Prefix'
            terminal.print(x=armour_menu_x + 2, y=armour_menu_y - 1, s=string_to_print)

            string_to_print = '[color=' + colourUtilities.get('LIGHTSLATEGRAY') + ']' + 'Bonus to...'
            terminal.print(x=attx, y=armour_menu_y - 1, s=string_to_print)

            string_to_print = '[color=' + colourUtilities.get('LIGHTSLATEGRAY') + ']' + 'Flavour'
            terminal.print(x=flx, y=armour_menu_y - 1, s=string_to_print)

            # blit changes to root console
            terminal.refresh()

            pointy_menu(header='',
                        menu_options=menu_options, menu_id_format=True, menu_start_x=armour_menu_x,
                        menu_start_y=armour_menu_y, blank_line=True, selected_option=selected_menu_option)

            # display attribute to be modified
            fg = colourUtilities.get('LIGHTBLUE1')
            coloured_list(list_options=px_att_name,
                          list_x=attx, list_y=armour_menu_y,
                          selected_option='nothing', blank_line=True, fg=fg)

            # display flavour text
            coloured_list(list_options=px_flavour,
                          list_x=flx, list_y=armour_menu_y,
                          selected_option='nothing', blank_line=True, fg=fg)

            event_to_be_processed, event_action = handle_game_keys()
            if event_to_be_processed != '':
                if event_to_be_processed == 'keypress':
                    if event_action == 'quit':
                        show_armour_options = False
                    if event_action == 'up':
                        selected_menu_option -= 1
                        if selected_menu_option < 0:
                            selected_menu_option = max_menu_option
                    if event_action == 'down':
                        selected_menu_option += 1
                        if selected_menu_option > max_menu_option:
                            selected_menu_option = 0
                    if event_action == 'enter':
                        armourset = as_display_name
                        armour_prefix = menu_options[selected_menu_option]

                        # assign armour prefix benefit
                        player = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)

                        if menu_options[selected_menu_option].lower() == 'healer':
                            current_healingpower = MobileUtilities.get_mobile_secondary_healing_power(gameworld=gameworld,
                                                                                                      entity=player)
                            px_bonus = int(px_att_bonus[selected_menu_option])
                            new_bonus = current_healingpower + px_bonus
                            MobileUtilities.set_mobile_secondary_healing_power(gameworld=gameworld, entity=player,
                                                                               value=new_bonus)

                        if menu_options[selected_menu_option].lower() == 'malign':
                            current_condidamage = MobileUtilities.get_mobile_secondary_condition_damage(gameworld=gameworld,
                                                                                                        entity=player)
                            px_bonus = int(px_att_bonus[selected_menu_option])
                            new_bonus = current_condidamage + px_bonus
                            MobileUtilities.set_mobile_secondary_condition_damage(gameworld=gameworld, entity=player,
                                                                                  value=new_bonus)

                        if menu_options[selected_menu_option].lower() == 'mighty':
                            current_power = MobileUtilities.get_mobile_primary_power(gameworld=gameworld, entity=player)
                            px_bonus = int(px_att_bonus[selected_menu_option])
                            new_bonus = current_power + px_bonus
                            MobileUtilities.set_mobile_primary_power(gameworld=gameworld, entity=player, value=new_bonus)

                        if menu_options[selected_menu_option].lower() == 'precise':
                            current_precision = MobileUtilities.get_mobile_primary_precision(gameworld=gameworld, entity=player)
                            px_bonus = int(px_att_bonus[selected_menu_option])
                            new_bonus = current_precision + px_bonus
                            MobileUtilities.set_mobile_primary_precision(gameworld=gameworld, entity=player, value=new_bonus)

                        if menu_options[selected_menu_option].lower() == 'resilient':
                            current_toughness = MobileUtilities.get_mobile_primary_toughness(gameworld=gameworld, entity=player)
                            px_bonus = int(px_att_bonus[selected_menu_option])
                            new_bonus = current_toughness + px_bonus
                            MobileUtilities.set_mobile_primary_toughness(gameworld=gameworld, entity=player, value=new_bonus)

                        if menu_options[selected_menu_option].lower() == 'vital':
                            current_vitality = MobileUtilities.get_mobile_primary_vitality(gameworld=gameworld, entity=player)
                            px_bonus = int(px_att_bonus[selected_menu_option])
                            new_bonus = current_vitality + px_bonus
                            MobileUtilities.set_mobile_primary_vitality(gameworld=gameworld, entity=player, value=new_bonus)
                        #
                        # now generate the player character - part 1
                        #
                        CharacterCreation.generate_player_character_from_choices(gameworld=gameworld)

    @staticmethod
    def generate_player_character_from_choices(gameworld):
        # get config items
        game_config = configUtilities.load_config()

        player_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                       parameter='CLASSESFILE')

        # get player entity
        player = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)

        build_entity = BuildLibrary.get_build_entity(gameworld=gameworld)

        # get race details for character
        racial_details = MobileUtilities.get_mobile_race_details(gameworld=gameworld, entity=player)
        player_race = racial_details[0]

        # create racial bonuses
        if player_race.lower() == 'dilga':
            BuildLibrary.set_build_race(gameworld=gameworld, entity=build_entity, label='A')
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
            BuildLibrary.set_build_race(gameworld=gameworld, entity=build_entity, label='B')
            cur_power = MobileUtilities.get_mobile_primary_power(gameworld=gameworld, entity=player)
            cur_concentration = MobileUtilities.get_mobile_secondary_concentration(gameworld=gameworld, entity=player)

            cur_power += 1
            MobileUtilities.set_mobile_primary_power(gameworld=gameworld, entity=player, value=cur_power)
            cur_concentration += 1
            MobileUtilities.set_mobile_secondary_concentration(gameworld=gameworld, entity=player, value=cur_concentration)

        if player_race.lower() == 'jogah':
            BuildLibrary.set_build_race(gameworld=gameworld, entity=build_entity, label='C')
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
            BuildLibrary.set_build_race(gameworld=gameworld, entity=build_entity, label='D')
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


        # # create starting armour from armourset and prefix
        # this_armourset = ItemManager.create_full_armour_set(gameworld=gameworld, armourset=armourset,
        #                                                     prefix=armour_prefix, game_config=game_config)
        #
        #
        # ItemUtilities.equip_full_set_of_armour(gameworld=gameworld, entity=player, armourset=this_armourset)
        #
        # # update buildcode
        # if armour_prefix.lower() == 'giver':
        #     BuildLibrary.set_build_armour(gameworld=gameworld, entity=build_entity, label='A')
        # if armour_prefix.lower() == 'healer':
        #     BuildLibrary.set_build_armour(gameworld=gameworld, entity=build_entity, label='B')
        # if armour_prefix.lower() == 'malign':
        #     BuildLibrary.set_build_armour(gameworld=gameworld, entity=build_entity, label='C')
        # if armour_prefix.lower() == 'mighty':
        #     BuildLibrary.set_build_armour(gameworld=gameworld, entity=build_entity, label='D')
        # if armour_prefix.lower() == 'precise':
        #     BuildLibrary.set_build_armour(gameworld=gameworld, entity=build_entity, label='E')
        # if armour_prefix.lower() == 'resilient':
        #     BuildLibrary.set_build_armour(gameworld=gameworld, entity=build_entity, label='F')
        # if armour_prefix.lower() == 'vital':
        #     BuildLibrary.set_build_armour(gameworld=gameworld, entity=build_entity, label='G')
        #
        # # create starting weapon(s) - based on what's passed into this method
        # if main_hand == off_hand:
        #     logger.info('creating a starting 2-handed weapon for the player')
        #
        #     created_weapon = ItemManager.create_weapon(gameworld=gameworld, weapon_type=main_hand,
        #                                                game_config=game_config)
        #     weapon_type = ItemUtilities.get_weapon_type(gameworld, created_weapon)
        #
        #     if weapon_type == 'staff':
        #         BuildLibrary.set_build_main_hand(gameworld=gameworld, entity=build_entity, label='C')
        #         BuildLibrary.set_build_off_hand(gameworld=gameworld, entity=build_entity, label='C')
        #
        #     if weapon_type == 'sword':
        #         BuildLibrary.set_build_main_hand(gameworld=gameworld, entity=build_entity, label='A')
        #         BuildLibrary.set_build_off_hand(gameworld=gameworld, entity=build_entity, label='A')
        #
        #     # parameters are: gameworld, weapon object, weapon type as a string, mobile class
        #     logger.info('Loading the {} with the necessary spells', weapon_type)
        #     WeaponClass.load_weapon_with_spells(gameworld, created_weapon, weapon_type, class_component)
        #
        #     # equip player with newly created starting weapon
        #     MobileUtilities.equip_weapon(gameworld=gameworld, entity=player, weapon=created_weapon, hand='both')
        #
        # if main_hand != '' and main_hand != off_hand:
        #     logger.info('creating a 1-handed weapon (main hand) for the player')
        #     created_weapon = ItemManager.create_weapon(gameworld=gameworld, weapon_type=main_hand,
        #                                                game_config=game_config)
        #     weapon_type = ItemUtilities.get_weapon_type(gameworld, created_weapon)
        #
        #     if weapon_type == 'wand':
        #         BuildLibrary.set_build_main_hand(gameworld=gameworld, entity=build_entity, label='B')
        #
        #     if weapon_type == 'dagger':
        #         BuildLibrary.set_build_main_hand(gameworld=gameworld, entity=build_entity, label='F')
        #
        #     if weapon_type == 'scepter':
        #         BuildLibrary.set_build_main_hand(gameworld=gameworld, entity=build_entity, label='G')
        #
        #     # parameters are: gameworld, weapon object, weapon type as a string, mobile class
        #     logger.info('Loading that weapon with the necessary spells')
        #     WeaponClass.load_weapon_with_spells(gameworld, created_weapon, weapon_type, class_component)
        #
        #     # equip player with newly created starting weapon
        #     MobileUtilities.equip_weapon(gameworld=gameworld, entity=player, weapon=created_weapon, hand='main')
        #
        # if off_hand != '' and off_hand != main_hand:
        #
        #     created_weapon = ItemManager.create_weapon(gameworld=gameworld, weapon_type=off_hand,
        #                                                game_config=game_config)
        #     weapon_type = ItemUtilities.get_weapon_type(gameworld, created_weapon)
        #
        #     if weapon_type == 'rod':
        #         BuildLibrary.set_build_off_hand(gameworld=gameworld, entity=build_entity, label='D')
        #
        #     if weapon_type == 'focus':
        #         BuildLibrary.set_build_off_hand(gameworld=gameworld, entity=build_entity, label='E')
        #
        #     # parameters are: gameworld, weapon object, weapon type as a string, mobile class
        #     logger.info('Loading that weapon with the necessary spells')
        #     WeaponClass.load_weapon_with_spells(gameworld, created_weapon, weapon_type, class_component)
        #
        #     # equip player with newly created starting weapon
        #     MobileUtilities.equip_weapon(gameworld=gameworld, entity=player, weapon=created_weapon, hand='off')
        #
        #
        # # load spell bar with spells from weapon
        # spell_bar_entity = MobileUtilities.create_spell_bar_as_entity(gameworld=gameworld)
        # MobileUtilities.set_spellbar_for_entity(gameworld=gameworld, entity=player, spellbar_entity=spell_bar_entity)
        # logger.info('Loading spell bar based on equipped weapons')
        # SpellUtilities.populate_spell_bar_initially(gameworld=gameworld, player_entity=player)
        #
        # # create jewellery pieces and equip them
        # jewellery_package = BuildLibrary.get_build_jewellery(gameworld=gameworld, entity=build_entity)
        #
        # # class
        # player_class = MobileUtilities.get_character_class(gameworld=gameworld, entity=player)
        # class_file = read_json_file(player_class_file)
        # jewellery_set = ''
        # if jewellery_package == 'A':
        #     jewellery_set = 'defensive'
        # if jewellery_package == 'B':
        #     jewellery_set = 'balanced'
        # if jewellery_package == 'C':
        #     jewellery_set = 'offensive'
        #
        # for p_class in class_file['classes']:
        #     if p_class['name'] == player_class:
        #         neck_gemstone = p_class[jewellery_set]['neck']
        #         ring1_gemstone = p_class[jewellery_set]['ring1']
        #         ring2_gemstone = p_class[jewellery_set]['ring2']
        #         ear1_gemstone = p_class[jewellery_set]['earring1']
        #         ear2_gemstone = p_class[jewellery_set]['earring2']
        #
        # # create jewellery entity
        # pendant = ItemManager.create_jewellery(gameworld=gameworld, bodylocation='neck', e_setting='copper',
        #                                        e_hook='copper', e_activator=neck_gemstone)
        # left_ring = ItemManager.create_jewellery(gameworld=gameworld, bodylocation='ring', e_setting='copper',
        #                                          e_hook='copper', e_activator=ring1_gemstone)
        # right_ring = ItemManager.create_jewellery(gameworld=gameworld, bodylocation='ring', e_setting='copper',
        #                                           e_hook='copper', e_activator=ring2_gemstone)
        # left_ear = ItemManager.create_jewellery(gameworld=gameworld, bodylocation='ear', e_setting='copper',
        #                                         e_hook='copper', e_activator=ear1_gemstone)
        # right_ear = ItemManager.create_jewellery(gameworld=gameworld, bodylocation='ear', e_setting='copper',
        #                                          e_hook='copper', e_activator=ear2_gemstone)
        #
        # # equip jewellery entity to player character
        # ItemUtilities.equip_jewellery(gameworld=gameworld, mobile=player, bodylocation='neck', trinket=pendant)
        # ItemUtilities.equip_jewellery(gameworld=gameworld, mobile=player, bodylocation='left hand', trinket=left_ring)
        # ItemUtilities.equip_jewellery(gameworld=gameworld, mobile=player, bodylocation='right hand', trinket=right_ring)
        # ItemUtilities.equip_jewellery(gameworld=gameworld, mobile=player, bodylocation='left ear', trinket=left_ear)
        # ItemUtilities.equip_jewellery(gameworld=gameworld, mobile=player, bodylocation='right ear', trinket=right_ear)
        #
        # # apply gemstone benefits
        # jewelley_stat_bonus = ItemUtilities.get_jewellery_stat_bonus(gameworld=gameworld, entity=pendant)
        # ItemUtilities.add_jewellery_benefit(gameworld=gameworld, entity=player, statbonus=jewelley_stat_bonus)
        #
        # jewelley_stat_bonus = ItemUtilities.get_jewellery_stat_bonus(gameworld=gameworld, entity=left_ring)
        # ItemUtilities.add_jewellery_benefit(gameworld=gameworld, entity=player, statbonus=jewelley_stat_bonus)
        #
        # jewelley_stat_bonus = ItemUtilities.get_jewellery_stat_bonus(gameworld=gameworld, entity=right_ring)
        # ItemUtilities.add_jewellery_benefit(gameworld=gameworld, entity=player, statbonus=jewelley_stat_bonus)
        #
        # jewelley_stat_bonus = ItemUtilities.get_jewellery_stat_bonus(gameworld=gameworld, entity=left_ear)
        # ItemUtilities.add_jewellery_benefit(gameworld=gameworld, entity=player, statbonus=jewelley_stat_bonus)
        #
        # jewelley_stat_bonus = ItemUtilities.get_jewellery_stat_bonus(gameworld=gameworld, entity=right_ear)
        # ItemUtilities.add_jewellery_benefit(gameworld=gameworld, entity=player, statbonus=jewelley_stat_bonus)
        #
        # #
        # # calculate derived stats
        # #

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
            if event_to_be_processed != '':
                if event_to_be_processed == 'keypress':
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
                    if event_action == 'left':
                        if selected_menu_option == 0:
                            gender_choice -= 1
                            if gender_choice < 1:
                                gender_choice = 2
                    if event_action == 'right':
                        if selected_menu_option == 0:
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
                                if event_to_be_processed == 'textinput' and letter_count < max_letters:
                                    if (64 < ord(event_action) < 91) or (96 < ord(event_action) < 123):

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
                                    if event_action == 'delete':
                                        if letter_count > 0:
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

                                        CharacterCreation.display_starting_character(gameworld=gameworld)
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
                            CharacterCreation.display_starting_character(gameworld=gameworld)

    @staticmethod
    def display_starting_character(gameworld):
        logger.info('Displaying character starting stats')
        game_config = configUtilities.load_config()
        file_name = configUtilities.get_config_value_as_string(game_config, 'files', 'BUILDLIBRARYFILE')
        display_char_menu_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_MENU_X')
        display_char_menu_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_MENU_Y')
        display_char_personal_x = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                              'DISPLAY_CHAR_PERSONAL_X')
        display_char_personal_y = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                              'DISPLAY_CHAR_PERSONAL_Y')
        display_char_personal_w = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                              'DISPLAY_CHAR_PERSONAL_W')
        display_char_personal_h = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                              'DISPLAY_CHAR_PERSONAL_H')
        dcp_fg = configUtilities.get_config_value_as_string(game_config, 'newgame', 'DISPLAY_CHAR_PERSONAL_FG')
        display_char_attributes_x = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                                'DISPLAY_CHAR_ATTRIBUTES_FRAME_X')
        display_char_attributes_y = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                                'DISPLAY_CHAR_ATTRIBUTES_FRAME_Y')
        display_char_attributes_w = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                                'DISPLAY_CHAR_ATTRIBUTES_FRAME_W')
        display_char_attributes_h = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                                'DISPLAY_CHAR_ATTRIBUTES_FRAME_H')
        dca_fg = configUtilities.get_config_value_as_string(game_config, 'newgame', 'DISPLAY_CHAR_ATTRIBUTES_FG')
        dca_bg = configUtilities.get_config_value_as_string(game_config, 'newgame', 'DISPLAY_CHAR_ATTRIBUTES_BG')
        display_char_pri_attributes_x = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                                    'DISPLAY_CHAR_PRI_ATTRIBUTES_X')
        display_char_pri_attributes_y = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                                    'DISPLAY_CHAR_PRI_ATTRIBUTES_Y')
        display_char_pri_attributes_w = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                                    'DISPLAY_CHAR_PRI_ATTRIBUTES_W')
        display_char_pri_attributes_h = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                                    'DISPLAY_CHAR_PRI_ATTRIBUTES_H')
        display_char_pri_attr_x = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                              'DISPLAY_CHAR_PRI_ATTR_X')
        display_char_pri_attr_y = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                              'DISPLAY_CHAR_PRI_ATTR_Y')

        display_char_sec_attributes_x = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                                    'DISPLAY_CHAR_SEC_ATTRIBUTES_X')
        display_char_sec_attributes_y = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                                    'DISPLAY_CHAR_SEC_ATTRIBUTES_Y')
        display_char_sec_attributes_w = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                                    'DISPLAY_CHAR_SEC_ATTRIBUTES_W')
        display_char_sec_attributes_h = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                                    'DISPLAY_CHAR_SEC_ATTRIBUTES_H')
        display_char_sec_attr_x = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                              'DISPLAY_CHAR_SEC_ATTR_X')
        display_char_sec_attr_y = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                              'DISPLAY_CHAR_SEC_ATTR_Y')

        display_char_der_attributes_x = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                                    'DISPLAY_CHAR_DER_ATTRIBUTES_X')
        display_char_der_attributes_y = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                                    'DISPLAY_CHAR_DER_ATTRIBUTES_Y')
        display_char_der_attributes_w = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                                    'DISPLAY_CHAR_DER_ATTRIBUTES_W')
        display_char_der_attributes_h = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                                    'DISPLAY_CHAR_DER_ATTRIBUTES_H')
        display_char_der_attr_x = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                              'DISPLAY_CHAR_DER_ATTR_X')
        display_char_der_attr_y = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                              'DISPLAY_CHAR_DER_ATTR_Y')

        display_char_armset_attr_x = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                                 'DISPLAY_CHAR_ARMSET_ATTR_X')
        display_char_armset_attr_y = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                                 'DISPLAY_CHAR_ARMSET_ATTR_Y')
        display_char_armset_attr_w = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                                 'DISPLAY_CHAR_ARMSET_W')
        display_char_armset_attr_h = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                                 'DISPLAY_CHAR_ARMSET_H')

        display_char_armour_attr_x = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                                 'DISPLAY_CHAR_ARMOUR_ATTR_X')
        display_char_armour_attr_y = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                                 'DISPLAY_CHAR_ARMOUR_ATTR_Y')
        dap_fg = configUtilities.get_config_value_as_string(game_config, 'newgame', 'DISPLAY_ARMOUR_INFO_BG')

        display_wpn_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_WPN_X')
        display_wpn_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_WPN_Y')
        display_wpn_w = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_WPN_W')
        display_wpn_h = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_WPN_H')

        display_main_wpn_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_MAIN_WPN_X')
        display_main_wpn_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_MAIN_WPN_Y')

        display_off_wpn_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_OFF_WPN_X')
        display_off_wpn_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_OFF_WPN_Y')

        display_char_personal_fg = colourUtilities.get(dcp_fg)
        display_char_attributes_fg = colourUtilities.get(dca_fg)
        display_char_attributes_bg = colourUtilities.get(dca_bg)
        display_armour_info_bg = colourUtilities.get(dap_fg)

        player_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)

        draw_colourful_frame(title=' Character Creation - Finished ', title_decorator=False, title_loc='centre',
                             corner_decorator='', msg=2)

        menu_options = ['Accept', 'Save Build', 'New Character']
        max_menu_option = len(menu_options) - 1
        selected_menu_option = 0
        not_ready_to_proceed = True

        # get build entity
        build_entity = BuildLibrary.get_build_entity(gameworld=gameworld)

        # personal information
        # name
        player_names = MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=player_entity)
        first_name = player_names[0]
        last_name = player_names[1]

        BuildLibrary.set_build_name(gameworld=gameworld, entity=build_entity, label=first_name + ' ' + last_name)

        # gender
        player_gender = MobileUtilities.get_player_gender(gameworld=gameworld, entity=player_entity)

        if player_gender == 'male':
            BuildLibrary.set_build_gender(gameworld=gameworld, entity=build_entity, label='A')

        if player_gender == 'female':
            BuildLibrary.set_build_gender(gameworld=gameworld, entity=build_entity, label='B')
        #
        # race
        #
        racial_details = MobileUtilities.get_mobile_race_details(gameworld=gameworld, entity=player_entity)
        player_race = racial_details[0]
        # class
        #
        player_class = MobileUtilities.get_character_class(gameworld=gameworld, entity=player_entity)

        if player_class == 'necromancer':
            BuildLibrary.set_build_class(gameworld=gameworld, entity=build_entity, label='A')

        if player_class == 'witch doctor':
            BuildLibrary.set_build_class(gameworld=gameworld, entity=build_entity, label='B')

        if player_class == 'druid':
            BuildLibrary.set_build_class(gameworld=gameworld, entity=build_entity, label='C')

        if player_class == 'illusionist':
            BuildLibrary.set_build_class(gameworld=gameworld, entity=build_entity, label='D')

        if player_class == 'elementalist':
            BuildLibrary.set_build_class(gameworld=gameworld, entity=build_entity, label='E')

        if player_class == 'chronomancer':
            BuildLibrary.set_build_class(gameworld=gameworld, entity=build_entity, label='F')

        # personality
        player_personality = MobileUtilities.get_mobile_personality_title(gameworld=gameworld, entity=player_entity)

        personal_info = 'You are ' + first_name + ' a ' + player_gender + ' ' + player_class + ' from ' + player_race + '.'
        personality_info = ' Your personality would be described as ' + player_personality.lower() + '.'

        personal_details = personal_info + personality_info

        string_to_print = personal_details
        terminal.print_(x=display_char_personal_x, y=display_char_personal_y,
                        width=display_char_personal_w, height=display_char_personal_h, align=terminal.TK_ALIGN_LEFT,
                        s=string_to_print)
        # armour
        #
        # display_coloured_box(title='Armour', posx=display_char_armset_attr_x, posy=display_char_armset_attr_y,
        #                      width=display_char_armset_attr_w, height=display_char_armset_attr_h,
        #                      fg=display_char_personal_fg, bg=display_armour_info_bg)
        #
        # str_to_print = "[color=blue]Location Material Display Defense[/color]"
        # terminal.print_(x=display_char_armour_attr_x, y=display_char_armour_attr_y,
        #                 width=len(str_to_print), height=1, align=terminal.TK_ALIGN_LEFT, s=str_to_print)
        #
        # head_armour_id = MobileUtilities.is_entity_wearing_head_armour(gameworld=gameworld, entity=player_entity)
        # armour_material = ItemUtilities.get_item_material(gameworld=gameworld, entity=head_armour_id)
        # armour_displayname = ItemUtilities.get_item_displayname(gameworld=gameworld, entity=head_armour_id)
        # def_head_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, entity=head_armour_id)
        # str_to_print = "Head:    " + armour_material + '  ' + armour_displayname + '         ' + str(def_head_value)
        #
        # terminal.print_(x=display_char_armour_attr_x, y=display_char_armour_attr_y + 1,
        #                 width=len(str_to_print), height=1, align=terminal.TK_ALIGN_LEFT, s=str_to_print)
        #
        # chest_armour_id = MobileUtilities.is_entity_wearing_chest_armour(gameworld=gameworld, entity=player_entity)
        # armour_material = ItemUtilities.get_item_material(gameworld=gameworld, entity=chest_armour_id)
        # armour_displayname = ItemUtilities.get_item_displayname(gameworld=gameworld, entity=chest_armour_id)
        # def_chest_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, entity=chest_armour_id)
        # str_to_print = "Chest:   " + armour_material + '  ' + armour_displayname + '        ' + str(def_chest_value)
        #
        # terminal.print_(x=display_char_armour_attr_x, y=display_char_armour_attr_y + 2,
        #                 width=len(str_to_print), height=1, align=terminal.TK_ALIGN_LEFT, s=str_to_print)
        #
        # hands_armour_id = MobileUtilities.is_entity_wearing_hands_armour(gameworld=gameworld, entity=player_entity)
        # armour_material = ItemUtilities.get_item_material(gameworld=gameworld, entity=hands_armour_id)
        # armour_displayname = ItemUtilities.get_item_displayname(gameworld=gameworld, entity=hands_armour_id)
        # def_hands_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, entity=hands_armour_id)
        # str_to_print = "Hands:   " + armour_material + '  ' + armour_displayname + ' ' + str(def_hands_value)
        #
        # terminal.print_(x=display_char_armour_attr_x, y=display_char_armour_attr_y + 3,
        #                 width=len(str_to_print), height=1, align=terminal.TK_ALIGN_LEFT, s=str_to_print)
        #
        # legs_armour_id = MobileUtilities.is_entity_wearing_legs_armour(gameworld=gameworld, entity=player_entity)
        # armour_material = ItemUtilities.get_item_material(gameworld=gameworld, entity=legs_armour_id)
        # armour_displayname = ItemUtilities.get_item_displayname(gameworld=gameworld, entity=legs_armour_id)
        # def_legs_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, entity=legs_armour_id)
        # str_to_print = "Legs:    " + armour_material + '  ' + armour_displayname + '    ' + str(def_legs_value)
        #
        # terminal.print_(x=display_char_armour_attr_x, y=display_char_armour_attr_y + 4,
        #                 width=len(str_to_print), height=1, align=terminal.TK_ALIGN_LEFT, s=str_to_print)
        #
        # feet_armour_id = MobileUtilities.is_entity_wearing_feet_armour(gameworld=gameworld, entity=player_entity)
        # armour_material = ItemUtilities.get_item_material(gameworld=gameworld, entity=feet_armour_id)
        # armour_displayname = ItemUtilities.get_item_displayname(gameworld=gameworld, entity=feet_armour_id)
        # def_feet_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, entity=feet_armour_id)
        # str_to_print = "Feet:    " + armour_material + '  ' + armour_displayname + '     ' + str(def_feet_value)
        #
        # terminal.print_(x=display_char_armour_attr_x, y=display_char_armour_attr_y + 5,
        #                 width=len(str_to_print), height=1, align=terminal.TK_ALIGN_LEFT, s=str_to_print)

        #
        # attributes

        display_coloured_box(title="Attributes",
                             posx=display_char_attributes_x, posy=display_char_attributes_y,
                             width=display_char_attributes_w, height=display_char_attributes_h,
                             fg=display_char_attributes_fg, bg=display_char_attributes_bg)

        player_power = MobileUtilities.get_mobile_primary_power(gameworld=gameworld, entity=player_entity)
        player_precision = MobileUtilities.get_mobile_primary_precision(gameworld=gameworld, entity=player_entity)
        player_toughness = MobileUtilities.get_mobile_primary_toughness(gameworld=gameworld, entity=player_entity)
        player_vitality = MobileUtilities.get_mobile_primary_vitality(gameworld=gameworld, entity=player_entity)
        player_concentration = MobileUtilities.get_mobile_secondary_concentration(gameworld=gameworld, entity=player_entity)
        player_condi_damage = MobileUtilities.get_mobile_secondary_condition_damage(gameworld=gameworld, entity=player_entity)
        player_expertise = MobileUtilities.get_mobile_secondary_expertise(gameworld=gameworld, entity=player_entity)
        player_ferocity = MobileUtilities.get_mobile_secondary_ferocity(gameworld=gameworld, entity=player_entity)
        player_healing_power = MobileUtilities.get_mobile_secondary_healing_power(gameworld=gameworld, entity=player_entity)
        player_armour = MobileUtilities.get_mobile_derived_armour_value(gameworld=gameworld, entity=player_entity)
        player_boon_duration = MobileUtilities.get_mobile_derived_boon_duration(gameworld=gameworld, entity=player_entity)

        player_critical_chance = MobileUtilities.get_mobile_derived_critical_hit_chance(gameworld=gameworld,
                                                                                        entity=player_entity)
        player_critical_damage = MobileUtilities.get_mobile_derived_critical_damage(gameworld=gameworld, entity=player_entity)
        player_condi_duration = MobileUtilities.get_mobile_derived_condition_duration(gameworld=gameworld,
                                                                                      entity=player_entity)
        player_max_health = MobileUtilities.get_mobile_derived_maximum_health(gameworld=gameworld, entity=player_entity)
        player_cur_health = MobileUtilities.get_mobile_derived_current_health(gameworld=gameworld, entity=player_entity)
        player_maximum_mana = MobileUtilities.get_mobile_derived_maximum_mana(gameworld=gameworld, entity=player_entity)
        #
        # # primary / secondary / derived / bonuses highlighted
        display_coloured_box(title="Primary",
                             posx=display_char_pri_attributes_x, posy=display_char_pri_attributes_y,
                             width=display_char_pri_attributes_w, height=display_char_pri_attributes_h,
                             fg=display_char_attributes_fg, bg=display_char_attributes_bg)

        string_to_print = "Power:" + str(player_power)
        terminal.print_(x=display_char_pri_attr_x, y=display_char_pri_attr_y, width=len("Power:" + str(player_power)),
                        height=1, align=terminal.TK_ALIGN_LEFT, s=string_to_print)

        string_to_print = "Precision:" + str(player_precision)
        terminal.print_(x=display_char_pri_attr_x, y=display_char_pri_attr_y + 1,
                        width=len("Precision:" + str(player_precision)), height=1, align=terminal.TK_ALIGN_LEFT,
                        s=string_to_print)
        string_to_print = "Toughness:" + str(player_toughness)
        terminal.print_(x=display_char_pri_attr_x, y=display_char_pri_attr_y + 2,
                        width=len("Toughness:" + str(player_toughness)), height=1, align=terminal.TK_ALIGN_LEFT,
                        s=string_to_print)
        string_to_print = "Vitality:" + str(player_vitality)
        terminal.print_(x=display_char_pri_attr_x, y=display_char_pri_attr_y + 3,
                        width=len("Vitality:" + str(player_vitality)), height=1, align=terminal.TK_ALIGN_LEFT,
                        s=string_to_print)

        display_coloured_box(title="Secondary",
                             posx=display_char_sec_attributes_x, posy=display_char_sec_attributes_y,
                             width=display_char_sec_attributes_w, height=display_char_sec_attributes_h,
                             fg=display_char_attributes_fg, bg=display_char_attributes_bg)

        string_to_print = "Concentration:" + str(player_concentration)
        terminal.print_(x=display_char_sec_attr_x, y=display_char_sec_attr_y,
                        width=len("Concentration:" + str(player_concentration)), height=1, align=terminal.TK_ALIGN_LEFT,
                        s=string_to_print)

        string_to_print = "Condition Damage:" + str(player_condi_damage)
        terminal.print_(x=display_char_sec_attr_x, y=display_char_sec_attr_y + 1,
                        width=len("Condition Damage:" + str(player_condi_damage)), height=1,
                        align=terminal.TK_ALIGN_LEFT,
                        s=string_to_print)

        string_to_print = "Expertise:" + str(player_expertise)
        terminal.print_(x=display_char_sec_attr_x, y=display_char_sec_attr_y + 2,
                        width=len("Expertise:" + str(player_expertise)), height=1, align=terminal.TK_ALIGN_LEFT,
                        s=string_to_print)

        string_to_print = "Ferocity:" + str(player_ferocity)
        terminal.print_(x=display_char_sec_attr_x, y=display_char_sec_attr_y + 3,
                        width=len("Ferocity:" + str(player_ferocity)), height=1, align=terminal.TK_ALIGN_LEFT,
                        s=string_to_print)

        string_to_print = "Healing Power:" + str(player_healing_power)
        terminal.print_(x=display_char_sec_attr_x, y=display_char_sec_attr_y + 4,
                        width=len("Healing Power:" + str(player_healing_power)), height=1, align=terminal.TK_ALIGN_LEFT,
                        s=string_to_print)

        display_coloured_box(title="Derived",
                             posx=display_char_der_attributes_x, posy=display_char_der_attributes_y,
                             width=display_char_der_attributes_w, height=display_char_der_attributes_h,
                             fg=display_char_attributes_fg, bg=display_char_attributes_bg)

        string_to_print = "Armour:" + str(player_armour)
        terminal.print_(x=display_char_der_attr_x, y=display_char_der_attr_y, width=len("Armour:" + str(player_armour)),
                        height=1, align=terminal.TK_ALIGN_LEFT,
                        s=string_to_print)

        string_to_print = "Boon Duration:" + str(player_boon_duration)
        terminal.print_(x=display_char_der_attr_x, y=display_char_der_attr_y + 1,
                        width=len("Boon Duration:" + str(player_boon_duration)), height=1, align=terminal.TK_ALIGN_LEFT,
                        s=string_to_print)

        string_to_print = "Critical Chance:" + str(player_critical_chance) + '%'
        terminal.print_(x=display_char_der_attr_x, y=display_char_der_attr_y + 2,
                        width=len("Critical Chance:" + str(player_critical_chance) + '%'), height=1,
                        align=terminal.TK_ALIGN_LEFT,
                        s=string_to_print)

        string_to_print = "Critical Damage:" + str(player_critical_damage) + '%'
        terminal.print_(x=display_char_der_attr_x, y=display_char_der_attr_y + 3,
                        width=len("Critical Damage:" + str(player_critical_damage) + '%'), height=1,
                        align=terminal.TK_ALIGN_LEFT,
                        s=string_to_print)

        string_to_print = "Condition Duration:" + str(player_condi_duration)
        terminal.print_(x=display_char_der_attr_x, y=display_char_der_attr_y + 4,
                        width=len("Condition Duration:" + str(player_condi_duration)), height=1,
                        align=terminal.TK_ALIGN_LEFT,
                        s=string_to_print)
        # health
        string_to_print = "Health:" + str(player_cur_health)
        terminal.print_(x=display_char_der_attr_x, y=display_char_der_attr_y + 6,
                        width=len("Health:" + str(player_cur_health)), height=1, align=terminal.TK_ALIGN_LEFT,
                        s=string_to_print)

        string_to_print = " / " + str(player_max_health)
        terminal.print_(x=display_char_der_attr_x + 10, y=display_char_der_attr_y + 6,
                        width=len(" / " + str(player_max_health)), height=1, align=terminal.TK_ALIGN_LEFT,
                        s=string_to_print)

        # mana
        string_to_print = "Mana:" + str(player_maximum_mana)
        terminal.print_(x=display_char_der_attr_x, y=display_char_der_attr_y + 7,
                        width=len("Mana:" + str(player_maximum_mana)), height=1, align=terminal.TK_ALIGN_LEFT,
                        s=string_to_print)

        # weapons
        #
        # display_coloured_box(title="Weapons / Spells",
        #                      posx=display_wpn_x, posy=display_wpn_y,
        #                      width=display_wpn_w, height=display_wpn_h,
        #                      fg=display_char_attributes_fg, bg=display_char_attributes_bg)
        #
        # weapons_list = MobileUtilities.get_weapons_equipped(gameworld=gameworld, entity=player_entity)
        # main_weapon = weapons_list[0]
        # off_weapon = weapons_list[1]
        # both_weapon = weapons_list[2]
        #
        # if both_weapon > 0:
        #     main_hand_weapon_name = ItemUtilities.get_item_name(gameworld=gameworld, entity=both_weapon)
        #     slot1_name = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=gameworld, weapon_equipped=both_weapon,
        #                                                               slotid=1)
        #     slot2_name = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=gameworld, weapon_equipped=both_weapon,
        #                                                               slotid=2)
        #     slot3_name = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=gameworld, weapon_equipped=both_weapon,
        #                                                               slotid=3)
        #
        #     off_hand_weapon_name = main_hand_weapon_name
        #     slot4_name = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=gameworld, weapon_equipped=both_weapon,
        #                                                               slotid=4)
        #     slot5_name = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=gameworld, weapon_equipped=both_weapon,
        #                                                               slotid=5)
        #
        # else:
        #     main_hand_weapon_name = ItemUtilities.get_item_name(gameworld=gameworld, entity=main_weapon)
        #     slot1_name = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=gameworld, weapon_equipped=main_weapon,
        #                                                               slotid=1)
        #     slot2_name = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=gameworld, weapon_equipped=main_weapon,
        #                                                               slotid=2)
        #     slot3_name = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=gameworld, weapon_equipped=main_weapon,
        #                                                               slotid=3)
        #
        #     off_hand_weapon_name = ItemUtilities.get_item_name(gameworld=gameworld, entity=off_weapon)
        #     slot4_name = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=gameworld, weapon_equipped=off_weapon,
        #                                                               slotid=4)
        #     slot5_name = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=gameworld, weapon_equipped=off_weapon,
        #                                                               slotid=5)
        #
        # main_wpn_display = '[color=blue]Main Hand: ' + main_hand_weapon_name + '[\color]'
        # slot1_display = 'Slot 1:' + slot1_name
        # slot2_display = 'Slot 2:' + slot2_name
        # slot3_display = 'Slot 3:' + slot3_name
        # slot4_display = 'Slot 4:' + slot4_name
        # slot5_display = 'Slot 5:' + slot5_name
        #
        # off_wpn_display = '[color=green]Off Hand: ' + off_hand_weapon_name
        #
        # # main hand
        #
        # terminal.print_(x=display_main_wpn_x, y=display_main_wpn_y, width=len(main_wpn_display), height=1,
        #                 align=terminal.TK_ALIGN_LEFT,
        #                 s=main_wpn_display)
        # terminal.print_(x=display_main_wpn_x, y=display_main_wpn_y + 1, width=len(slot1_display), height=1,
        #                 align=terminal.TK_ALIGN_LEFT,
        #                 s=slot1_display)
        # terminal.print_(x=display_main_wpn_x, y=display_main_wpn_y + 2, width=len(slot2_display), height=1,
        #                 align=terminal.TK_ALIGN_LEFT,
        #                 s=slot2_display)
        # terminal.print_(x=display_main_wpn_x, y=display_main_wpn_y + 3, width=len(slot3_display), height=1,
        #                 align=terminal.TK_ALIGN_LEFT,
        #                 s=slot3_display)
        #
        # # off hand
        # terminal.print_(x=display_off_wpn_x, y=display_off_wpn_y, width=len(off_wpn_display), height=1,
        #                 align=terminal.TK_ALIGN_LEFT,
        #                 s=off_wpn_display)
        # terminal.print_(x=display_off_wpn_x, y=display_off_wpn_y + 1, width=len(slot4_display), height=1,
        #                 align=terminal.TK_ALIGN_LEFT,
        #                 s=slot4_display)
        # terminal.print_(x=display_off_wpn_x, y=display_off_wpn_y + 2, width=len(slot5_display), height=1,
        #                 align=terminal.TK_ALIGN_LEFT,
        #                 s=slot5_display)

        saved_build = False

        while not_ready_to_proceed:
            # menu options
            pointy_menu(header='',
                        menu_options=menu_options, menu_id_format=True, menu_start_x=display_char_menu_x,
                        menu_start_y=display_char_menu_y, blank_line=True, selected_option=selected_menu_option)

            # blit changes to root console
            terminal.refresh()

            event_to_be_processed, event_action = handle_game_keys()
            if event_to_be_processed != '' and event_to_be_processed == 'keypress':
                if event_action == 'quit':
                    not_ready_to_proceed = False
                    terminal.clear()
                if event_action == 'up':
                    selected_menu_option -= 1
                    if selected_menu_option < 0:
                        selected_menu_option = max_menu_option
                if event_action == 'down':
                    selected_menu_option += 1
                    if selected_menu_option > max_menu_option:
                        selected_menu_option = 0
                if event_action == 'enter':
                    if selected_menu_option == 0:  # accept character build and start game
                        messagelog_entity = MobileUtilities.get_next_entity_id(gameworld=gameworld)
                        CommonUtils.create_message_log_as_entity(gameworld=gameworld, log_entity=messagelog_entity)
                        MobileUtilities.set_MessageLog_for_player(gameworld=gameworld, entity=player_entity,
                                                                  logid=messagelog_entity)
                        logger.info('Mesage log stored as entity {}', messagelog_entity)
                        game_loop(gameworld=gameworld)
                    if selected_menu_option == 1:  # save current build
                        if not saved_build:
                            build_info = BuildLibrary.save_build_to_library(gameworld=gameworld)
                            Externalfiles.write_to_existing_file(filename=file_name, value=build_info)
                            saved_build = True
                    if selected_menu_option == 2:  # reject build and start again
                        not_ready_to_proceed = False
                        MobileUtilities.unequip_all_weapons(gameworld=gameworld, entity=player_entity)
                        # remove jewellery
                        # delete player entity
                        world.delete_entity(gameworld=gameworld, entity=player_entity)
                        terminal.clear()
                        CharacterCreation.OLDcreate_new_character(gameworld=gameworld)
