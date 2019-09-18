import tcod.console
import tcod.event

from newGame.initialiseNewGame import setup_game, initialise_game_map
from utilities.game_messages import MessageLog, Message
from utilities.mobileHelp import MobileUtilities
from utilities.input_handlers import handle_keys
from utilities.replayGame import ReplayGame
from loguru import logger
from utilities import configUtilities

from newGame import newGame, LoadPrefab


def start_game(con, gameworld, game_config):

    msg_panel_across_pos = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MSG_PANEL_START_X')
    msg_panel_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MSG_PANEL_WIDTH')
    msg_panel_lines = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MSG_PANEL_LINES')

    setup_game(game_config)
    # create_spell_entities(gameworld, game_config)
    # player, spell_bar = create_new_character(con, gameworld, game_config)

    message_log = MessageLog(x=msg_panel_across_pos, width=msg_panel_width, height=msg_panel_lines)
    game_map = initialise_game_map(con, gameworld, player, spell_bar, message_log, game_config)

    # test code

    player_description = MobileUtilities.describe_the_mobile(gameworld, player)
    logger.info(player_description)

    key = tcod.Key()
    mouse = tcod.Mouse()
    playing_game = True

    message_log.add_message(message=Message('New game starting', color=tcod.yellow), game_config=game_config)

    while playing_game:
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
            playing_game = False

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

    # LoadPrefab.loadPrefab()
    newGame.new_game()


if __name__ == '__main__':
    main()

