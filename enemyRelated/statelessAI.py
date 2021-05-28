from loguru import logger

from components import mobiles
from utilities import configUtilities, formulas, common, gamemap, mobileHelp, scorekeeper, spellHelp
from utilities.ai_utilities import AIUtilities


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
    def gather_surrounding_information(gameworld, game_map, entity):
        # what can I see
        AIUtilities.what_can_i_see_around_me(gameworld=gameworld, source_entity=entity, game_map=game_map)
        # what's my physical state
        am_i_injured = AIUtilities.have_i_taken_damage(gameworld=gameworld, source_entity=entity)

    @staticmethod
    def do_something(gameworld, game_config, player_entity, game_map):
        StatelessAI.gather_surrounding_information(gameworld=gameworld, game_map=game_map, entity=player_entity)


