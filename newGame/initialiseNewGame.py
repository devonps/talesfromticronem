import esper
import random
import tcod

from loguru import logger
from newGame.ClassWeapons import WeaponClass
from newGame import constants
from newGame.newCharacter import NewCharacter
from newGame.game_messages import MessageLog, Message
from components import spells
from components.addStatusEffects import process_status_effect
from components import mobiles
from utilities.jsonUtilities import read_json_file
from utilities.randomNumberGenerator import PCG32Generator
from utilities.externalfileutilities import Externalfiles
from utilities.dateTimeUtilities import secondsToText
from mapRelated.gameMap import GameMap
from processors.render import RenderConsole, RenderInventory, RenderPlayerCharacterScreen
from processors.move_entities import MoveEntities
from mapRelated.dungeonGenerator import dungeonGenerator
from mapRelated.fov import FieldOfView
from time import time


def setup_game(con, gameworld):

    filehandle = Externalfiles.create_new_file(constants.GAME_ACTIONS_FILE)

    # world seed generation
    generate_world_seed()

    # create entities for game world
    generate_spells(gameworld)
    generate_items(gameworld)
    generate_monsters(gameworld)


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
    player, spell_bar = NewCharacter.create(con, gameworld)
    return player, spell_bar


def initialise_game_map(con, gameworld, player, spell_bar, message_log):
    # create game map
    dungeon_seed_stream = PCG32Generator(constants.WORLD_SEED, constants.PRNG_STREAM_DUNGEONS)

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

    # this isn't working as intended
    # d.generateBSPMap()
    game_map = d

    logger.info("Map Generated in %s" % (str(secondsToText(time() - start_time))))

    fov_compute = True

    fov = FieldOfView(game_map)

    # place entities (enemies, items)

    render_console_process = RenderConsole(con=con, game_map=game_map, gameworld=gameworld, fov_compute=fov_compute, fov_object=fov, spell_bar=spell_bar, message_log=message_log )
    render_inventory_screen = RenderInventory()
    render_character_screen = RenderPlayerCharacterScreen()
    move_entities_processor = MoveEntities(gameworld=gameworld, game_map=game_map)
    gameworld.add_processor(render_console_process)
    gameworld.add_processor(render_inventory_screen)
    gameworld.add_processor(render_character_screen)
    gameworld.add_processor(move_entities_processor)


# create esper world (enemies, items, spells, etc)
def create_game_world():
    return esper.World()


def generate_spells(gameworld):
    logger.debug('Creating spells as entities')
    spell_file = read_json_file(constants.JSONFILEPATH + 'spells.json')
    for spell in spell_file['spells']:
        myspell = gameworld.create_entity()
        gameworld.add_component(myspell, spells.Name(spell['name']))
        gameworld.add_component(myspell, spells.Description(spell['description']))
        gameworld.add_component(myspell, spells.WeaponType(spell['weapon_type']))
        gameworld.add_component(myspell, spells.ClassName(spell['class']))
        gameworld.add_component(myspell, spells.CastTime(spell['cast_time']))
        gameworld.add_component(myspell, spells.CoolDown(spell['cool_down']))
        gameworld.add_component(myspell, spells.LivesFor(spell['lives_for']))
        gameworld.add_component(myspell, spells.WeaponSlot(spell['weapon_slot']))
        gameworld.add_component(myspell, spells.MaxTargets(spell['max_targets']))
        gameworld.add_component(myspell, spells.GroundTargeted(spell['ground_targeted']))
        gameworld.add_component(myspell, spells.MaxRange(spell['max_range']))
        gameworld.add_component(myspell, spells.AreaOfEffect(spell['aoe']))
        gameworld.add_component(myspell, spells.AreaOfEffectSize(spell['aoe_size']))
        effects = spell['effects']
        process_status_effect(gameworld, myspell, spell['name'], effects)


def generate_monsters(gameworld):
    logger.debug('Creating monsters as entities')

    # create the mobile including its class:
    # determine it's weapons & armour based on its class
    # create each weapon and load spells to that weapon
    # create any armour
    # determine/calculate its starting stats based on weapons, armour, and class


def create_monster(gameworld):
    pass


def generate_items(gameworld):
    logger.debug('Creating items as entities - for testing purposes only')
    # generate_weapons(gameworld)

    # assign spells to weapons
