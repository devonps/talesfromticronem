
from components import spells, weapons


class SpellUtilities:

    def get_spell_name_in_weapon_slot(gameworld, weapon_equipped, slotid):
        spell_name = 'no spell'
        spell = SpellUtilities.get_spell_at_weapon_slot(gameworld, weapon_equipped, slotid)
        if spell > 0:
            spell_name = gameworld.component_for_entity(spell, spells.Name).label

        return spell_name

    def get_spell_at_weapon_slot(gameworld, weapon_equipped, slotid):

        spell_entity = 0

        if slotid == 1:
            spell_entity = gameworld.component_for_entity(weapon_equipped, weapons.Spells).slot_one
        if slotid == 2:
            spell_entity = gameworld.component_for_entity(weapon_equipped, weapons.Spells).slot_two
        if slotid == 3:
            spell_entity = gameworld.component_for_entity(weapon_equipped, weapons.Spells).slot_three
        if slotid == 4:
            spell_entity = gameworld.component_for_entity(weapon_equipped, weapons.Spells).slot_four
        if slotid == 5:
            spell_entity = gameworld.component_for_entity(weapon_equipped, weapons.Spells).slot_five

        return spell_entity