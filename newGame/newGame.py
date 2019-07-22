import tcod.console
import tcod.event

from newGame.start_game_screen import StartGame
from newGame.CharacterCreation import CharacterCreation
from loguru import logger
from utilities import configUtilities
from utilities.input_handlers import handle_game_keys


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

        show_game_start_screen = True

        while show_game_start_screen:
            event_to_be_processed, event_action = handle_game_keys()
            if event_to_be_processed != '':
                if event_to_be_processed == 'keypress':
                    if event_action == 'quit':
                        raise SystemExit()
                if event_to_be_processed == 'textinput':
                    if event_action == 'a':     # new game
                        CharacterCreation.display_character_creation_options(root_console=root_console, game_config=game_config)
                        root_console.clear(ch=32, fg=(0, 0, 0), bg=(0, 0, 0))
                        StartGame.start_game_screen(root_console, game_config)

                    if event_action == 'b':     # continue existing game
                        pass
                    if event_action == 'c':     # Replay old game
                        pass
                    if event_action == 'd':     # Game options
                        pass
                    if event_action == 'e':     # Help menu
                        pass
                    if event_action == 'f':
                        raise SystemExit()


