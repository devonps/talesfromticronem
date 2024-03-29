import random

from loguru import logger
from components import items
from newGame import CreateSpells, Items
from utilities import configUtilities, jsonUtilities, world, itemsHelp, randomNumberGenerator, externalfileutilities
from newGame.Entities import NewEntity
from static.data import constants

def create_world():
    gameconfig = configUtilities.load_config()
    # Esper initialisation
    gameworld = world.create_game_world()
    setup_gameworld(game_config=gameconfig)
    CreateSpells.AsEntities.generate(gameworld=gameworld)
    create_jewellery_entities(gameworld=gameworld)
    # create the scorekeeper
    NewEntity.create_scorekeeper_entity(gameworld=gameworld)

    return gameworld


def setup_gameworld(game_config):
    # world seed generation
    world_seed = generate_world_seed(game_config)
    store_world_seed(game_config, world_seed)


def generate_world_seed(game_config):
    player_seed = configUtilities.get_config_value_as_string(configfile=game_config, section='pcg',
                                                             parameter='PLAYER_SEED')

    if player_seed != '':
        world_seed = randomNumberGenerator.PCG32Generator.convert_string_to_integer(value=player_seed)
        logger.info('Using player provided seed for world seed {}', player_seed)
    else:
        world_seed = random.getrandbits(30)
        logger.info('No player seed, using large random number for world seed {}', world_seed)

    return world_seed


def store_world_seed(game_config, world_seed):
    action_file = constants.FILE_GAME_ACTIONS_FILE

    externalfileutilities.Externalfiles.new_file(filename=action_file)
    value = 'world_seed:' + str(world_seed)
    externalfileutilities.Externalfiles.write_to_existing_file(action_file, value)
    f = open(action_file, 'r')
    f.close()


def create_jewellery_entities(gameworld):
    jewellery_file_path = constants.FILE_JEWELLERYFILE

    jewellery_file = jsonUtilities.read_json_file(jewellery_file_path)

    for jewellery in jewellery_file['jewellery']:
        piece_of_jewellery = Items.ItemManager.create_base_item(gameworld=gameworld)
        itemsHelp.ItemUtilities.set_type_of_item(gameworld=gameworld, entity_id=piece_of_jewellery, value='jewellery')
        gameworld.add_component(piece_of_jewellery, items.Material(texture=jewellery['material']))
        itemsHelp.ItemUtilities.set_item_name(gameworld=gameworld, entity_id=piece_of_jewellery, value=jewellery['name'])
        itemsHelp.ItemUtilities.set_item_description(gameworld=gameworld, entity_id=piece_of_jewellery, value=jewellery['description'])
        itemsHelp.ItemUtilities.set_item_glyph(gameworld=gameworld, entity_id=piece_of_jewellery, value=jewellery['glyph'])
        itemsHelp.ItemUtilities.set_item_foreground_colour(gameworld=gameworld, entity_id=piece_of_jewellery,
                                                 value=jewellery['fg'])
        itemsHelp.ItemUtilities.set_item_background_colour(gameworld=gameworld, entity_id=piece_of_jewellery,
                                                 value=jewellery['bg'])

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
