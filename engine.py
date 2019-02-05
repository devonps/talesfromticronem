import tcod


from newGame.initialiseNewGame import setup_game, create_game_world
from processors.render import RenderGameStartScreen
from input_handler import handle_main_menu

from newGame.ClassArmour import *
from utilities.mobileHelp import MobileUtilities
from utilities.input_handlers import handle_keys
from utilities.gameworld import reset_gameworld


def start_game(con, gameworld):

    game_map, player = setup_game(con, gameworld)

    # test code

    player_description = MobileUtilities.describe_the_mobile(gameworld, player)

    logger.info(player_description + ' is ready!')

    key = tcod.Key()
    mouse = tcod.Mouse()

    while not tcod.console_is_window_closed():

        action = handle_keys(mouse, key, gameworld, player)

        exit_game = action.get('exit')
        fullscreen = action.get('fullscreen')

        if exit_game:
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        # run ALL game processors
        gameworld.process()
        tcod.console_flush()


def main():

    # logger.add(constants.LOGFILE, format=constants.LOGFORMAT)

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
    # move_entities_processor = MoveEntities(gameworld=gameworld)

    gameworld.add_processor(render_game_screen)
    # gameworld.add_processor(move_entities_processor)

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
            reset_gameworld(gameworld)
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
