import tcod
import tcod.console

from loguru import logger
from utilities import configUtilities
from utilities.display import draw_colourful_frame, better_menu


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

        # place game menu options
        better_menu(console=start_game_console, header='',
                    menu_options=['New Game', 'Continue', 'Replay', 'Options', 'Help', 'Quit'], menu_id_format=True,
                    menu_start_x=menu_start_x, blank_line=True)

        # place game version message
        start_game_console.print(x=version_x, y=version_y, string=game_version, fg=tcod.light_grey, bg=tcod.black, bg_blend=tcod.BKGND_DEFAULT)

        # place game copyright message
        start_game_console.print(x=copyright_x, y=copyright_y, string=game_copyright, fg=tcod.white, bg=tcod.black, bg_blend=tcod.BKGND_DEFAULT, alignment=tcod.LEFT)
        start_game_console.print(x=copyright_x + len(game_copyright) + 1, y=copyright_y, string=game_author, fg=tcod.yellow, bg=tcod.black, bg_blend=tcod.BKGND_DEFAULT, alignment=tcod.LEFT)

        # blit changes to root console
        start_game_console.blit(dest=root_console, dest_x=5, dest_y=5)
        tcod.console_flush()



