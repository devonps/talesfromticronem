import tcod
import random
import textwrap

from loguru import logger
from components import weapons, mobiles
from newGame.ClassWeapons import WeaponClass
from utilities.mobileHelp import MobileUtilities
from newGame import constants
from utilities.jsonUtilities import read_json_file


class NewCharacter:

    def create(con, gameworld):
        player = generate_player_character(gameworld=gameworld)
        select_race(con=con, gameworld=gameworld, player=player)
        select_character_class(con=con, gameworld=gameworld, player=player)
        select_personality_choices(con=con, gameworld=gameworld, player=player)
        name_your_character(con=con, gameworld=gameworld, player=player)
        get_starting_equipment(con=con, gameworld=gameworld, player=player)

        return player


def generate_player_character(gameworld):
    """
    Creates a shell for the player character details to be populated with
    :param gameworld:
    :return:
    """

    logger.debug('Creating the player character entity')
    player = MobileUtilities.generate_base_mobile(gameworld)
    gameworld.add_component(player, mobiles.Describable())
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
    logger.info('Reading racial information')
    race_file = read_json_file(constants.JSONFILEPATH + 'races.json')

    tcod.console_print_frame(con, x=10, y=5, w=80, h=50, clear=False, flag=tcod.BKGND_DEFAULT, fmt='Select Race')

    race_x = 12
    race_y = 10
    flavour_x = 20
    flavour_y = race_y - 1

    for race in race_file['races']:
        race_name = race['name']
        race_flavour = race['flavour']
        # print race details

        tcod.console_print(con, race_x, race_y, race_name)
        my_wrap = textwrap.TextWrapper(width=50)
        new_flavour_lines = my_wrap.wrap(text=race_flavour)

        for line in new_flavour_lines:
            tcod.console_print(con, flavour_x, flavour_y, line)
            flavour_y += 1

        tcod.console_put_char_ex(con, 10, flavour_y + 1, chr(195), tcod.yellow, tcod.black)
        tcod.console_hline(con, 11, flavour_y + 1, 78, tcod.BKGND_DEFAULT)
        tcod.console_put_char_ex(con, 89, flavour_y + 1, chr(180), tcod.yellow, tcod.black)

        flavour_y += 3
        race_y = flavour_y + 1

    tcod.console_blit(con, 0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, 0, 0, 0)
    dummy = True

    key = tcod.Key()
    mouse = tcod.Mouse()

    while dummy:
        tcod.sys_check_for_event(tcod.EVENT_KEY, key, mouse)

        tcod.console_flush()

        key = tcod.console_check_for_keypress()
        if key.vk == tcod.KEY_ENTER:
            dummy = False
    tcod.console_clear(con)

    gameworld.add_component(player, mobiles.Race(race='human'))


def select_character_class(con, gameworld, player):
    logger.info('Selecting character class')
    class_file = read_json_file(constants.JSONFILEPATH + 'classes.json')

    tcod.console_print_frame(con, x=10, y=5, w=80, h=50, clear=False, flag=tcod.BKGND_DEFAULT, fmt='Select Class')

    class_x = 12
    class_y = 10
    flavour_x = 25
    flavour_y = class_y - 1

    for pclass in class_file['classes']:
        class_name = pclass['name']
        class_flavour = pclass['flavour']
        # print race details

        tcod.console_print(con, class_x, class_y, class_name)
        my_wrap = textwrap.TextWrapper(width=50)
        new_flavour_lines = my_wrap.wrap(text=class_flavour)

        for line in new_flavour_lines:
            tcod.console_print(con, flavour_x, flavour_y, line)
            flavour_y += 1

        tcod.console_put_char_ex(con, 10, flavour_y + 1, chr(195), tcod.yellow, tcod.black)
        tcod.console_hline(con, 11, flavour_y + 1, 78, tcod.BKGND_DEFAULT)
        tcod.console_put_char_ex(con, 89, flavour_y + 1, chr(180), tcod.yellow, tcod.black)

        flavour_y += 3
        class_y = flavour_y + 1

    tcod.console_blit(con, 0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, 0, 0, 0)
    dummy = True

    key = tcod.Key()
    mouse = tcod.Mouse()

    while dummy:
        tcod.sys_check_for_event(tcod.EVENT_KEY, key, mouse)

        tcod.console_flush()

        key = tcod.console_check_for_keypress()
        if key.vk == tcod.KEY_ENTER:
            dummy = False
    tcod.console_clear(con)

    gameworld.add_component(player, mobiles.CharacterClass(label='necromancer'))


def select_profession_background(con, gameworld, player):
    # The profession-oriented question affects a character's starting armor
    player_class_component = gameworld.component_for_entity(player, mobiles.CharacterClass)

    # different options presented to player based on their chosen class


def select_personality_choices(con, gameworld, player):
    logger.info('Selecting character personality choices')
    # The personality-oriented question affects the conversational options that NPCs provide.
    # there will be 3 options: charm, dignity, ferocity

    gameworld.add_component(player, mobiles.Describable(personality='charm'))


def name_your_character(con, gameworld, player):
    logger.info('Naming the character')
    gameworld.add_component(player, mobiles.Name(first='Steve', suffix='none'))


def get_starting_equipment(con, gameworld, player):
    logger.info('Selecting starting equipment')

    # create starting armour
    logger.info('creating some armour for the player')
    # create starting jewellery
    logger.info('creating some basic jewellery for the player')
    # create starting weapons
    logger.info('creating a weapon for the player')
    class_component = gameworld.component_for_entity(player, mobiles.CharacterClass)
    # create a new weapon for the player
    weapon = WeaponClass.create_weapon(gameworld, 'sword')
    weapon_type = gameworld.component_for_entity(weapon, weapons.Name)
    # parameters are: gameworld, weapon object, weapon type as a string, mobile class
    logger.info('Loading that weapon with the necessary spells')
    WeaponClass.load_weapon_with_spells(gameworld, weapon, weapon_type.label, class_component.label)

    # equip wizard with weapon
    logger.info('Equipping player with that loaded weapon')
    MobileUtilities.equip_weapon(gameworld, player, weapon, 'main')

    logger.debug('Player is ready to rock and roll!')

