from bearlibterminal import terminal

from components.messages import Message
from enemyRelated.statelessAI import StatelessAI
from newGame.initialiseNewGame import setup_gameworld
from utilities.mobileHelp import MobileUtilities
from utilities.replayGame import ReplayGame
from loguru import logger
from utilities import configUtilities
from utilities.input_handlers import handle_game_keys
from gameworld.sceneManager import SceneManager
from newGame import newGame
from utilities.spellHelp import SpellUtilities
from utilities.common import CommonUtils
from ui.debug import Debug


def game_loop(gameworld):

    # turn zero setup
    game_config = configUtilities.load_config()
    player = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
    terminal.clear()
    setup_gameworld(game_config)

    playing_game = True
    current_scene = 1
    current_turn = 0

    spell_bar_keys = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    message_log_id = MobileUtilities.get_MessageLog_id(gameworld=gameworld, entity=player)
    MobileUtilities.set_view_message_log(gameworld=gameworld, entity=player, view_value=False)

    msg_text = CommonUtils.fire_event("new-game", player_name="Steve")

    msg = Message(text=msg_text, msgclass=0, fg="white", bg="black", fnt="")
    log_message = msg_text
    CommonUtils.add_message(gameworld=gameworld, message=msg, logid=message_log_id, message_for_export=log_message)


    # call scene manager
    game_map = SceneManager.new_scene(currentscene=current_scene, gameworld=gameworld)
    scene_change = False
    # process all intended actions
    gameworld.process(game_config)
    # blit the console
    terminal.refresh()
    current_turn += 1
    MobileUtilities.set_current_turn(gameworld=gameworld, thisturn=current_turn, entity=player)

    while playing_game:
        #
        # scene manager
        #
        if scene_change:
            # call scene manager
            SceneManager.new_scene(currentscene=current_scene, gameworld=gameworld)
            scene_change = False
        #
        # get player action aka their intent to do something
        #
        MobileUtilities.set_view_message_log(gameworld=gameworld, entity=player, view_value=False)
        logger.debug('Starting turn {}', current_turn)
        msglog = MobileUtilities.get_MessageLog_id(gameworld=gameworld, entity=player)

        valid_event = False
        advance_game_turn = False
        event_to_be_processed = ''
        event_action = ''
        logger.debug('Waiting for player to take an action')
        while not valid_event:
            event_to_be_processed, event_action = handle_game_keys()
            if event_to_be_processed not in ('mousemove', None):
                valid_event = True
        logger.debug('Event captured is {} and the value is {}', event_to_be_processed, event_action)
        if event_to_be_processed == 'keypress':
            if event_action == 'quit':
                value = 'exit:true'
                ReplayGame.update_game_replay_file(game_config, value)
                # Externalfiles.write_full_game_log(gameworld=gameworld, log_id=message_log_id)
                raise SystemExit()
            if event_action in ('left', 'right', 'up', 'down'):
                MobileUtilities.set_mobile_velocity(gameworld=gameworld, entity=player, direction=event_action, speed=1)
                advance_game_turn = True
            if event_action in spell_bar_keys:
                SpellUtilities.cast_spell(slot=event_action, gameworld=gameworld, player=player)
                advance_game_turn = True
            if event_action == 'log':
                CommonUtils.set_current_log(gameworld=gameworld, log_entity=msglog)
                advance_game_turn = False
        if event_to_be_processed == 'mouseleftbutton':
            Debug.entity_spy(gameworld=gameworld, game_config=game_config, coords=event_action)
            advance_game_turn = False

        if advance_game_turn:
            #
            # get monsters intended action
            #
            StatelessAI.do_something(gameworld=gameworld, game_config=game_config, player_entity=player, game_map=game_map)
            current_turn += 1
            MobileUtilities.set_current_turn(gameworld=gameworld, thisturn=current_turn, entity=player)
        # process all intended actions
        gameworld.process(game_config)

        # blit the console
        terminal.refresh()


def game_replay(con, game_config):
    ReplayGame.process(con, game_config)


@logger.catch()
def main():

    terminal.open()
    newGame.new_game()


if __name__ == '__main__':
    main()

