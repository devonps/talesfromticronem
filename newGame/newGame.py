from newGame.start_game_screen import StartGame
from loguru import logger

from static.data import constants
from utilities import configUtilities, externalfileutilities


def new_game():

    logger.info('*********************')
    logger.info('* Initialising game *')
    logger.info('*********************')

    file_name = constants.FILE_BUILDLIBRARYFILE

    # does file exist
    file_exists = externalfileutilities.Externalfiles.does_file_exist(file_name)

    # dynamically update start X & Y positions of where to start drawing the dungeon map
    # the dungeon is visually AFTER the message log

    if not file_exists:
        externalfileutilities.Externalfiles.new_file(filename=file_name)
        logger.info('Creating blank build file')

    StartGame.start_game_screen()


