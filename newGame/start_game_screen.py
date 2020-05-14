
from loguru import logger

from ui.build_library import display_build_library
from utilities import configUtilities
from utilities.display import draw_colourful_frame, pointy_menu
from utilities.input_handlers import handle_game_keys
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
        start_panel_frame_width = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                              'START_PANEL_FRAME_WIDTH')
        start_panel_frame_height = configUtilities.get_config_value_as_integer(game_config, 'newgame',
                                                                               'START_PANEL_FRAME_HEIGHT')
        start_panel_frame_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_X')
        start_panel_frame_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_Y')
        menu_start_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'MENU_START_X')
        menu_start_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'MENU_START_Y')

        show_game_start_screen = True
        selected_menu_option = 0

        while show_game_start_screen:

            draw_colourful_frame(title=game_title, title_decorator=True, title_loc='centre', corner_decorator='',
                                 corner_studs='',
                                 msg='ESC/ to go back, up & down arrows to select, enter to accept choice')

            # place game version message
            string_to_print = '[color=light grey]' + game_version
            terminal.printf(x=version_x, y=version_y, s=string_to_print)

            # place game copyright message
            string_to_print = '[color=white]' + game_copyright + ' [color=yellow]' + game_author
            terminal.printf(x=copyright_x, y=copyright_y, s=string_to_print)

            pointy_menu(header='', menu_options=['New Game', 'Choose build from library', 'Replay', 'Options', 'Help', 'Quit'],
                        menu_id_format=True, menu_start_x=menu_start_x,menu_start_y=menu_start_y,
                        blank_line=True, selected_option=selected_menu_option)

            # blit changes to terminal
            terminal.refresh()

            event_to_be_processed, event_action = handle_game_keys()

            if event_to_be_processed != '':
                if event_to_be_processed == 'keypress':
                    if event_action == 'quit':
                        show_game_start_screen = False
                        logger.info('*** GAME ENDING ***')

                    if event_action == 'up':
                        selected_menu_option -= 1
                        if selected_menu_option < 0:
                            selected_menu_option = 5

                    if event_action == 'down':
                        selected_menu_option += 1
                        if selected_menu_option > 5:
                            selected_menu_option = 0

                    if event_action == 'enter':
                        if selected_menu_option == 0:
                            terminal.clear()
                            CharacterCreation.display_character_creation_options()
                        if selected_menu_option == 1:     # use existing build
                            display_build_library()
                            terminal.clear()
                        if selected_menu_option == 2:     # Replay old game
                            pass
                        if selected_menu_option == 3:     # Game options
                            pass
                        if selected_menu_option == 4:     # Help menu
                            pass
                        if selected_menu_option == 5:
                            show_game_start_screen = False
                            logger.info('*** GAME ENDING ***')

                if event_to_be_processed == 'mouseleftbutton':
                    (mx, my) = event_action
                    logger.info('MX {}', terminal.state(terminal.TK_MOUSE_X))
                    logger.info('MY {}', terminal.state(terminal.TK_MOUSE_Y))

        terminal.close()