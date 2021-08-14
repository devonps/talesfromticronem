import random

from loguru import logger

from components import mobiles
from utilities import configUtilities
from utilities.ai_utilities import AIUtilities
from utilities.mobileHelp import MobileUtilities


class StatelessAI:
    """
    The AI I'm looking to build out here in pseudo code is:
        Intrinsic pointers (things the enemy knows about itself)
            damage taken --> do I need to refine this further?
            morale --> hardcoded so they won't naturally retreat
        Questions it needs to answer:
            can-run-away-from-player --> am I under the effects of immobilize or cripple
            can-attack-player --> am I able to cast a spell
            too-far-from-player --> Am I further away from the player than my max spell range
            can-move-toward-player --> am I under the effects of immobilize or cripple or fear
            too-close-to-character --> am I too close to the player
            can-move-away-from-player --> am I under the effects of immobilize or cripple
            can-i-cast-a-spell --> is there one available to me
        Actions to consider:
            stand-still --> what should I do here?
            cast-spell-against-target --> pick a random one

    re-thinking 24th May 2021
    Think big - start small!!
    Have the monster look around: what can it see or hear
    update monster memory based on senses
    What is the physical state of the monster: low health, is it wounded
    Update monster health flags

    Based on the above information, what does the monster want to do?


    """

    @staticmethod
    def update_entity_with_local_information(gameworld, entity):
        # what's my physical state
        AIUtilities.have_i_taken_damage(gameworld=gameworld, source_entity=entity)

    @staticmethod
    def do_something(gameworld, game_config, player_entity, game_map):
        mobile_ai_level = configUtilities.get_config_value_as_integer(configfile=game_config, section='game',
                                                                      parameter='AI_LEVEL_MONSTER')
        for entity, ai in gameworld.get_component(mobiles.AILevel):
            entity_ai = MobileUtilities.get_mobile_ai_level(gameworld=gameworld, entity_id=entity)
            if entity_ai == mobile_ai_level:
                StatelessAI.update_entity_with_local_information(gameworld=gameworld, entity=entity)
                entity_combat_role = MobileUtilities.get_enemy_combat_role(gameworld=gameworld, entity=entity)

                # what next?
                if entity_combat_role != 'none':
                    if entity_combat_role == 'bomber':
                        StatelessAI.perform_ai_for_bomber(monster_entity=entity, game_config=game_config,
                                                          gameworld=gameworld, game_map=game_map,
                                                          player_entity=player_entity)
                    elif entity_combat_role == 'bully':
                        StatelessAI.perform_ai_for_bully(gameworld=gameworld, monster_entity=entity,
                                                         game_config=game_config, game_map=game_map,
                                                         player_entity=player_entity)
                    else:
                        StatelessAI.perform_ai_for_sniper(gameworld=gameworld, monster_entity=entity, game_config=game_config, game_map=game_map, player_entity=player_entity)

    @staticmethod
    def perform_ai_for_bomber(gameworld, monster_entity, game_config, game_map, player_entity):
        # the bomber will use long range AoE spells to attack the player or their allies
        # It will always try to use the heavy damage spells first
        # PSEUDO AI - version 2
        # Get information
        too_close_to_player, too_far_from_player, ideal_distance_from_target = AIUtilities.distance_to_target(
            gameworld=gameworld, source_entity=monster_entity, target_entity=player_entity)

        # set some AI flags
        i_can_cast_a_combat_spell, remaining_spells = AIUtilities.can_i_cast_a_spell(gameworld=gameworld,
                                                                                     entity_id=monster_entity,
                                                                                     target_entity=player_entity)
        # gets a list of entities the monster can see around them
        visible_entities = MobileUtilities.get_ai_visible_entities(gameworld=gameworld, target_entity=monster_entity)
        # is the player (hardcoded target) visible?
        i_can_see_the_player = AIUtilities.is_the_player_visible(player_entity=player_entity,
                                                                 visible_entities=visible_entities)

        target_has_been_attacked = False
        if i_can_see_the_player:
            #
            # if bomber is too close to the target
            #
            if not ideal_distance_from_target:
                AIUtilities.move_towards_or_away_from_target(too_far=too_far_from_player, too_close=too_close_to_player,
                                                             gameworld=gameworld, source_entity=monster_entity,
                                                             target_entity=player_entity)
            else:
                # can I cast a combat spell
                # random.chance('attack', 'move')
                coin_flip = random.randrange(0, 10)
                if coin_flip < 8:
                    # cast a combat spell
                    if i_can_cast_a_combat_spell:
                        target_has_been_attacked = AIUtilities.attack_the_target(player_entity=player_entity,
                                                                                 gameworld=gameworld,
                                                                                 game_map=game_map,
                                                                                 game_config=game_config,
                                                                                 monster_entity=monster_entity)
                    else:
                        # there's no combat spell to cast - but can I / do I need to cast my heal spell
                        AIUtilities.do_something_non_combat(gameworld=gameworld, monster_entity=monster_entity)
                        AIUtilities.let_me_say(gameworld=gameworld,
                                               message='I can see the player but have no combat spells available.')
                        logger.warning('I am out of spells')

                else:
                    # move away from play
                    AIUtilities.move_towards_or_away_from_target(too_far=False,
                                                                 too_close=True, gameworld=gameworld,
                                                                 source_entity=monster_entity,
                                                                 target_entity=player_entity)
        if not target_has_been_attacked:
            # do something non-combat here
            AIUtilities.do_something_non_combat(gameworld=gameworld, monster_entity=monster_entity)

    @staticmethod
    def perform_ai_for_bully(gameworld, monster_entity, game_config, game_map, player_entity):
        # the bully will go toe-to-toe with the player then retreat once damage reaches a threshold
        # to heal and then go back into battle

        # Get information
        too_close_to_player, too_far_from_player, ideal_distance_from_target = AIUtilities.distance_to_target(
            gameworld=gameworld, source_entity=monster_entity, target_entity=player_entity)
        visible_entities = MobileUtilities.get_ai_visible_entities(gameworld=gameworld, target_entity=monster_entity)

        i_can_see_the_player = AIUtilities.is_the_player_visible(player_entity=player_entity,
                                                                 visible_entities=visible_entities)
        ideal_distance_from_target = (not too_far_from_player and not too_close_to_player)

        # can I attack the player from this position and player within attack range
        if i_can_see_the_player:
            if ideal_distance_from_target:
                target_has_been_attacked = AIUtilities.attack_the_target(player_entity=player_entity,
                                                                         gameworld=gameworld, game_map=game_map,
                                                                         game_config=game_config,
                                                                         monster_entity=monster_entity)
                if not target_has_been_attacked:
                    # do something non-combat here
                    AIUtilities.do_something_non_combat(gameworld=gameworld, monster_entity=monster_entity)
            else:
                AIUtilities.move_towards_or_away_from_target(too_far=too_far_from_player, too_close=too_close_to_player,
                                                             gameworld=gameworld, source_entity=monster_entity,
                                                             target_entity=player_entity)

        # no I can't see the player
        else:
            player_last_known_position = MobileUtilities.get_player_last_known_position(gameworld=gameworld,
                                                                                        source_entity=monster_entity)
            # can I move
            i_can_move = AIUtilities.can_i_move(gameworld=gameworld, source_entity=monster_entity)
            if i_can_move and player_last_known_position != (0, 0):
                px = player_last_known_position(0)
                py = player_last_known_position(1)
                AIUtilities.prep_move_to_specific_location(gameworld=gameworld, source_entity=monster_entity, px=px, py=py)

    @staticmethod
    def perform_ai_for_sniper(gameworld, monster_entity, game_config, game_map, player_entity):
        # the sniper stays at a maximum range at all times
        # they will always target the player first
        logger.warning('ALL the way from stateless AI: Sniper role')
        logger.debug('Entity id {}', monster_entity)

        # Get information
        too_close_to_player, too_far_from_player, ideal_distance_from_target = AIUtilities.distance_to_target(
            gameworld=gameworld, source_entity=monster_entity, target_entity=player_entity)
        visible_entities = MobileUtilities.get_ai_visible_entities(gameworld=gameworld, target_entity=monster_entity)
        i_can_see_the_player = AIUtilities.is_the_player_visible(player_entity=player_entity,
                                                                 visible_entities=visible_entities)
        ideal_distance_from_target = (not too_far_from_player and not too_close_to_player)

        # can I attack the player from this position and player within attack range
        if i_can_see_the_player:
            if ideal_distance_from_target:
                target_has_been_attacked = AIUtilities.attack_the_target(player_entity=player_entity,
                                                                         gameworld=gameworld, game_map=game_map,
                                                                         game_config=game_config,
                                                                         monster_entity=monster_entity)
                if not target_has_been_attacked:
                    # do something non-combat here
                    AIUtilities.do_something_non_combat(gameworld=gameworld, monster_entity=monster_entity)
            else:
                AIUtilities.move_towards_or_away_from_target(too_far=too_far_from_player, too_close=too_close_to_player,
                                                             gameworld=gameworld, source_entity=monster_entity,
                                                             target_entity=player_entity)

        # no I can't see the player
        else:
            player_last_known_position = MobileUtilities.get_player_last_known_position(gameworld=gameworld,
                                                                                        source_entity=monster_entity)
            # can I move
            i_can_move = AIUtilities.can_i_move(gameworld=gameworld, source_entity=monster_entity)
            if i_can_move and player_last_known_position != (0, 0):
                px = player_last_known_position(0)
                py = player_last_known_position(1)
                AIUtilities.prep_move_to_specific_location(gameworld=gameworld, source_entity=monster_entity, px=px, py=py)