from loguru import logger

from utilities.jewelleryManagement import JewelleryUtilities
from utilities.mobileHelp import MobileUtilities
from utilities.spellHelp import SpellUtilities
from utilities.weaponManagement import WeaponUtilities


def swap_spells(gameworld, player_entity, key_pressed):
    if key_pressed in [7, 8, 9]:
        # I need to limit this swap based on what the player has access to...
        # I need to check both armour and jewellery equipped
        # from that I can build a list of available spells to swap out
        utility_spells_list = JewelleryUtilities.get_list_of_spell_entities_for_equpped_jewellery(gameworld=gameworld, player_entity=player_entity)

        if len(utility_spells_list) > 0:
            # temp code - for testing purposes only
            logger.debug('Utility spells for player are {}', utility_spells_list)
            for a in range(len(utility_spells_list)):
                spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=utility_spells_list[a])
                logger.info('Utility Spell Name/id{} / {}', spell_name, utility_spells_list[a])
        else:
            logger.info('No jewellery equipped')

    if key_pressed in [1, 2, 3, 4, 5]:
        weapons_equipped_list = MobileUtilities.get_weapons_equipped(gameworld=gameworld, entity=player_entity)
        dual_wielded_weapon_id = weapons_equipped_list[2]
        weapon_type = WeaponUtilities.get_weapon_type(gameworld=gameworld, weapon_entity=dual_wielded_weapon_id)
        list_of_weapon_spells = SpellUtilities.get_list_of_weapon_spells_for_player(gameworld=gameworld, player_entity=player_entity, weapon_type=weapon_type)
        # temp code - for testing purposes only
        logger.debug('Combat spells for player are {}', list_of_weapon_spells)
        for a in range(len(list_of_weapon_spells)):
            spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=list_of_weapon_spells[a])
            logger.info('Utility Spell Name is {}', spell_name)

def swap_utility_spells():
    pass