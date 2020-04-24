
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

    if not fileExists:
        Externalfiles.create_new_file(fileName)
        logger.info('Creating blank build file')

    StartGame.start_game_screen()


