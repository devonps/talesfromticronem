
import random

from newGame.initialiseNewGame import setup_game, create_game_world
from processors.render import *
from newGame.newCharacter import NewCharacter
from input_handler import handle_main_menu

from newGame.ClassArmour import *
from components import jewellery
from newGame.ClassJewellery import Trinkets


def start_game(con, gameworld):

    gameworld, game_map = setup_game(con, gameworld)

    player = NewCharacter.create(con, gameworld)

    # test code
    player_name_component = gameworld.component_for_entity(player, mobiles.Name)
    player_race_component = gameworld.component_for_entity(player, mobiles.Race)
    player_class_component = gameworld.component_for_entity(player, mobiles.CharacterClass)

    logger.info(player_name_component.first + ' the ' + player_race_component.label + ' ' + player_class_component.label + ' is ready!')

    chest_piece = ArmourClass.describe_armour_at_bodylocation(gameworld, player, 'chest')
    legs_piece = ArmourClass.describe_armour_at_bodylocation(gameworld, player, 'legs')
    feet_piece = ArmourClass.describe_armour_at_bodylocation(gameworld, player, 'feet')

    amulet = Trinkets.get_jewellery_entity_at_bodylocation(gameworld, player, 'neck')

    # TURN THE BELOW CODE INTO A METHOD
    gemstone_component = gameworld.component_for_entity(amulet, jewellery.Describable)
    material_component = gameworld.component_for_entity(amulet, jewellery.Material)
    type_component = gameworld.component_for_entity(amulet, jewellery.Type)

    # TURN THE BELOW CODE INTO A METHOD
    attribute_component = gameworld.component_for_entity(amulet, jewellery.ImprovementTo)
    stat_name = attribute_component.stat1name
    stat_bonus = attribute_component.stat1bonus


    logger.info(player_name_component.first + ' is wearing a ' + chest_piece)
    logger.info(' with matching ' + legs_piece)
    logger.info(' and he has a pair of ' + feet_piece)

    logger.info('Around his neck he has an {} {} {}', gemstone_component.component3, material_component.label, type_component.label)
    logger.info('This provides a +{} to his {} attribute', stat_bonus, stat_name)
    key = tcod.Key()
    mouse = tcod.Mouse()

    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY, key, mouse)

        # run ALL game processors
        gameworld.process()

        tcod.console_flush()

        key = tcod.console_check_for_keypress()
        if key.vk == tcod.KEY_ENTER:
            gameworld.component_for_entity(player, mobiles.Position).x = random.randrange(1, 79)
            gameworld.component_for_entity(player, mobiles.Position).y = random.randrange(1, 39)

        if key.vk == tcod.KEY_ESCAPE:
            return True


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
    gameworld = create_game_world()

    # start game screen
    background_image = tcod.image_load('static/images/menu_background.png')

    # add the processors we need to display and handle the game start screen, character selection, etc.

    render_game_screen = RenderGameStartScreen(con=con, image=background_image)
    gameworld.add_processor(render_game_screen)

    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY, key, mouse)
        gameworld.process()

        tcod.console_flush()

        action = handle_main_menu(key)

        new_game = action.get('new_game')
        load_saved_game = action.get('load_game')
        exit_game = action.get('exit')

        if new_game:
            gameworld.remove_processor(RenderGameStartScreen)
            tcod.console_clear(con)
            start_game(con, gameworld)
            print('left game')
            gameworld.clear_database()
            tcod.console_delete(con)
            con = tcod.console_new(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
            render_game_screen = RenderGameStartScreen(con=con, image=background_image)
            gameworld.add_processor(render_game_screen)
        elif load_saved_game:
            pass
        elif exit_game:
            break


if __name__ == '__main__':
    main()
