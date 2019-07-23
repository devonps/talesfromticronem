import tcod.console
import tcod.event

from newGame.start_game_screen import StartGame
from loguru import logger
from utilities import configUtilities


def new_game():
    game_config = configUtilities.load_config()
    #
    # logfile = configUtilities.get_config_value_as_string(game_config, 'logging', 'LOGFILE')
    # logformat = configUtilities.get_config_value_as_string(game_config, 'logging', 'LOGFORMAT')

    # logger.add(logfile, format=logformat)

    logger.info('*********************')
    logger.info('* Initialising game *')
    logger.info('*********************')

    game_title = configUtilities.get_config_value_as_string(game_config, 'default', 'GAME_TITLE')
    con_width = configUtilities.get_config_value_as_integer(game_config, 'tcod', 'SCREEN_WIDTH')
    con_height = configUtilities.get_config_value_as_integer(game_config, 'tcod', 'SCREEN_HEIGHT')

    tcod.console_set_custom_font('static/fonts/prestige12x12_gs_tc.png',
                                 tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    with tcod.console_init_root(w=con_width, h=con_height, title=game_title, fullscreen=False,
                                renderer=tcod.RENDERER_SDL2, order='F', vsync=True) as root_console:
        StartGame.start_game_screen(root_console, game_config)


