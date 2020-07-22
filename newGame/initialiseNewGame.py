import random

from loguru import logger

from components import items
from newGame.CreateSpells import AsEntities
from utilities.randomNumberGenerator import PCG32Generator
from utilities.externalfileutilities import Externalfiles
from utilities import configUtilities, jsonUtilities, world


def create_world():
    gameconfig = configUtilities.load_config()
    # Esper initialisation
    gameworld = world.create_game_world()
    setup_gameworld(game_config=gameconfig)
    AsEntities.generate(gameworld=gameworld)
    create_jewellery_entities(gameworld=gameworld)

    return gameworld


def setup_gameworld(game_config):
    # world seed generation
    world_seed = generate_world_seed(game_config)
    store_world_seed(game_config, world_seed)


def generate_world_seed(game_config):
    player_seed = configUtilities.get_config_value_as_string(configfile=game_config, section='pcg',
                                                             parameter='PLAYER_SEED')

    if player_seed != '':
        world_seed = PCG32Generator.convert_string_to_integer(value=player_seed)
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


def create_jewellery_entities(gameworld):
    game_config = configUtilities.load_config()
    jewellery_file_path = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                     parameter='JEWELLERYFILE')

    jewellery_file = jsonUtilities.read_json_file(jewellery_file_path)

    for jewellery in jewellery_file['jewellery']:
        piece_of_jewellery = world.get_next_entity_id(gameworld=gameworld)
        gameworld.add_component(piece_of_jewellery, items.TypeOfItem(label='jewellery'))
        gameworld.add_component(piece_of_jewellery, items.Describable(name=jewellery['name'], description=jewellery['description'], glyph=jewellery['glyph'], fg=jewellery['fg'], bg=jewellery['bg']))
        gameworld.add_component(piece_of_jewellery, items.Material(texture=jewellery['material']))
        gameworld.add_component(piece_of_jewellery, items.JewellerySpell)
        gameworld.add_component(piece_of_jewellery, items.RenderItem(istrue=True))
        gameworld.add_component(piece_of_jewellery, items.JewelleryGemstone(name=jewellery['gemstone']))
        if jewellery['body_location'] == 'neck':
            gameworld.add_component(piece_of_jewellery, items.JewelleryBodyLocation(fingers=False, neck=True, ears=False))

        if jewellery['body_location'] == 'fingers':
            gameworld.add_component(piece_of_jewellery,
                                    items.JewelleryBodyLocation(fingers=True, neck=False, ears=False))

        if jewellery['body_location'] == 'ear':
            gameworld.add_component(piece_of_jewellery,
                                    items.JewelleryBodyLocation(fingers=False, neck=False, ears=True))

        gameworld.add_component(piece_of_jewellery, items.JewelleryStatBonus(statname=jewellery['attributes'][0]['attributename'], statbonus=jewellery['attributes'][0]['attributevalue']))
