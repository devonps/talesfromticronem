import random

from loguru import logger

from newGame.CreateSpells import AsEntities
from utilities.randomNumberGenerator import PCG32Generator
from utilities.externalfileutilities import Externalfiles
from utilities import configUtilities
from utilities.world import create_game_world


def create_world():
    gameconfig = configUtilities.load_config()
    # Esper initialisation
    gameworld = create_game_world()
    setup_gameworld(game_config=gameconfig)
    AsEntities.generate(gameworld=gameworld)

    return gameworld


def setup_gameworld(game_config):
    # world seed generation
    world_seed = generate_world_seed(game_config)
    store_world_seed(game_config, world_seed)


def generate_world_seed(game_config):
    player_seed = configUtilities.get_config_value_as_string(configfile=game_config, section='pcg',
                                                             parameter='PLAYER_SEED')

    if player_seed != '':
        world_seed = PCG32Generator.convert_string_to_integer(player_seed)
        logger.info('Using player provided seed for world seed {}', player_seed)
    else:
        world_seed = random.getrandbits(30)
        logger.info('No player seed, using large random number for world seed {}', world_seed)

    return world_seed


def store_world_seed(game_config, world_seed):
    action_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                             parameter='GAME_ACTIONS_FILE')
    fileobject = Externalfiles.start_new_game_replay_file(action_file)

    value = 'world_seed:' + str(world_seed)
    Externalfiles.write_to_existing_file(action_file, value)
    Externalfiles.close_existing_file(fileobject)
