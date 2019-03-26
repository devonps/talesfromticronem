import tcod
import random
import textwrap

from loguru import logger
from components import weapons, spellBar, userInput
from newGame.ClassWeapons import WeaponClass
from newGame.ClassArmour import *
from newGame.ClassJewellery import Trinkets
from utilities.mobileHelp import MobileUtilities
from utilities.jsonUtilities import read_json_file
from utilities.spellHelp import SpellUtilities
from utilities.input_handlers import handle_menus
from utilities.text_input import text_entry
from utilities.display import menu


class NewCharacter:

    def create(con, gameworld):
        player = generate_player_character(gameworld=gameworld)
        select_race(con=con, gameworld=gameworld, player=player)
        select_character_class(con=con, gameworld=gameworld, player=player)
        select_personality_choices(con=con, gameworld=gameworld, player=player)
        name_your_character(con=con, gameworld=gameworld, player=player)
        spell_bar_entity = generate_spell_bar(gameworld=gameworld)
        get_starting_equipment(con=con, gameworld=gameworld, player=player, spellbar=spell_bar_entity)

        MobileUtilities.calculate_derived_attributes(gameworld, player)

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
    :return: player entity
    """

    logger.debug('Creating the player character entity')
    player = MobileUtilities.generate_base_mobile(gameworld)
    gameworld.add_component(player, mobiles.Describable())
    gameworld.add_component(player, mobiles.AI(ailevel=constants.AI_LEVEL_PLAYER))
    gameworld.add_component(player, mobiles.Inventory())
    gameworld.add_component(player, mobiles.Armour())
    gameworld.add_component(player, mobiles.Jewellery())
    gameworld.add_component(player, mobiles.Equipped())
    gameworld.add_component(player, mobiles.Velocity())
    gameworld.add_component(player, mobiles.Personality())
    gameworld.add_component(player, mobiles.ManaPool(current=500, maximum=1000))
    gameworld.add_component(player, mobiles.SpecialBar(valuecurrent=10, valuemaximum=100))
    gameworld.add_component(player, mobiles.Renderable(is_visible=True))
    gameworld.add_component(player, mobiles.StatusEffects())
    gameworld.add_component(player, mobiles.PrimaryAttributes())
    gameworld.add_component(player, mobiles.SecondaryAttributes())
    gameworld.add_component(player, mobiles.DerivedAttributes())

    logger.info('stored as entity {}', player)

    return player


def select_race(con, gameworld, player):
    logger.info('Select Race')
    race_file = read_json_file(constants.JSONFILEPATH + 'races.json')

    menu_options = []
    menu_options_flavour = []
    race_prefix = []
    race_bg_colour = []
    race_size = []
    race_glyph = []

    for option in race_file['races']:
        menu_options.append(option['name'])
        menu_options_flavour.append(option['flavour'])
        race_prefix.append(option['prefix'])
        race_bg_colour.append(option['bg_colour'])
        race_size.append(option['size'])
        race_glyph.append(option['glyph'])

    race_not_selected = True

    key = tcod.Key()
    mouse = tcod.Mouse()
    tcod.console_clear(con)
    selected_race = ''

    while race_not_selected:

        ret_value = menu(con,
                         header='Select Race',
                         options=menu_options,
                         width=24,
                         screen_width=constants.SCREEN_WIDTH,
                         screen_height=constants.SCREEN_HEIGHT,
                         posx=10,
                         posy=26,
                         foreground=tcod.yellow,
                         key=key,
                         mouse=mouse,
                         gameworld=gameworld)
        if ret_value != '':
            ret_value = handle_menus(key=key, mouse=mouse, gameworld=gameworld)
            index = key.c - ord('a')
            if ret_value == 'a':
                selected_race = 'human'
                gameworld.add_component(player, mobiles.Describable(background=tcod.black))
            elif ret_value == 'b':
                selected_race = 'elf'
                gameworld.add_component(player, mobiles.Describable(background=tcod.blue))
            elif ret_value == 'c':
                selected_race = 'orc'
                gameworld.add_component(player, mobiles.Describable(background=tcod.red))
            elif ret_value == 'd':
                selected_race = 'troll'
                gameworld.add_component(player, mobiles.Describable(background=tcod.white))
            logger.info('Selected race {}', selected_race)
            gameworld.add_component(player, mobiles.Race(race=selected_race, size=race_size[index]))
            logger.info('Racial Size {}', race_size[index])

            race_not_selected = False
            tcod.console_clear(con)


def select_character_class(con, gameworld, player):
    logger.info('Selecting character class')
    class_file = read_json_file(constants.JSONFILEPATH + 'classes.json')

    menu_options = []
    menu_options_flavour = []

    for option in class_file['classes']:
        menu_options.append(option['name'])
        menu_options_flavour.append(option['flavour'])

    class_not_selected = True

    key = tcod.Key()
    mouse = tcod.Mouse()
    selected_class = ''

    while class_not_selected:

        ret_value = menu(con, header='Select Class',
             options=menu_options,
             width=24, screen_width=constants.SCREEN_WIDTH, screen_height=constants.SCREEN_HEIGHT, posx=10, posy=26,
             foreground=tcod.yellow,
             key=key,
             mouse=mouse,
             gameworld=gameworld)

        if ret_value != '':
            ret_value = handle_menus(key=key, mouse=mouse, gameworld=gameworld)

            if ret_value == 'a':
                selected_class = 'necromancer'
                gameworld.add_component(player, mobiles.CharacterClass(base_health=22))
            elif ret_value == 'b':
                selected_class = 'witch doctor'
                gameworld.add_component(player, mobiles.CharacterClass(base_health=22))
            elif ret_value == 'c':
                selected_class = 'druid'
                gameworld.add_component(player, mobiles.CharacterClass(base_health=18))
            elif ret_value == 'd':
                selected_class = 'mesmer'
                gameworld.add_component(player, mobiles.CharacterClass(base_health=18))
            elif ret_value == 'e':
                selected_class = 'elementalist'
                gameworld.add_component(player, mobiles.CharacterClass(base_health=5))
            elif ret_value == 'f':
                selected_class = 'chronomancer'
                gameworld.add_component(player, mobiles.CharacterClass(base_health=5))

            logger.info('Selected class {}', selected_class)
            gameworld.add_component(player, mobiles.CharacterClass(label=selected_class))
            class_not_selected = False
            tcod.console_clear(con)


def select_profession_background(con, gameworld, player):
    # The profession-oriented question affects a character's starting armor
    player_class_component = gameworld.component_for_entity(player, mobiles.CharacterClass)

    # different options presented to player based on their chosen class


def select_personality_choices(con, gameworld, player):
    logger.info('Selecting character personality choices')
    # The personality-oriented question affects the conversational options that NPCs provide.
    # there will be 3 options: charm, dignity, ferocity

    MobileUtilities.calculate_player_personality(gameworld)

    personality_component = gameworld.component_for_entity(player, mobiles.Describable)

    logger.debug('Your personality is viewed as {} by other NPCs', personality_component.personality_title)


def name_your_character(con, gameworld, player):
    logger.info('Naming the character')

    this_name = text_entry()

    if this_name == '':
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
    else:
        selected_name = this_name

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

    chest_armour = ArmourClass.get_armour_piece_from_body_location(gameworld, player, 'chest')

    logger.info('Chest armour: {}', chest_armour)


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
