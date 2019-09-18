import random


from loguru import logger
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


def setup_gameworld(game_config):

    # world seed generation
    world_seed = generate_world_seed(game_config)
    store_world_seed(game_config, world_seed)


def generate_world_seed(game_config):

    player_seed = configUtilities.get_config_value_as_string(configfile=game_config, section='pcg', parameter='PLAYER_SEED')

    if player_seed != '':
        world_seed = PCG32Generator.convert_string_to_integer(player_seed)
        logger.info('Using player provided seed for world seed {}', player_seed)
    else:
        world_seed = random.getrandbits(30)
        logger.info('No player seed, using large random number for world seed {}', world_seed)

    return world_seed


def store_world_seed(game_config, world_seed):
    action_file = configUtilities.get_config_value_as_string(configfile=game_config, section='default', parameter='GAME_ACTIONS_FILE')
    fileobject = Externalfiles.start_new_game_replay_file(action_file)

    value = 'world_seed:' + str(world_seed)
    Externalfiles.write_to_existing_file(action_file, value)
    Externalfiles.close_existing_file(fileobject)


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


def generate_spells(gameworld, game_config, spell_file, player_class):

    spellsfile = spell_file.upper() + '_SPELLSFILE'

    spell_file_path = configUtilities.get_config_value_as_string(configfile=game_config, section='default', parameter=spellsfile)
    spell_file = read_json_file(spell_file_path)

    logger.debug('Creating spells as entities')
    for spell in spell_file['spells']:
        thisspell = world.get_next_entity_id(gameworld=gameworld)
        gameworld.add_component(thisspell, spells.Name(spell['name']))
        logger.info('Spell name {}', spell['name'])
        gameworld.add_component(thisspell, spells.Description(spell['description']))
        gameworld.add_component(thisspell, spells.ShortDescription(spell['short_description']))
        gameworld.add_component(thisspell, spells.CastTime(spell['turns_to_cast']))
        gameworld.add_component(thisspell, spells.CoolDown(spell['cool_down']))
        gameworld.add_component(thisspell, spells.ClassName(player_class))
        if spell['type_of_spell'] == 'combat':
            gameworld.add_component(thisspell, spells.WeaponType(spell['weapon_type']))
            gameworld.add_component(thisspell, spells.WeaponSlot(spell['weapon_slot']))
            gameworld.add_component(thisspell, spells.MaxTargets(spell['max_targets']))
            spell_range_in_file = spell['spell_range']
            spell_range = configUtilities.get_config_value_as_integer(configfile=game_config, section='spells',
                                                                     parameter=spell_range_in_file.upper())
            gameworld.add_component(thisspell, spells.MaxRange(spell_range))
            gameworld.add_component(thisspell, spells.DamageDuration(spell['damage_duration']))
            gameworld.add_component(thisspell, spells.DamageCoefficient(spell['damage_coef']))
            gameworld.add_component(thisspell, spells.GroundTargeted(spell['ground_targeted']))
            if spell['aoe'] == 'True':
                gameworld.add_component(thisspell, spells.AreaOfEffect(spell['aoe']))
                gameworld.add_component(thisspell, spells.AreaOfEffectSize(spell['aoe_size']))

        if spell['type_of_spell'] == 'heal':
            spell_heal_file = spell['heal_duration']
            spell_heal = configUtilities.get_config_value_as_integer(configfile=game_config, section='spells',
                                                                     parameter='SPELL_HEAL_'+spell_heal_file.upper())
            gameworld.add_component(thisspell, spells.HealingDuration(spell_heal))
            gameworld.add_component(thisspell, spells.HealingCoef(float(spell['heal_coef'])))

        if spell['type_of_spell'] == 'utility':
            gameworld.add_component(thisspell, spells.ItemLocation(spell['location']))
            gameworld.add_component(thisspell, spells.ItemType(spell['item_type']))

        effects = spell['effects']
        process_status_effect(gameworld, thisspell, spell['name'], effects, game_config)


