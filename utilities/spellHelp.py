from loguru import logger
from components import spells, weapons, spellBar, items
from utilities.mobileHelp import MobileUtilities


class SpellUtilities:

    def get_spell_name_in_weapon_slot(gameworld, weapon_equipped, slotid):
        """
        Returns the spell name from weapon slot
        :param weapon_equipped:
        :param slotid:
        :return:
        """
        spell_name = 'no spell'
        spell = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld, weapon_equipped, slotid)
        if spell > 0:
            spell_name = gameworld.component_for_entity(spell, spells.Name).label

        return spell_name

    def get_spell_entity_at_weapon_slot(gameworld, weapon_equipped, slotid):

        spell_entity = 0

        if slotid == 1:
            spell_entity = gameworld.component_for_entity(weapon_equipped, items.Spells).slot_one
        if slotid == 2:
            spell_entity = gameworld.component_for_entity(weapon_equipped, items.Spells).slot_two
        if slotid == 3:
            spell_entity = gameworld.component_for_entity(weapon_equipped, items.Spells).slot_three
        if slotid == 4:
            spell_entity = gameworld.component_for_entity(weapon_equipped, items.Spells).slot_four
        if slotid == 5:
            spell_entity = gameworld.component_for_entity(weapon_equipped, items.Spells).slot_five

        return spell_entity

    def populate_spell_bar_from_weapon(gameworld, player_entity, spellbar):

        # this method takes each of the spells 'loaded into the weapon' and 'loads them into the spellbar entity'

        weapons_equipped = MobileUtilities.get_weapons_equipped(gameworld=gameworld, entity=player_entity)

        # are there any weapons equippped
        if len(weapons_equipped) == 0:
            logger.debug('no weapons equipped for player')

        main_hand_weapon = weapons_equipped[0]
        off_hand_weapon = weapons_equipped[1]
        both_hands_weapon = weapons_equipped[2]

        if both_hands_weapon > 0:
            this_spell_entity = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld,weapon_equipped=both_hands_weapon, slotid=1)
            gameworld.component_for_entity(spellbar, spellBar.SlotOne).id = this_spell_entity
            this_spell_entity = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld,weapon_equipped=both_hands_weapon, slotid=2)
            gameworld.component_for_entity(spellbar, spellBar.SlotTwo).id = this_spell_entity
            this_spell_entity = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld,weapon_equipped=both_hands_weapon, slotid=3)
            gameworld.component_for_entity(spellbar, spellBar.SlotThree).id = this_spell_entity
            this_spell_entity = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld,weapon_equipped=both_hands_weapon, slotid=4)
            gameworld.component_for_entity(spellbar, spellBar.SlotFour).id = this_spell_entity
            this_spell_entity = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld,weapon_equipped=both_hands_weapon, slotid=5)
            gameworld.component_for_entity(spellbar, spellBar.SlotFive).id = this_spell_entity

        if main_hand_weapon > 0:
            this_spell_entity = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld,weapon_equipped=main_hand_weapon, slotid=1)
            gameworld.component_for_entity(spellbar, spellBar.SlotOne).id = this_spell_entity
            this_spell_entity = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld,weapon_equipped=main_hand_weapon, slotid=2)
            gameworld.component_for_entity(spellbar, spellBar.SlotTwo).id = this_spell_entity
            this_spell_entity = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld,weapon_equipped=main_hand_weapon, slotid=3)
            gameworld.component_for_entity(spellbar, spellBar.SlotThree).id = this_spell_entity

        if off_hand_weapon > 0:
            this_spell_entity = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld,weapon_equipped=off_hand_weapon, slotid=4)
            gameworld.component_for_entity(spellbar, spellBar.SlotFour).id = this_spell_entity
            this_spell_entity = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld,weapon_equipped=off_hand_weapon, slotid=5)
            gameworld.component_for_entity(spellbar, spellBar.SlotFive).id = this_spell_entity

    def get_spell_bar_slot_componet(gameworld, spell_bar, slotid):
        if slotid == 1:
            return gameworld.component_for_entity(spell_bar, spellBar.SlotOne)
        if slotid == 2:
            return gameworld.component_for_entity(spell_bar, spellBar.SlotTwo)
        if slotid == 3:
            return gameworld.component_for_entity(spell_bar, spellBar.SlotThree)
        if slotid == 4:
            return gameworld.component_for_entity(spell_bar, spellBar.SlotFour)
        if slotid == 5:
            return gameworld.component_for_entity(spell_bar, spellBar.SlotFive)
        if slotid == 6:
            return gameworld.component_for_entity(spell_bar, spellBar.SlotSix)
        if slotid == 7:
            return gameworld.component_for_entity(spell_bar, spellBar.SlotSeven)
        if slotid == 8:
            return gameworld.component_for_entity(spell_bar, spellBar.SlotEight)
        if slotid == 9:
            return gameworld.component_for_entity(spell_bar, spellBar.SlotNine)
        if slotid == 10:
            return gameworld.component_for_entity(spell_bar, spellBar.SlotTen)
        return -1
