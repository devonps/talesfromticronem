import esper
import random


from loguru import logger
from newGame import constants
from newGame.newCharacter import NewCharacter
from newGame.Items import ItemManager
from components import spells
from components.addStatusEffects import process_status_effect

from utilities.jsonUtilities import read_json_file
from utilities.randomNumberGenerator import PCG32Generator
from utilities.externalfileutilities import Externalfiles
from utilities.dateTimeUtilities import secondsToText
from utilities import world

from processors.render import RenderConsole
from processors.move_entities import MoveEntities
from processors.updateEntities import UpdateEntitiesProcessor
from mapRelated.dungeonGenerator import dungeonGenerator
from mapRelated.fov import FieldOfView
from time import time


def setup_game(gameworld):

    filehandle = Externalfiles.create_new_file(constants.GAME_ACTIONS_FILE)

    # world seed generation
    generate_world_seed()


def create_and_place_world_entities(gameworld, game_map):
    # create entities for game world
    generate_spells(gameworld)
    generate_items_and_place_them(gameworld, game_map)
    generate_monsters_and_place_them(gameworld)


def generate_world_seed():

    if constants.PLAYER_SEED != '':
        constants.WORLD_SEED = PCG32Generator.convert_string_to_integer(constants.PLAYER_SEED)
        # constants.WORLD_SEED = tcod.random_new_from_seed(seed=constants.PLAYER_SEED, algo=tcod.RNG_CMWC)
        logger.info('Using player provided seed for world seed {}',constants.PLAYER_SEED)
    else:
        constants.WORLD_SEED = random.getrandbits(30)
        logger.info('No player seed, using large random number for world seed {}', constants.WORLD_SEED)
    value = 'world_seed:' + str(constants.WORLD_SEED)
    Externalfiles.write_to_existing_file(constants.GAME_ACTIONS_FILE, value)

    # Test Code
    # dung_rooms = PCG32Generator(constants.WORLD_SEED, constants.PRNG_STREAM_DUNGEONS)
    #
    # constants.ROOM_MIN_SIZE, constants.ROOM_MAX_SIZE
    # for n in range(10):
    #     # nxt = dung_rooms.get_next_uint(constants.ROOM_MAX_SIZE)
    #     nxt = dung_rooms.get_next_number_in_range(constants.ROOM_MIN_SIZE, constants.ROOM_MAX_SIZE)
    #     logger.info('Random No {}. is {} range is between {} and {}', n, nxt, constants.ROOM_MIN_SIZE, constants.ROOM_MAX_SIZE)


def create_new_character(con, gameworld):
    player, spell_bar = NewCharacter.create(con=con, gameworld=gameworld)
    return player, spell_bar


def initialise_game_map(con, gameworld, player, spell_bar, message_log):
    # create game map

    dungeon_seed_stream = PCG32Generator(constants.WORLD_SEED, constants.PRNG_STREAM_DUNGEONS)
    # myd = MyGenerateDungeon(height=40, width=80, rand_gen_object=dungeon_seed_stream, gameworld=gameworld)
    # myd.make_floors()



    # define map size (y,x) max tiles to use in direction
    levelSize = [40, 80]
    # create class instance; ALWAYS required
    d = dungeonGenerator(height=levelSize[0], width=levelSize[1], rand_gen_object=dungeon_seed_stream, gameworld=gameworld)
    start_time = time()
    d.placeRandomRooms(minRoomSize=5, maxRoomSize=15, roomStep=1, margin=1, attempts=2000)
    d.generateCorridors('l')
    d.connectAllRooms(0)
    d.pruneDeadends(50)

    # join unconnected areas
    unconnected = d.findUnconnectedAreas()
    d.joinUnconnectedAreas(unconnected)
    d.placeWalls()
    d.set_tiles()

    game_map = d

    logger.info("Map Generated in %s" % (str(secondsToText(time() - start_time))))

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


def generate_spells(gameworld):
    logger.debug('Creating spells as entities')
    spell_file = read_json_file(constants.JSONFILEPATH + 'spells.json')
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


def generate_items_and_place_them(gameworld, game_map):
    logger.debug('Creating items as entities - for testing purposes only')

    # generate weapons
    new_weapon = ItemManager.create_weapon(gameworld=gameworld, weapon_type='sword')
    has_item_been_placed = ItemManager.place_item_in_dungeon(gameworld=gameworld, item_to_be_placed=new_weapon, game_map=game_map)
    logger.info('Has item been placed :{}', has_item_been_placed)
    # generate jewellery
    # new_piece_of_jewellery = ItemManager.create_jewellery(
    #     gameworld=gameworld,
    #     bodylocation='neck',
    #     e_setting='copper',
    #     e_hook='copper',
    #     e_activator='Garnet')
    # ItemManager.place_item_in_dungeon(gameworld=gameworld, item_to_be_placed=new_piece_of_jewellery, game_map=game_map)
    # # generate armour
    # new_piece_of_armour = ItemManager.create_piece_of_armour(
    #     gameworld=gameworld,
    #     bodylocation='legs',
    #     quality='basic',
    #     setname='Apprentice',
    #     prefix='',
    #     level=0,
    #     majorname='',
    #     majorbonus=0,
    #     minoronename='',
    #     minoronebonus=0)
    # ItemManager.place_item_in_dungeon(gameworld=gameworld, item_to_be_placed=new_piece_of_armour, game_map=game_map)


