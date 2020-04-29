from loguru import logger

from components import mobiles
from utilities import configUtilities
from utilities.mobileHelp import MobileUtilities


class StatelessAI:
    """
    The AI I'm looking to build out here in pseudo code is:
    If damage > morale
        if can-run-away-from-player
          run-away-from-player
        else if can-attack-player
          attack-player --> shout 'arrrgh I'll never yield'
        else stand-still --> shout for help!
    else if too-far-from-player
        AND can-attack-player
        AND can-move-toward-player
        if  random < charge-probability
         move-toward-player
        else attack-player
    else if too-close-to-character
         AND can-attack-player
         AND can-move-away-from-player
         if random < retreat-probability
            move-away-from-player
         else attack-player
    else if can-attack-player
         attack-player
    else if too-far-from-player
         AND can-move-toward-player
         move-toward-player
    else if too-close-to-player
         AND can-move-away-from-player
         move-away-from-player
    else stand-still

        Intrnsic pointers (things the enemy knows about itself)
        damage taken
        morale

        can-run-away-from-player --> am I under the effects of a spell
        can-attack-player --> am I able to cast a spell AND within spell casting range
        too-far-from-player --> how far away from the target am I
        can-move-toward-player --> am I able to walk towards the player
        charge-probability --> should I keep walking or attack the player
        too-close-to-character --> am I too close to the player
        can-move-away-from-player --> can I move away from the player
        retreat-probability --> should I walk or flee from the player
        stand-still --> what should I do here?
    """
    @staticmethod
    def do_something(gameworld, game_config, player_entity):

        mobile_ai_level = configUtilities.get_config_value_as_integer(configfile=game_config, section='game',
                                                                parameter='AI_LEVEL_MONSTER')

        current_turn = MobileUtilities.get_current_turn(gameworld=gameworld, entity=player_entity)

        for ent, ai in gameworld.get_component(mobiles.AI):
            entity_ai = MobileUtilities.get_mobile_ai_level(gameworld=gameworld, entity_id=ent)
            entity_names = MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=ent)
            current_health = MobileUtilities.get_derived_current_health(gameworld=gameworld, entity=ent)
            current_morale = 25
            can_i_run_from_the_target = False
            can_i_move_towards_the_target = False
            should_i_charge_the_target = False
            can_i_cast_a_spell = False
            am_i_within_spell_range = False
            am_i_too_close_to_the_target = True
            am_i_too_far_from_the_target_to_cast_a_spell = False
            can_i_move_away_from_the_target = False
            should_i_retreat_from_the_target = False

            if entity_ai == mobile_ai_level:
                if current_health < current_morale:
                    if can_i_run_from_the_target:
                        # run away from target (stupid for now)
                        logger.info('on turn {}: {} decided to move away', current_turn, entity_names[0])
                        MobileUtilities.set_mobile_velocity(gameworld=gameworld, entity=ent, direction='down', speed=1)
                    elif can_i_cast_a_spell and am_i_within_spell_range:
                        # cast a spell
                        logger.info('on turn {}: {} decided to cast a random spell', current_turn, entity_names[0])
                    else:
                        # stand still
                        logger.info('on turn {}: {} was too scared to run away or cast a spell', current_turn, entity_names[0])
                elif am_i_too_far_from_the_target_to_cast_a_spell:
                    if can_i_move_towards_the_target:
                        if should_i_charge_the_target:
                            # charge the player
                            logger.info('on turn {}: {} decided to charge the player', current_turn, entity_names[0])
                        else:
                            # move towards the player
                            logger.info('on turn {}: {} decided to move towards the player', current_turn, entity_names[0])
                elif am_i_too_close_to_the_target:
                    if can_i_move_away_from_the_target:
                        if should_i_retreat_from_the_target:
                            # retreat from the player
                            logger.info('on turn {}: {} decided to retreat from the player', current_turn, entity_names[0])
                        else:
                            # cast a spell
                            logger.info('on turn {}: {} chose not to retreat but to cast a spell', current_turn, entity_names[0])
                elif can_i_cast_a_spell:
                    # cast a spell
                    logger.info('on turn {}: {} decided to cast a spell', current_turn, entity_names[0])
                elif am_i_too_far_from_the_target_to_cast_a_spell:
                    # move towards the player
                    logger.info('on turn {}: {} decided to skip towards the player', current_turn, entity_names[0])
                elif am_i_too_close_to_the_target:
                    # move from the player
                    logger.info('on turn {}: {} decided to move from the player', current_turn, entity_names[0])
                else:
                    # stand still
                    logger.info('on turn {}: {} really didnt know what to do', current_turn, entity_names[0])

