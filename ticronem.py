import tcod.console
import tcod.event

from bearlibterminal import terminal

from components import items
from newGame.ClassWeapons import WeaponClass
from newGame.Items import ItemManager
from ui.character_screen import display_hero_panel
from newGame.initialiseNewGame import setup_gameworld
from utilities.itemsHelp import ItemUtilities
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

    terminal.composition(terminal.TK_ON)
    terminal.clear()

    setup_gameworld(game_config)


    # create some weapons and drop them on the ground
    class_component = MobileUtilities.get_character_class(gameworld, player)

    created_weapon = ItemManager.create_weapon(gameworld=gameworld, weapon_type='wand', game_config=game_config)
    gameworld.add_component(created_weapon, items.Location(x=0, y=0))
    ItemUtilities.set_item_location(gameworld=gameworld, item_entity=created_weapon, posx=5, posy=2)
    logger.info('Loading the wand with the necessary spells')
    WeaponClass.load_weapon_with_spells(gameworld, created_weapon, 'wand', class_component)

    created_weapon2 = ItemManager.create_weapon(gameworld=gameworld, weapon_type='staff', game_config=game_config)
    gameworld.add_component(created_weapon2, items.Location(x=0, y=0))
    ItemUtilities.set_item_location(gameworld=gameworld, item_entity=created_weapon2, posx=14, posy=7)

    created_weapon3 = ItemManager.create_weapon(gameworld=gameworld, weapon_type='dagger', game_config=game_config)
    gameworld.add_component(created_weapon3, items.Location(x=0, y=0))
    ItemUtilities.set_item_location(gameworld=gameworld, item_entity=created_weapon3, posx=17, posy=12)

    created_weapon4 = ItemManager.create_weapon(gameworld=gameworld, weapon_type='rod', game_config=game_config)
    gameworld.add_component(created_weapon4, items.Location(x=0, y=0))
    ItemUtilities.set_item_location(gameworld=gameworld, item_entity=created_weapon4, posx=7, posy=6)

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

