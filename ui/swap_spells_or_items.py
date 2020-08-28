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
            available_spells_dict['utility'] = utility_spells_list
        else:
            logger.info('No jewellery equipped')

        armour_spells_list = JewelleryUtilities.get_list_of_spell_entities_for_equipped_armour(gameworld=gameworld,
                                                                                               player_entity=player_entity)
        if len(armour_spells_list) > 0:
            available_spells_dict['armour'] = armour_spells_list
        else:
            logger.info('No armour equipped')

        if len(utility_spells_list) > 0 or len(armour_spells_list) > 0:
            swap_utility_spells(gameworld=gameworld, spells_to_choose_from=available_spells_dict,
                                key_pressed=key_pressed, player_entity=player_entity)


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
        # remove equipped utility spells
        utility_spells_list = remove_already_equipped_utility_spells(gameworld=gameworld, player_entity=player_entity,
                                                                     utility_spells_list=utility_spells_list)

        # now work with only those spells not equipped in slots 6,7,8
        for a in range(len(utility_spells_list)):
            spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=utility_spells_list[a])
            swap_spells_list.append(chr(start_char) + ' ' + spell_name)
            sort_spells_list.append(spell_name)
            valid_keys.append(chr(start_char))
            start_char += 1

    if 'armour' in spells_to_choose_from:
        armour_spells_list = spells_to_choose_from['armour']
        # remove already equipped armour spells
        armour_spells_list = remove_already_equipped_armour_spells(gameworld=gameworld, player_entity=player_entity,
                                                                   armour_spells_list=armour_spells_list)
        for a in range(len(armour_spells_list)):
            spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=armour_spells_list[a])
            swap_spells_list.append(chr(start_char) + ' ' + spell_name)
            sort_spells_list.append(spell_name)
            valid_keys.append(chr(start_char))
            start_char += 1

    swap_spells_list.append('[ESC] Quit')

    swap_mode_is_active = True

    while swap_mode_is_active:
        event_to_be_processed, event_action = handle_game_keys()
        if event_to_be_processed == 'keypress':
            if event_action == 'quit':
                swap_mode_is_active = False
            if event_action in valid_keys:
                swap_mode_is_active = False
                pos = valid_keys.index(event_action)
                swap_the_spell(gameworld=gameworld, pos=pos, sort_spells_list=sort_spells_list,
                               utility_slot_to_be_swapped_out=utility_slot_to_be_swapped_out,
                               player_entity=player_entity)


def swap_the_spell(gameworld, pos, sort_spells_list, utility_slot_to_be_swapped_out, player_entity):
    for ent, (name, desc) in gameworld.get_components(spells.Name, spells.Description):
        if name.label == sort_spells_list[pos]:
            SpellUtilities.set_spellbar_slot(gameworld=gameworld, spell_entity=ent,
                                             slot=utility_slot_to_be_swapped_out,
                                             player_entity=player_entity)


def remove_already_equipped_utility_spells(gameworld, player_entity, utility_spells_list):
    slot6_spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=gameworld, slot=6,
                                                                            player_entity=player_entity)
    slot7_spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=gameworld, slot=7,
                                                                            player_entity=player_entity)
    slot8_spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=gameworld, slot=8,
                                                                            player_entity=player_entity)

    if slot6_spell_entity in utility_spells_list:
        utility_spells_list.remove(slot6_spell_entity)

    if slot7_spell_entity in utility_spells_list:
        utility_spells_list.remove(slot7_spell_entity)

    if slot8_spell_entity in utility_spells_list:
        utility_spells_list.remove(slot8_spell_entity)

    return utility_spells_list


def remove_already_equipped_armour_spells(gameworld, player_entity, armour_spells_list):
    slot6_spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=gameworld, slot=6,
                                                                            player_entity=player_entity)
    slot7_spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=gameworld, slot=7,
                                                                            player_entity=player_entity)
    slot8_spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=gameworld, slot=8,
                                                                            player_entity=player_entity)

    if slot6_spell_entity in armour_spells_list:
        armour_spells_list.remove(slot6_spell_entity)

    if slot7_spell_entity in armour_spells_list:
        armour_spells_list.remove(slot7_spell_entity)

    if slot8_spell_entity in armour_spells_list:
        armour_spells_list.remove(slot8_spell_entity)

    return armour_spells_list
