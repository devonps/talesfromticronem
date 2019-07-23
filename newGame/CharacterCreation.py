import tcod
import tcod.console

from loguru import logger
from utilities import configUtilities
from utilities.display import draw_colourful_frame, better_menu, pointy_menu
from utilities.input_handlers import handle_game_keys
from utilities.world import create_game_world
from utilities.jsonUtilities import read_json_file
from utilities.mobileHelp import MobileUtilities
from utilities.spellHelp import SpellUtilities
from newGame.newCharacter import NewCharacter
from newGame.initialiseNewGame import setup_game


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
                        menu_start_y=0,  blank_line=True, selected_option=selected_menu_option)

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

        menu_options = []
        menu_options_flavour = []
        race_prefix = []
        race_bg_colour = []
        race_size = []
        race_glyph = []

        for option in race_file['races']:
            menu_options.append(option['name'])
            menu_options_flavour.append(option['flavour'])
            race_prefix.append(option['prefix'])
            race_bg_colour.append(option['bg_colour'])
            race_size.append(option['size'])
            race_glyph.append(option['glyph'])

        show_race_options = True
        selected_menu_option = 0
        max_menu_option = len(menu_options) - 1

        while show_race_options:
            pointy_menu(console=race_console, header='',
                        menu_options=menu_options, menu_id_format=True, menu_start_x=menu_start_x, menu_start_y= 0,
                        blank_line=True, selected_option=selected_menu_option)
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
                        if selected_menu_option == 0:  # Human selected
                            MobileUtilities.setup_racial_attributes(gameworld=gameworld,
                                                                    player=player, selected_race='human',
                                                                    race_size=race_size[0], bg=tcod.black)
                        if selected_menu_option == 1:  # Elf selected
                            MobileUtilities.setup_racial_attributes(gameworld=gameworld,
                                                                    player=player, selected_race='elf',
                                                                    race_size=race_size[1], bg=tcod.blue)
                        if selected_menu_option == 2:  # Orc selected
                            MobileUtilities.setup_racial_attributes(gameworld=gameworld,
                                                                    player=player, selected_race='orc',
                                                                    race_size=race_size[2], bg=tcod.red)
                        if selected_menu_option == 3:  # Troll selected
                            MobileUtilities.setup_racial_attributes(gameworld=gameworld,
                                                                    player=player, selected_race='troll',
                                                                    race_size=race_size[3], bg=tcod.white)

                        CharacterCreation.choose_player_class(root_console, gameworld, player, game_config)

    @staticmethod
    def choose_player_class(root_console, gameworld, player, game_config):

        player_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='default',
                                                                       parameter='CLASSESFILE')
        start_panel_width = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_WIDTH')
        start_panel_height = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_HEIGHT')
        start_panel_frame_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_X')
        start_panel_frame_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_Y')
        start_panel_frame_width = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_WIDTH')
        start_panel_frame_height = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_HEIGHT')
        menu_start_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'MENU_START_X')

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

        for option in class_file['classes']:
            menu_options.append(option['name'])
            menu_options_flavour.append(option['flavour'])

        class_not_selected = True
        selected_menu_option = 0
        max_menu_option = len(menu_options) - 1

        while class_not_selected:
            pointy_menu(console=class_console, header='',
                        menu_options=menu_options, menu_id_format=True, menu_start_x=menu_start_x, menu_start_y=0,
                        blank_line=True, selected_option=selected_menu_option)

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
                    if event_action == 'enter':
                        if selected_menu_option == 0:  # necromancer selected
                            selected_class = 'necromancer'
                            MobileUtilities.setup_class_attributes(gameworld=gameworld, player=player,
                                                                   selected_class=selected_class, health=22)
                        if selected_menu_option == 1:  # witch doctor selected
                            selected_class = 'witch doctor'
                            MobileUtilities.setup_class_attributes(gameworld=gameworld, player=player,
                                                                   selected_class=selected_class, health=22)
                        if selected_menu_option == 2:  # druid selected
                            selected_class = 'druid'
                            MobileUtilities.setup_class_attributes(gameworld=gameworld, player=player,
                                                                   selected_class=selected_class, health=18)
                        if selected_menu_option == 3:  # mesmer selected
                            selected_class = 'mesmer'
                            MobileUtilities.setup_class_attributes(gameworld=gameworld, player=player,
                                                                   selected_class=selected_class, health=18)
                        if selected_menu_option == 4:  # elementalist selected
                            selected_class = 'elementalist'
                            MobileUtilities.setup_class_attributes(gameworld=gameworld, player=player,
                                                                   selected_class=selected_class, health=5)
                        if selected_menu_option == 5:  # chronomancer selected
                            selected_class = 'chronomancer'
                            MobileUtilities.setup_class_attributes(gameworld=gameworld, player=player,
                                                                   selected_class=selected_class, health=5)

                        CharacterCreation.choose_starting_weapons(root_console=root_console, gameworld=gameworld,
                                                                  player=player, game_config=game_config, selected_class=selected_class)

    @staticmethod
    def select_personality_choices(con, gameworld, player, game_config):
        logger.info('Selecting character personality choices')
        # The personality-oriented question affects the conversational options that NPCs provide.
        # there will be 3 options: charm, dignity, ferocity

        MobileUtilities.calculate_mobile_personality(gameworld, game_config)

        personality_component = gameworld.component_for_entity(player, mobiles.Describable)

        logger.debug('Your personality is viewed as {} by other NPCs', personality_component.personality_title)

    @staticmethod
    def choose_starting_weapons(root_console, gameworld, player, game_config, selected_class):

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

        logger.info('Selecting character class')
        class_file = read_json_file(player_class_file)

        available_weapons = []

        # gather list of available weapons for the player class
        for option in class_file['classes']:
            if option['name'] == selected_class:
                class_weapons = option['weapons']

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
        spell_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='default', parameter='SPELLSFILE')

        weapon_file = read_json_file(weapon_class_file)
        spell_file = read_json_file(spell_class_file)

        #initialise blank 2D list (array)
        weapon_info = [['' for x in range(3)] for x in range(len(available_weapons))]
        spell_info = [['' for x in range(6)] for x in range(len(available_weapons))]
        spellPrint1 = []

        weapon_counter = 0
        for weapon in available_weapons:
            for wpn in weapon_file['weapons']:
                if wpn['name'] == weapon:
                    weapon_info[weapon_counter][0] = wpn['display_name']
                    weapon_info[weapon_counter][1] = wpn['wielded_hands']
                    weapon_info[weapon_counter][2] = wpn['quality_level']

                    for spell in spell_file['spells']:
                        if spell['weapon_type'] == weapon:
                            slot_id = int(spell['weapon_slot'])

                            spell_info[weapon_counter][slot_id] = spell['name'] \
                                                                  + '.\n\n' + spell['description']\
                                                                  + '\ncast time:' + spell['cast_time'] \
                                                                  + '\ncool down' + spell['cool_down'] \
                                                                  + '\nmax range' + spell['max_range']

                            # spell_info[weapon_counter][slot_id] = spell['aoe']
                            # spell_info[weapon_counter][slot_id] = spell['aoe_size']
                            # spell_info[weapon_counter][slot_id] = spell['effects']

                    weapon_counter += 1

        menu_options = available_weapons

        show_weapons_options = True
        selected_menu_option = 0
        main_hand_selected_weapon = 'nothing'
        off_hand_selected_weapon = 'nothing'
        hand_choice = 1
        hand_selector = chr(62)

        max_menu_option = len(menu_options) - 1
        # display spell slot labels x,y values
        px = start_panel_frame_x + 1
        py = start_panel_frame_y + 17
        panellWidth = start_panel_frame_width - start_panel_frame_x
        slot_box_gap = int((panellWidth / 5))
        wd = slot_box_gap - 2
        for weapon_slot in range(1, 6):
            strToPrint = 'SLOT ' + str(weapon_slot)
            if weapon_slot < 3:
                foreground_colour = tcod.yellow
            else:
                foreground_colour = tcod.blue
            weapons_console.print_box(x=px + 4, y=py - 1, width=wd, height=9, string=strToPrint, fg=foreground_colour)

            # spell information
            weapons_console.print_box(x=px, y=py, width=wd, height=9, string=spell_info[selected_menu_option][weapon_slot],fg=foreground_colour)

            px += slot_box_gap

        while show_weapons_options:

            # list available weapons
            pointy_menu(console=weapons_console, header='',
                        menu_options=menu_options, menu_id_format=True, menu_start_x=start_panel_frame_x + 3,
                        menu_start_y=start_panel_frame_y + 4, blank_line=True, selected_option=selected_menu_option)

            weaponInfoString = 'This is ' + weapon_info[selected_menu_option][0] + '\n' + \
                               'Wielded in ' + weapon_info[selected_menu_option][1] + ' hand(s) \n' + \
                               'Weapon quality ' + weapon_info[selected_menu_option][2]

            # display weapon info as a block of information
            weapons_console.print_box(x=start_panel_frame_x + 15, y=(start_panel_frame_y + 5), width=25, height=4,
                                      string=weaponInfoString, fg=tcod.white)

            # display spell information for each of the weapon/spell slots
            px = start_panel_frame_x + 1
            for weapon_slot in range(1, 6):
                # spell information

                weapons_console.draw_rect(x=px, y=py, width=wd, height=9, ch=32, fg=tcod.white)
                weapons_console.print_box(x=px, y=py, width=wd, height=9, string=spell_info[selected_menu_option][weapon_slot])
                px += slot_box_gap

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
                                  fg=tcod.yellow)

            weapons_console.print(x=start_panel_frame_x + 50, y=start_panel_frame_y + 14, string=off_hand_weapon,
                                  fg=tcod.blue)

            # blit changes to root console
            weapons_console.blit(dest=root_console, dest_x=5, dest_y=5)
            tcod.console_flush()

            event_to_be_processed, event_action = handle_game_keys()
            if event_to_be_processed != '':
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
                            CharacterCreation.choose_starting_armour(root_console, gameworld, player, game_config, selected_class, main_hand_selected_weapon, off_hand_selected_weapon)

                        if weapon_info[selected_menu_option][1] == 'off' and hand_choice == 2:
                            off_hand_selected_weapon = available_weapons[selected_menu_option]

                        if weapon_info[selected_menu_option][1] == 'main' and hand_choice == 1:
                            main_hand_selected_weapon = available_weapons[selected_menu_option]

    @staticmethod
    def choose_starting_armour(root_console, gameworld, player, game_config, selected_class, main_hand, off_hand):

        player_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='default',
                                                                       parameter='CLASSESFILE')
        start_panel_width = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_WIDTH')
        start_panel_height = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_HEIGHT')
        start_panel_frame_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_X')
        start_panel_frame_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_Y')
        start_panel_frame_width = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                              'START_PANEL_FRAME_WIDTH')
        start_panel_frame_height = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                               'START_PANEL_FRAME_HEIGHT')

        armour_console = tcod.console.Console(width=start_panel_width, height=start_panel_height, order='F')

        draw_colourful_frame(console=armour_console, game_config=game_config,
                             startx=start_panel_frame_x, starty=start_panel_frame_y,
                             width=start_panel_frame_width,
                             height=start_panel_frame_height,
                             title='[ Character Creation - Select Armour ]', title_loc='centre',
                             title_decorator=False,
                             corner_decorator='', corner_studs='square',
                             msg='ESC/ to go back, up & down arrows to select, Enter to accept')

        show_armour_options = True
        selected_menu_option = 0
        menu_options = ['head', 'chest', 'hands', 'legs', 'feet']
        max_menu_option = len(menu_options) - 1

        while show_armour_options:

            # blit changes to root console
            armour_console.blit(dest=root_console, dest_x=5, dest_y=5)
            tcod.console_flush()

            # list available armour
            pointy_menu(console=armour_console, header='',
                        menu_options=menu_options, menu_id_format=True, menu_start_x=start_panel_frame_x + 3,
                        menu_start_y=start_panel_frame_y + 4, blank_line=True, selected_option=selected_menu_option)

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
                        armourset = 'apprentice'
                        CharacterCreation.generate_player_character_from_choices(
                            root_console=root_console, gameworld=gameworld, game_config=game_config, player=player,
                            main_hand=main_hand, off_hand=off_hand, armourset=armourset)

    @staticmethod
    def generate_player_character_from_choices(root_console, gameworld, game_config, player, main_hand, off_hand, armourset):

        spell_bar_entity = NewCharacter.generate_spell_bar(gameworld=gameworld)

        # create starting weapon(s) - based on what's passed into this method
        if main_hand == off_hand:
            logger.info('creating a starting 2-handed weapon for the player')
            created_weapon, hands_to_hold = NewCharacter.create_starting_weapon(gameworld, player, game_config)
            # equip player with newly created starting weapon
            NewCharacter.equip_starting_weapon(gameworld, player, created_weapon, 'both')
        if main_hand != '' and main_hand != off_hand:
            logger.info('creating a 1-handed weapon (main hand) for the player')
            created_weapon, hands_to_hold = NewCharacter.create_starting_weapon(gameworld, player, game_config)
            # equip player with newly created starting weapon
            NewCharacter.equip_starting_weapon(gameworld, player, created_weapon, 'main')
        if off_hand !='' and off_hand != main_hand:
            # equip player with newly created starting weapon
            NewCharacter.equip_starting_weapon(gameworld, player, created_weapon, 'off')

        # load spell bar with spells from weapon
        logger.info('Loading spell bar based on equipped weapons')
        weapons_equipped = MobileUtilities.get_weapons_equipped(gameworld=gameworld, entity=player)
        SpellUtilities.populate_spell_bar_from_weapon(gameworld, player_entity=player, spellbar=spell_bar_entity, wpns_equipped=weapons_equipped)

        CharacterCreation.tweak_starting_attributes(root_console=root_console, player=player, game_config=game_config)

    @staticmethod
    def tweak_starting_attributes(root_console, player, game_config):
        CharacterCreation.name_your_character(root_console=root_console, game_config=game_config)

    @staticmethod
    def name_your_character(root_console, game_config):

        start_panel_width = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_WIDTH')
        start_panel_height = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_HEIGHT')
        start_panel_frame_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_X')
        start_panel_frame_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_Y')
        start_panel_frame_width = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_WIDTH')
        start_panel_frame_height = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_HEIGHT')

        txt_panel_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='TXT_PANEL_WIDTH')
        txt_panel_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='TXT_PANEL_HEIGHT')
        txt_panel_write_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='TXT_PANEL_WRITE_X')
        txt_panel_write_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='TXT_PANEL_WRITE_Y')
        txt_panel_ins_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='TXT_PANEL_INS_X')
        txt_panel_ins_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='TXT_PANEL_INS_Y')
        txt_panel_cursor = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='TXT_PANEL_CURSOR')
        txt_panel_letters_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='TXT_PANEL_LETTERS_LEFT_X')
        txt_panel_cursor_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='TXT_PANEL_CURSOR_X')
        txt_panel_cursor_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='TXT_PANEL_CURSOR_Y')

        textinput_console = tcod.console.Console(width=start_panel_width, height=start_panel_height, order='F')

        draw_colourful_frame(console=textinput_console, game_config=game_config,
                             startx=start_panel_frame_x, starty=start_panel_frame_y,
                             width=start_panel_frame_width,
                             height=start_panel_frame_height,
                             title='[ Character Creation - Name Your Character ]', title_loc='centre',
                             title_decorator=False,
                             corner_decorator='', corner_studs='square',
                             msg='ESC/ to go back.')
        letter_count = 0
        my_word = ""
        max_letters = 15
        character_not_named = True
        text_controls = ['Backspace to delete', 'Escape to quit', 'Enter to accept', 'Leave blank for random name', 'Only alphas allowed']

        # draw horizontal line
        textinput_console.hline(x=txt_panel_ins_x, y=txt_panel_ins_y - 1, width=txt_panel_width - 2, bg_blend=tcod.BKGND_DEFAULT)

        # instructions
        textinput_console.default_alignment = tcod.LEFT

        for instruction in text_controls:
            textinput_console.print_box(x=txt_panel_ins_x, y=txt_panel_ins_y, width=txt_panel_width - 5, height=txt_panel_height - 10,
                                        string=instruction)
            txt_panel_ins_y += 1

        # display cursor
        textinput_console.put_char(x=txt_panel_cursor_x + letter_count, y=txt_panel_cursor_y, ch=txt_panel_cursor)

        # display letters remaining
        letters_remaining = max_letters - letter_count
        letters_left = ' ' + str(letters_remaining) + ' letters left'
        textinput_console.default_alignment = tcod.RIGHT
        textinput_console.print_box(x=txt_panel_letters_x, y=txt_panel_write_y, fg=tcod.yellow,
                                    width=txt_panel_width - 5, height=txt_panel_height - 10, string=letters_left)

        while character_not_named:

            # blit changes to root console
            textinput_console.blit(dest=root_console, dest_x=5, dest_y=5)
            tcod.console_flush()

            event_to_be_processed, event_action = handle_game_keys()
            if event_to_be_processed != '':
                if event_to_be_processed == 'keypress':
                    if event_action == 'quit':
                        character_not_named = False
                    if event_action == 'delete':
                        if letter_count > 0:
                            textinput_console.default_fg = tcod.white
                            textinput_console.put_char(x=(txt_panel_write_x + letter_count) - 1, y=txt_panel_write_y, ch=32)
                            textinput_console.put_char(x=txt_panel_cursor_x + letter_count, y=txt_panel_cursor_y, ch=32)
                            my_word = my_word[:-1]
                            letter_count -= 1
                    if event_action == 'enter':
                        pass
                if event_to_be_processed == 'textinput' and letter_count < max_letters:
                    if (64 < ord(event_action) < 91) or (96 < ord(event_action) < 123):
                        textinput_console.put_char(x=txt_panel_write_x + letter_count, y=txt_panel_write_y, ch=ord(event_action))
                        textinput_console.put_char(x=txt_panel_cursor_x + letter_count, y=txt_panel_cursor_y, ch=32)
                        textinput_console.default_fg = tcod.white
                        my_word += event_action
                        letter_count += 1

                # display cursor
                textinput_console.put_char(x=txt_panel_cursor_x + letter_count, y=txt_panel_cursor_y, ch=txt_panel_cursor)

                # display letters remaining
                letters_remaining = max_letters - letter_count
                letters_left = ' ' + str(letters_remaining) + ' letters left '
                textinput_console.default_alignment = tcod.RIGHT
                textinput_console.print_box(x=txt_panel_letters_x, y=txt_panel_write_y, fg=tcod.yellow,
                                        width=txt_panel_width - 5, height=txt_panel_height - 10, string=letters_left)
