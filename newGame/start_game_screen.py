import tcod
import tcod.console

from loguru import logger
from utilities import configUtilities
from utilities.display import draw_colourful_frame, pointy_menu
from utilities.input_handlers import handle_game_keys
from newGame.CharacterCreation import CharacterCreation


class StartGame:

    @staticmethod
    def start_game_screen(root_console, game_config):
        logger.info('Game Start Screen')

        game_title = configUtilities.get_config_value_as_string(configfile=game_config, section='default', parameter='GAME_TITLE')
        game_version = configUtilities.get_config_value_as_string(configfile=game_config, section='default', parameter='VERSION')
        game_copyright = configUtilities.get_config_value_as_string(configfile=game_config, section='default', parameter='COPYRIGHT')
        game_author = configUtilities.get_config_value_as_string(configfile=game_config, section='default', parameter='AUTHOR')
        version_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'VERSION_Y')
        version_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'VERSION_X')
        copyright_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'COPYRIGHT_X')
        copyright_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'COPYRIGHT_Y')
        start_panel_frame_width = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_WIDTH')
        start_panel_frame_height = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_HEIGHT')
        start_panel_width = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_WIDTH')
        start_panel_height = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_HEIGHT')
        start_panel_frame_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_X')
        start_panel_frame_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'START_PANEL_FRAME_Y')
        menu_start_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'MENU_START_X')

        start_game_console = tcod.console.Console(width=start_panel_width, height=start_panel_height, order='F')

        draw_colourful_frame(console=start_game_console, game_config=game_config,
                             startx=start_panel_frame_x, starty=start_panel_frame_y,
                             width=start_panel_frame_width, height=start_panel_frame_height,
                             title=game_title, title_loc='centre',
                             title_decorator=True,
                             corner_decorator='', corner_studs='',
                             msg='')

        # place game version message
        start_game_console.print(x=version_x, y=version_y, string=game_version, fg=tcod.light_grey, bg=tcod.black, bg_blend=tcod.BKGND_DEFAULT)

        # place game copyright message
        start_game_console.print(x=copyright_x, y=copyright_y, string=game_copyright, fg=tcod.white, bg=tcod.black, bg_blend=tcod.BKGND_DEFAULT, alignment=tcod.LEFT)
        start_game_console.print(x=copyright_x + len(game_copyright) + 1, y=copyright_y, string=game_author, fg=tcod.yellow, bg=tcod.black, bg_blend=tcod.BKGND_DEFAULT, alignment=tcod.LEFT)

        show_game_start_screen = True
        selected_menu_option = 0

        while show_game_start_screen:

            pointy_menu(console=start_game_console, header='',
                        menu_options=['New Game', 'Continue', 'Replay', 'Options', 'Help', 'Quit'], menu_id_format=True, menu_start_x=menu_start_x,
                        menu_start_y=0,  blank_line=True, selected_option=selected_menu_option)

            # blit changes to root console
            start_game_console.blit(dest=root_console, dest_x=5, dest_y=5)
            tcod.console_flush()

            event_to_be_processed, event_action = handle_game_keys()
            if event_to_be_processed != '':
                if event_to_be_processed == 'keypress':
                    if event_action == 'quit':
                        raise SystemExit()
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
                            CharacterCreation.display_character_creation_options(root_console=root_console, game_config=game_config)
                            root_console.clear(ch=32, fg=(0, 0, 0), bg=(0, 0, 0))
                            StartGame.start_game_screen(root_console, game_config)
                        if selected_menu_option == 1:     # continue existing game
                            pass
                        if selected_menu_option == 2:     # Replay old game
                            pass
                        if selected_menu_option == 3:     # Game options
                            pass
                        if selected_menu_option == 4:     # Help menu
                            pass
                        if selected_menu_option == 5:
                            raise SystemExit()

