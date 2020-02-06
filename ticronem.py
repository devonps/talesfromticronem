from bearlibterminal import terminal

from components import mobiles
from components.messages import Message
from ui.character_screen import display_hero_panel
from newGame.initialiseNewGame import setup_gameworld
from utilities.common import CommonUtils
from utilities.mobileHelp import MobileUtilities
from utilities.replayGame import ReplayGame
from loguru import logger
from utilities import configUtilities
from utilities.input_handlers import handle_game_keys, which_ui_hotspot_was_clicked
from gameworld.sceneManager import SceneManager
from newGame import newGame
from utilities.spellHelp import SpellUtilities


def game_loop(gameworld):

    game_config = configUtilities.load_config()
    player = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)

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
        message_log_id = MobileUtilities.get_MessageLog_id(gameworld=gameworld, entity=player)
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
                hotspot_clicked = which_ui_hotspot_was_clicked(mx=event_action[0], my=event_action[1])

                if 0 <= hotspot_clicked <= 9:
                    spellbarId = MobileUtilities.get_spellbar_id_for_entity(gameworld=gameworld, entity=player)
                    spell_entity = SpellUtilities.get_spell_bar_slot_componet(gameworld=gameworld, spell_bar=spellbarId, slotid=hotspot_clicked + 1)
                    spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=spell_entity.id)
                    msg = Message(text="Spell:" + spell_name + " activated.", msgclass="all", fg="red", bg="white",
                                  fnt="")
                    CommonUtils.add_message(gameworld=gameworld, message=msg, logid=message_log_id)

                if hotspot_clicked == 10:
                    msglog = MobileUtilities.get_MessageLog_id(gameworld=gameworld, entity=player)
                    CommonUtils.set_visible_log(gameworld=gameworld, logid=msglog, logToDisplay="all")

                if hotspot_clicked == 11:
                    msglog = MobileUtilities.get_MessageLog_id(gameworld=gameworld, entity=player)
                    CommonUtils.set_visible_log(gameworld=gameworld, logid=msglog, logToDisplay="combat")

                if hotspot_clicked == 12:
                    msglog = MobileUtilities.get_MessageLog_id(gameworld=gameworld, entity=player)
                    CommonUtils.set_visible_log(gameworld=gameworld, logid=msglog, logToDisplay="story")

                if hotspot_clicked == 13:
                    msglog = MobileUtilities.get_MessageLog_id(gameworld=gameworld, entity=player)
                    CommonUtils.set_visible_log(gameworld=gameworld, logid=msglog, logToDisplay="personal")

                # check for entity at location

                for ent, (pos, name) in gameworld.get_components(mobiles.Position, mobiles.Name):
                    if pos.x == event_action[0] and pos.y == event_action[1]:
                        msg = Message(text="Enemy called " + name.first + " targetted.", msgclass="all", fg="yellow", bg="", fnt="")
                        CommonUtils.add_message(gameworld=gameworld, message=msg, logid=message_log_id)

        #
        # get monsters intended action
        #

        # run ALL game processors
        gameworld.process(game_config)
        # blit the console
        terminal.refresh()


def game_replay(con, game_config):
    ReplayGame.process(con, game_config)


@logger.catch()
def main():

    # LoadPrefab.loadPrefab()
    terminal.open()
    newGame.new_game()


if __name__ == '__main__':
    main()

