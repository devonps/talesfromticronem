import tcod
import random


from newGame.initialiseNewGame import setup_game, create_game_world
from processors.render import *
from newGame.newCharacter import NewCharacter


def start_game(con, gameworld):
    logger.info('For testing')

    gameworld, game_map = setup_game(con, gameworld)

    player = NewCharacter.create(con, gameworld)

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

        key = tcod.console_check_for_keypress()
        key_char = chr(key.c)

        if key_char == 'a':
            gameworld.remove_processor(RenderGameStartScreen)
            tcod.console_clear(con)
            start_game(con, gameworld)
            print('left game')
            gameworld.clear_database()
            tcod.console_delete(con)
            con = tcod.console_new(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
            render_game_screen = RenderGameStartScreen(con=con, image=background_image)
            gameworld.add_processor(render_game_screen)

        if key.vk == tcod.KEY_ESCAPE:
            return True


if __name__ == '__main__':
    main()
