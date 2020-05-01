from loguru import logger

from components import mobiles
from utilities import configUtilities
from utilities.mobileHelp import MobileUtilities
from utilities.spellHelp import SpellUtilities


class StatelessAI:
    """
    The AI I'm looking to build out here in pseudo code is:
        Intrnsic pointers (things the enemy knows about itself)
        damage taken --> do I need to refine this further?
        morale --> what is this?

        can-run-away-from-player --> am I under the effects of immobilize or cripple
        can-attack-player --> am I able to cast a spell
        too-far-from-player --> Am I further away from the player than my max spell range
        can-move-toward-player --> am I under the effects of immobilize or cripple or fear
        charge-probability --> should I keep walking or attack the player
        too-close-to-character --> am I too close to the player
        can-move-away-from-player --> am I under the effects of immobilize or cripple
        retreat-probability --> should I walk or flee from the player
        stand-still --> what should I do here?
    """

    @staticmethod
    def do_something(gameworld, game_config, player_entity):

        mobile_ai_level = configUtilities.get_config_value_as_integer(configfile=game_config, section='game',
                                                                      parameter='AI_LEVEL_MONSTER')

        current_turn = MobileUtilities.get_current_turn(gameworld=gameworld, entity=player_entity)
        message_log_id = MobileUtilities.get_MessageLog_id(gameworld=gameworld, entity=player_entity)

        for ent, ai in gameworld.get_component(mobiles.AI):
            entity_ai = MobileUtilities.get_mobile_ai_level(gameworld=gameworld, entity_id=ent)
            if entity_ai == mobile_ai_level:
                entity_names = MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=ent)
                current_health = MobileUtilities.get_derived_current_health(gameworld=gameworld, entity=ent)
                current_morale = 25
                can_i_move_away_from_the_target = MobileUtilities.can_i_move_away_from_the_target(gameworld=gameworld, source_entity=player_entity)
                can_i_cast_a_spell, spell_to_cast, spell_bar_slot_id = SpellUtilities.can_mobile_cast_a_spell(gameworld=gameworld, entity_id=ent)

                am_i_too_far_from_the_target_to_cast_a_spell = False
                can_i_move_towards_the_target = True
                should_i_charge_the_target = False

                am_i_too_close_to_the_target_to_cast_a_spell = False
                should_i_retreat_from_the_target = False

                if current_health < current_morale:
                    if can_i_move_away_from_the_target:
                        # run away from target (stupid for now)
                        logger.info('on turn {}: {} decided to move away', current_turn, entity_names[0])
                        MobileUtilities.set_direction_velocity_away_from_player(gameworld=gameworld,
                                                                                game_config=game_config,
                                                                                enemy_entity=ent)
                    elif can_i_cast_a_spell:
                        # cast a spell
                        logger.info('on turn {}: {} decided to cast spell entity {}', current_turn, entity_names[0],
                                    spell_to_cast)
                    else:
                        # stand still
                        logger.info('on turn {}: {} was too scared to run away or cast a spell', current_turn,
                                    entity_names[0])
                elif am_i_too_far_from_the_target_to_cast_a_spell:
                    if can_i_move_towards_the_target:
                        if should_i_charge_the_target:
                            # charge the player
                            logger.info('on turn {}: {} decided to charge the player', current_turn, entity_names[0])
                            MobileUtilities.set_direction_velocity_towards_player(gameworld=gameworld,
                                                                                  game_config=game_config,
                                                                                  enemy_entity=ent)
                        else:
                            # move towards the player
                            logger.info('on turn {}: {} decided to move towards the player', current_turn,
                                        entity_names[0])
                            MobileUtilities.set_direction_velocity_towards_player(gameworld=gameworld,
                                                                                  game_config=game_config,
                                                                                  enemy_entity=ent)
                elif am_i_too_close_to_the_target_to_cast_a_spell:
                    if can_i_move_away_from_the_target:
                        if should_i_retreat_from_the_target:
                            # retreat from the player
                            logger.info('on turn {}: {} decided to retreat from the player', current_turn,
                                        entity_names[0])
                            MobileUtilities.set_direction_velocity_away_from_player(gameworld=gameworld,
                                                                                    game_config=game_config,
                                                                                    enemy_entity=ent)
                        else:
                            # cast a spell
                            logger.info('on turn {}: {} chose not to retreat but to cast a spell', current_turn,
                                        entity_names[0])
                    else:
                        # stand still
                        logger.info('on turn {}: {} stood still and took the punishment', current_turn, entity_names[0])
                elif can_i_cast_a_spell:
                    # cast a spell as I'm in the sweet spot
                    logger.info('on turn {}: {} decided to cast spell entity {}', current_turn, entity_names[0],
                                spell_to_cast)
                    # add component covering spell has been cast
                    gameworld.add_component(player_entity,
                                            mobiles.SpellCast(truefalse=True, spell_entity=spell_to_cast,
                                                              spell_target=player_entity, spell_bar_slot=spell_bar_slot_id, spell_caster=ent))
                    logger.warning('enemy casting: message log id is {}', message_log_id)
                    SpellUtilities.helper_add_valid_target_to_message_log(gameworld=gameworld, target_name='player', player_not_pressed_a_key=False)
                else:
                    # stand still
                    logger.info('on turn {}: {} really didnt know what to do', current_turn, entity_names[0])
            else:
                # not the right entity
                pass