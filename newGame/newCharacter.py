import tcod
import random
import textwrap

from loguru import logger
from components import weapons, mobiles, armour
from newGame.ClassWeapons import WeaponClass
from utilities.mobileHelp import MobileUtilities
from newGame import constants
from utilities.jsonUtilities import read_json_file
from input_handler import handle_new_race, handle_new_class


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

    frame_x = 5
    frame_y = 4
    frame_w = 80
    flavour_x = 19
    flavour_y = frame_y + 1
    race_not_selected = True
    selected_race = 'human'

    key = tcod.Key()
    mouse = tcod.Mouse()

    while race_not_selected:

        posy = display_selection(con=con, filename=race_file, element='races', posx=frame_x + 1, posy=frame_y + 2,
                                 width=frame_w,
                                 flavour_x=flavour_x, flavour_y=flavour_y)

        tcod.console_print_frame(con, x=frame_x, y=frame_y - 2, w=frame_w, h=posy, clear=False, flag=tcod.BKGND_DEFAULT,
                                 fmt='Select Race')

        tcod.console_print_ex(con=con, x=20, y=posy + 3, flag=tcod.BKGND_NONE, alignment=tcod.LEFT,
                              fmt='Press letter to select')

        tcod.console_blit(con, 0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, 0, 0, 0)

        tcod.console_flush()
        tcod.sys_wait_for_event(tcod.EVENT_KEY_PRESS, key, mouse, True)
        selected_race = handle_new_race(key)
        if selected_race != '':
            race_not_selected = False

    tcod.console_clear(con)

    gameworld.add_component(player, mobiles.Race(race=selected_race))


def select_character_class(con, gameworld, player):
    logger.info('Selecting character class')
    class_file = read_json_file(constants.JSONFILEPATH + 'classes.json')

    frame_x = 5
    frame_y = 4
    frame_w = 80
    flavour_x = 24
    flavour_y = frame_y + 1

    class_not_selected = True
    selected_class = 'necromancer'

    key = tcod.Key()
    mouse = tcod.Mouse()

    while class_not_selected:
        posy = display_selection(con=con, filename=class_file, element='classes', posx=frame_x + 1, posy=frame_y + 2,
                                 width=frame_w,
                                 flavour_x=flavour_x, flavour_y=flavour_y)

        tcod.console_print_frame(con, x=frame_x, y=frame_y - 2, w=frame_w, h=posy, clear=False, flag=tcod.BKGND_DEFAULT,
                                 fmt='Select Class')

        tcod.console_print_ex(con=con, x=20, y=posy + 3, flag=tcod.BKGND_NONE, alignment=tcod.LEFT,
                              fmt='Arrows to highlight, enter to select')

        tcod.console_blit(con, 0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, 0, 0, 0)

        tcod.console_flush()
        tcod.sys_wait_for_event(tcod.EVENT_KEY_PRESS, key, mouse, True)
        selected_class = handle_new_class(key)
        if selected_class != '':
            class_not_selected = False
    tcod.console_clear(con)

    gameworld.add_component(player, mobiles.CharacterClass(label=selected_class))


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
    create_starting_armour(gameworld, player)

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


def create_starting_armour(gameworld, player):
    logger.debug('Creating starting armour')
    chest_armour = gameworld.create_entity()
    legs_armour = gameworld.create_entity()
    feet_armour = gameworld.create_entity()
    armour_file = read_json_file(constants.JSONFILEPATH + 'armour.json')
    for arms in armour_file['armour']:
        if arms['quality'] == 'basic':
            if arms['location'] == 'chest':
                gameworld.add_component(chest_armour, armour.Location(arms['location']))
                gameworld.add_component(chest_armour, armour.Set(arms['set']))
                gameworld.add_component(chest_armour, armour.Quality(arms['quality']))
                gameworld.add_component(chest_armour, armour.Weight(arms['weight']))
                gameworld.add_component(chest_armour, armour.Defense(arms['defense']))
                gameworld.add_component(chest_armour, armour.Describable(prefix=arms['prefix']))
                gameworld.add_component(chest_armour, armour.AttributeBonus(
                    majorname=arms['attr-majorname'],
                    majorbonus=arms['attr-majorbonus'],
                    minoronename=arms['attr-minoronename'],
                    minoronebonus=arms['attr-minoronebonus'],
                    minortwoname=arms['attr-minortwoname'],
                    minortwobonus=arms['attr-minortwobonus']))

            if arms['location'] == 'legs':
                gameworld.add_component(legs_armour, armour.Location(arms['location']))
                gameworld.add_component(legs_armour, armour.Set(arms['set']))
                gameworld.add_component(legs_armour, armour.Quality(arms['quality']))
                gameworld.add_component(legs_armour, armour.Weight(arms['weight']))
                gameworld.add_component(legs_armour, armour.Defense(arms['defense']))
                gameworld.add_component(chest_armour, armour.Describable(prefix=arms['prefix']))
                gameworld.add_component(legs_armour, armour.AttributeBonus(
                    majorname=arms['attr-majorname'],
                    majorbonus=arms['attr-majorbonus'],
                    minoronename=arms['attr-minoronename'],
                    minoronebonus=arms['attr-minoronebonus'],
                    minortwoname=arms['attr-minortwoname'],
                    minortwobonus=arms['attr-minortwobonus']))

            if arms['location'] == 'feet':
                gameworld.add_component(feet_armour, armour.Location(arms['location']))
                gameworld.add_component(feet_armour, armour.Set(arms['set']))
                gameworld.add_component(feet_armour, armour.Quality(arms['quality']))
                gameworld.add_component(feet_armour, armour.Weight(arms['weight']))
                gameworld.add_component(feet_armour, armour.Defense(arms['defense']))
                gameworld.add_component(chest_armour, armour.Describable(prefix=arms['prefix']))
                gameworld.add_component(feet_armour, armour.AttributeBonus(
                    majorname=arms['attr-majorname'],
                    majorbonus=arms['attr-majorbonus'],
                    minoronename=arms['attr-minoronename'],
                    minoronebonus=arms['attr-minoronebonus'],
                    minortwoname=arms['attr-minortwoname'],
                    minortwobonus=arms['attr-minortwobonus']))

    gameworld.component_for_entity(player, mobiles.Armour).chest = chest_armour
    gameworld.component_for_entity(player, mobiles.Armour).legs = legs_armour
    gameworld.component_for_entity(player, mobiles.Armour).feet = feet_armour


def display_selection(con, filename, element, posx, posy, width, flavour_x, flavour_y):

    letter_index = ord('a')
    for option in filename[element]:
        option_name = option['name']
        option_flavour = option['flavour']

        tcod.console_set_default_foreground(con, tcod.white)
        tcod.console_set_default_background(con, tcod.black)

        menu_choice = '(' + chr(letter_index) + ') '

        tcod.console_print(con, posx, posy, menu_choice + option_name.capitalize())
        my_wrap = textwrap.TextWrapper(width=50)
        new_flavour_lines = my_wrap.wrap(text=option_flavour)

        tcod.console_set_default_foreground(con, tcod.yellow)
        tcod.console_set_default_background(con, tcod.black)

        for line in new_flavour_lines:
            tcod.console_print(con, flavour_x, flavour_y, line)
            flavour_y += 1

        tcod.console_hline(con, posx, flavour_y + 1, width - 1, tcod.BKGND_DEFAULT)

        flavour_y += 3
        posy = flavour_y + 1
        letter_index += 1

    return flavour_y - 3
