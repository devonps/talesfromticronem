from components import items, mobiles
from utilities import configUtilities
from utilities.jsonUtilities import read_json_file
from utilities.mobileHelp import MobileUtilities


class JewelleryUtilities:

    @staticmethod
    def get_gemstone_details(this_gemstone):
        game_config = configUtilities.load_config()
        playable_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                    parameter='GEMSTONESFILE')
        gemstone_file = read_json_file(playable_class_file)

        gem_details = []

        for gems in gemstone_file['gemstones']:
            if this_gemstone == gems['Stone'].lower():
                gem_details.append(gems['shop_display'])
                gem_details.append(str(gems['Amulet']))
                gem_details.append(str(gems['Ring']))
                gem_details.append(str(gems['Earring']))

        return gem_details


    @staticmethod
    def load_jewellery_package_based_on_class(playable_class, game_config):
        playable_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                    parameter='CLASSESFILE')
        class_file = read_json_file(playable_class_file)

        balanced = []
        defensive = []
        offensive = []

        for play_class in class_file['classes']:
            if playable_class == play_class['name']:
                balanced.append(play_class['balanced'])
                defensive.append(play_class['defensive'])
                offensive.append(play_class['offensive'])

        return defensive, balanced, offensive


    @staticmethod
    def get_jewellery_activator(gameworld, jewellery_entity):
        jewellery_materials_componet = gameworld.component_for_entity(jewellery_entity, items.JewelleryComponents)
        return jewellery_materials_componet.activator

    @staticmethod
    def get_jewellery_stat_bonus(gameworld, jewellery_entity):
        jewellery_statbonus_component = gameworld.component_for_entity(jewellery_entity, items.JewelleryStatBonus)
        statbonus = [jewellery_statbonus_component.stat_name, jewellery_statbonus_component.stat_bonus]
        return statbonus

    @staticmethod
    def get_jewellery_already_equipped_status(gameworld, jewellery_entity):
        jewellery_equipped_component = gameworld.component_for_entity(jewellery_entity, items.JewelleryEquipped)
        return jewellery_equipped_component.istrue

    @staticmethod
    def set_jewellery_equipped_status_to_true(gameworld, jewellery_entity):
        gameworld.component_for_entity(jewellery_entity, items.JewelleryEquipped).istrue = True

    @staticmethod
    def set_jewellery_equipped_status_to_false(gameworld, jewellery_entity):
        gameworld.component_for_entity(jewellery_entity, items.JewelleryEquipped).istrue = False

    @staticmethod
    def get_jewellery_entity_from_body_location(gameworld, entity, bodylocation):
        jewellery_worn = 0
        if bodylocation == 'neck':
            jewellery_worn = gameworld.component_for_entity(entity, mobiles.Jewellery).neck
        if bodylocation == 'lear':
            jewellery_worn = gameworld.component_for_entity(entity, mobiles.Jewellery).left_ear
        if bodylocation == 'rear':
            jewellery_worn = gameworld.component_for_entity(entity, mobiles.Jewellery).right_ear
        if bodylocation == 'lhand':
            jewellery_worn = gameworld.component_for_entity(entity, mobiles.Jewellery).left_hand
        if bodylocation == 'rhand':
            jewellery_worn = gameworld.component_for_entity(entity, mobiles.Jewellery).right_hand

        return jewellery_worn

    @staticmethod
    def equip_jewellery(gameworld, mobile, bodylocation, trinket):
        is_jewellery_equipped = JewelleryUtilities.get_jewellery_already_equipped_status(gameworld, jewellery_entity=trinket)
        if not is_jewellery_equipped:
            if bodylocation == 'left ear':
                gameworld.component_for_entity(mobile, mobiles.Jewellery).left_ear = trinket
            if bodylocation == 'right ear':
                gameworld.component_for_entity(mobile, mobiles.Jewellery).right_ear = trinket
            if bodylocation == 'left hand':
                gameworld.component_for_entity(mobile, mobiles.Jewellery).left_hand = trinket
            if bodylocation == 'right hand':
                gameworld.component_for_entity(mobile, mobiles.Jewellery).right_hand = trinket
            if bodylocation == 'neck':
                gameworld.component_for_entity(mobile, mobiles.Jewellery).neck = trinket

            JewelleryUtilities.set_jewellery_equipped_status_to_true(gameworld, jewellery_entity=trinket)

    @staticmethod
    def add_jewellery_benefit(gameworld, entity, statbonus):

        stat = statbonus[0]
        benefit = statbonus[1]

        if stat.lower() == 'condition damage':
            MobileUtilities.set_mobile_secondary_condition_damage(gameworld=gameworld, entity=entity, value=benefit)

        if stat.lower() == 'power':
            MobileUtilities.set_mobile_primary_power(gameworld=gameworld, entity=entity, value=benefit)

        if stat.lower() == 'vitality':
            MobileUtilities.set_mobile_primary_vitality(gameworld=gameworld, entity=entity, value=benefit)

        if stat.lower() == 'toughness':
            MobileUtilities.set_mobile_primary_toughness(gameworld=gameworld, entity=entity, value=benefit)

        if stat.lower() == 'healing power':
            MobileUtilities.set_mobile_secondary_healing_power(gameworld=gameworld, entity=entity, value=benefit)

        if stat.lower() == 'precision':
            MobileUtilities.set_mobile_primary_precision(gameworld=gameworld, entity=entity, value=benefit)

    @staticmethod
    def add_spell_to_jewellery(gameworld, piece_of_jewellery, spell_entity):
        gameworld.add_component(piece_of_jewellery, items.JewellerySpell(entity=spell_entity))
