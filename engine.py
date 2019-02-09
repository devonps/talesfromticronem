import tcod


from newGame.initialiseNewGame import setup_game, create_game_world, initialise_game_map, create_new_character
from processors.render import RenderGameStartScreen

from newGame.ClassArmour import *
from utilities.mobileHelp import MobileUtilities
from utilities.input_handlers import handle_keys, handle_main_menu
from utilities.gameworld import reset_gameworld
from components import userInput


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

        if player_moved:
            pass

        if exit_game:
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        # run ALL game processors
        gameworld.process()
        tcod.console_flush()


@logger.catch()
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

    # user input entity created
    ent = gameworld.create_entity()
    gameworld.add_component(ent, userInput.Keyboard())
    gameworld.add_component(ent, userInput.Mouse())

    # start game screen image
    background_image = tcod.image_load('static/images/menu_background.png')

    # add the processors we need to display the game start screen

    render_game_screen = RenderGameStartScreen(con=con, image=background_image, key=key, mouse=mouse, gameworld=gameworld)

    gameworld.add_processor(render_game_screen)

    while not tcod.console_is_window_closed():
        gameworld.process()
        tcod.console_flush()

        action = handle_main_menu(key, mouse, gameworld)
        logger.info('action is set to {}', action)

        new_game = action.get('new_game')
        load_saved_game = action.get('load_game')
        exit_game = action.get('exit')
        player_seed = action.get('player_seed')

        if player_seed:
            player_supplied_seed = "ABSTRACTIONISM"
            constants.PLAYER_SEED = player_supplied_seed

        if new_game:
            logger.info('New game starting')
            gameworld.remove_processor(RenderGameStartScreen)
            tcod.console_clear(con)
            start_game(con, gameworld)
            logger.info('*********************')
            logger.info('* Left Game         *')
            logger.info('*********************')
            reset_gameworld(gameworld)
            # Esper initialisation
            gameworld = create_game_world()
            # user input entity created
            ent = gameworld.create_entity()
            gameworld.add_component(ent, userInput.Keyboard())
            gameworld.add_component(ent, userInput.Mouse())

            tcod.console_clear(con)
            render_game_screen = RenderGameStartScreen(con=con, image=background_image, key=key, mouse=mouse, gameworld=gameworld)
            gameworld.add_processor(render_game_screen)

        elif load_saved_game:
            pass
        elif exit_game:
            break


if __name__ == '__main__':
    main()
