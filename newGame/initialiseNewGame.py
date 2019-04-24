import esper
import random


from loguru import logger
from newGame.newCharacter import NewCharacter
from newGame.Items import ItemManager
from components import spells
from components.addStatusEffects import process_status_effect

from utilities.jsonUtilities import read_json_file
from utilities.randomNumberGenerator import PCG32Generator
from utilities.externalfileutilities import Externalfiles
from utilities import world
from utilities import configUtilities

from processors.render import RenderConsole
from processors.move_entities import MoveEntities
from processors.updateEntities import UpdateEntitiesProcessor
from mapRelated.fov import FieldOfView
from mapRelated.gameMap import GameMap


def setup_game(game_config):

    # world seed generation
    generate_world_seed(game_config)


def create_and_place_world_entities(gameworld, game_map, game_config):
    # create entities for game world
    generate_spells(gameworld, game_config)
    generate_items_and_place_them(gameworld, game_map, game_config)
    generate_monsters_and_place_them(gameworld)


def generate_world_seed(game_config):

    player_seed = configUtilities.get_config_value_as_string(configfile=game_config, section='pcg', parameter='PLAYER_SEED')

    if player_seed != '':
        world_seed = PCG32Generator.convert_string_to_integer(player_seed)
        logger.info('Using player provided seed for world seed {}', player_seed)
    else:
        world_seed = random.getrandbits(30)
        logger.info('No player seed, using large random number for world seed {}', world_seed)
    value = 'world_seed:' + str(world_seed)
    action_file = configUtilities.get_config_value_as_string(configfile=game_config, section='default', parameter='GAME_ACTIONS_FILE')

    Externalfiles.write_to_existing_file(action_file, value)


def create_new_character(con, gameworld, game_config):
    player, spell_bar = NewCharacter.create(con=con, gameworld=gameworld, game_config=game_config)
    return player, spell_bar


def initialise_game_map(con, gameworld, player, spell_bar, message_log, game_config):

    map_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='game', parameter='MAP_WIDTH')
    map_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='game', parameter='MAP_HEIGHT')
    max_rooms_per_level = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon', parameter='DNG_MAX_ROOMS')
    room_min = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon', parameter='DNG_ROOM_MIN_SIZE')
    room_max = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon', parameter='DNG_ROOM_MAX_SIZE')

    # create game map
    game_map = GameMap(mapwidth=map_width, mapheight=map_height)
    game_map.make_map(
        max_rooms=max_rooms_per_level,
        room_min_size=room_min,
        room_max_size=room_max,
        map_width=map_width,
        map_height=map_height,
        gameworld=gameworld,
        player=player,
        game_config=game_config)

    # logger.info("Map Generated in %s" % (str(secondsToText(time() - start_time))))

    fov_compute = True

    fov = FieldOfView(game_map)

    render_console_process = RenderConsole(con=con, game_map=game_map, gameworld=gameworld, fov_compute=fov_compute, fov_object=fov, spell_bar=spell_bar, message_log=message_log )
    move_entities_processor = MoveEntities(gameworld=gameworld, game_map=game_map)
    update_entities_processor = UpdateEntitiesProcessor(gameworld=gameworld)
    gameworld.add_processor(render_console_process)
    gameworld.add_processor(move_entities_processor)
    gameworld.add_processor(update_entities_processor)

    return game_map


# create esper world (enemies, items, spells, etc)
def create_game_world():
    return esper.World()


def generate_spells(gameworld, game_config):

    json_file_path = configUtilities.get_config_value_as_string(configfile=game_config, section='default', parameter='JSONFILEPATH')
    spell_file = read_json_file(json_file_path + 'spells.json')

    logger.debug('Creating spells as entities')
    for spell in spell_file['spells']:
        thisspell = world.get_next_entity_id(gameworld=gameworld)
        gameworld.add_component(thisspell, spells.Name(spell['name']))
        gameworld.add_component(thisspell, spells.Description(spell['description']))
        gameworld.add_component(thisspell, spells.WeaponType(spell['weapon_type']))
        gameworld.add_component(thisspell, spells.ClassName(spell['class']))
        gameworld.add_component(thisspell, spells.CastTime(spell['cast_time']))
        gameworld.add_component(thisspell, spells.CoolDown(spell['cool_down']))
        gameworld.add_component(thisspell, spells.LivesFor(spell['lives_for']))
        gameworld.add_component(thisspell, spells.WeaponSlot(spell['weapon_slot']))
        gameworld.add_component(thisspell, spells.MaxTargets(spell['max_targets']))
        gameworld.add_component(thisspell, spells.GroundTargeted(spell['ground_targeted']))
        gameworld.add_component(thisspell, spells.MaxRange(spell['max_range']))
        gameworld.add_component(thisspell, spells.AreaOfEffect(spell['aoe']))
        gameworld.add_component(thisspell, spells.AreaOfEffectSize(spell['aoe_size']))
        effects = spell['effects']
        process_status_effect(gameworld, thisspell, spell['name'], effects)


def generate_monsters_and_place_them(gameworld):
    logger.debug('Creating monsters as entities')

    # create the mobile including its class:
    # determine it's weapons & armour based on its class
    # create each weapon and load spells to that weapon
    # create any armour
    # determine/calculate its starting stats based on weapons, armour, and class


def generate_items_and_place_them(gameworld, game_map, game_config):
    logger.debug('Creating items as entities - for testing purposes only')

    # generate weapons
    new_weapon = ItemManager.create_weapon(gameworld=gameworld, weapon_type='sword', game_config=game_config)
    has_item_been_placed = ItemManager.place_item_in_dungeon(gameworld=gameworld, item_to_be_placed=new_weapon, game_map=game_map, game_config=game_config)
    logger.info('Has weapon been placed :{}', has_item_been_placed)
    # generate jewellery
    new_piece_of_jewellery = ItemManager.create_jewellery(
        gameworld=gameworld,
        bodylocation='neck',
        e_setting='copper',
        e_hook='copper',
        e_activator='Garnet', game_config=game_config)
    has_item_been_placed = ItemManager.place_item_in_dungeon(gameworld=gameworld, item_to_be_placed=new_piece_of_jewellery, game_map=game_map, game_config=game_config)
    logger.info('Has jewellery been placed :{}', has_item_been_placed)
    # generate jewellery
    new_piece_of_jewellery = ItemManager.create_jewellery(
        gameworld=gameworld,
        bodylocation='ear',
        e_setting='copper',
        e_hook='copper',
        e_activator='Garnet', game_config=game_config)
    has_item_been_placed = ItemManager.place_item_in_dungeon(gameworld=gameworld,
                                                             item_to_be_placed=new_piece_of_jewellery,
                                                             game_map=game_map, game_config=game_config)
    logger.info('Has jewellery been placed :{}', has_item_been_placed)
    # generate jewellery
    new_piece_of_jewellery = ItemManager.create_jewellery(
        gameworld=gameworld,
        bodylocation='ear',
        e_setting='copper',
        e_hook='copper',
        e_activator='Pearl', game_config=game_config)
    has_item_been_placed = ItemManager.place_item_in_dungeon(gameworld=gameworld,
                                                             item_to_be_placed=new_piece_of_jewellery,
                                                             game_map=game_map, game_config=game_config)
    logger.info('Has jewellery been placed :{}', has_item_been_placed)
    # generate jewellery
    new_piece_of_jewellery = ItemManager.create_jewellery(
        gameworld=gameworld,
        bodylocation='neck',
        e_setting='copper',
        e_hook='copper',
        e_activator='Amber', game_config=game_config)
    has_item_been_placed = ItemManager.place_item_in_dungeon(gameworld=gameworld,
                                                             item_to_be_placed=new_piece_of_jewellery,
                                                             game_map=game_map, game_config=game_config)
    logger.info('Has jewellery been placed :{}', has_item_been_placed)
    # generate jewellery
    new_piece_of_jewellery = ItemManager.create_jewellery(
        gameworld=gameworld,
        bodylocation='ear',
        e_setting='copper',
        e_hook='copper',
        e_activator='Turquoise', game_config=game_config)
    has_item_been_placed = ItemManager.place_item_in_dungeon(gameworld=gameworld,
                                                             item_to_be_placed=new_piece_of_jewellery,
                                                             game_map=game_map, game_config=game_config)
    logger.info('Has jewellery been placed :{}', has_item_been_placed)

    # generate armour
    new_piece_of_armour = ItemManager.create_piece_of_armour(
        gameworld=gameworld,
        bodylocation='legs',
        quality='basic',
        setname='Apprentice',
        prefix='',
        level=0,
        majorname='',
        majorbonus=0,
        minoronename='',
        minoronebonus=0, game_config=game_config)
    has_item_been_placed = ItemManager.place_item_in_dungeon(gameworld=gameworld, item_to_be_placed=new_piece_of_armour, game_map=game_map, game_config=game_config)
    logger.info('Has armour been placed :{}', has_item_been_placed)

# generate armour
    new_piece_of_armour = ItemManager.create_piece_of_armour(
        gameworld=gameworld,
        bodylocation='chest',
        quality='basic',
        setname='Apprentice',
        prefix='',
        level=0,
        majorname='',
        majorbonus=0,
        minoronename='',
        minoronebonus=0, game_config=game_config)
    has_item_been_placed = ItemManager.place_item_in_dungeon(gameworld=gameworld, item_to_be_placed=new_piece_of_armour, game_map=game_map, game_config=game_config)
    logger.info('Has armour been placed :{}', has_item_been_placed)
# generate armour
    new_piece_of_armour = ItemManager.create_piece_of_armour(
        gameworld=gameworld,
        bodylocation='feet',
        quality='basic',
        setname='Apprentice',
        prefix='',
        level=0,
        majorname='',
        majorbonus=0,
        minoronename='',
        minoronebonus=0, game_config=game_config)
    has_item_been_placed = ItemManager.place_item_in_dungeon(gameworld=gameworld, item_to_be_placed=new_piece_of_armour, game_map=game_map, game_config=game_config)
    logger.info('Has armour been placed :{}', has_item_been_placed)
# generate armour
    new_piece_of_armour = ItemManager.create_piece_of_armour(
        gameworld=gameworld,
        bodylocation='hands',
        quality='basic',
        setname='Apprentice',
        prefix='',
        level=0,
        majorname='',
        majorbonus=0,
        minoronename='',
        minoronebonus=0, game_config=game_config)
    has_item_been_placed = ItemManager.place_item_in_dungeon(gameworld=gameworld, item_to_be_placed=new_piece_of_armour, game_map=game_map, game_config=game_config)
    logger.info('Has armour been placed :{}', has_item_been_placed)
# generate armour
    new_piece_of_armour = ItemManager.create_piece_of_armour(
        gameworld=gameworld,
        bodylocation='hands',
        quality='basic',
        setname='Apprentice',
        prefix='',
        level=0,
        majorname='',
        majorbonus=0,
        minoronename='',
        minoronebonus=0, game_config=game_config)
    has_item_been_placed = ItemManager.place_item_in_dungeon(gameworld=gameworld, item_to_be_placed=new_piece_of_armour, game_map=game_map, game_config=game_config)
    logger.info('Has armour been placed :{}', has_item_been_placed)
# generate armour
    new_piece_of_armour = ItemManager.create_piece_of_armour(
        gameworld=gameworld,
        bodylocation='head',
        quality='basic',
        setname='Apprentice',
        prefix='',
        level=0,
        majorname='',
        majorbonus=0,
        minoronename='',
        minoronebonus=0, game_config=game_config)
    has_item_been_placed = ItemManager.place_item_in_dungeon(gameworld=gameworld, item_to_be_placed=new_piece_of_armour, game_map=game_map, game_config=game_config)
    logger.info('Has armour been placed :{}', has_item_been_placed)
