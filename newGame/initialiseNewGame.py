import esper
import random

from loguru import logger
from newGame.ClassWeapons import WeaponClass
from newGame import constants
from newGame.newCharacter import NewCharacter
from components import spells, weapons
from components.addStatusEffects import process_status_effect
from utilities.mobileHelp import MobileUtilities
from utilities.jsonUtilities import read_json_file
from map_objects.gameMap import GameMap
from processors.render import RenderConsole, RenderInventory, RenderPlayerCharacterScreen, RenderSpellBar
from processors.move_entities import MoveEntities


def setup_game(con, gameworld):

    # create entities for game world
    generate_spells(gameworld)
    generate_items(gameworld)
    generate_monsters(gameworld)


def create_new_character(con, gameworld):
    player, spell_bar = NewCharacter.create(con, gameworld)
    return player, spell_bar


def initialise_game_map(con, gameworld, player, spell_bar):
    # create game map
    game_map = GameMap(constants.VIEWPORT_WIDTH, constants.VIEWPORT_HEIGHT)
    game_map.make_map(constants.MAX_ROOMS, constants.ROOM_MIN_SIZE, constants.ROOM_MAX_SIZE, constants.MAP_WIDTH,
                      constants.MAP_HEIGHT, gameworld, player)
    # place entities (enemies, items)

    render_console_process = RenderConsole(con=con, game_map=game_map, gameworld=gameworld)
    render_inventory_screen = RenderInventory()
    render_character_screen = RenderPlayerCharacterScreen()
    move_entities_processor = MoveEntities(gameworld=gameworld, game_map=game_map)
    render_spell_bar_processor = RenderSpellBar(con=con, spell_bar=spell_bar, gameworld=gameworld)
    gameworld.add_processor(render_console_process)
    gameworld.add_processor(render_inventory_screen)
    gameworld.add_processor(render_character_screen)
    gameworld.add_processor(move_entities_processor)
    gameworld.add_processor(render_spell_bar_processor)


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


def create_wizard(gameworld):
    """
    This method creates an enemy type of Wizard - this represents the toughest opponent for the player.
    Wizards are created from the same playable classes the player can select.

    :param gameworld:
    :return wizard:
    """
    logger.debug('Creating new wizard')
    # generate base mobile
    wizard = MobileUtilities.generate_base_mobile(gameworld)
    # add wizard specific components - this selection will become more complex over time

    # determine the type of wizard, i.e. it's character class
    characterclass = random.choice(constants.playable_classes)
    gameworld.add_component(wizard, mobiles.CharacterClass(label=characterclass))
    class_component = gameworld.component_for_entity(wizard, mobiles.CharacterClass)

    # add race to Wizard - again better 'selection' techniques need to be created
    gameworld.add_component(wizard, mobiles.Race(race='human'))

    # add renderable component to wizard
    gameworld.add_component(wizard, mobiles.Renderable(is_visible=True))

    # add AI component
    gameworld.add_component(wizard, mobiles.AI(ailevel=constants.AI_LEVEL_WIZARD))

    # make the wizard appear
    gameworld.add_component(wizard, mobiles.Position(x=random.randrange(3,55), y=random.randrange(5,39)))

    gameworld.add_component(wizard, mobiles.Describable(glyph='@', foreground=tcod.white))

    # create inventory for wizard
    gameworld.add_component(wizard, mobiles.Inventory())

    # assign starting weapon + spells

    # will this wizard use a 2-handed weapon or not!

    # create a new weapon for the wizard
    sword = WeaponClass.create_weapon(gameworld, 'sword')
    # get the weapon type
    weapon_type = gameworld.component_for_entity(sword, weapons.Name)
    # parameters are: gameworld, weapon object, weapon type as a string, mobile class
    WeaponClass.load_weapon_with_spells(gameworld, sword, weapon_type.label, class_component.label)

    # add the equipable component
    gameworld.add_component(wizard, mobiles.Equipped())
    # equip wizard with weapon
    MobileUtilities.equip_weapon(gameworld, wizard, sword, 'main')

    # create a 2nd weapon for the wizard
    focus = WeaponClass.create_weapon(gameworld, 'focus')
    # get the weapon type
    weapon_type = gameworld.component_for_entity(focus, weapons.Name)
    # parameters are: gameworld, weapon object, weapon type as a string, mobile class
    load_weapon_with_spells(gameworld, focus, weapon_type.label, class_component.label)

    # equip wizard with weapon
    MobileUtilities.equip_weapon(gameworld, wizard, focus, 'off')

    # add the armour component
    gameworld.add_component(wizard, mobiles.Armour())

    # add the jewellery component
    gameworld.add_component(wizard, mobiles.Jewellery())

    # calculate starting health
    gameworld.add_component(wizard, mobiles.Health())

    return wizard


def create_demon(gameworld):
    logger.debug('Creating new demon')
    # generate base mobile
    demon = generate_base_mobile(gameworld)
    # add demon specific components - this selection will become more complex over time

    # determine the type of demon, i.e. it's character class
    characterclass = random.choice(constants.demon_classes)
    gameworld.add_component(demon, mobiles.CharacterClass(label=characterclass))

    class_component = gameworld.component_for_entity(demon, mobiles.CharacterClass)

    # add race to Demon - again better 'selection' techniques need to be created
    gameworld.add_component(demon, mobiles.Race(race='demon'))

    # create a new weapon for the demon
    weapon = WeaponClass.create_weapon(gameworld, random.choice(constants.demon_weapons))
    # get the weapon type
    weapon_type = gameworld.component_for_entity(weapon, weapons.Name)
    # parameters are: gameworld, weapon object, weapon type as a string, mobile class
    load_weapon_with_spells(gameworld, weapon, weapon_type.label, class_component.label)

    # add the equipable component
    gameworld.add_component(demon, mobiles.Equipped())
    # equip demon with weapon
    MobileUtilities.equip_weapon(gameworld, demon, weapon, 'main')

    # add the armour component
    gameworld.add_component(demon, mobiles.Armour())

    # calculate starting health
    gameworld.add_component(demon, mobiles.Health())

    # add renderable component to demon
    gameworld.add_component(demon, mobiles.Renderable)

    # add AI component
    gameworld.add_component(demon, mobiles.AI(ailevel=constants.AI_LEVEL_DEMON))

    return demon


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
