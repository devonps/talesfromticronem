import tcod.console


from newGame.initialiseNewGame import setup_game, create_game_world, initialise_game_map, create_new_character, constants
from newGame.game_messages import MessageLog, Message
from processors.render import RenderGameStartScreen
from utilities.mobileHelp import MobileUtilities
from utilities.input_handlers import handle_keys, handle_menus
from utilities.world import reset_gameworld
from utilities.replayGame import ReplayGame
from ui.character_screen import display_hero_panel
from loguru import logger

from newGame.Items import ItemManager


def start_game(con, gameworld):

    setup_game(con, gameworld)
    player, spell_bar = create_new_character(con, gameworld)
    message_log = MessageLog(x=constants.MSG_PANEL_START_X, width=constants.MSG_PANEL_WIDTH, height=constants.MSG_PANEL_LINES)
    initialise_game_map(con, gameworld, player, spell_bar, message_log)

    # test code

    player_description = MobileUtilities.describe_the_mobile(gameworld, player)
    logger.info(player_description)

    # my_weapon = ItemManager.create_weapon(gameworld=gameworld, weapon_type='sword')
    # head_armour_piece = ItemManager.create_piece_of_armour(gameworld=gameworld, bodylocation='head', quality='basic')
    # new_bag = ItemManager.create_bag(gameworld=gameworld)
    # earring = ItemManager.create_jewellery(gameworld=gameworld, bodylocation='ear', e_activator='Garnet', e_setting='copper', e_hook='copper')
    # amulet = ItemManager.create_jewellery(gameworld=gameworld, bodylocation='neck', e_activator='Garnet', e_setting='copper', e_hook='copper')
    # ring = ItemManager.create_jewellery(gameworld=gameworld, bodylocation='finger', e_activator='Garnet', e_setting='copper', e_hook='copper')

    key = tcod.Key()
    mouse = tcod.Mouse()

    message_log.add_message(message=Message('New game starting', color=tcod.yellow))

    while not tcod.console_is_window_closed():
        action = handle_keys(mouse, key, gameworld, player, message_log)

        exit_game = action.get('exit')
        fullscreen = action.get('fullscreen')
        player_moved = action.get('player_moved')
        display_hero = action.get('display_hero_panel')

        if display_hero:
            display_hero_panel(con, key, mouse, gameworld)

        if player_moved:
            pass

        if exit_game:
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        # run ALL game processors
        gameworld.process()
        tcod.console_flush()


def game_replay(con):
    ReplayGame.process(con)
    tcod.console_clear(con)

@logger.catch()
def main():

    # logger.add(constants.LOGFILE, format=constants.LOGFORMAT)

    logger.info('*********************')
    logger.info('* Initialising game *')
    logger.info('*********************')

    tcod.console_set_custom_font('static/fonts/prestige12x12_gs_tc.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    tcod.console_init_root(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.GAME_WINDOW_TITLE, False)

    # con = tcod.console_new(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
    con = tcod.console.Console(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)

    key = tcod.Key()
    mouse = tcod.Mouse()
    action = {}

    # Esper initialisation
    gameworld = create_game_world()

    # needed here to gather player input from the main menu
    MobileUtilities.create_player_input_entity(gameworld)

    # start game screen image
    background_image = tcod.image_load('static/images/menu_background.png')

    # add the processors we need to display the game start screen

    render_game_screen = RenderGameStartScreen(con=con, image=background_image, key=key, mouse=mouse, gameworld=gameworld)

    gameworld.add_processor(render_game_screen)

    while not tcod.console_is_window_closed():
        gameworld.process()
        tcod.console_flush()
        new_game = load_saved_game = save_game = exit_game = player_seed = replay_game = False

        action = handle_menus(key, mouse, gameworld)

        if action == 'a':
            # return {'new_game': True}
            new_game = True
        elif action == 'b':
            # return {'load_game': True}
            load_saved_game = True
        elif action == 'c':
            # save current game
            save_game = True
        elif action == 'd':
            # return {'player_seed': True}
            player_seed = True
        elif action == 'e':
            # return {'replay': True}
            replay_game = True
        elif action == 'f':
            # return {'exit': True}
            exit_game = True

        if replay_game:
            logger.info('Replaying game')
            game_replay(con)

        if player_seed:
            player_supplied_seed = "ABSTRACTIONISM"
            constants.PLAYER_SEED = player_supplied_seed

            my_random = tcod.random_new_from_seed(1059)
            logger.info('random seed set up {}', my_random)

            for x in range(11):
                r = my_random.randint(0,10)
                logger.info('random number chosen {}', r)

        if new_game:
            logger.info('New game starting')
            gameworld.remove_processor(RenderGameStartScreen)
            # tcod.console_clear(con)
            con.clear(ch=32, fg=(0, 0, 0), bg=(0, 0, 0))
            start_game(con, gameworld)
            logger.info('*********************')
            logger.info('* Left Game         *')
            logger.info('*********************')
            reset_gameworld(gameworld)
            # Esper initialisation
            gameworld = create_game_world()

            # tcod.console_clear(con)
            con.clear(ch=32, fg=(0, 0, 0), bg=(0, 0, 0))
            render_game_screen = RenderGameStartScreen(con=con, image=background_image, key=key, mouse=mouse, gameworld=gameworld)
            gameworld.add_processor(render_game_screen)

        elif load_saved_game:
            pass
        elif save_game:
            pass
        elif exit_game:
            break


if __name__ == '__main__':
    main()
