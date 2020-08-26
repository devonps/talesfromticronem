from loguru import logger

from utilities.spellHelp import SpellUtilities


def swap_spells(gameworld, player_entity):
    list_of_utility_spells = SpellUtilities.get_list_of_utility_spells_for_player(gameworld=gameworld, player_entity=player_entity)

    # temp code - for testing purposes only
    logger.debug('Utility spells for player are {}', list_of_utility_spells)
    for a in range(len(list_of_utility_spells)):
        spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=list_of_utility_spells[a])
        logger.info('Utility Spell Name is {}', spell_name)
