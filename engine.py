import tcod


from newGame.initialiseNewGame import setup_game, create_game_world, initialise_game_map, create_new_character
from processors.render import RenderGameStartScreen

from newGame.ClassArmour import *
from utilities.mobileHelp import MobileUtilities
from utilities.input_handlers import handle_keys, handle_main_menu
from utilities.gameworld import reset_gameworld
from utilities.text_input import text_to_entry


def start_game(con, gameworld):

    setup_game(con, gameworld)
    player, spell_bar = create_new_character(con, gameworld)
    initialise_game_map(con, gameworld, player, spell_bar)

    # test code

    player_description = MobileUtilities.describe_the_mobile(gameworld, player)
    logger.info(player_description + ' is ready!')

    key = tcod.Key()
    mouse = tcod.Mouse()

    while not tcod.console_is_window_closed():
        action = handle_keys(mouse, key, gameworld, player)

        exit_game = action.get('exit')
        fullscreen = action.get('fullscreen')
        player_moved = action.get('player_moved')
        text_entered = action.get('text')

        if text_entered:
            my_word = text_to_entry()
            logger.info('text returned {}', my_word)

        if player_moved:
            pass

        if exit_game:
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        # run ALL game processors
        gameworld.process()
        tcod.console_flush()


def main():

    # logger.add(constants.LOGFILE, format=constants.LOGFORMAT)

    logger.info('*********************')
    logger.info('* Initialising game *')
    logger.info('*********************')

    tcod.console_set_custom_font('static/fonts/prestige12x12_gs_tc.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    tcod.console_init_root(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.GAME_WINDOW_TITLE, False)

    con = tcod.console_new(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)

    key = tcod.Key()
    mouse = tcod.Mouse()
    action = {}

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
        gameworld.process()
        tcod.console_flush()

        tcod.sys_wait_for_event(tcod.EVENT_KEY_PRESS, key, mouse, flush=False)
        action = handle_main_menu(key, mouse)

        new_game = action.get('new_game')
        load_saved_game = action.get('load_game')
        exit_game = action.get('exit')
        player_seed = action.get('player_seed')

        if player_seed:
            player_supplied_seed = "ABSTRACTIONISM"
            constants.PLAYER_SEED = player_supplied_seed

        if new_game:
            gameworld.remove_processor(RenderGameStartScreen)
            tcod.console_clear(con)
            start_game(con, gameworld)
            logger.info('*********************')
            logger.info('* Left Game         *')
            logger.info('*********************')
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
