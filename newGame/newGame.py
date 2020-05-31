
from newGame.start_game_screen import StartGame
from loguru import logger
from utilities import configUtilities
from utilities.externalfileutilities import Externalfiles


def new_game():
    game_config = configUtilities.load_config()

    #
    # logfile = configUtilities.get_config_value_as_string(game_config, 'logging', 'LOGFILE')
    # logformat = configUtilities.get_config_value_as_string(game_config, 'logging', 'LOGFORMAT')

    # logger.add(logfile, format=logformat)

    logger.info('*********************')
    logger.info('* Initialising game *')
    logger.info('*********************')

    fileName = configUtilities.get_config_value_as_string(game_config, 'files', 'BUILDLIBRARYFILE')

    # does file exist
    fileExists = Externalfiles.does_file_exist(fileName)

    # dynamically update start X & Y positions of where to start drawing the dungeon map
    # the dungeon is visually AFTER the message log

    # message_panel_depth = configUtilities.get_config_value_as_integer(configfile=game_config, section='messagePanel',
    #                                                                   parameter='MSG_PANEL_DEPTH')

    # configUtilities.set_config_value(configfile=game_config, section='gui', parameter='VIEWPORT_START_Y',
    #                                  value=str(message_panel_depth + 1))

    if not fileExists:
        new_file_object = Externalfiles.create_new_file(fileName)
        logger.info('Creating blank build file')
        Externalfiles.close_existing_file(new_file_object)

    StartGame.start_game_screen()


