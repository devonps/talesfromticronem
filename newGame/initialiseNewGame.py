
# not sure what I'm going to do with this file
# Originally it held the different constants my game needs, but they've been moved to a different file

# create spells as entities

import esper

from utilities.jsonUtilities import read_json_file
from loguru import logger
from newGame import constants
from components import spells
from components.addStatusEffects import process_status_effect


def setup_game():
    # read in JSON files - maybe
    # create Esper game world
    world = create_game_world()
    # create entities for game world
    generate_spells(world)
    generate_items(world)
    generate_monsters(world)
    generate_player_character(world)
    # create game map
    # place entities (enemies, items)

    return world


# create esper world (enemies, items, spells, etc)
def create_game_world():
    return esper.World()


def generate_spells(gameworld):
    spellFile = read_json_file(constants.JSONFILEPATH + 'spells.json')
    logger.debug('Creating spells as entities')
    for spell in spellFile['spells']:
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


def generate_items(gameworld):
    logger.debug('Creating items as entities')


def generate_player_character(gameworld):
    logger.debug('Creating the player character entity')
    player = gameworld.create_entity()
    logger.info('stored as entitiy {}', player)