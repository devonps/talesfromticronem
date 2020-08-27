from loguru import logger

from components import spells
from utilities.input_handlers import handle_game_keys
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

        if len(utility_spells_list) > 0 or len(armour_spells_list) > 0:
            swap_utility_spells(gameworld=gameworld, spells_to_choose_from=available_spells_dict, key_pressed=key_pressed, player_entity=player_entity)


def swap_utility_spells(gameworld, spells_to_choose_from, key_pressed, player_entity):
    # display a list of available spells
    # initially use the keyboard to swap the spell
    # use letters as the selector
    # example:
    # A Signet of the locust
    # B Blood Is Power
    # C Epidemic
    # [ESC] cancel
    start_char = 65
    swap_spells_list = []
    sort_spells_list = []
    valid_keys = []
    utility_slot_to_be_swapped_out = key_pressed - 1

    if 'utility' in spells_to_choose_from:
        utility_spells_list = spells_to_choose_from['utility']
        for a in range(len(utility_spells_list)):
            spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=utility_spells_list[a])
            swap_spells_list.append(chr(start_char) + ' ' + spell_name)
            sort_spells_list.append(spell_name)
            valid_keys.append(chr(start_char))
            start_char += 1

    if 'armour' in spells_to_choose_from:
        armour_spells_list = spells_to_choose_from['armour']
        for a in range(len(armour_spells_list)):
            spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=armour_spells_list[a])
            swap_spells_list.append(chr(start_char) + ' ' + spell_name)
            sort_spells_list.append(spell_name)
            start_char += 1

    swap_spells_list.append('[ESC] Quit')

    # temp code
    for a in range(len(swap_spells_list)):
        logger.debug('spell...{}', swap_spells_list[a])

    swap_mode_is_active = True

    while swap_mode_is_active:
        event_to_be_processed, event_action = handle_game_keys()
        if event_to_be_processed == 'keypress':
            if event_action == 'quit':
                swap_mode_is_active = False
            if event_action != '':
                logger.info('event is {}', event_action)
            if event_action in valid_keys:
                swap_mode_is_active = False
                pos = valid_keys.index(event_action)
                logger.debug('This is in index position {}', pos)
                for ent, (name, desc) in gameworld.get_components(spells.Name, spells.Description):
                    if name.label == sort_spells_list[pos]:
                        logger.warning('Found a spell called {} with an id of {}', name.label, ent)
                        SpellUtilities.set_spellbar_slot(gameworld=gameworld, spell_entity=ent, slot=utility_slot_to_be_swapped_out, player_entity=player_entity)
