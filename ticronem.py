import tcod.console
import tcod.event

from bearlibterminal import terminal

from newGame.Entities import Entity
from ui.character_screen import display_hero_panel
from newGame.initialiseNewGame import setup_gameworld
from utilities.mobileHelp import MobileUtilities
from utilities.replayGame import ReplayGame
from loguru import logger
from utilities import configUtilities
from utilities.input_handlers import handle_game_keys
from gameworld.sceneManager import SceneManager

from newGame import newGame


def game_loop(gameworld):

    game_config = configUtilities.load_config()
    player = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)

    # enemyObject = Entity(gameworld=gameworld)
    # enemy_id = enemyObject.create_new_entity()
    # enemyObject.create_new_enemy(entity_id=enemy_id)
    #
    # logger.warning('NEW ENEMY CREATED WITH {} AS THE ENTITY ID', enemy_id)

    terminal.composition(terminal.TK_ON)
    terminal.clear()

    setup_gameworld(game_config)

    playing_game = True

    currentScene = 1
    previousScene = 0
    SceneChange = True

    while playing_game:

        #
        # scene manager
        #
        if SceneChange:
            # call scene manager
            SceneManager.newScene(currentscene=currentScene, gameworld=gameworld)
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
                if event_action == 'h':
                    display_hero_panel(gameworld=gameworld)
                if event_action == 'g':
                    MobileUtilities.mobile_pick_up_item(gameworld=gameworld, mobile=player)

            if event_to_be_processed == 'mouseleftbutton':
                logger.info('cell x/y {}/{}', event_action[0], event_action[1])
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
    terminal.open()
    newGame.new_game()


if __name__ == '__main__':
    main()

