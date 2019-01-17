
# not sure what I'm going to do with this file
# Originally it held the different constants my game needs, but they've been moved to a different file

# create spells as entities

import esper

from utilities.jsonUtilities import read_json_file
from loguru import logger
from newGame import constants
from newGame.ClassWeapons import WeaponClass
from components import spells, weapons, mobiles
from components.addStatusEffects import process_status_effect


def setup_game():
    # read in JSON files - maybe
    # create Esper game world
    world = create_game_world()
    # create entities for game world
    generate_spells(world)
    generate_items(world)
    generate_monsters(world)
#    generate_player_character(world)
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

    # create the monbile including its class15:
    # determine it's weapons & armour based on its class
    # create each weapon and load spells to that weapon
    # create any armour
    # determine/calculate its starting stats based on weapons, armour, and class


def create_wizard(gameworld):
    pass


def create_demon(gameworld):
    pass


def create_monster(gameworld):
    pass


def generate_items(gameworld):
    logger.debug('Creating items as entities - for testing purposes only')
    generate_weapons(gameworld)

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


def generate_player_character(gameworld, characterclass):
    logger.debug('Creating the player character entity')
    player = generate_base_mobile(gameworld)
    gameworld.add_component(player, mobiles.Name(first='Steve', suffix='none'))
    gameworld.add_component(player, mobiles.Describable())
    gameworld.add_component(player, mobiles.CharacterClass(label=characterclass))
    gameworld.add_component(player, mobiles.AI(ailevel=constants.AI_LEVEL_PLAYER))
    gameworld.add_component(player, mobiles.Health(current=1, maximum=10))
    gameworld.add_component(player, mobiles.Inventory())
    gameworld.add_component(player, mobiles.Armour())
    gameworld.add_component(player, mobiles.Jewellery())
    gameworld.add_component(player, mobiles.Equipped())

    logger.info('stored as entity {}', player)

    return player


def generate_base_mobile(gameworld):
    logger.info('Creating base mobile entity')
    mobile = gameworld.create_entity()
    gameworld.add_component(mobile, mobiles.Name(first='', suffix=''))
    gameworld.add_component(mobile, mobiles.Describable())
    gameworld.add_component(mobile, mobiles.CharacterClass())
    gameworld.add_component(mobile, mobiles.AI(ailevel=constants.AI_LEVEL_NONE))
    gameworld.add_component(mobile, mobiles.Health())
    gameworld.add_component(mobile, mobiles.Inventory())
    gameworld.add_component(mobile, mobiles.Armour())
    gameworld.add_component(mobile, mobiles.Jewellery())
    gameworld.add_component(mobile, mobiles.Equipped())

    return mobile
