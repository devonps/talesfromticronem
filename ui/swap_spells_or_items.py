from loguru import logger

from utilities.jewelleryManagement import JewelleryUtilities
from utilities.spellHelp import SpellUtilities


def swap_spells(gameworld, player_entity, key_pressed):
    available_spells_dict = {}
    if key_pressed in [7, 8, 9]:
        # I need to limit this swap based on what the player has access to...
        # I need to check both armour and jewellery equipped
        # from that I can build a list of available spells to swap out
        utility_spells_list = JewelleryUtilities.get_list_of_spell_entities_for_equpped_jewellery(gameworld=gameworld,
                                                                                                  player_entity=player_entity)

        if len(utility_spells_list) > 0:
            # temp code - for testing purposes only
            logger.debug('Utility spells for player are {}', utility_spells_list)
            available_spells_dict['utility'] = utility_spells_list
            for a in range(len(utility_spells_list)):
                spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=utility_spells_list[a])
                logger.info('Utility Spell Name/id {} / {}', spell_name, utility_spells_list[a])
        else:
            logger.info('No jewellery equipped')

        armour_spells_list = JewelleryUtilities.get_list_of_spell_entities_for_equipped_armour(gameworld=gameworld,
                                                                                               player_entity=player_entity)
        if len(armour_spells_list) > 0:
            available_spells_dict['armour'] = armour_spells_list
            # temp code - for testing purposes only
            for a in range(len(armour_spells_list)):
                spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=armour_spells_list[a])
                logger.info('Armour Spell Name/id {} / {}', spell_name, armour_spells_list[a])
        else:
            logger.info('No armour equipped')

        # logger.debug('ALL available spells are {}', available_spells_dict)
        #
        # logger.debug('Utility spells are {}', available_spells_dict['utility'])

        swap_utility_spells(gameworld=gameworld, spells_to_choose_from=available_spells_dict)


def swap_utility_spells(gameworld, spells_to_choose_from):
    # display a list of available spells
    # initially use the keyboard to swap the spell
    # use letters as the selector
    # example:
    # A Signet of the locust
    # B Blood Is Power
    # C Epidemic
    # [ESC] cancel
    utility_spells_list = spells_to_choose_from['utility']
    armour_spells_list = spells_to_choose_from['armour']
    start_char = 65
    swap_spells_list = []

    for a in range(len(utility_spells_list)):
        spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=utility_spells_list[a])
        swap_spells_list.append(chr(start_char) + ' ' + spell_name)
        start_char += 1

    for a in range(len(armour_spells_list)):
        spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=armour_spells_list[a])
        swap_spells_list.append(chr(start_char) + ' ' + spell_name)
        start_char += 1

    # temp code
    for a in range(len(swap_spells_list)):
        logger.debug('spell...{}',swap_spells_list[a] )
