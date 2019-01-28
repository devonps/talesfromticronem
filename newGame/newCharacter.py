import tcod
import random

from loguru import logger
from components import weapons, mobiles
from newGame.ClassWeapons import WeaponClass
from utilities.mobileHelp import MobileUtilities
from newGame import constants


class NewCharacter:

    def create(con, gameworld):
        player = generate_player_character(gameworld=gameworld)
        select_race(con=con, gameworld=gameworld, player=player)
        select_character_class(con=con, gameworld=gameworld, player=player)
        select_personality_choices(con=con, gameworld=gameworld)
        name_your_character(con=con, gameworld=gameworld, player=player)
        get_starting_equipment(con=con, gameworld=gameworld, player=player)

        return player


def generate_player_character(gameworld):
    logger.debug('Creating the player character entity')
    player = MobileUtilities.generate_base_mobile(gameworld)
    gameworld.add_component(player, mobiles.Describable(glyph='@', foreground=tcod.orange))
    gameworld.add_component(player, mobiles.AI(ailevel=constants.AI_LEVEL_PLAYER))
    gameworld.add_component(player, mobiles.Inventory())
    gameworld.add_component(player, mobiles.Armour())
    gameworld.add_component(player, mobiles.Jewellery())
    gameworld.add_component(player, mobiles.Equipped())
    gameworld.add_component(player, mobiles.Health(current=1, maximum=10))

    # add renderable component to player
    gameworld.add_component(player, mobiles.Renderable(is_visible=True))

    # give player a false starting position - just for testing
    gameworld.add_component(player, mobiles.Position(x=random.randrange(3, 55), y=random.randrange(5, 39)))

    logger.info('stored as entity {}', player)

    return player


def select_race(con, gameworld, player):
    logger.info('Selecting character race')
    gameworld.add_component(player, mobiles.Race(race='human'))


def select_character_class(con, gameworld, player):
    logger.info('Selecting character class')
    gameworld.add_component(player, mobiles.CharacterClass(label='necromancer'))


def select_personality_choices(con, gameworld):
    logger.info('Selecting character personality choices')


def name_your_character(con, gameworld, player):
    logger.info('Naming the character')
    gameworld.add_component(player, mobiles.Name(first='Steve', suffix='none'))


def get_starting_equipment(con, gameworld, player):
    logger.info('Selecting starting equipment')

    # create starting armour

    # create starting jewellery

    # create starting weapons
    class_component = gameworld.component_for_entity(player, mobiles.CharacterClass)
    # create a new weapon for the player
    weapon = WeaponClass.create_weapon(gameworld, 'sword')
    weapon_type = gameworld.component_for_entity(weapon, weapons.Name)
    # parameters are: gameworld, weapon object, weapon type as a string, mobile class
    WeaponClass.load_weapon_with_spells(gameworld, weapon, weapon_type.label, class_component.label)

    # equip wizard with weapon
    MobileUtilities.equip_weapon(gameworld, player, weapon, 'main')



