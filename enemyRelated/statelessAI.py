import random

from loguru import logger

from components import mobiles
from utilities import configUtilities, common
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
                    if entity_combat_role == 'squealer':
                        StatelessAI.perform_ai_for_squealer(entity=entity)
                    elif entity_combat_role == 'bomber':
                        StatelessAI.perform_ai_for_bomber(monster_entity=entity, game_config=game_config,
                                                          gameworld=gameworld, game_map=game_map,
                                                          player_entity=player_entity)
                    elif entity_combat_role == 'bully':
                        StatelessAI.perform_ai_for_bully(entity=entity)
                    else:
                        StatelessAI.perform_ai_for_sniper(entity=entity)

    @staticmethod
    def dump_ai_debugging_information(gameworld, ai_debugging_first_name, target_entity, entity_combat_role):
        visible_entities = MobileUtilities.get_visible_entities(gameworld=gameworld, target_entity=target_entity)
        vision_range = MobileUtilities.get_mobile_senses_vision_range(gameworld=gameworld, entity=target_entity)

        visible_entity_names = []
        if len(visible_entities) > 0:
            for a in range(len(visible_entities)):
                entity_names = MobileUtilities.get_mobile_name_details(gameworld=gameworld,
                                                                       entity=visible_entities[a])
                mobile_first_name = entity_names[0]
                visible_entity_names.append(mobile_first_name)

        logger.debug('=== AI Debugging information ===')
        logger.info('mobile AI name: {}', ai_debugging_first_name)
        logger.info('mobile AI combat role: {}', entity_combat_role)
        logger.info('mobile intrinsic information')
        damage_string = 'Has mobile taken damage:'
        damage_status = ' no'
        logger.info(damage_string + damage_status)
        logger.info('mobile vision range: {}', vision_range)
        logger.info('What can the mobile see around them')
        logger.info('list of entities: {}', visible_entity_names)

    @staticmethod
    def perform_ai_for_squealer(entity):
        # a squealer will always run away from the player and their allies
        # additionally it will alert other enemies of the player
        logger.warning('ALL the way from stateless AI: Squealer role')
        logger.debug('Entity id {}', entity)

    @staticmethod
    def perform_ai_for_bomber(gameworld, monster_entity, game_config, game_map, player_entity):
        # the bomber will use long range AoE spells to attack the player or their allies
        # It will always try to use the heavy damage spells first
        # PSEUDO AI - version 2
        # entity_names = MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=entity)
        # ai_debugging_first_name = entity_names[0]
        # StatelessAI.dump_ai_debugging_information(gameworld=gameworld,
        #                                           ai_debugging_first_name=ai_debugging_first_name,
        #                                           target_entity=entity,
        #                                           entity_combat_role='bomber')
        logger.warning('ALL the way from stateless AI: Bomber role')
        # Get information
        i_can_move = AIUtilities.can_i_move(gameworld=gameworld, source_entity=monster_entity)
        min_attack_range = MobileUtilities.get_enemy_preferred_min_range(gameworld=gameworld, entity=monster_entity)
        max_attack_range = MobileUtilities.get_enemy_preferred_max_range(gameworld=gameworld, entity=monster_entity)
        monster_is_hurt = MobileUtilities.get_mobile_physical_hurt_status(gameworld=gameworld, entity=monster_entity)

        # set some AI flags
        i_can_cast_a_combat_spell, remaining_spells, _ = AIUtilities.can_i_cast_a_spell(gameworld=gameworld,
                                                                                        entity_id=monster_entity,
                                                                                        target_entity=player_entity)
        # gets a list of entities the monster can see around them
        visible_entities = MobileUtilities.get_visible_entities(gameworld=gameworld, target_entity=monster_entity)
        # is the player (hardcoded target) visible?
        if player_entity in visible_entities:
            i_can_see_the_player = True
        else:
            i_can_see_the_player = False

        if i_can_see_the_player:
            dist_to_target = AIUtilities.can_i_see_my_target(gameworld=gameworld, from_entity=monster_entity,
                                                             to_entity=player_entity)

            # based on the distance to the target what should the bomber do?
            if dist_to_target < min_attack_range:
                too_close_to_player = True
            else:
                too_close_to_player = False

            if dist_to_target > max_attack_range:
                too_far_from_player = True
            else:
                too_far_from_player = False

            #
            # if bomber is too close to the target
            #
            if too_close_to_player:
                # if bomber can move
                # move away from target
                if i_can_move:
                    AIUtilities.move_away_from_target(gameworld=gameworld, target_entity=player_entity,
                                                      source_entity=monster_entity)
                    common.CommonUtils.fire_event('dialog-general', gameworld=gameworld,
                                                  dialog='Too close for me, time to back off')
                else:
                    # can I cast a spell
                    if i_can_cast_a_combat_spell:
                        spell_to_cast = AIUtilities.pick_a_spell_to_cast(gameworld=gameworld, entity_id=monster_entity,
                                                                         remaining_spells=remaining_spells,
                                                                         player_entity=player_entity)
                        if spell_to_cast != 'no spell':
                            spell_cast_message = 'I will cast ' + spell_to_cast
                            AIUtilities.cast_a_spell(gameworld=gameworld, game_config=game_config,
                                                     enemy_list=[player_entity], player_entity=player_entity,
                                                     game_map=game_map, spell_has_aoe=False)
                            AIUtilities.let_me_say(gameworld=gameworld, message=spell_cast_message)
                    else:
                        # there's no combat spell to cast - but can I / do I need to cast my heal spell
                        AIUtilities.let_me_say(gameworld=gameworld,
                                               message='I can see the player but have no combat spells available.')
                        logger.warning('There is no spell to cast, remaining {}', remaining_spells)
                        if monster_is_hurt:
                            AIUtilities.let_me_say(gameworld=gameworld, message='I am hurting, medic!')

            #
            # If bomber is out of range to attack
            #
            if too_far_from_player:
                #  if bomber can move
                if i_can_move:
                    # move towards player
                    AIUtilities.move_towards_target(gameworld=gameworld, target_entity=player_entity,
                                                    source_entity=monster_entity)
                    AIUtilities.let_me_say(gameworld=gameworld, message='Time to get hustling.')
                # else
                else:
                    # do something non-combat here
                    if monster_is_hurt:
                        AIUtilities.let_me_say(gameworld=gameworld, message='I am hurting, medic!')
                    else:
                        AIUtilities.let_me_say(gameworld=gameworld, message='I feel good!')

            #
            # if bomber is in the middle ground of distance to the target
            #
            if not too_close_to_player and not too_far_from_player:
                # random.chance('attack', 'move')
                coin_flip = random.randint(0, 1)
                if coin_flip < 0.5:
                    # if random.chance('attack')
                    # cast a combat spell
                    if i_can_cast_a_combat_spell:
                        spell_to_cast = AIUtilities.pick_a_spell_to_cast(gameworld=gameworld, entity_id=monster_entity,
                                                                         remaining_spells=remaining_spells,
                                                                         player_entity=player_entity)
                        if spell_to_cast != 'no spell':
                            AIUtilities.cast_a_spell(gameworld=gameworld, game_config=game_config,
                                                     enemy_list=[player_entity], player_entity=player_entity,
                                                     game_map=game_map, spell_has_aoe=False)
                            AIUtilities.let_me_say(gameworld=gameworld, message='I will cast ' + spell_to_cast)
                        else:
                            AIUtilities.let_me_say(gameworld=gameworld, message='coin flip said cast a spell but could not')
                    else:
                        # there's no combat spell to cast - but can I / do I need to cast my heal spell
                        AIUtilities.let_me_say(gameworld=gameworld,
                                               message='I can see the player but have no combat spells available.')
                        logger.warning('I am out of spells')
                        if monster_is_hurt:
                            AIUtilities.let_me_say(gameworld=gameworld, message='Medic!')
                        else:
                            AIUtilities.let_me_say(gameworld=gameworld, message='Perfect distance, coin flip says attack, not hurt')

                else:
                    # move away from play
                    AIUtilities.move_away_from_target(gameworld=gameworld, target_entity=player_entity,
                                                      source_entity=monster_entity)
                    AIUtilities.let_me_say(gameworld=gameworld, message='coin flip says move away from the player!')

    @staticmethod
    def perform_ai_for_bully(entity):
        # the bully will got toe-to-toe with the player then retreat once damage reaches a threshold
        # to heal and then go back into battle
        logger.warning('ALL the way from stateless AI: Bully role')
        logger.debug('Entity id {}', entity)

    @staticmethod
    def perform_ai_for_sniper(entity):
        # the sniper stays at a maximum range at all times
        # they will always target the player first
        logger.warning('ALL the way from stateless AI: Sniper role')
        logger.debug('Entity id {}', entity)
