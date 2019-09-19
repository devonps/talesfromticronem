import tcod.console
import tcod.event

from newGame.initialiseNewGame import setup_gameworld, initialise_game_map
from utilities.game_messages import MessageLog, Message
from utilities.mobileHelp import MobileUtilities
from utilities.replayGame import ReplayGame
from loguru import logger
from utilities import configUtilities
from utilities.input_handlers import handle_game_keys
from gameworld.sceneManager import SceneManager

from newGame import newGame


def game_loop(con, gameworld, game_config):

    msg_panel_across_pos = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MSG_PANEL_START_X')
    msg_panel_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MSG_PANEL_WIDTH')
    msg_panel_lines = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MSG_PANEL_LINES')
    player = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
    spell_bar = MobileUtilities.get_spellbar_id_for_entity(gameworld=gameworld, entity=player)
    message_log = MessageLog(x=msg_panel_across_pos, width=msg_panel_width, height=msg_panel_lines)

    # 'clears' the root console, therefore the other consoles are not showing
    con.clear()
    setup_gameworld(game_config)

    playing_game = True
    message_log.add_message(message=Message('New game starting', color=tcod.yellow), game_config=game_config)

    game_map = initialise_game_map(con, gameworld, player, spell_bar, message_log, game_config)
    currentScene = 1
    previousScene = 0
    SceneChange = True

    while playing_game:

        #
        # scene manager
        #
        if SceneChange:
            # call scene manager
            SceneManager.newScene(currentscene=currentScene, gameConfig=game_config)
            SceneChange = False
            # initialise_game_map(con, gameworld, player, spell_bar, message_log, game_config, game_map)

        # I'm thinking about bringing 'render' out of the esper model

        # run ALL game processors
        gameworld.process(game_config)

        event_to_be_processed, event_action = handle_game_keys()
        if event_to_be_processed != '':
            if event_to_be_processed == 'keypress':
                if event_action == 'quit':
                    value = 'exit:true'
                    ReplayGame.update_game_replay_file(game_config, value)
                    playing_game = False
                    raise SystemExit()
                if event_action in ('left', 'right', 'up', 'down'):
                    MobileUtilities.set_player_velocity(gameworld=gameworld, player_entity=player, direction=event_action, speed=1)


def start_game(con, gameworld, game_config):

    msg_panel_across_pos = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MSG_PANEL_START_X')
    # msg_panel_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MSG_PANEL_WIDTH')
    # msg_panel_lines = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MSG_PANEL_LINES')
    #
    # # 'clears' the root console, therefore the other consoles are not showing
    # con.clear()
    #
    # setup_gameworld(game_config)
    #
    # player = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
    # spell_bar = MobileUtilities.get_spellbar_id_for_entity(gameworld=gameworld, entity=player)
    #
    # message_log = MessageLog(x=msg_panel_across_pos, width=msg_panel_width, height=msg_panel_lines)
    # game_map = initialise_game_map(con, gameworld, player, spell_bar, message_log, game_config)
    #
    # key = tcod.Key()
    # mouse = tcod.Mouse()
    # playing_game = True
    #
    # message_log.add_message(message=Message('New game starting', color=tcod.yellow), game_config=game_config)

    # while playing_game:
    #     action = handle_keys(mouse, key, gameworld, player, message_log, game_config)
    #
    #     exit_game = action.get('exit')
    #     fullscreen = action.get('fullscreen')
    #     player_moved = action.get('player_moved')
    #     display_inventory = action.get('display_inv_panel')
    #     pick_up_entity = action.get('pickup')
    #
    #     if display_inventory:
    #         configUtilities.write_config_value(configfile=game_config, section='game',parameter='DISPLAY_GAME_STATE', value=str(2))
    #
    #     if pick_up_entity:
    #         MobileUtilities.mobile_pick_up_item(gameworld=gameworld, mobile=player)
    #
    #     if player_moved:
    #         pass
    #
    #     if exit_game:
    #         value = 'exit:true'
    #         ReplayGame.update_game_replay_file(game_config, value)
    #         playing_game = False
    #         raise SystemExit()
    #
    #     if fullscreen:
    #         tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
    #
    #     # run ALL game processors
    #     gameworld.process(game_config)
    #     tcod.console_flush()


def game_replay(con, game_config):
    ReplayGame.process(con, game_config)
    tcod.console_clear(con)


@logger.catch()
def main():

    # LoadPrefab.loadPrefab()
    newGame.new_game()


if __name__ == '__main__':
    main()

