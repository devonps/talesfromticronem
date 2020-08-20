from components import items, mobiles
from utilities.mobileHelp import MobileUtilities


class JewelleryUtilities:

    @staticmethod
    def get_jewellery_setting(gameworld, jewellery_entity):
        jewellery_materials_componet = gameworld.component_for_entity(jewellery_entity, items.JewelleryComponents)
        return jewellery_materials_componet.setting

    @staticmethod
    def get_jewellery_hook(gameworld, jewellery_entity):
        jewellery_materials_componet = gameworld.component_for_entity(jewellery_entity, items.JewelleryComponents)
        return jewellery_materials_componet.hook

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
    def get_jewellery_valid_body_location(gameworld, jewellery_entity):
        jewellery_body_location_component = gameworld.component_for_entity(jewellery_entity,
                                                                           items.JewelleryBodyLocation)
        loc = [jewellery_body_location_component.ears, jewellery_body_location_component.fingers,
               jewellery_body_location_component.neck]
        return loc

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
    def unequp_piece_of_jewellery(gameworld, entity, bodylocation):

        if bodylocation == 'left ear':
            gameworld.component_for_entity(entity, mobiles.Jewellery).left_ear = 0
        if bodylocation == 'right ear':
            gameworld.component_for_entity(entity, mobiles.Jewellery).right_ear = 0
        if bodylocation == 'left hand':
            gameworld.component_for_entity(entity, mobiles.Jewellery).left_hand = 0
        if bodylocation == 'right hand':
            gameworld.component_for_entity(entity, mobiles.Jewellery).right_hand = 0
        if bodylocation == 'neck':
            gameworld.component_for_entity(entity, mobiles.Jewellery).neck = 0

        JewelleryUtilities.set_jewellery_equipped_status_to_false(gameworld=gameworld, jewellery_entity=entity)

    @staticmethod
    def add_jewellery_benefit(gameworld, entity, statbonus):

        stat = statbonus[0]
        benefit = statbonus[1]

        if stat.lower() == 'condition damage':
            current_stat_bonus = gameworld.component_for_entity(entity, mobiles.SecondaryAttributes).condition_damage
            new_stat_bonus = current_stat_bonus + benefit
            gameworld.component_for_entity(entity, mobiles.SecondaryAttributes).condition_damage = new_stat_bonus

        if stat.lower() == 'power':
            current_stat_bonus = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).power
            new_stat_bonus = current_stat_bonus + benefit
            gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).power = new_stat_bonus

        if stat.lower() == 'vitality':
            current_stat_bonus = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).vitality
            new_stat_bonus = current_stat_bonus + benefit
            gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).vitality = new_stat_bonus

        if stat.lower() == 'toughness':
            MobileUtilities.set_mobile_primary_toughness(gameworld=gameworld, entity=entity, value=benefit)

        if stat.lower() == 'healing power':
            current_stat_bonus = gameworld.component_for_entity(entity, mobiles.SecondaryAttributes).healing_power
            new_stat_bonus = current_stat_bonus + benefit
            gameworld.component_for_entity(entity, mobiles.SecondaryAttributes).healing_power = new_stat_bonus

        if stat.lower() == 'precision':
            current_stat_bonus = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).precision
            new_stat_bonus = current_stat_bonus + benefit
            gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).precision = new_stat_bonus

    @staticmethod
    def add_spell_to_jewellery(gameworld, piece_of_jewellery, spell_entity):
        gameworld.add_component(piece_of_jewellery, items.JewellerySpell(entity=spell_entity))
