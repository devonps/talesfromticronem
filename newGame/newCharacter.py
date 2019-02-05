import tcod
import random
import textwrap

from loguru import logger
from components import weapons, spellBar
from newGame.ClassWeapons import WeaponClass
from newGame.ClassArmour import *
from newGame.ClassJewellery import Trinkets
from utilities.mobileHelp import MobileUtilities
from utilities.jsonUtilities import read_json_file
from utilities.spellHelp import SpellUtilities
from input_handler import handle_new_race, handle_new_class


class NewCharacter:

    def create(con, gameworld):
        player = generate_player_character(gameworld=gameworld)
        select_race(con=con, gameworld=gameworld, player=player)
        select_character_class(con=con, gameworld=gameworld, player=player)
        select_personality_choices(con=con, gameworld=gameworld, player=player)
        name_your_character(con=con, gameworld=gameworld, player=player)
        spell_bar_entity = generate_spell_bar(gameworld=gameworld)
        get_starting_equipment(con=con, gameworld=gameworld, player=player, spellbar=spell_bar_entity)
        return player, spell_bar_entity


def generate_spell_bar(gameworld):
    logger.debug('Creating the spell bar')
    spell_bar = gameworld.create_entity()

    gameworld.add_component(spell_bar, spellBar.SlotOne())
    gameworld.add_component(spell_bar, spellBar.SlotTwo())
    gameworld.add_component(spell_bar, spellBar.SlotThree())
    gameworld.add_component(spell_bar, spellBar.SlotFour())
    gameworld.add_component(spell_bar, spellBar.SlotFive())
    gameworld.add_component(spell_bar, spellBar.SlotSix())
    gameworld.add_component(spell_bar, spellBar.SlotSeven())
    gameworld.add_component(spell_bar, spellBar.SlotEight())
    gameworld.add_component(spell_bar, spellBar.SlotNine())
    gameworld.add_component(spell_bar, spellBar.SlotTen())

    return spell_bar


def generate_player_character(gameworld):
    """
    Creates a shell for the player character details to be populated with
    :param gameworld:
    :return:
    """

    logger.debug('Creating the player character entity')
    player = MobileUtilities.generate_base_mobile(gameworld)
    gameworld.add_component(player, mobiles.Describable(background=tcod.blue))
    gameworld.add_component(player, mobiles.AI(ailevel=constants.AI_LEVEL_PLAYER))
    gameworld.add_component(player, mobiles.Inventory())
    gameworld.add_component(player, mobiles.Armour())
    gameworld.add_component(player, mobiles.Jewellery())
    gameworld.add_component(player, mobiles.Equipped())
    gameworld.add_component(player, mobiles.Health(current=1, maximum=10))
    gameworld.add_component(player, mobiles.Velocity())

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

    # frame_x = 5
    # frame_y = 4
    # frame_w = 80
    # flavour_x = 19
    # flavour_y = frame_y + 1
    # name_not_selected = True
    selected_name = ''
    #
    # key = tcod.Key()
    # mouse = tcod.Mouse()
    #
    # while name_not_selected:
    #
    #     tcod.console_print_frame(con, x=frame_x, y=frame_y - 2, w=frame_w, h=frame_y, clear=False, flag=tcod.BKGND_DEFAULT,
    #                              fmt='Make Your Choices')
    #
    #     selected_name = input('What is your name? ')
    #     tcod.console_blit(con, 0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, 0, 0, 0)
    #
    #     tcod.console_flush()
    #     tcod.sys_wait_for_event(tcod.EVENT_KEY_PRESS, key, mouse, True)
    #     if selected_name != '':
    #         name_not_selected = False
    #
    # tcod.console_clear(con)

    player_race_component = gameworld.component_for_entity(player, mobiles.Race)
    logger.info('Race selected {}', player_race_component.label)

    if player_race_component.label == 'human':
        tcod.namegen_parse(constants.HUMANNAMESFILE)
        logger.info('reading from human file')
    if player_race_component.label == 'elf':
        tcod.namegen_parse(constants.ELFNAMESFILE)
    if player_race_component.label == 'orc':
        tcod.namegen_parse(constants.ORCNAMESFILE)
    if player_race_component.label == 'troll':
        tcod.namegen_parse(constants.TROLLNAMESFILE)

    if random.randrange(0,100) < 50:
        sn = tcod.namegen_generate('male')
        gameworld.component_for_entity(player, mobiles.Describable).gender = 'male'
    else:
        sn = tcod.namegen_generate('female')
        gameworld.component_for_entity(player, mobiles.Describable).gender = 'female'

    selected_name = sn.capitalize()
    logger.info('Name chosen {}', selected_name)

    gameworld.add_component(player, mobiles.Name(first=selected_name, suffix='none'))


def get_starting_equipment(con, gameworld, player, spellbar):
    logger.debug('Selecting starting equipment')

    # create starting armour
    create_starting_armour(gameworld, player)

    # create starting jewellery
    logger.info('creating some basic jewellery for the player')
    create_starting_jewellery(gameworld, player)

    # create starting weapons
    logger.info('creating a weapon for the player')
    class_component = gameworld.component_for_entity(player, mobiles.CharacterClass)

    # create a new weapon for the player
    weapon = WeaponClass.create_weapon(gameworld, 'staff')
    weapon_type = gameworld.component_for_entity(weapon, weapons.Name)
    # parameters are: gameworld, weapon object, weapon type as a string, mobile class
    logger.info('Loading that weapon with the necessary spells')
    WeaponClass.load_weapon_with_spells(gameworld, weapon, weapon_type.label, class_component.label)

    # equip player with weapon
    logger.info('Equipping player with that loaded weapon')
    MobileUtilities.equip_weapon(gameworld, player, weapon, 'both')

    # load spell bar with spells from weapon
    logger.info('Loading spell bar')
    SpellUtilities.populate_spell_bar_from_weapon(gameworld, player_entity=player, spellbar=spellbar)

    logger.debug('Player is ready to rock and roll!')


def create_starting_armour(gameworld, player):
    logger.info('Creating starting armour')

    my_armour = ArmourClass.create_full_armour_set(gameworld, armourset='Apprentice', level=0, quality='basic')

    logger.info('Attaching starting armour to player character')
    ArmourClass.equip_full_set_of_armour(gameworld, entity=player, armourset=my_armour)


def create_starting_jewellery(gameworld, player):
    stud = Trinkets.create_earring(gameworld, e_setting='copper', e_hook='copper', e_activator='Amber')
    stud2 = Trinkets.create_earring(gameworld, e_setting='copper', e_hook='copper', e_activator='Amber')
    ring1 = Trinkets.create_ring(gameworld, e_setting='copper', e_hook='copper', e_activator='Amber')
    ring2 = Trinkets.create_ring(gameworld, e_setting='copper', e_hook='copper', e_activator='Amber')
    amulet = Trinkets.create_amulet(gameworld, e_setting='copper', e_hook='copper', e_activator='Amber')

    Trinkets.equip_piece_of_jewellery(gameworld, player, 'left ear', stud)
    Trinkets.equip_piece_of_jewellery(gameworld, player, 'right ear', stud2)
    Trinkets.equip_piece_of_jewellery(gameworld, player, 'left hand', ring1)
    Trinkets.equip_piece_of_jewellery(gameworld, player, 'right hand', ring2)
    Trinkets.equip_piece_of_jewellery(gameworld, player, 'neck', amulet)


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
