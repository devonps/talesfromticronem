from bearlibterminal import terminal

from components import mobiles
from enemyRelated.statelessAI import StatelessAI
from newGame import initialiseNewGame, GameOver, newGame
from utilities import mobileHelp, dialogUtilities, replayGame, configUtilities, input_handlers, common, scorekeeper, \
    spellHelp
from ui import swap_spells_or_items, debug, items_and_spells_info_panel
from loguru import logger
from gameworld.sceneManager import SceneManager


def game_loop(gameworld):
    # turn zero setup
    game_turn = 0
    game_config = configUtilities.load_config()
    player = mobileHelp.MobileUtilities.get_player_entity(gameworld=gameworld)
    terminal.clear()
    initialiseNewGame.setup_gameworld(game_config)

    playing_game = True
    current_scene = 1
    player_died = False

    spell_bar_keys = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    movement_actions = ['left', 'right', 'up', 'down']
    mobileHelp.MobileUtilities.set_view_message_log(gameworld=gameworld, entity=player, view_value=False)

    player_name = mobileHelp.MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=player)
    player_race = mobileHelp.MobileUtilities.get_mobile_race_details(gameworld=gameworld, entity=player)
    player_class = mobileHelp.MobileUtilities.get_character_class(gameworld=gameworld, entity=player)
    common.CommonUtils.fire_event("new-game", gameworld=gameworld, player_name=player_name[0],
                                  player_class=player_class, player_race=player_race[3])

    # call scene manager
    mobileHelp.MobileUtilities.set_player_current_scene(gameworld=gameworld, current_scene=current_scene,
                                                        player_entity=player)
    mobileHelp.MobileUtilities.set_player_current_scene_exit(gameworld=gameworld, scene_exit=1, player_entity=player)
    mobileHelp.MobileUtilities.set_player_scene_change(gameworld=gameworld, player_entity=player, value=True)
    advance_game_turn = False

    spell_list2 = spellHelp.SpellUtilities.get_current_spellbar_spells(gameworld=gameworld, player_entity=player)

    # generate meta events for spells loaded into spell bar - at this point it is weapons + class health spell
    current_area_tag = scorekeeper.ScorekeeperUtilities.get_current_area(gameworld=gameworld)
    for spell_entity in spell_list2:
        if spell_entity > 0:
            spell_name = spellHelp.SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=spell_entity)
            updated_spell_name = spell_name.replace(" ", "_")
            updated_spell_name = current_area_tag + '_' + updated_spell_name + "_cast"
            scorekeeper.ScorekeeperUtilities.register_scorekeeper_meta_event(gameworld=gameworld,
                                                                             event_name=updated_spell_name.lower(),
                                                                             event_starting_value=0)

    scorekeeper.ScorekeeperUtilities.register_scorekeeper_meta_event(gameworld=gameworld, event_name='game_turn',
                                                                     event_starting_value=1)

    while playing_game:
        #
        # scene manager
        #
        scene_change = mobileHelp.MobileUtilities.get_player_scene_change(gameworld=gameworld, player_entity=player)
        if scene_change:
            advance_game_turn = False
            new_scene = mobileHelp.MobileUtilities.get_player_current_scene_exit(gameworld=gameworld,
                                                                                 player_entity=player)
            logger.debug('Changing to scene {}', new_scene)
            # call scene manager
            game_map, scene_exits = SceneManager.new_scene(currentscene=new_scene, gameworld=gameworld)

            if scene_exits == 0:
                logger.warning('No valid scene exits from current scene')
            else:
                logger.debug('CURRENT SCENE EXIT IS {}', scene_exits)

            mobileHelp.MobileUtilities.set_player_scene_change(gameworld=gameworld, player_entity=player, value=False)
            current_area_tag = scorekeeper.ScorekeeperUtilities.get_current_area(gameworld=gameworld)
            # register damage types for this area
            scorekeeper.ScorekeeperUtilities.register_damage_types_for_current_area(gameworld=gameworld,
                                                                                    current_area_tag=current_area_tag)
            meta_events = scorekeeper.ScorekeeperUtilities.get_list_of_meta_events(gameworld=gameworld)
            logger.warning('list of meta events:{}', meta_events)

        # blit the console
        gameworld.process(game_config, advance_game_turn)
        terminal.refresh()
        #
        # get player action aka their intent to do something
        #
        mobileHelp.MobileUtilities.set_view_message_log(gameworld=gameworld, entity=player, view_value=False)
        msglog = mobileHelp.MobileUtilities.get_MessageLog_id(gameworld=gameworld, entity=player)

        valid_event = False
        advance_game_turn = False
        event_to_be_processed = None
        event_action = None
        logger.warning('=== STARTING TURN: {}===', game_turn)
        while not valid_event:
            event_to_be_processed, event_action = input_handlers.handle_game_keys()
            if event_to_be_processed not in ('mousemove', None):
                valid_event = True
        if event_to_be_processed == 'keypress':
            if event_action == 'quit':
                value = 'exit:true'
                replayGame.ReplayGame.update_game_replay_file(value)
                # Externalfiles.write_full_game_log(gameworld=gameworld, log_id=message_log_id)
                playing_game = False
                logger.info('Player has quit the game.')
            if event_action in movement_actions:
                mobileHelp.MobileUtilities.set_mobile_velocity(gameworld=gameworld, entity=player,
                                                               direction=event_action, speed=1)
                advance_game_turn = True
                logger.info('Player moved')
            if event_action in spell_bar_keys:
                spellHelp.SpellUtilities.cast_spell(slot=event_action, gameworld=gameworld, player=player,
                                                    game_map=game_map)
                advance_game_turn = True
                logger.info('Player cast spell')

            if event_action == 'log':
                common.CommonUtils.set_current_log(gameworld=gameworld, log_entity=msglog)
                advance_game_turn = False
        if event_to_be_processed == 'chat':
            logger.debug('Chat inititiated.')
            dialogUtilities.initiate_dialog(gameworld=gameworld, game_config=game_config)
            advance_game_turn = False
        if event_to_be_processed == 'infopopup' and event_action is not None:
            logger.debug('Information needed on item {}', event_action)
            items_and_spells_info_panel.display_spell_info_popup(menu_selection=event_action, gameworld=gameworld,
                                                                 player_entity=player)
            advance_game_turn = False
        if event_to_be_processed == 'swap' and event_action is not None:
            swap_spells_or_items.swap_spells(gameworld=gameworld, player_entity=player, key_pressed=event_action)
            advance_game_turn = True
            logger.info('Player swapped an item')

        if event_to_be_processed == 'mouseleftbutton':
            debug.Debug.entity_spy(gameworld=gameworld, game_config=game_config, coords_clicked=event_action,
                                   game_map=game_map)
            advance_game_turn = False
        if event_to_be_processed == 'death':
            gameworld.component_for_entity(player, mobiles.DerivedAttributes).current_health = -1
            advance_game_turn = True
            logger.info('Player died')

        if advance_game_turn:
            #
            # get monsters intended action
            #
            StatelessAI.do_something(gameworld=gameworld, game_config=game_config, player_entity=player,
                                     game_map=game_map)
            scorekeeper.ScorekeeperUtilities.increase_meta_event_by_value(gameworld=gameworld, event_name='game_turn',
                                                                          value=1)
            game_turn += 1
        # now check if the player is still alive
        current_health = mobileHelp.MobileUtilities.get_mobile_derived_current_health(gameworld=gameworld,
                                                                                      entity=player)
        # if the player is dead then end the game
        if current_health <= 0:
            playing_game = False
            player_died = True

    # player has died or quit the game
    GameOver.GameOver.process_game_over(player_died=player_died, gameworld=gameworld)
    raise SystemExit()


@logger.catch()
def main():
    terminal.open()
    newGame.new_game()


if __name__ == '__main__':
    main()
