import tcod
import random

from loguru import logger
from newGame.initialiseNewGame import setup_game, generate_player_character, create_wizard, create_demon
from newGame import constants
from components import spells, weapons, mobiles
from utilities.mobileHelp import MobileUtilities


def main():

#    logger.add(constants.LOGFILE, format=constants.LOGFORMAT)

    logger.info('********************')
    logger.info('* New game started *')
    logger.info('********************')

    tcod.console_set_custom_font('static/fonts/prestige12x12_gs_tc.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    tcod.console_init_root(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.GAME_WINDOW_TITLE, False)

    con = tcod.console_new(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)

    key = tcod.Key()
    mouse = tcod.Mouse()

    # Esper initialisation
    gameworld, game_map = setup_game(con)


    # create the player
    player = generate_player_character(gameworld, 'necromancer')
    player_name = gameworld.component_for_entity(player, mobiles.Name)
    class_component = gameworld.component_for_entity(player, mobiles.CharacterClass)

    # confirm the weapon is equipped
    # get the entity id for the equipped weapon
    # weapon_equipped = List of weapons equipped always returned in order: main, off, both hands

    weapons_equipped = MobileUtilities.get_weapons_equipped(gameworld, player)

    wpns = ''

    if weapons_equipped[0] > 0:
        wpn_name = gameworld.component_for_entity(weapons_equipped[0], weapons.Name)
        wpns = wpn_name.label + ' in his main hand'

    if weapons_equipped[1] > 0:
        if weapons_equipped[0] > 0:
            wpns = wpns + ' and a '
        wpn_name = gameworld.component_for_entity(weapons_equipped[1], weapons.Name)
        wpns = wpns + wpn_name.label + ' in his off hand'

    if weapons_equipped[2] > 0:
        wpn_name = gameworld.component_for_entity(weapons_equipped[2], weapons.Name)
        wpns = wpn_name.label + ' in both his hands'

    print(player_name.first + ' the ' + class_component.label + ' is holding a ' + wpns)

    thiswizard = create_wizard(gameworld)

    wizard_name = gameworld.component_for_entity(thiswizard, mobiles.Name)
    class_component = gameworld.component_for_entity(thiswizard, mobiles.CharacterClass)

    # get the weapon name component

    weapons_equipped = MobileUtilities.get_weapons_equipped(gameworld, thiswizard)

    wpns = ''

    if weapons_equipped[0] > 0:
        wpn_name = gameworld.component_for_entity(weapons_equipped[0], weapons.Name)
        wpns = wpn_name.label + ' in his main hand'

    if weapons_equipped[1] > 0:
        if weapons_equipped[0] > 0:
            wpns = wpns + ' and a '
        wpn_name = gameworld.component_for_entity(weapons_equipped[1], weapons.Name)
        wpns = wpns + wpn_name.label + ' in his off hand'

    if weapons_equipped[2] > 0:
        wpn_name = gameworld.component_for_entity(weapons_equipped[2], weapons.Name)
        wpns = wpn_name.label + ' in both his hands'

    print(wizard_name.first + ' the ' + class_component.label + ' is holding a ' + wpns)

    thisdemon = create_demon(gameworld)
    class_component = gameworld.component_for_entity(thisdemon, mobiles.CharacterClass)

    ai_component = gameworld.component_for_entity(thisdemon, mobiles.AI)

    print('be careful there is a ' + class_component.label + ' demon about!')
    print(ai_component.ailevel)


    # temp code to display the console!

    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY, key, mouse)

        # run ALL game processors
        gameworld.process()

        key = tcod.console_check_for_keypress()
        if key.vk == tcod.KEY_ENTER:
            gameworld.component_for_entity(player, mobiles.Position).x = random.randrange(1, 79)
            gameworld.component_for_entity(player, mobiles.Position).y = random.randrange(1, 39)

        if key.vk == tcod.KEY_ESCAPE:
            return True


if __name__ == '__main__':
    main()