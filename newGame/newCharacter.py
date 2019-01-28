import tcod
import random

from loguru import logger
from newGame.initialiseNewGame import setup_game, generate_player_character, create_wizard, create_demon, create_game_world
from newGame import constants
from components import spells, weapons, mobiles
from utilities.mobileHelp import MobileUtilities

# for each (race, class, perssonality, name) choices:
# display a new screen with options
# provide optional questions


class NewCharacter:

    def create(con, gameworld):
        select_race(con=con, gameworld=gameworld)
        select_character_class(con=con, gameworld=gameworld)
        select_personality_choices(con=con, gameworld=gameworld)
        name_your_character(con=con, gameworld=gameworld)
        get_starting_equipment(con=con, gameworld=gameworld)


def select_race(con, gameworld):
    logger.info('Selecting character race')


def select_character_class(con, gameworld):
    logger.info('Selecting character class')


def select_personality_choices(con, gameworld):
    logger.info('Selecting character personality choices')


def name_your_character(con, gameworld):
    logger.info('Naming the character')


def get_starting_equipment(con, gameworld):
    logger.info('Selecting starting equipment')


