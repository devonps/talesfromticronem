
# not sure what I'm going to do with this file
# Originally it held the different constants my game needs, but they've been moved to a different file

# create spells as entities

import esper

from utilities.jsonUtilities import read_json_file
from loguru import logger
from newGame import constants, ClassWeapons as c
from components import spells, weapons
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

    # create the monbile including its class
    # determine it's weapons & armour based on its class
    # create each weapon and load spells to that weapon
    # create any armour
    # determine/calculate its starting stats based on weapons, armour, and class


def generate_items(gameworld):
    logger.debug('Creating items as entities - for testing purposes only')
    generate_weapons(gameworld)

    # assign spells to weapons


def generate_weapons(gameworld):
    staff = c.WeaponClass.create_staff(gameworld)
    logger.info('Staff created with entity id of {}', staff)
    load_weapon_with_spells(gameworld, staff, 'staff', 'necromancer')
    # TODO assign spells to weapons
    # load the staff with necro spells


def load_weapon_with_spells(gameworld, weapon_obj, weapon_type, mobile_class):
    # get list of spells for that weapon and mobile class
    for ent, (cl, wpn, weapon_slot) in gameworld.get_components(spells.ClassName, spells.WeaponType, spells.WeaponSlot):
        if (wpn.label == weapon_type) and (cl.label == mobile_class):
            if weapon_slot.slot == '1':
                logger.info('Spell {} added to weapon slot 1', ent)
                weapon_slot_component = gameworld.component_for_entity(weapon_obj, weapons.Spells)
                weapon_slot_component.slot_one = ent
            if weapon_slot.slot == '2':
                logger.info('Spell {} added to weapon slot 2', ent)
                weapon_slot_component = gameworld.component_for_entity(weapon_obj, weapons.Spells)
                weapon_slot_component.slot_two = ent
            if weapon_slot.slot == '3':
                logger.info('Spell {} added to weapon slot 3', ent)
                weapon_slot_component = gameworld.component_for_entity(weapon_obj, weapons.Spells)
                weapon_slot_component.slot_three = ent
            if weapon_slot.slot == '4':
                logger.info('Spell {} added to weapon slot 4', ent)
                weapon_slot_component = gameworld.component_for_entity(weapon_obj, weapons.Spells)
                weapon_slot_component.slot_four = ent
            if weapon_slot.slot == '5':
                logger.info('Spell {} added to weapon slot 5', ent)
                weapon_slot_component = gameworld.component_for_entity(weapon_obj, weapons.Spells)
                weapon_slot_component.slot_five = ent


def generate_player_character(gameworld):
    logger.debug('Creating the player character entity')
    player = gameworld.create_entity()
    logger.info('stored as entity {}', player)