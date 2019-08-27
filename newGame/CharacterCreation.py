import tcod
import tcod.console

from loguru import logger
from utilities import configUtilities, colourUtilities
from utilities.display import draw_colourful_frame, pointy_menu, coloured_list, draw_clear_text_box, display_coloured_box
from utilities.input_handlers import handle_game_keys
from utilities.world import create_game_world
from utilities.jsonUtilities import read_json_file
from utilities.mobileHelp import MobileUtilities
from utilities.spellHelp import SpellUtilities
from newGame.newCharacter import NewCharacter
from newGame.initialiseNewGame import setup_game, create_spell_entities
from newGame.Items import ItemManager
from newGame.ClassWeapons import WeaponClass
from utilities.itemsHelp import ItemUtilities

from engine import start_game


class CharacterCreation:

    @staticmethod
    def display_character_creation_options(root_console, game_config):
        logger.info('Character creation options')

        start_panel_width = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_WIDTH')
        start_panel_height = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_HEIGHT')
        start_panel_frame_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_X')
        start_panel_frame_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_Y')
        start_panel_frame_width = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_WIDTH')
        start_panel_frame_height = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_HEIGHT')
        menu_start_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'MENU_START_X')
        menu_start_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'MENU_START_Y')

        character_console = tcod.console.Console(width=start_panel_width, height=start_panel_height, order='F')

        draw_colourful_frame(console=character_console, game_config=game_config,
                             startx=start_panel_frame_x, starty=start_panel_frame_y,
                             width=start_panel_frame_width,
                             height=start_panel_frame_height,
                             title='[ Character Creation Options ]', title_loc='centre',
                             title_decorator=False,
                             corner_decorator='', corner_studs='square',
                             msg='ESC/ to go back, up & down arrows to select, enter to accept choice')

        show_character_options = True
        selected_menu_option = 0

        while show_character_options:
            # place game menu options
            pointy_menu(console=character_console, header='',
                        menu_options=['Create New Character', 'Random Character', 'Choose build from your library',
                                      'Replay most recent character'], menu_id_format=True, menu_start_x=menu_start_x,
                        menu_start_y=menu_start_y,  blank_line=True, selected_option=selected_menu_option)

            # blit changes to root console
            character_console.blit(dest=root_console, dest_x=5, dest_y=5)
            tcod.console_flush()

            event_to_be_processed, event_action = handle_game_keys()
            if event_to_be_processed != '':
                if event_to_be_processed == 'keypress':
                    if event_action == 'quit':
                        show_character_options = False

                    if event_action == 'up':
                        selected_menu_option -= 1
                        if selected_menu_option < 0:
                            selected_menu_option = 3
                    if event_action == 'down':
                        selected_menu_option += 1
                        if selected_menu_option > 3:
                            selected_menu_option = 0
                    if event_action == 'enter':
                        if selected_menu_option == 0:     # create new character
                            gameworld = CharacterCreation.create_world(gameconfig=game_config)
                            CharacterCreation.create_new_character(gameworld=gameworld, gameconfig=game_config, root_console=root_console)
                            character_console.blit(dest=root_console, dest_x=5, dest_y=5)
                            tcod.console_flush()
                        if selected_menu_option == 1:     # create random character
                            pass
                        if selected_menu_option == 2:     # use existing build
                            pass
                        if selected_menu_option == 3:     # replay most recent character
                            pass

    @staticmethod
    def create_world(gameconfig):
        # Esper initialisation
        gameworld = create_game_world()
        setup_game(game_config=gameconfig)

        return gameworld

    @staticmethod
    def create_new_character(gameworld, gameconfig, root_console):
        player_entity = NewCharacter.generate_player_character(gameworld=gameworld, game_config=gameconfig)
        CharacterCreation.choose_race(root_console=root_console, gameworld=gameworld, player=player_entity, game_config=gameconfig)

    @staticmethod
    def choose_race(root_console, gameworld, player, game_config):
        player_race_file = configUtilities.get_config_value_as_string(configfile=game_config, section='default', parameter='RACESFILE')
        start_panel_width = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_WIDTH')
        start_panel_height = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_HEIGHT')
        start_panel_frame_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_X')
        start_panel_frame_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_Y')
        start_panel_frame_width = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_WIDTH')
        start_panel_frame_height = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_HEIGHT')
        menu_start_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'MENU_START_X')
        menu_start_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'MENU_START_Y')
        primary_attributes = configUtilities.get_config_value_as_list(game_config, 'newgame', 'PRIMARY_ATTRIBUTES')
        race_flavour_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'RACE_CONSOLE_FLAVOR_X')
        race_flavour_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'RACE_CONSOLE_FLAVOR_Y')
        race_benefits_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'RACE_CONSOLE_BENEFITS_X')
        race_benefits_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'RACE_CONSOLE_BENEFITS_Y')

        race_console = tcod.console.Console(width=start_panel_width, height=start_panel_height, order='F')

        draw_colourful_frame(console=race_console, game_config=game_config,
                             startx=start_panel_frame_x, starty=start_panel_frame_y,
                             width=start_panel_frame_width,
                             height=start_panel_frame_height,
                             title='[ Character Creation - Select Race ]', title_loc='centre',
                             title_decorator=False,
                             corner_decorator='', corner_studs='square',
                             msg='ESC/ to go back, up & down arrows to select, enter to accept choice')

        logger.info('Select Race options')
        race_file = read_json_file(player_race_file)

        race_name = []
        race_flavour = []
        race_prefix = []
        race_bg_colour = []
        race_size = []
        race_attributes = []

        for option in race_file['races']:
            race_name.append(option['name'])
            race_flavour.append(option['flavour'])
            race_prefix.append(option['prefix'])
            race_bg_colour.append(option['bg_colour'])
            race_size.append(option['size'])
            race_attributes.append(option['attributes'])

        show_race_options = True
        selected_menu_option = 0
        max_menu_option = len(race_name) - 1

        while show_race_options:
            pointy_menu(console=race_console, header='',
                        menu_options=race_name, menu_id_format=True, menu_start_x=menu_start_x, menu_start_y=menu_start_y,
                        blank_line=True, selected_option=selected_menu_option)

            # racial flavour text
            draw_clear_text_box(console=race_console,
                                posx=race_flavour_x, posy=race_flavour_y,
                                width=30, height=10,
                                text=race_flavour[selected_menu_option],
                                fg=colourUtilities.WHITE, bg=colourUtilities.BLACK)

            # racial benefits
            race_console.print(x=race_benefits_x, y=race_benefits_y, string='Benefit', fg=colourUtilities.GREEN)
            race_benefit = race_attributes[selected_menu_option]
            benefit_value = race_benefit['benefitValue']
            benefit_name = race_benefit['benefitName']

            coloured_list(console=race_console, list_options=primary_attributes,
                          list_x=race_benefits_x + 3, list_y=race_benefits_y + 2,
                          selected_option=benefit_name, blank_line=False, fg=colourUtilities.WHITE)

            posy = 0
            for benefit in primary_attributes:
                if benefit_name.lower() == benefit.lower():

                    race_console.print(x=race_benefits_x, y=(race_benefits_y + 2) + posy, string='+' + benefit_value,
                                       fg=colourUtilities.YELLOW1, bg=colourUtilities.BLACK)
                else:
                    race_console.print(x=race_benefits_x, y=(race_benefits_y + 2) + posy, string='   ',
                                       fg=colourUtilities.BLACK, bg=colourUtilities.BLACK)
                posy += 1

            # blit changes to root console
            race_console.blit(dest=root_console, dest_x=5, dest_y=5)
            tcod.console_flush()

            event_to_be_processed, event_action = handle_game_keys()
            if event_to_be_processed != '':
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
                            gameworld=gameworld,player=player, selected_race=race_name[selected_menu_option],
                            race_size=race_size[selected_menu_option], bg=race_bg_colour[selected_menu_option])
                        logger.info('Race selected:' + race_name[selected_menu_option])
                        CharacterCreation.choose_class(root_console, gameworld, player, game_config)

    @staticmethod
    def choose_class(root_console, gameworld, player, game_config):

        player_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='default',
                                                                       parameter='CLASSESFILE')
        start_panel_width = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_WIDTH')
        start_panel_height = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_HEIGHT')
        start_panel_frame_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_X')
        start_panel_frame_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_Y')
        start_panel_frame_width = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_WIDTH')
        start_panel_frame_height = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_HEIGHT')
        class_flavour_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'CLASS_CONSOLE_FLAVOR_X')
        class_flavour_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'CLASS_CONSOLE_FLAVOR_Y')
        class_menu_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'CLASS_MENU_X')
        class_menu_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'CLASS_MENU_Y')
        class_package_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'CLASS_PACKAGE_X')
        class_package_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'CLASS_PACKAGE_Y')
        class_packages = configUtilities.get_config_value_as_list(game_config, 'newgame', 'CLASS_PACKAGES')
        jewellery_locations = configUtilities.get_config_value_as_list(game_config, 'newgame', 'JEWELLERY_LOCATIONS')

        class_console = tcod.console.Console(width=start_panel_width, height=start_panel_height, order='F')

        draw_colourful_frame(console=class_console, game_config=game_config,
                             startx=start_panel_frame_x, starty=start_panel_frame_y,
                             width=start_panel_frame_width,
                             height=start_panel_frame_height,
                             title='[ Character Creation - Select Class ]', title_loc='centre',
                             title_decorator=False,
                             corner_decorator='', corner_studs='square',
                             msg='ESC/ to go back, up & down arrows to select, enter to accept choice')

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

        defensive_class = [['' for x in range(5)] for x in range(len(menu_options))]
        balanced_class = [['' for x in range(5)] for x in range(len(menu_options))]
        offensive_class = [['' for x in range(5)] for x in range(len(menu_options))]

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

        while class_not_selected:
            pointy_menu(console=class_console, header='',
                        menu_options=menu_options, menu_id_format=True, menu_start_x=class_menu_x, menu_start_y=class_menu_y,
                        blank_line=True, selected_option=selected_menu_option)

            # draw class flavour text
            draw_clear_text_box(console=class_console,
                                posx=class_flavour_x, posy=class_flavour_y,
                                width=30, height=10,
                                text=menu_options_flavour[selected_menu_option],
                                fg=colourUtilities.WHITE, bg=colourUtilities.BLACK)

            # draw jewellery title
            class_console.print(x=class_package_x + 15, y=class_package_y - 2, string='Jewellery Bonus', fg=colourUtilities.YELLOW1)

            coloured_list(console=class_console,
                          list_options=jewellery_locations,
                          list_x=class_package_x, list_y=class_package_y + 2,
                          selected_option='nothing',
                          blank_line=False, fg=colourUtilities.WHITE)

            # draw class packages incl jewellery benefits
            pkg_pointer = '>'
            pkg_empty = ' '
            p1 = 9
            p2 = 24
            p3 = 39
            if package_selected == 1:
                class_console.print(x=class_package_x + p1, y=class_package_y, string=pkg_pointer + class_packages[0], fg=colourUtilities.YELLOW1)
                class_console.print(x=class_package_x + p2, y=class_package_y, string=pkg_empty + class_packages[1], fg=colourUtilities.WHITE)
                class_console.print(x=class_package_x + p3, y=class_package_y, string=pkg_empty + class_packages[2], fg=colourUtilities.WHITE)
            if package_selected == 2:
                class_console.print(x=class_package_x + p1, y=class_package_y, string=pkg_empty + class_packages[0], fg=colourUtilities.WHITE)
                class_console.print(x=class_package_x + p2, y=class_package_y, string=pkg_pointer + class_packages[1], fg=colourUtilities.YELLOW1)
                class_console.print(x=class_package_x + p3, y=class_package_y, string=pkg_empty + class_packages[2], fg=colourUtilities.WHITE)
            if package_selected == 3:
                class_console.print(x=class_package_x + p1, y=class_package_y, string=pkg_empty + class_packages[0], fg=colourUtilities.WHITE)
                class_console.print(x=class_package_x + p2, y=class_package_y, string=pkg_empty + class_packages[1], fg=colourUtilities.WHITE)
                class_console.print(x=class_package_x + p3, y=class_package_y, string=pkg_pointer + class_packages[2], fg=colourUtilities.YELLOW1)

            counter = class_package_y + 2
            for loc in range(5):
                class_console.draw_rect(x=class_package_x + 10, y=counter, width=20, height=5, ch=32, fg=colourUtilities.BLACK)
                class_console.print(x=class_package_x + 10, y=counter, string=defensive_class[selected_menu_option][loc], fg=colourUtilities.WHITE)
                class_console.draw_rect(x=class_package_x + 25, y=counter, width=20, height=5, ch=32, fg=colourUtilities.BLACK)
                class_console.print(x=class_package_x + 25, y=counter, string=balanced_class[selected_menu_option][loc], fg=colourUtilities.WHITE)
                class_console.draw_rect(x=class_package_x + 40, y=counter, width=14, height=5, ch=32, fg=colourUtilities.BLACK)
                class_console.print(x=class_package_x + 40, y=counter, string=offensive_class[selected_menu_option][loc], fg=colourUtilities.WHITE)
                counter += 1

            # draw class attribute bonus


            # blit changes to root console
            class_console.blit(dest=root_console, dest_x=5, dest_y=5)
            tcod.console_flush()

            event_to_be_processed, event_action = handle_game_keys()
            if event_to_be_processed != '':
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
                        MobileUtilities.setup_class_attributes(gameworld=gameworld, player=player,
                                                               selected_class=menu_options[selected_menu_option],
                                                               health=class_health[selected_menu_option],
                                                               spellfile=class_spell_file[selected_menu_option])
                        logger.info('{} class chosen', menu_options[selected_menu_option])
                        CharacterCreation.choose_weapons(root_console=root_console, gameworld=gameworld,
                                                                  player=player, game_config=game_config,
                                                                  selected_class=menu_options[selected_menu_option])

    @staticmethod
    def select_personality_choices(con, gameworld, player, game_config):
        # The personality-oriented question affects the conversational options that NPCs provide.
        # there will be 3 options: charm, dignity, ferocity

        MobileUtilities.calculate_mobile_personality(gameworld, game_config)

        personality_component = gameworld.component_for_entity(player, mobiles.Describable)

        logger.debug('Your personality is viewed as {} by other NPCs', personality_component.personality_title)

    @staticmethod
    def choose_weapons(root_console, gameworld, player, game_config, selected_class):

        player_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='default',
                                                                       parameter='CLASSESFILE')
        start_panel_width = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_WIDTH')
        start_panel_height = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_HEIGHT')
        start_panel_frame_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_X')
        start_panel_frame_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_Y')
        start_panel_frame_width = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_WIDTH')
        start_panel_frame_height = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_HEIGHT')

        weapons_console = tcod.console.Console(width=start_panel_width, height=start_panel_height, order='F')

        draw_colourful_frame(console=weapons_console, game_config=game_config,
                             startx=start_panel_frame_x, starty=start_panel_frame_y,
                             width=start_panel_frame_width,
                             height=start_panel_frame_height,
                             title='[ Character Creation - Select Weapon ]', title_loc='centre',
                             title_decorator=False,
                             corner_decorator='', corner_studs='square',
                             msg='ESC/ to go back, up & down, left & right arrows to select, Enter to accept')

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
        weapon_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='default', parameter='WEAPONSFILE')

        spellsfile = class_spellfile.upper() + '_SPELLSFILE'

        spell_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='default', parameter=spellsfile)

        weapon_file = read_json_file(weapon_class_file)
        spell_file = read_json_file(spell_class_file)

        #initialise blank 2D list (array)
        weapon_info = [['' for x in range(3)] for x in range(len(available_weapons))]
        spell_name = [['' for x in range(6)] for x in range(len(available_weapons))]
        spell_descripton = [['' for x in range(6)] for x in range(len(available_weapons))]
        spell_cast_time = [['' for x in range(6)] for x in range(len(available_weapons))]
        spell_cool_down = [['' for x in range(6)] for x in range(len(available_weapons))]
        spell_range = [['' for x in range(6)] for x in range(len(available_weapons))]

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
                    spellCounter = 0

                    for spell in spell_file['spells']:
                        if spell['type_of_spell'] == 'combat':
                            if spell['weapon_type'] == weapon:
                                slot_id = int(spell['weapon_slot'])

                                spell_name[weapon_counter][slot_id] = spell['name']
                                spell_descripton[weapon_counter][slot_id] = spell['short_description']
                                spell_cast_time[weapon_counter][slot_id] = 'Cast time:' + spell['turns_to_cast']
                                spell_cool_down[weapon_counter][slot_id] = 'Cool down:' + spell['cool_down']
                                spellRange = -1
                                RangeOfSpell = configUtilities.get_config_value_as_string(configfile=game_config,
                                                                                              section='spells',
                                                                                              parameter=spell['spell_range'])
                                if RangeOfSpell != '':
                                    spellRange = int(RangeOfSpell)
                                else:
                                    logger.warning('Spell Range is set to zero! file:{} spell name:{}', spellsfile, spell['name'])
                                spell_range[weapon_counter][slot_id] = 'Range:' + str(spellRange)
                        spellCounter += 1
                    weapon_counter += 1

        menu_options = available_weapons

        show_weapons_options = True
        selected_menu_option = 0
        main_hand_selected_weapon = 'nothing'
        off_hand_selected_weapon = 'nothing'
        hand_choice = 1
        hand_selector = chr(62)
        main_hand_color = colourUtilities.DARKORANGE4
        off_hand_color = colourUtilities.BLUE
        spell_name_color = colourUtilities.PALEGREEN
        spell_description_color = colourUtilities.BISQUE4
        spell_cast_time_color = colourUtilities.KHAKI3
        spell_cool_down_color = colourUtilities.LIGHTBLUE3
        spell_range_color = colourUtilities.MOCCASIN

        max_menu_option = len(menu_options) - 1
        # display spell slot labels x,y values
        px = start_panel_frame_x + 5
        py = start_panel_frame_y + 17
        panellWidth = start_panel_frame_width - start_panel_frame_x
        slot_box_gap = int((panellWidth / 5))
        wd = slot_box_gap - 2
        for weapon_slot in range(1, 6):
            strToPrint = 'SLOT ' + str(weapon_slot)
            if weapon_slot < 4:
                foreground_colour = main_hand_color
            else:
                foreground_colour = off_hand_color
            weapons_console.print_box(x=px, y=py - 1, width=wd, height=1, string=strToPrint, fg=foreground_colour)

            px += slot_box_gap
            off_hand_weapon_id = 0
            main_hand_weapon_id = 0

        while show_weapons_options:

            # list available weapons
            pointy_menu(console=weapons_console, header='',
                        menu_options=menu_options, menu_id_format=True, menu_start_x=start_panel_frame_x + 3,
                        menu_start_y=start_panel_frame_y + 4, blank_line=True, selected_option=selected_menu_option)

            weaponInfoString = 'This is ' + weapon_info[selected_menu_option][weapon_name] + '\n' + \
                               'Wielded in ' + weapon_info[selected_menu_option][weapon_hands] + ' hand(s) \n' + \
                               'Weapon quality ' + weapon_info[selected_menu_option][weapon_quality]

            # display weapon info as a block of information
            weapons_console.print_box(x=start_panel_frame_x + 15, y=(start_panel_frame_y + 5), width=25, height=4,
                                      string=weaponInfoString, fg=tcod.white)

            # display spell information for each of the weapon/spell slots
            px = start_panel_frame_x + 5

            weapons_console.draw_rect(x=px, y=py, width=panellWidth - 6, height=17, ch=32, fg=tcod.white)

            if main_hand_selected_weapon != 'nothing':

                weapons_console.print_box(
                    x=px, y=py,
                    width=wd, height=2,
                    string=spell_name[main_hand_weapon_id][1], fg=spell_name_color)
                weapons_console.print_box(
                    x=px, y=py + 3,
                    width=wd, height=8,
                    string=spell_descripton[main_hand_weapon_id][1], fg=spell_description_color)
                weapons_console.print_box(
                    x=px, y=py + 12,
                    width=wd, height=1,
                    string=spell_cast_time[main_hand_weapon_id][1], fg=spell_cast_time_color)

                weapons_console.print_box(
                    x=px, y=py + 13,
                    width=wd, height=1,
                    string=spell_cool_down[main_hand_weapon_id][1], fg=spell_cool_down_color)
                weapons_console.print_box(
                    x=px, y=py + 14,
                    width=wd, height=1,
                    string=spell_range[main_hand_weapon_id][1], fg=spell_range_color)

                px += slot_box_gap

                weapons_console.print_box(
                    x=px, y=py,
                    width=wd, height=2,
                    string=spell_name[main_hand_weapon_id][2], fg=spell_name_color)
                weapons_console.print_box(
                    x=px, y=py + 3,
                    width=wd, height=8,
                    string=spell_descripton[main_hand_weapon_id][2], fg=spell_description_color)
                weapons_console.print_box(
                    x=px, y=py + 12,
                    width=wd, height=1,
                    string=spell_cast_time[main_hand_weapon_id][2], fg=spell_cast_time_color)

                weapons_console.print_box(
                    x=px, y=py + 13,
                    width=wd, height=1,
                    string=spell_cool_down[main_hand_weapon_id][2], fg=spell_cool_down_color)
                weapons_console.print_box(
                    x=px, y=py + 14,
                    width=wd, height=1,
                    string=spell_range[main_hand_weapon_id][2], fg=spell_range_color)

                px += slot_box_gap

                weapons_console.print_box(
                    x=px, y=py,
                    width=wd, height=2,
                    string=spell_name[main_hand_weapon_id][3], fg=spell_name_color)
                weapons_console.print_box(
                    x=px, y=py + 3,
                    width=wd, height=8,
                    string=spell_descripton[main_hand_weapon_id][3], fg=spell_description_color)
                weapons_console.print_box(
                    x=px, y=py + 12,
                    width=wd, height=1,
                    string=spell_cast_time[main_hand_weapon_id][3], fg=spell_cast_time_color)

                weapons_console.print_box(
                    x=px, y=py + 13,
                    width=wd, height=1,
                    string=spell_cool_down[main_hand_weapon_id][3], fg=spell_cool_down_color)
                weapons_console.print_box(
                    x=px, y=py + 14,
                    width=wd, height=1,
                    string=spell_range[main_hand_weapon_id][3], fg=spell_range_color)

                px += slot_box_gap

            if off_hand_selected_weapon != 'nothing':

                px = 52

                weapons_console.print_box(
                    x=px, y=py,
                    width=wd, height=2,
                    string=spell_name[off_hand_weapon_id][4], fg=spell_name_color)
                weapons_console.print_box(
                    x=px, y=py + 3,
                    width=wd, height=8,
                    string=spell_descripton[off_hand_weapon_id][4], fg=spell_description_color)
                weapons_console.print_box(
                    x=px, y=py + 12,
                    width=wd, height=1,
                    string=spell_cast_time[off_hand_weapon_id][4], fg=spell_cast_time_color)

                weapons_console.print_box(
                    x=px, y=py + 13,
                    width=wd, height=1,
                    string=spell_cool_down[off_hand_weapon_id][4], fg=spell_cool_down_color)
                weapons_console.print_box(
                    x=px, y=py + 14,
                    width=wd, height=1,
                    string=spell_range[off_hand_weapon_id][4], fg=spell_range_color)

                px += slot_box_gap

                weapons_console.print_box(
                    x=px, y=py,
                    width=wd, height=2,
                    string=spell_name[off_hand_weapon_id][5], fg=spell_name_color)
                weapons_console.print_box(
                    x=px, y=py + 3,
                    width=wd, height=8,
                    string=spell_descripton[off_hand_weapon_id][5], fg=spell_description_color)
                weapons_console.print_box(
                    x=px, y=py + 12,
                    width=wd, height=1,
                    string=spell_cast_time[off_hand_weapon_id][5], fg=spell_cast_time_color)

                weapons_console.print_box(
                    x=px, y=py + 13,
                    width=wd, height=1,
                    string=spell_cool_down[off_hand_weapon_id][5], fg=spell_cool_down_color)
                weapons_console.print_box(
                    x=px, y=py + 14,
                    width=wd, height=1,
                    string=spell_range[off_hand_weapon_id][5], fg=spell_range_color)


            # display main / off hand labels + weapon type selected
            main_hand_weapon = 'MAIN HAND (' + main_hand_selected_weapon + ')    '
            off_hand_weapon = 'OFF HAND (' + off_hand_selected_weapon + ')    '
            if hand_choice == 1:
                weapons_console.draw_rect(x=start_panel_frame_x + 49, y=start_panel_frame_y + 14, width=1, height=1, ch=32, fg=tcod.white)
                weapons_console.print(x=start_panel_frame_x + 19, y=start_panel_frame_y + 14, string=hand_selector, fg=tcod.yellow)
            else:
                weapons_console.draw_rect(x=start_panel_frame_x + 19, y=start_panel_frame_y + 14, width=1, height=1, ch=32, fg=tcod.white)
                weapons_console.print(x=start_panel_frame_x + 49, y=start_panel_frame_y + 14, string=hand_selector, fg=tcod.blue)

            weapons_console.print(x=start_panel_frame_x + 20, y=start_panel_frame_y + 14, string=main_hand_weapon,
                                  fg=main_hand_color)

            weapons_console.print(x=start_panel_frame_x + 50, y=start_panel_frame_y + 14, string=off_hand_weapon,
                                  fg=off_hand_color)

            # blit changes to root console
            weapons_console.blit(dest=root_console, dest_x=5, dest_y=5)
            tcod.console_flush()

            event_to_be_processed, event_action = handle_game_keys()
            if event_to_be_processed != '':
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
                            CharacterCreation.choose_armourset(root_console, gameworld, player, game_config,
                                                               main_hand_selected_weapon, off_hand_selected_weapon)

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
    def choose_armourset(root_console, gameworld, player, game_config, main_hand, off_hand):

        armourset_file = configUtilities.get_config_value_as_string(configfile=game_config, section='default', parameter='ARMOURSETFILE')
        start_panel_width = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_WIDTH')
        start_panel_height = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_HEIGHT')
        start_panel_frame_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_X')
        start_panel_frame_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_Y')
        start_panel_frame_width = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                              'START_PANEL_FRAME_WIDTH')
        start_panel_frame_height = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_HEIGHT')
        armour_menu_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'ARMOUR_MENU_X')
        armour_menu_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'ARMOUR_MENU_Y')
        armour_desc_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'ARMOUR_DESCRIPTION_X')
        armour_desc_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'ARMOUR_DESCRIPTION_Y')

        logger.info('Selecting armourset')
        armour_file = read_json_file(armourset_file)

        as_internal_name = []
        as_display_name = ''
        as_weight = ''
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
                as_weight = (armourset['weight'])
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

        armour_console = tcod.console.Console(width=start_panel_width, height=start_panel_height, order='F')

        draw_colourful_frame(console=armour_console, game_config=game_config,
                             startx=start_panel_frame_x, starty=start_panel_frame_y,
                             width=start_panel_frame_width,
                             height=start_panel_frame_height,
                             title='[ Character Creation - Choose Armourset ]', title_loc='centre',
                             title_decorator=False,
                             corner_decorator='', corner_studs='square',
                             msg='ESC/ to go back, up & down arrows to select, Enter to accept')

        armour_description = 'You will be wearing ' + as_display_name + ' armour, ' + 'which is made from ' +\
                             as_material + '. ' + 'Your colleagues would describe it as ' + as_flavour

        armour_console.print_box(x=armour_desc_x, y=armour_desc_y, width=50, height=6, string=armour_description, fg=colourUtilities.PALEGREEN)
        # list available armour
        armour_console.print(x=23, y=8, string='You can modify your armour thus...', fg=colourUtilities.BLUE)

        flx = 38
        attx= 20
        # armour column titles
        armour_console.print(x=armour_menu_x + 2, y=armour_menu_y - 1, string='Prefix', fg=colourUtilities.LIGHTSLATEGRAY)
        armour_console.print(x=attx, y=armour_menu_y - 1, string='Bonus to...', fg=colourUtilities.LIGHTSLATEGRAY)
        armour_console.print(x=flx, y=armour_menu_y - 1, string='Flavour', fg=colourUtilities.LIGHTSLATEGRAY)

        show_armour_options = True
        selected_menu_option = 0
        menu_options = as_prefix_list
        max_menu_option = len(menu_options) - 1

        while show_armour_options:

            # blit changes to root console
            armour_console.blit(dest=root_console, dest_x=5, dest_y=5)
            tcod.console_flush()

            pointy_menu(console=armour_console, header='',
                        menu_options=menu_options, menu_id_format=True, menu_start_x=armour_menu_x,
                        menu_start_y=armour_menu_y, blank_line=True, selected_option=selected_menu_option)

            # display attribute to be modified
            coloured_list(console=armour_console, list_options=px_att_name,
                          list_x=attx, list_y=armour_menu_y,
                          selected_option='nothing', blank_line=True, fg=colourUtilities.LIGHTBLUE1)

            # display flavour text
            coloured_list(console=armour_console, list_options=px_flavour,
                          list_x=flx, list_y=armour_menu_y,
                          selected_option='nothing', blank_line=True, fg=colourUtilities.LIGHTBLUE1)

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
                        CharacterCreation.generate_player_character_from_choices(
                            root_console=root_console, gameworld=gameworld, game_config=game_config, player=player,
                            main_hand=main_hand, off_hand=off_hand, armourset=armourset, armour_prefix=armour_prefix)

    @staticmethod
    def generate_player_character_from_choices(root_console, gameworld, game_config, player, main_hand, off_hand, armourset, armour_prefix):

        # create starting armour from armourset and prefix
        this_armourset = ItemManager.create_full_armour_set(gameworld=gameworld, armourset=armourset, prefix=armour_prefix, game_config=game_config)

        ItemUtilities.equip_full_set_of_armour(gameworld=gameworld, entity=player, armourset=this_armourset)

        MobileUtilities.calculate_derived_attributes(gameworld=gameworld, entity=player)

        # creating spells --> this loads all spells into the game as entities
        create_spell_entities(gameworld, game_config)

        # create starting weapon(s) - based on what's passed into this method
        if main_hand == off_hand:
            logger.info('creating a starting 2-handed weapon for the player')

            class_component = MobileUtilities.get_character_class(gameworld, player)

            created_weapon = ItemManager.create_weapon(gameworld=gameworld, weapon_type=main_hand, game_config=game_config)
            weapon_type = ItemUtilities.get_weapon_type(gameworld, created_weapon)

            # parameters are: gameworld, weapon object, weapon type as a string, mobile class
            logger.info('Loading the {} with the necessary spells', weapon_type)
            WeaponClass.load_weapon_with_spells(gameworld, created_weapon, weapon_type, class_component)

            # equip player with newly created starting weapon
            MobileUtilities.equip_weapon(gameworld=gameworld, entity=player, weapon=created_weapon, hand='both')

        if main_hand != '' and main_hand != off_hand:
            logger.info('creating a 1-handed weapon (main hand) for the player')

            class_component = MobileUtilities.get_character_class(gameworld, player)
            # class_component = gameworld.component_for_entity(player, mobiles.CharacterClass)

            # created_weapon, hands_to_hold = NewCharacter.create_starting_weapon(gameworld, player, game_config)
            created_weapon = ItemManager.create_weapon(gameworld=gameworld, weapon_type=main_hand, game_config=game_config)
            weapon_type = ItemUtilities.get_weapon_type(gameworld, created_weapon)

            # parameters are: gameworld, weapon object, weapon type as a string, mobile class
            logger.info('Loading that weapon with the necessary spells')
            WeaponClass.load_weapon_with_spells(gameworld, created_weapon, weapon_type, class_component)

            # equip player with newly created starting weapon
            MobileUtilities.equip_weapon(gameworld=gameworld, entity=player, weapon=created_weapon, hand='main')

        if off_hand != '' and off_hand != main_hand:
            class_component = MobileUtilities.get_character_class(gameworld, player)

            created_weapon = ItemManager.create_weapon(gameworld=gameworld, weapon_type=off_hand,
                                                       game_config=game_config)
            weapon_type = ItemUtilities.get_weapon_type(gameworld, created_weapon)

            # parameters are: gameworld, weapon object, weapon type as a string, mobile class
            logger.info('Loading that weapon with the necessary spells')
            WeaponClass.load_weapon_with_spells(gameworld, created_weapon, weapon_type, class_component)

            # equip player with newly created starting weapon
            MobileUtilities.equip_weapon(gameworld=gameworld, entity=player, weapon=created_weapon, hand='off')

        # load spell bar with spells from weapon
        spell_bar_entity = NewCharacter.generate_spell_bar(gameworld=gameworld)
        logger.info('Loading spell bar based on equipped weapons')
        weapons_equipped = MobileUtilities.get_weapons_equipped(gameworld=gameworld, entity=player)
        SpellUtilities.populate_spell_bar_from_weapon(gameworld, player_entity=player, spellbar=spell_bar_entity, wpns_equipped=weapons_equipped)

        racial_details = MobileUtilities.get_mobile_race_details(gameworld=gameworld, entity=player)
        player_race_component = racial_details[0]
        CharacterCreation.name_your_character(root_console=root_console, game_config=game_config, gameworld=gameworld,
                                              player_race_component=player_race_component)

    @staticmethod
    def name_your_character(root_console, game_config, gameworld, player_race_component):

        start_panel_width = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_WIDTH')
        start_panel_height = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_HEIGHT')
        start_panel_frame_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_X')
        start_panel_frame_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_Y')
        start_panel_frame_width = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_WIDTH')
        start_panel_frame_height = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_HEIGHT')
        name_menu_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'NAME_MENU_X')
        name_menu_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'NAME_MENU_Y')
        name_list_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'NAME_LIST_X')
        name_list_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'NAME_LIST_Y')
        mx = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'NAME_MALE_TAG_X')
        fx = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'NAME_FEMALE_TAG_X')
        gy = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'NAME_MALE_TAG_Y')
        txt_panel_write_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='TXT_PANEL_WRITE_X')
        txt_panel_write_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='TXT_PANEL_WRITE_Y')
        txt_panel_cursor = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='TXT_PANEL_CURSOR')
        txt_panel_cursor_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='TXT_PANEL_CURSOR_X')
        txt_panel_cursor_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='TXT_PANEL_CURSOR_Y')
        txt_panel_letters_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='TXT_PANEL_LETTERS_LEFT_X')
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
        textinput_console = tcod.console.Console(width=start_panel_width, height=start_panel_height, order='F')

        textinput_console.print(x=mx, y=gy, string='Male', fg=tcod.white)
        textinput_console.print(x=fx, y=gy, string='Female', fg=tcod.white)

        draw_colourful_frame(console=textinput_console, game_config=game_config,
                             startx=start_panel_frame_x, starty=start_panel_frame_y,
                             width=start_panel_frame_width,
                             height=start_panel_frame_height,
                             title='[ Character Creation - Name Your Character ]', title_loc='centre',
                             title_decorator=False,
                             corner_decorator='', corner_studs='square',
                             msg='ESC/ to go back. Enter to choose.')
        while character_not_named:

            if gender_choice == 1:
                textinput_console.draw_rect(x=fx - cxoffset, y=gy, width=1, height=1, ch=32, fg=tcod.white)
                textinput_console.print(x=mx - cxoffset, y=gy, string=gender_selector, fg=tcod.yellow)
            else:
                textinput_console.draw_rect(x=mx - cxoffset, y=gy, width=1, height=1, ch=32, fg=tcod.white)
                textinput_console.print(x=fx - cxoffset, y=gy, string=gender_selector, fg=tcod.yellow)

            if selected_name != '':
                textinput_console.draw_rect(x=name_menu_x, y=30, width=35, height=1, ch=32, fg=tcod.white)
                textinput_console.print(x=name_menu_x, y=30, string='Selected Name: ' + selected_name, fg=tcod.desaturated_blue)

            # blit changes to root console
            textinput_console.blit(dest=root_console, dest_x=5, dest_y=5)
            tcod.console_flush()

            pointy_menu(console=textinput_console, header='',
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
                            MobileUtilities.set_player_gender(gameworld=gameworld, entity=player_entity, gender='female')

                        if selected_menu_option == 1:
                            enter_name = True
                            if my_word != '':
                                textinput_console.draw_rect(x=txt_panel_write_x, y=txt_panel_write_y,
                                                            width=35, height=1, ch=32, fg=tcod.white)
                            if selected_name != '':
                                textinput_console.draw_rect(x=mx, y=(name_menu_y + 3) + max_menu_option, width=35,
                                                            height=1, ch=32, fg=tcod.white)
                            while enter_name:
                                textinput_console.put_char(x=txt_panel_cursor_x + letter_count, y=txt_panel_cursor_y, ch=txt_panel_cursor)
                                # blit changes to root console
                                textinput_console.blit(dest=root_console, dest_x=5, dest_y=5)
                                tcod.console_flush()
                                event_to_be_processed, event_action = handle_game_keys()
                                if event_to_be_processed == 'textinput' and letter_count < max_letters:
                                    if (64 < ord(event_action) < 91) or (96 < ord(event_action) < 123):
                                        textinput_console.default_fg = tcod.white
                                        textinput_console.put_char(x=txt_panel_write_x + letter_count, y=txt_panel_write_y, ch=ord(event_action))
                                        my_word += event_action
                                        letter_count += 1
                                if event_to_be_processed == 'keypress':
                                    if event_action == 'quit':
                                        enter_name = False
                                        my_word = ''
                                        letter_count = 0
                                        textinput_console.draw_rect(x=txt_panel_write_x, y=txt_panel_write_y,
                                                                    width=35, height=1, ch=32, fg=tcod.white)
                                    if event_action == 'delete':
                                        if letter_count > 0:
                                            textinput_console.default_fg = tcod.white
                                            textinput_console.put_char(x=(txt_panel_write_x + letter_count) - 1, y=txt_panel_write_y, ch=32)
                                            textinput_console.put_char(x=txt_panel_cursor_x + letter_count, y=txt_panel_cursor_y, ch=32)
                                            my_word = my_word[:-1]
                                            letter_count -= 1

                                    if event_action == 'enter':
                                        selected_name = my_word
                                        my_word = ''
                                        enter_name = False
                                        character_not_named = False
                                        textinput_console.put_char(x=txt_panel_cursor_x + letter_count,
                                                                   y=txt_panel_cursor_y, ch=32)
                                        letter_count = 0
                                        textinput_console.draw_rect(x=txt_panel_letters_x, y=txt_panel_write_y,
                                                                    width=18, height=1, ch=32, fg=tcod.white)
                                        MobileUtilities.set_mobile_first_name(gameworld=gameworld, entity=player_entity,name=selected_name)

                                        CharacterCreation.display_starting_character(root_console=root_console,
                                                                                     gameworld=gameworld,
                                                                                     player=player_entity)
                                # display letters remaining
                                if enter_name:
                                    letters_remaining = max_letters - letter_count
                                    letters_left = ' ' + str(letters_remaining) + ' letters left '
                                    textinput_console.default_alignment = tcod.RIGHT
                                    textinput_console.print(x=txt_panel_letters_x, y=txt_panel_write_y, fg=tcod.yellow, string=letters_left)

                        if selected_menu_option == 2:
                            listOfNames = MobileUtilities.generate_list_of_random_names(gameworld=gameworld, game_config=game_config, entity=player_entity, gender=gender_choice, race=player_race_component)
                            for idx in range(10):
                                strToPrint = str(idx) + '. ' + listOfNames[idx]
                                textinput_console.draw_rect(x=name_list_x, y=name_list_y + idx, width=35, height=1, ch=32, fg=tcod.white)
                                textinput_console.print(x=name_list_x, y=name_list_y + idx, string=strToPrint, fg=tcod.white)
                            # blit changes to root console
                            textinput_console.blit(dest=root_console, dest_x=5, dest_y=5)
                            tcod.console_flush()
                            name_not_chosen = True
                            while name_not_chosen:
                                event_to_be_processed, event_action = handle_game_keys()
                                if event_to_be_processed == 'textinput':
                                    if 47 < ord(event_action) < 58:
                                        selected_name = listOfNames[int(event_action)]
                                        name_not_chosen = False
                                        character_not_named = False
                                        textinput_console.draw_rect(x=name_list_x, y=name_list_y, width=35,
                                                                    height=11, ch=32, fg=tcod.white)

                                        MobileUtilities.set_mobile_first_name(gameworld=gameworld, entity=player_entity,name=selected_name)
                                        CharacterCreation.display_starting_character(root_console=root_console,
                                                                                     gameworld=gameworld,
                                                                                     player=player_entity)
                                if event_to_be_processed == 'keypress':
                                    if event_action == 'quit':
                                        name_not_chosen = False
                                        selected_name = ''
                                textinput_console.draw_rect(x=name_list_x, y=name_list_y, width=35, height=11, ch=32, fg=tcod.white)

                        if selected_menu_option == 3:
                            if selected_name != '':
                                textinput_console.draw_rect(x=txt_panel_write_x, y=txt_panel_write_y,
                                                            width=35, height=1, ch=32, fg=tcod.white)
                            selected_name = MobileUtilities.choose_random_name(gameworld=gameworld, game_config=game_config, entity=player_entity, gender=gender_choice, race=player_race_component)
                            textinput_console.draw_rect(x=mx, y=(name_menu_y + 3) + max_menu_option, width=35, height=1, ch=32, fg=tcod.white)
                            textinput_console.print(x=mx, y=(name_menu_y + 3) + max_menu_option, string=selected_name, fg=tcod.white)
                            character_not_named = False

                            MobileUtilities.set_mobile_first_name(gameworld=gameworld, entity=player_entity,
                                                                  name=selected_name)
                            CharacterCreation.display_starting_character(root_console=root_console, gameworld=gameworld)

    @staticmethod
    def display_starting_character(root_console, gameworld):
        logger.info('Displaying character starting stats')
        game_config = configUtilities.load_config()
        start_panel_width = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_WIDTH')
        start_panel_height = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_HEIGHT')
        start_panel_frame_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_X')
        start_panel_frame_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_Y')
        start_panel_frame_width = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_WIDTH')
        start_panel_frame_height = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_HEIGHT')
        display_char_menu_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_MENU_X')
        display_char_menu_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_MENU_Y')
        display_char_personal_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_PERSONAL_X')
        display_char_personal_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_PERSONAL_Y')
        display_char_personal_w = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_PERSONAL_W')
        display_char_personal_h = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_PERSONAL_H')
        dcp_fg = configUtilities.get_config_value_as_string(game_config, 'newgame', 'DISPLAY_CHAR_PERSONAL_FG')
        dcp_bg = configUtilities.get_config_value_as_string(game_config, 'newgame', 'DISPLAY_CHAR_PERSONAL_BG')
        display_char_attributes_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_ATTRIBUTES_FRAME_X')
        display_char_attributes_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_ATTRIBUTES_FRAME_Y')
        display_char_attributes_w = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_ATTRIBUTES_FRAME_W')
        display_char_attributes_h = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_ATTRIBUTES_FRAME_H')
        dca_fg = configUtilities.get_config_value_as_string(game_config, 'newgame', 'DISPLAY_CHAR_ATTRIBUTES_FG')
        dca_bg = configUtilities.get_config_value_as_string(game_config, 'newgame', 'DISPLAY_CHAR_ATTRIBUTES_BG')
        display_char_pri_attributes_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_PRI_ATTRIBUTES_X')
        display_char_pri_attributes_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_PRI_ATTRIBUTES_Y')
        display_char_pri_attributes_w = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_PRI_ATTRIBUTES_W')
        display_char_pri_attributes_h = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_PRI_ATTRIBUTES_H')
        display_char_pri_attr_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_PRI_ATTR_X')
        display_char_pri_attr_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_PRI_ATTR_Y')

        display_char_sec_attributes_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_SEC_ATTRIBUTES_X')
        display_char_sec_attributes_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_SEC_ATTRIBUTES_Y')
        display_char_sec_attributes_w = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_SEC_ATTRIBUTES_W')
        display_char_sec_attributes_h = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_SEC_ATTRIBUTES_H')
        display_char_sec_attr_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_SEC_ATTR_X')
        display_char_sec_attr_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_SEC_ATTR_Y')

        display_char_der_attributes_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_DER_ATTRIBUTES_X')
        display_char_der_attributes_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_DER_ATTRIBUTES_Y')
        display_char_der_attributes_w = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_DER_ATTRIBUTES_W')
        display_char_der_attributes_h = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_DER_ATTRIBUTES_H')
        display_char_der_attr_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_DER_ATTR_X')
        display_char_der_attr_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_DER_ATTR_Y')

        display_char_hea_attr_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_HEA_ATTR_X')
        display_char_hea_attr_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_HEA_ATTR_Y')

        display_char_man_attr_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_MAN_ATTR_X')
        display_char_man_attr_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_MAN_ATTR_Y')

        display_char_armset_attr_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_ARMSET_ATTR_X')
        display_char_armset_attr_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_ARMSET_ATTR_Y')
        display_char_armset_attr_w = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_ARMSET_W')
        display_char_armset_attr_h = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_ARMSET_H')

        display_char_armour_attr_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_ARMOUR_ATTR_X')
        display_char_armour_attr_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_CHAR_ARMOUR_ATTR_Y')
        dap_fg = configUtilities.get_config_value_as_string(game_config, 'newgame', 'DISPLAY_ARMOUR_INFO_BG')

        display_wpn_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_WPN_X')
        display_wpn_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_WPN_Y')
        display_wpn_w = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_WPN_W')
        display_wpn_h = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_WPN_H')

        display_main_wpn_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_MAIN_WPN_X')
        display_main_wpn_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_MAIN_WPN_Y')

        display_off_wpn_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_OFF_WPN_X')
        display_off_wpn_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'DISPLAY_OFF_WPN_Y')

        display_char_personal_fg = colourUtilities.colors[dcp_fg]
        display_char_personal_bg = colourUtilities.colors[dcp_bg]
        display_char_attributes_fg = colourUtilities.colors[dca_fg]
        display_char_attributes_bg = colourUtilities.colors[dca_bg]
        display_armour_info_bg = colourUtilities.colors[dap_fg]

        character_display = tcod.console.Console(width=start_panel_width, height=start_panel_height, order='F')
        player_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)

        draw_colourful_frame(console=character_display, game_config=game_config,
                             startx=start_panel_frame_x, starty=start_panel_frame_y,
                             width=start_panel_frame_width,
                             height=start_panel_frame_height,
                             title='[ Character Creation - Finished ]', title_loc='centre',
                             title_decorator=False,
                             corner_decorator='', corner_studs='square',
                             msg='')
        menu_options = ['Accept', 'Save Build', 'Start Again']
        max_menu_option = len(menu_options) - 1
        selected_menu_option = 0
        not_ready_to_proceed = True

        # personal information
        # name
        player_names = MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=player_entity)
        first_name = player_names[0]
        last_name = player_names[1]
        # gender
        player_gender = MobileUtilities.get_player_gender(gameworld=gameworld, entity=player_entity)
        # race
        racial_details = MobileUtilities.get_mobile_race_details(gameworld=gameworld, entity=player_entity)
        player_race = racial_details[0]
        # class
        player_class = MobileUtilities.get_character_class(gameworld=gameworld, entity=player_entity)
        # personality
        player_personality = MobileUtilities.get_mobile_personality_title(gameworld=gameworld, entity=player_entity)

        personal_info = 'You are ' + first_name + ' ' + last_name + ', a ' + player_gender + ', ' + player_class + ' from ' + player_race + '.'
        personality_info = ' Your personality would be described as ' + player_personality.lower() + '.'

        personal_details = personal_info + personality_info

        # display_coloured_box(console=character_display, title='Personal Info',
        #                      posx=display_char_personal_x, posy=display_char_personal_y,
        #                      width=display_char_personal_w, height=display_char_personal_h,
        #                      fg=display_char_personal_fg, bg=display_char_personal_bg)
        character_display.print_box(x=display_char_personal_x, y=display_char_personal_y,
                                    width=display_char_personal_w, height=display_char_personal_h,
                                    string=personal_details,
                                    fg=display_char_personal_fg)
        # armour
        display_coloured_box(console=character_display, title='Armour',
                             posx=display_char_armset_attr_x, posy=display_char_armset_attr_y,
                             width=display_char_armset_attr_w, height=display_char_armset_attr_h,
                             fg=display_char_personal_fg, bg=display_armour_info_bg)
        # armourset / prefix + flavour text / bonus attribute
        # bodylocation / armour display name / defense value

        strToPrint = "Location Material Display Defense"
        character_display.print_box(x=display_char_armour_attr_x, y=display_char_armour_attr_y + 1, width=len(strToPrint), height=1,
                             string=strToPrint)

        head_armour_id = MobileUtilities.is_entity_wearing_head_armour(gameworld=gameworld, entity=player_entity)
        armour_material = ItemUtilities.get_item_material(gameworld=gameworld, entity=head_armour_id)
        armour_displayname = ItemUtilities.get_item_displayname(gameworld=gameworld, entity=head_armour_id)
        def_head_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, entity=head_armour_id)
        strToPrint = "Head:    " + armour_material + '  ' + armour_displayname + '         ' + str(def_head_value)
        character_display.print_box(x=display_char_armour_attr_x, y=display_char_armour_attr_y + 2, width=len(strToPrint), height=1,
                             string=strToPrint)

        chest_armour_id = MobileUtilities.is_entity_wearing_chest_armour(gameworld=gameworld, entity=player_entity)
        armour_material = ItemUtilities.get_item_material(gameworld=gameworld, entity=chest_armour_id)
        armour_displayname = ItemUtilities.get_item_displayname(gameworld=gameworld, entity=chest_armour_id)
        def_chest_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, entity=chest_armour_id)
        strToPrint = "Chest:   " + armour_material + '  ' + armour_displayname + '        ' + str(def_chest_value)
        character_display.print_box(x=display_char_armour_attr_x, y=display_char_armour_attr_y + 3, width=len(strToPrint), height=1,
                             string=strToPrint)

        hands_armour_id = MobileUtilities.is_entity_wearing_hands_armour(gameworld=gameworld, entity=player_entity)
        armour_material = ItemUtilities.get_item_material(gameworld=gameworld, entity=hands_armour_id)
        armour_displayname = ItemUtilities.get_item_displayname(gameworld=gameworld, entity=hands_armour_id)
        def_hands_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, entity=hands_armour_id)
        strToPrint = "Hands:   " + armour_material + '  ' + armour_displayname + ' ' + str(def_hands_value)
        character_display.print_box(x=display_char_armour_attr_x, y=display_char_armour_attr_y + 4, width=len(strToPrint), height=1,
                             string=strToPrint)

        legs_armour_id = MobileUtilities.is_entity_wearing_legs_armour(gameworld=gameworld, entity=player_entity)
        armour_material = ItemUtilities.get_item_material(gameworld=gameworld, entity=legs_armour_id)
        armour_displayname = ItemUtilities.get_item_displayname(gameworld=gameworld, entity=legs_armour_id)
        def_legs_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, entity=legs_armour_id)
        strToPrint = "Legs:    " + armour_material + '  ' + armour_displayname + '    ' + str(def_legs_value)
        character_display.print_box(x=display_char_armour_attr_x, y=display_char_armour_attr_y + 5, width=len(strToPrint), height=1,
                             string=strToPrint)

        feet_armour_id = MobileUtilities.is_entity_wearing_feet_armour(gameworld=gameworld, entity=player_entity)
        armour_material = ItemUtilities.get_item_material(gameworld=gameworld, entity=feet_armour_id)
        armour_displayname = ItemUtilities.get_item_displayname(gameworld=gameworld, entity=feet_armour_id)
        def_feet_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, entity=feet_armour_id)
        strToPrint = "Feet:    " + armour_material + '  ' + armour_displayname + '     ' + str(def_feet_value)
        character_display.print_box(x=display_char_armour_attr_x, y=display_char_armour_attr_y + 6, width=len(strToPrint), height=1,
                             string=strToPrint)
        # attributes

        display_coloured_box(console=character_display, title="Attributes",
                             posx=display_char_attributes_x,
                             posy=display_char_attributes_y,
                             width=display_char_attributes_w,
                             height=display_char_attributes_h,
                             fg=display_char_attributes_fg,
                             bg=display_char_attributes_bg)

        player_power = MobileUtilities.get_mobile_power(gameworld=gameworld, entity=player_entity)
        player_precision = MobileUtilities.get_mobile_precision(gameworld=gameworld, entity=player_entity)
        player_toughness = MobileUtilities.get_mobile_toughness(gameworld=gameworld, entity=player_entity)
        player_vitality = MobileUtilities.get_mobile_vitality(gameworld=gameworld, entity=player_entity)
        player_concentration = MobileUtilities.get_mobile_concentration(gameworld=gameworld, entity=player_entity)
        player_condi_damage = MobileUtilities.get_mobile_condition_damage(gameworld=gameworld, entity=player_entity)
        player_expertise = MobileUtilities.get_mobile_expertise(gameworld=gameworld, entity=player_entity)
        player_ferocity = MobileUtilities.get_mobile_ferocity(gameworld=gameworld, entity=player_entity)
        player_healing_power = MobileUtilities.get_mobile_healing_power(gameworld=gameworld, entity=player_entity)
        player_armour = MobileUtilities.get_derived_armour_value(gameworld=gameworld, entity=player_entity)
        player_boon_duration = MobileUtilities.get_derived_boon_duration(gameworld=gameworld, entity=player_entity)

        player_critical_chance = MobileUtilities.get_derived_critical_hit_chance(gameworld=gameworld, entity=player_entity)
        player_critical_damage = MobileUtilities.get_derived_critical_damage(gameworld=gameworld, entity=player_entity)
        player_condi_duration = MobileUtilities.get_derived_condition_duration(gameworld=gameworld, entity=player_entity)
        player_max_health = MobileUtilities.get_derived_maximum_health(gameworld=gameworld, entity=player_entity)
        player_maximum_mana = MobileUtilities.get_derived_maximum_mana(gameworld=gameworld, entity=player_entity)

        # primary / secondary / derived / bonuses highlighted
        display_coloured_box(console=character_display, title="Primary",
                             posx=display_char_pri_attributes_x,
                             posy=display_char_pri_attributes_y,
                             width=display_char_pri_attributes_w,
                             height=display_char_pri_attributes_h,
                             fg=display_char_attributes_fg,
                             bg=display_char_attributes_bg)

        character_display.print_box(x=display_char_pri_attr_x, y=display_char_pri_attr_y, width=len("Power:" + str(player_power)), height=1,
                             string="Power:" + str(player_power))

        character_display.print_box(x=display_char_pri_attr_x, y=display_char_pri_attr_y + 1, width=len("Precision:" + str(player_precision)),
                             height=1, string="Precision:" + str(player_precision))
        character_display.print_box(x=display_char_pri_attr_x, y=display_char_pri_attr_y + 2, width=len("Toughness:" + str(player_toughness)),
                             height=1, string="Toughness:" + str(player_toughness))
        character_display.print_box(x=display_char_pri_attr_x, y=display_char_pri_attr_y + 3, width=len("Vitality:" + str(player_vitality)), height=1,
                             string="Vitality:" + str(player_vitality))

        display_coloured_box(console=character_display, title="Secondary",
                             posx=display_char_sec_attributes_x,
                             posy=display_char_sec_attributes_y,
                             width=display_char_sec_attributes_w,
                             height=display_char_sec_attributes_h,
                             fg=display_char_attributes_fg,
                             bg=display_char_attributes_bg)

        character_display.print_box(x=display_char_sec_attr_x, y=display_char_sec_attr_y, width=len("Concentration:" + str(player_concentration)), height=1,
                             string="Concentration:" + str(player_concentration))
        character_display.print_box(x=display_char_sec_attr_x, y=display_char_sec_attr_y + 1, width=len("Condition Damage:" + str(player_condi_damage)), height=1,
                             string="Condition Damage:" + str(player_condi_damage))
        character_display.print_box(x=display_char_sec_attr_x, y=display_char_sec_attr_y + 2, width=len("Expertise:" + str(player_expertise)), height=1,
                             string="Expertise:" + str(player_expertise))
        character_display.print_box(x=display_char_sec_attr_x, y=display_char_sec_attr_y + 3, width=len("Ferocity:" + str(player_ferocity)), height=1,
                             string="Ferocity:" + str(player_ferocity))
        character_display.print_box(x=display_char_sec_attr_x, y=display_char_sec_attr_y + 4, width=len("Healing Power:" + str(player_healing_power)), height=1,
                             string="Healing Power:" + str(player_healing_power))

        display_coloured_box(console=character_display, title="Derived",
                             posx=display_char_der_attributes_x,
                             posy=display_char_der_attributes_y,
                             width=display_char_der_attributes_w,
                             height=display_char_der_attributes_h,
                             fg=display_char_attributes_fg,
                             bg=display_char_attributes_bg)

        character_display.print_box(x=display_char_der_attr_x, y=display_char_der_attr_y, width=len("Armour:" + str(player_armour)), height=1,
                             string="Armour:" + str(player_armour))
        character_display.print_box(x=display_char_der_attr_x, y=display_char_der_attr_y + 1, width=len("Boon Duration:" + str(player_boon_duration)), height=1,
                             string="Boon Duration:" + str(player_boon_duration))
        character_display.print_box(x=display_char_der_attr_x, y=display_char_der_attr_y + 2, width=len("Critical Chance:" + str(player_critical_chance) + '%'), height=1,
                             string="Critical Chance:" + str(player_critical_chance) + '%')
        character_display.print_box(x=display_char_der_attr_x, y=display_char_der_attr_y + 3, width=len("Critical Damage:" + str(player_critical_damage) + '%'), height=1,
                             string="Critical Damage:" + str(player_critical_damage) + '%')
        character_display.print_box(x=display_char_der_attr_x, y=display_char_der_attr_y + 4, width=len("Condition Duration:" + str(player_condi_duration)), height=1,
                             string="Condition Duration:" + str(player_condi_duration))
        # health
        character_display.print_box(x=display_char_hea_attr_x, y=display_char_hea_attr_y, width=len("Health:" + str(player_max_health)), height=1,
                             string="Health:" + str(player_max_health))
        # mana
        character_display.print_box(x=display_char_man_attr_x, y=display_char_man_attr_y, width=len("Mana:" + str(player_maximum_mana)), height=1,
                             string="Mana:" + str(player_maximum_mana))

        # weapons

        display_coloured_box(console=character_display, title="Weapons",
                             posx=display_wpn_x,
                             posy=display_wpn_y,
                             width=display_wpn_w,
                             height=display_wpn_h,
                             fg=display_char_attributes_fg,
                             bg=display_char_attributes_bg)

        weapons_list = MobileUtilities.get_weapons_equipped(gameworld=gameworld, entity=player_entity)
        logger.info('Equipped weapons:{}', weapons_list[2])
        main_weapon = weapons_list[0]
        off_weapon = weapons_list[1]
        both_weapon = weapons_list[2]
        main_hand_weapon_name = 'undefined'
        off_hand_weapon_name = 'undefined'

        if both_weapon > 0:
            main_hand_weapon_name = ItemUtilities.get_item_name(gameworld=gameworld, entity=both_weapon)
            slot1_name = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=gameworld, weapon_equipped=both_weapon, slotid=1)
            slot2_name = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=gameworld, weapon_equipped=both_weapon, slotid=2)
            slot3_name = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=gameworld, weapon_equipped=both_weapon, slotid=3)

            off_hand_weapon_name = main_hand_weapon_name
            slot4_name = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=gameworld, weapon_equipped=both_weapon, slotid=4)
            slot5_name = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=gameworld, weapon_equipped=both_weapon, slotid=5)
        else:
            main_hand_weapon_name = ItemUtilities.get_item_name(gameworld=gameworld, entity=main_weapon)
            slot1_name = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=gameworld, weapon_equipped=main_weapon, slotid=1)
            slot2_name = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=gameworld, weapon_equipped=main_weapon, slotid=2)
            slot3_name = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=gameworld, weapon_equipped=main_weapon, slotid=3)

            off_hand_weapon_name = ItemUtilities.get_item_name(gameworld=gameworld, entity=off_weapon)
            slot4_name = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=gameworld, weapon_equipped=off_weapon, slotid=4)
            slot5_name = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=gameworld, weapon_equipped=off_weapon, slotid=5)

        main_wpn_display = 'Main Hand: ' + main_hand_weapon_name
        slot1_display = 'Slot 1:' + slot1_name
        slot2_display = 'Slot 2:' + slot2_name
        slot3_display = 'Slot 3:' + slot3_name
        slot4_display = 'Slot 4:' + slot4_name
        slot5_display = 'Slot 5:' + slot5_name

        off_wpn_display = 'Off Hand: ' + off_hand_weapon_name

        # main hand
        character_display.print_box(x=display_main_wpn_x, y=display_main_wpn_y, width=len(main_wpn_display), height=1, string=main_wpn_display)
        character_display.print_box(x=display_main_wpn_x, y=display_main_wpn_y + 1, width=len(slot1_display), height=1, string=slot1_display)
        character_display.print_box(x=display_main_wpn_x, y=display_main_wpn_y + 2, width=len(slot2_display), height=1, string=slot2_display)
        character_display.print_box(x=display_main_wpn_x, y=display_main_wpn_y + 3, width=len(slot3_display), height=1, string=slot3_display)

        # off hand
        character_display.print_box(x=display_off_wpn_x, y=display_off_wpn_y, width=len(off_wpn_display), height=1, string=off_wpn_display)
        character_display.print_box(x=display_off_wpn_x, y=display_off_wpn_y + 1, width=len(slot4_display), height=1, string=slot4_display)
        character_display.print_box(x=display_off_wpn_x, y=display_off_wpn_y + 2, width=len(slot5_display), height=1, string=slot5_display)

        while not_ready_to_proceed:
            # blit changes to root console
            character_display.blit(dest=root_console, dest_x=5, dest_y=5)
            tcod.console_flush()
        # menu options
            pointy_menu(console=character_display, header='',
                        menu_options=menu_options, menu_id_format=True, menu_start_x=display_char_menu_x,
                        menu_start_y=display_char_menu_y, blank_line=True, selected_option=selected_menu_option)

            event_to_be_processed, event_action = handle_game_keys()
            if event_to_be_processed != '':
                if event_to_be_processed == 'keypress':
                    if event_action == 'up':
                        selected_menu_option -= 1
                        if selected_menu_option < 0:
                            selected_menu_option = max_menu_option
                    if event_action == 'down':
                        selected_menu_option += 1
                        if selected_menu_option > max_menu_option:
                            selected_menu_option = 0
                    if event_action == 'enter':
                        if selected_menu_option == 0:   # accept character build and start game
                            start_game(con=root_console, gameworld=gameworld, game_config=game_config)
                        if selected_menu_option == 1:   # save current build
                            pass
                        if selected_menu_option == 2:   # reject build and start again
                            not_ready_to_proceed = False
