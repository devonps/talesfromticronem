from loguru import logger
from utilities import configUtilities, display, input_handlers
from newGame.CharacterCreation import CharacterCreation
from bearlibterminal import terminal


class StartGame:

    @staticmethod
    def start_game_screen():
        logger.info('Game Start Screen')
        game_config = configUtilities.load_config()

        game_title = configUtilities.get_config_value_as_string(configfile=game_config, section='default',
                                                                parameter='GAME_TITLE')
        game_version = configUtilities.get_config_value_as_string(configfile=game_config, section='default',
                                                                  parameter='VERSION')
        game_copyright = configUtilities.get_config_value_as_string(configfile=game_config, section='default',
                                                                    parameter='COPYRIGHT')
        game_author = configUtilities.get_config_value_as_string(configfile=game_config, section='default',
                                                                 parameter='AUTHOR')
        version_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'VERSION_Y')
        version_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'VERSION_X')
        copyright_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'COPYRIGHT_X')
        copyright_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'COPYRIGHT_Y')
        menu_start_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'MENU_START_X')
        menu_start_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'MENU_START_Y')

        show_game_start_screen = True
        selected_menu_option = 0

        while show_game_start_screen:

            display.draw_colourful_frame(title=game_title, title_decorator=True, title_loc='centre', corner_decorator='', msg=0)

            # place game version message
            string_to_print = '[color=light grey]' + game_version
            terminal.printf(x=version_x, y=version_y, s=string_to_print)

            # place game copyright message
            string_to_print = '[color=white]' + game_copyright + ' [color=yellow]' + game_author
            terminal.printf(x=copyright_x, y=copyright_y, s=string_to_print)

            display.pointy_vertical_menu(header='', menu_options=['New Game', 'Quit'], menu_start_x=menu_start_x,
                                 menu_start_y=menu_start_y, blank_line=True, selected_option=selected_menu_option)

            # blit changes to terminal
            terminal.refresh()

            event_to_be_processed, event_action = input_handlers.handle_game_keys()

            if event_to_be_processed != '':
                if event_action == 'quit':
                    show_game_start_screen = False
                    logger.info('*** GAME ENDING ***')

                if event_action == 'up':
                    selected_menu_option -= 1
                    if selected_menu_option < 0:
                        selected_menu_option = 1

                if event_action == 'down':
                    selected_menu_option += 1
                    if selected_menu_option > 1:
                        selected_menu_option = 0

                if event_action == 'enter':
                    show_game_start_screen = StartGame.handle_enter_key_interactions(selected_menu_option=selected_menu_option)
                    terminal.clear()

        terminal.close()

    @staticmethod
    def handle_enter_key_interactions(selected_menu_option):
        if selected_menu_option == 0:
            CharacterCreation.create_new_character()
        if selected_menu_option == 1:
            show_game_start_screen = False
            logger.info('*** GAME ENDING ***')
            return show_game_start_screen
        return True
