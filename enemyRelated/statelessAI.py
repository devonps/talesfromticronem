from loguru import logger

from components import mobiles
from utilities import configUtilities
from utilities.ai_utilities import AIUtilities
from utilities.mobileHelp import MobileUtilities


class StatelessAI:
    """
    The AI I'm looking to build out here in pseudo code is:
        Intrnsic pointers (things the enemy knows about itself)
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
    def update_entity_with_local_information(gameworld, game_map, entity):
        # what can I see
        AIUtilities.what_can_i_see_around_me(gameworld=gameworld, source_entity=entity, game_map=game_map)
        # what's my physical state
        AIUtilities.have_i_taken_damage(gameworld=gameworld, source_entity=entity)

    @staticmethod
    def do_something(gameworld, game_config, player_entity, game_map):
        mobile_ai_level = configUtilities.get_config_value_as_integer(configfile=game_config, section='game',
                                                                      parameter='AI_LEVEL_MONSTER')
        ai_debug = True
        for entity, ai in gameworld.get_component(mobiles.AILevel):
            entity_ai = MobileUtilities.get_mobile_ai_level(gameworld=gameworld, entity_id=entity)
            if entity_ai == mobile_ai_level:
                entity_names = MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=entity)
                ai_debugging_first_name = entity_names[0]
                StatelessAI.update_entity_with_local_information(gameworld=gameworld, entity=entity, game_map=game_map)
                have_i_taken_damage = MobileUtilities.get_mobile_physical_hurt_status(gameworld=gameworld, entity=entity)
                what_entities_can_i_see_around_me = MobileUtilities.get_visible_entities(gameworld=gameworld, target_entity=entity)
                if ai_debug:
                    StatelessAI.dump_ai_debugging_information(gameworld=gameworld, ai_debugging_first_name=ai_debugging_first_name, what_entities_can_i_see_around_me=what_entities_can_i_see_around_me, have_i_taken_damage=have_i_taken_damage)
                # what next?

    @staticmethod
    def dump_ai_debugging_information(gameworld, ai_debugging_first_name, what_entities_can_i_see_around_me, have_i_taken_damage):
        visible_entity_names = []
        if len(what_entities_can_i_see_around_me) > 0:
            for a in range(len(what_entities_can_i_see_around_me)):
                entity_names = MobileUtilities.get_mobile_name_details(gameworld=gameworld,
                                                                       entity=what_entities_can_i_see_around_me[a])
                mobile_first_name = entity_names[0]
                visible_entity_names.append(mobile_first_name)

        logger.debug('=== AI Debugging information ===')
        logger.info('mobile AI name: {}', ai_debugging_first_name)
        logger.info('mobile intrinsic information')
        damage_string = 'Has mobile taken damage:'
        if have_i_taken_damage:
            damage_status = ' yes'
        else:
            damage_status = ' no'
        logger.info(damage_string + damage_status)
        logger.info('What can the mobile see around them')
        logger.info('list of entities: {}', visible_entity_names)



