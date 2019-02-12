import tcod

from utilities.externalfileutilities import Externalfiles
from newGame.initialiseNewGame import create_game_world, initialise_game_map, create_new_character, constants,\
    generate_items, generate_monsters, generate_spells
from newGame.newCharacter import generate_player_character, generate_spell_bar, get_starting_equipment
from loguru import logger
from components import mobiles


class ReplayGame:

    @staticmethod
    def process(con):
        game_actions = ReplayGame.get_game_replay_actions()
        ReplayGame.cycle_through_game_actions(con, game_actions)

    @staticmethod
    def cycle_through_game_actions(con, game_actions):

        # create gameworld
        gameworld = create_game_world()
        player = 0
        logger.debug('Actions {}', game_actions)

        for line in game_actions:
            logger.info('each line is {}', line)
            words = line.split(':')
            my_list = [current_word for current_word in words]

            logger.info('the list is {}', my_list)

            for current_word in my_list:
                logger.info('words are {}', current_word)

                # set world seed
                if current_word == 'world_seed':

                    constants.WORLD_SEED = int(my_list[1])

                    logger.info('World seed is now {}', constants.WORLD_SEED)
                    # create spells, items, and monsters --> the things the character will interract with
                    generate_spells(gameworld)
                    generate_items(gameworld)
                    generate_monsters(gameworld)

                    # generate a new character
                    player = generate_player_character(gameworld=gameworld)

                    # create the spell bar
                    spell_bar_entity = generate_spell_bar(gameworld=gameworld)

                    # assign starting equipment
                    get_starting_equipment(con=con, gameworld=gameworld, player=player, spellbar=spell_bar_entity)

                    # initialise and create a new game map
                    initialise_game_map(con=con, gameworld=gameworld, player=player, spell_bar=spell_bar_entity)

                    # clear current console and blit game map
                    tcod.console_clear(con)
                    logger.info('lets kick some ass')
                    logger.info('current word is {}', current_word)
                else:
                    #while not tcod.console_is_window_closed():

                        # carry out game actions

                        if current_word == 'move':
                            # original_player_entity = my_list[1]
                            # logger.info('orig player was {} and this player is {}', original_player_entity, player)
                            player_velocity_component = gameworld.component_for_entity(player, mobiles.Velocity)
                            position_component = gameworld.component_for_entity(player, mobiles.Position)
                            dx = int(my_list[2])
                            dy = int(my_list[3])
                            player_velocity_component.dx += dx
                            player_velocity_component.dy += dy
                            position_component.hasMoved = True
                    #
                    #     if action == 'exit':
                    #         return True
                    #
                    #     # exit_game = action.get('exit')
                    #     # fullscreen = action.get('fullscreen')
                    #     # player_moved = action.get('player_moved')
                    #     #
                    #     # if player_moved:
                    #     #     pass
                    #     #
                    #     # if exit_game:
                    #     #     return True
                    #     #
                    #     # if fullscreen:
                    #     #     tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
                    #
                            # run ALL game processors
                            gameworld.process()
                            tcod.console_flush()


    @staticmethod
    def get_game_replay_actions():

        # game_actions should be created as a list
        game_actions = Externalfiles.load_existing_file(constants.GAME_ACTIONS_FILE)

        return game_actions

