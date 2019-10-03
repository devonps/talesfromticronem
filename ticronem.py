import tcod.console
import tcod.event

from newGame.initialiseNewGame import setup_gameworld
from utilities.game_messages import MessageLog, Message
from utilities.mobileHelp import MobileUtilities
from utilities.replayGame import ReplayGame
from loguru import logger
from utilities import configUtilities
from utilities.input_handlers import handle_game_keys
from gameworld.sceneManager import SceneManager

from newGame import newGame


def game_loop(con, gameworld):

    game_config = configUtilities.load_config()

    msg_panel_across_pos = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MSG_PANEL_START_X')
    msg_panel_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MSG_PANEL_WIDTH')
    msg_panel_lines = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MSG_PANEL_LINES')
    con_width = configUtilities.get_config_value_as_integer(game_config, 'tcod', 'SCREEN_WIDTH')
    con_height = configUtilities.get_config_value_as_integer(game_config, 'tcod', 'SCREEN_HEIGHT')
    player = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
    message_log = MessageLog(x=msg_panel_across_pos, width=msg_panel_width, height=msg_panel_lines)

    # 'clears' the root console, therefore the other consoles are not showing
    con.clear()
    setup_gameworld(game_config)

    gameDisplay = tcod.console.Console(width=con_width, height=con_height, order='F')

    playing_game = True
    message_log.add_message(message=Message('New game starting', color=tcod.yellow), game_config=game_config)

    currentScene = 1
    previousScene = 0
    SceneChange = True

    while playing_game:

        #
        # scene manager
        #
        if SceneChange:
            # call scene manager
            SceneManager.newScene(console=gameDisplay, currentscene=currentScene, gameConfig=game_config, gameworld=gameworld)
            SceneChange = False
        #
        # get player action aka their intent to do something
        #
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

            if event_to_be_processed == 'textinput':
                if event_action == 'n':
                    SceneChange = True
                    previousScene = currentScene
                    currentScene += 1
                    if currentScene > 2:
                        currentScene = 1
        #
        # get monsters intended action
        #

        # run ALL game processors
        gameworld.process(game_config)


def game_replay(con, game_config):
    ReplayGame.process(con, game_config)
    tcod.console_clear(con)


@logger.catch()
def main():

    # LoadPrefab.loadPrefab()
    newGame.new_game()


if __name__ == '__main__':
    main()

