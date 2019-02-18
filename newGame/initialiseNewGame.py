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
from utilities.jsonUtilities import read_json_file
from utilities.randomNumberGenerator import PCG32Generator
from utilities.externalfileutilities import Externalfiles
from map_objects.gameMap import GameMap
from processors.render import RenderConsole, RenderInventory, RenderPlayerCharacterScreen
from processors.move_entities import MoveEntities


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
    # dungeon_seed_stream = PCG32Generator(constants.WORLD_SEED, constants.PRNG_STREAM_DUNGEONS)

    game_map = GameMap(constants.MAP_WIDTH, constants.MAP_HEIGHT)
    # game_map.make_map(constants.MAX_ROOMS, constants.ROOM_MIN_SIZE, constants.ROOM_MAX_SIZE, constants.MAP_WIDTH,constants.MAP_HEIGHT, gameworld, player)
    # game_map.generate_bsp_map()
    # game_map.test_map()
    game_map.rogue_make_bsp_map()

    fov_compute = True
    # fov_map = GameMap.make_fov_map(game_map)

    fov_map = tcod.map_new(game_map.width, game_map.height)

    for y in range(game_map.height):
        for x in range(game_map.width):
            tcod.map_set_properties(fov_map, x, y, not game_map.tiles[x][y].transparent,
                                    not game_map.tiles[x][y].block_path)


    # place entities (enemies, items)

    render_console_process = RenderConsole(con=con, game_map=game_map, gameworld=gameworld, fov_compute=fov_compute, fov_map=fov_map, spell_bar=spell_bar, message_log=message_log )
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


def generate_weapons(gameworld):
    staff = WeaponClass.create_weapon(gameworld, 'staff')
    # parameters are: gameworld, weapon object, weapon type as a string, mobile class
    load_weapon_with_spells(gameworld, staff, 'staff', 'necromancer')

    focus = WeaponClass.create_weapon(gameworld, 'focus')
    load_weapon_with_spells(gameworld, focus, 'focus', 'necromancer')

    rod = WeaponClass.create_weapon(gameworld, 'rod')
    load_weapon_with_spells(gameworld, rod, 'rod', 'necromancer')

    sword = WeaponClass.create_weapon(gameworld, 'sword')
    load_weapon_with_spells(gameworld, sword, 'sword', 'necromancer')

    wand = WeaponClass.create_weapon(gameworld, 'wand')
    load_weapon_with_spells(gameworld, wand, 'wand', 'necromancer')
