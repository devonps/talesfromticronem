import tcod.console


from newGame.initialiseNewGame import setup_game, create_game_world, initialise_game_map, create_new_character, create_and_place_world_entities, create_spell_entities
from utilities.game_messages import MessageLog, Message
from processors.render import RenderGameStartScreen
from utilities.mobileHelp import MobileUtilities
from utilities.input_handlers import handle_keys, handle_menus
from utilities.world import reset_gameworld
from utilities.replayGame import ReplayGame
from loguru import logger
from utilities import configUtilities


def start_game(con, gameworld, game_config):

    msg_panel_across_pos = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MSG_PANEL_START_X')
    msg_panel_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MSG_PANEL_WIDTH')
    msg_panel_lines = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MSG_PANEL_LINES')

    setup_game(game_config)
    create_spell_entities(gameworld, game_config)
    player, spell_bar = create_new_character(con, gameworld, game_config)
    message_log = MessageLog(x=msg_panel_across_pos, width=msg_panel_width, height=msg_panel_lines)
    game_map = initialise_game_map(con, gameworld, player, spell_bar, message_log, game_config)
    create_and_place_world_entities(gameworld=gameworld, game_map=game_map, game_config=game_config)

    # test code

    player_description = MobileUtilities.describe_the_mobile(gameworld, player)
    logger.info(player_description)

    key = tcod.Key()
    mouse = tcod.Mouse()

    message_log.add_message(message=Message('New game starting', color=tcod.yellow), game_config=game_config)

    while not tcod.console_is_window_closed():
        action = handle_keys(mouse, key, gameworld, player, message_log, game_config)

        exit_game = action.get('exit')
        fullscreen = action.get('fullscreen')
        player_moved = action.get('player_moved')
        display_inventory = action.get('display_inv_panel')
        pick_up_entity = action.get('pickup')

        if display_inventory:
            configUtilities.write_config_value(configfile=game_config, section='game',parameter='DISPLAY_GAME_STATE', value=str(2))

        if pick_up_entity:
            MobileUtilities.mobile_pick_up_item(gameworld=gameworld, mobile=player)

        if player_moved:
            pass

        if exit_game:
            value = 'exit:true'
            ReplayGame.update_game_replay_file(game_config, value)
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        # run ALL game processors
        gameworld.process(game_config)
        tcod.console_flush()


def game_replay(con, game_config):
    ReplayGame.process(con, game_config)
    tcod.console_clear(con)


@logger.catch()
def main():

    game_config = configUtilities.load_config()

    # logfile = configUtilities.get_config_value_as_string(game_config, 'logging', 'LOGFILE')
    # logformat = configUtilities.get_config_value_as_string(game_config, 'logging', 'LOGFORMAT')

    # logger.add(logfile, format=logformat)

    logger.info('*********************')
    logger.info('* Initialising game *')
    logger.info('*********************')

    game_title1 = configUtilities.get_config_value_as_string(game_config, 'default', 'GAME_WINDOW_TITLE')

    logger.info('config file test:{}', str(game_title1))

    con_width = configUtilities.get_config_value_as_integer(game_config, 'tcod', 'SCREEN_WIDTH')
    con_height = configUtilities.get_config_value_as_integer(game_config, 'tcod', 'SCREEN_HEIGHT')
    game_title = configUtilities.get_config_value_as_string(game_config, 'default', 'GAME_WINDOW_TITLE')

    tcod.console_set_custom_font('static/fonts/prestige12x12_gs_tc.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    tcod.console_init_root(con_width, con_height, game_title, False)

    con = tcod.console.Console(con_width, con_height)

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
        gameworld.process(game_config)
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
            game_replay(con, game_config)

        if player_seed:
            player_supplied_seed = "ABSTRACTIONISM"
            # this was a write back to the constants file. This doesn't work with the config file
            # need another option issue #57 created
            # constants.PLAYER_SEED = player_supplied_seed

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
            game_config = configUtilities.load_config()

            start_game(con, gameworld, game_config)
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
