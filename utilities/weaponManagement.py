import random
from loguru import logger
from components import items
from static.data import constants
from utilities import configUtilities, jsonUtilities, spellHelp


class WeaponUtilities:

    @staticmethod
    def get_available_weapons_for_class(selected_class):
        player_class_file = constants.FILE_CLASSESFILE
        class_file = jsonUtilities.read_json_file(player_class_file)
        available_weapons = []

        for option in class_file['classes']:
            if option['spellfile'] == selected_class:
                wpns = option["weapons"]

                # If you use this approach along
                # with a small trick, then you can process the keys and values of any dictionary.
                # The trick consists of using the indexing operator[] with the dictionary and its keys to
                # get access to the values:

                for key in wpns:
                    if wpns[key] == 'true':
                        available_weapons.append(key)
        return available_weapons

    @staticmethod
    def get_weapon_flavour_info(available_weapons):
        weapon_flavour_file = constants.FILE_WEAPONSFILE
        weapon_file = jsonUtilities.read_json_file(weapon_flavour_file)
        weapon_description = []
        weapon_wielded = []
        weapon_damage_ranges = []
        weapon_quality = []

        for weapon in available_weapons:
            for option in weapon_file['weapons']:
                if option['name'] == weapon:
                    weapon_description.append(option["description"])
                    weapon_wielded.append(option["wielded_hands"])
                    weapon_quality.append(option["quality_level"])

                    full_damage_range_list = option["damage_ranges"]
                    weapon_damage_ranges.append(full_damage_range_list[0])

        return weapon_description, weapon_wielded, weapon_quality, weapon_damage_ranges

    @staticmethod
    def get_is_weapon_wielded(gameworld, weapon_entity):
        wielded_component = gameworld.component_for_entity(weapon_entity, items.Wielded)
        return wielded_component.true_or_false

    @staticmethod
    def get_hand_weapon_can_be_wielded_in(gameworld, weapon_entity):
        wielded_component = gameworld.component_for_entity(weapon_entity, items.Wielded)
        return wielded_component.hands

    @staticmethod
    def get_weapon_type(gameworld, weapon_entity):
        weapon_type_component = gameworld.component_for_entity(weapon_entity, items.WeaponType)
        return weapon_type_component.label

    @staticmethod
    def get_weapon_experience_values(gameworld, entity):
        experience_component = gameworld.component_for_entity(entity, items.Experience)
        levels = [experience_component.current_level, experience_component.max_level]
        return levels

    @staticmethod
    def get_weapon_hallmarks(gameworld, entity):
        hallmarks_component = gameworld.component_for_entity(entity, items.Hallmarks)
        hallmarks = [hallmarks_component.hallmark_slot_one, hallmarks_component.hallmark_slot_two]
        return hallmarks

    @staticmethod
    def get_weapon_damage_ranges(gameworld, weapon):
        return gameworld.component_for_entity(weapon, items.DamageRange).ranges

    @staticmethod
    def calculate_weapon_strength(gameworld, weapon):
        weapon_level = WeaponUtilities.get_weapon_experience_values(gameworld=gameworld, entity=weapon)
        current_weapon_level = weapon_level[0]

        weapon_strength = WeaponUtilities.get_weapon_strength(gameworld=gameworld, weapon=weapon,
                                                            weapon_level=current_weapon_level)

        return weapon_strength

    @staticmethod
    def get_weapon_strength(gameworld, weapon, weapon_level):
        wpn_dmg_min = 0
        wpn_dmg_max = 0
        range_chosen = False
        weapon_damage_range = WeaponUtilities.get_weapon_damage_ranges(gameworld=gameworld, weapon=weapon)

        for lvl in weapon_damage_range:
            wid = lvl['id']
            if int(wid) > (weapon_level - 1) and range_chosen is False:
                range_chosen = True
                wpn_dmg_min = int(lvl['min'])
                wpn_dmg_max = int(lvl['max'])
                logger.info('Weapon damage range found: min {} max {}', str(wpn_dmg_min), str(wpn_dmg_max))

        if wpn_dmg_min == 0 or wpn_dmg_max == 0:
            # raise logger warning
            # return 0 damage
            return 0
        else:
            return random.randrange(wpn_dmg_min, wpn_dmg_max)


    @staticmethod
    def load_player_spellbar_from_weapons(weapon_type, spell_list, gameworld, player_entity):
        if weapon_type in ['sword', 'staff']:
            spellHelp.SpellUtilities.set_spellbar_slot(gameworld=gameworld, spell_entity=spell_list[0], slot=0, player_entity=player_entity)
            spellHelp.SpellUtilities.set_spellbar_slot(gameworld=gameworld, spell_entity=spell_list[1], slot=1, player_entity=player_entity)
            spellHelp.SpellUtilities.set_spellbar_slot(gameworld=gameworld, spell_entity=spell_list[2], slot=2, player_entity=player_entity)
            spellHelp.SpellUtilities.set_spellbar_slot(gameworld=gameworld, spell_entity=spell_list[3], slot=3, player_entity=player_entity)
            spellHelp.SpellUtilities.set_spellbar_slot(gameworld=gameworld, spell_entity=spell_list[4], slot=4, player_entity=player_entity)

    @staticmethod
    def load_enemy_weapon_with_spells(gameworld, enemy_id, spell_list, weapon_entity_id, weapon_type):
        sample_spells = []
        if weapon_type in ['sword', 'staff']:
            sample_spells = random.sample(spell_list, 5)
            weapon_slot_component = gameworld.component_for_entity(weapon_entity_id, items.Spells)
            weapon_slot_component.slot_one = sample_spells[0]
            weapon_slot_component = gameworld.component_for_entity(weapon_entity_id, items.Spells)
            weapon_slot_component.slot_two = sample_spells[1]
            weapon_slot_component = gameworld.component_for_entity(weapon_entity_id, items.Spells)
            weapon_slot_component.slot_three = sample_spells[2]
            weapon_slot_component = gameworld.component_for_entity(weapon_entity_id, items.Spells)
            weapon_slot_component.slot_four = sample_spells[3]
            weapon_slot_component = gameworld.component_for_entity(weapon_entity_id, items.Spells)
            weapon_slot_component.slot_five = sample_spells[4]

            logger.debug('5 Random spells loaded into {} are {}', weapon_type, sample_spells)

        if weapon_type in ['wand', 'scepter', 'dagger']:
            sample_spells = random.sample(spell_list, 3)
            weapon_slot_component = gameworld.component_for_entity(weapon_entity_id, items.Spells)
            weapon_slot_component.slot_one = sample_spells[0]
            weapon_slot_component = gameworld.component_for_entity(weapon_entity_id, items.Spells)
            weapon_slot_component.slot_two = sample_spells[1]
            weapon_slot_component = gameworld.component_for_entity(weapon_entity_id, items.Spells)
            weapon_slot_component.slot_three = sample_spells[2]

            logger.debug('3 Random spells loaded into {} are {}', weapon_type, sample_spells)

        if weapon_type in ['rod', 'focus']:
            sample_spells = random.sample(spell_list, 2)
            weapon_slot_component = gameworld.component_for_entity(weapon_entity_id, items.Spells)
            weapon_slot_component.slot_four = sample_spells[0]
            weapon_slot_component = gameworld.component_for_entity(weapon_entity_id, items.Spells)
            weapon_slot_component.slot_five = sample_spells[1]

            logger.debug('2 Random spells loaded into {} are {}', weapon_type, sample_spells)

        return sample_spells
