import random

from loguru import logger

from components import items, mobiles, spells
from utilities import world


class ItemUtilities:
    ####################################################
    #
    #   Methods applicable to all types of items
    #
    ####################################################
    @staticmethod
    def get_item_type(gameworld, entity):
        item_type_component = gameworld.component_for_entity(entity, items.TypeOfItem)
        return item_type_component.label

    @staticmethod
    def get_item_actions(gameworld, entity):
        item_actions_component = gameworld.component_for_entity(entity, items.Actionlist)
        return item_actions_component.actions

    @staticmethod
    def get_item_name(gameworld, entity):
        item_described_component = gameworld.component_for_entity(entity, items.Describable)
        return item_described_component.name

    @staticmethod
    def get_item_material(gameworld, entity):
        item_material_component = gameworld.component_for_entity(entity, items.Material)
        return item_material_component.texture

    @staticmethod
    def get_item_displayname(gameworld, entity):
        item_described_component = gameworld.component_for_entity(entity, items.Describable)
        return item_described_component.displayname

    @staticmethod
    def get_item_description(gameworld, entity):
        item_described_component = gameworld.component_for_entity(entity, items.Describable)
        return item_described_component.description

    @staticmethod
    def get_item_glyph(gameworld, entity):
        item_described_component = gameworld.component_for_entity(entity, items.Describable)
        return item_described_component.glyph

    @staticmethod
    def get_item_colours(gameworld, entity):
        describeable_component = gameworld.component_for_entity(entity,items.Describable)
        colours = [describeable_component.fg, describeable_component.bg]
        return colours

    @staticmethod
    def get_item_fg_colour(gameworld, entity):
        item_described_component = gameworld.component_for_entity(entity, items.Describable)
        return item_described_component.fg

    @staticmethod
    def get_item_bg_colour(gameworld, entity):
        item_described_component = gameworld.component_for_entity(entity, items.Describable)
        return item_described_component.bg

    @staticmethod
    def get_item_location(gameworld, entity):
        item_location_component = gameworld.component_for_entity(entity, items.Location)
        return item_location_component.x, item_location_component.y

    @staticmethod
    def add_dungeon_position_component(gameworld, entity):
        gameworld.add_component(entity, items.Location(x=0, y=0))


    @staticmethod
    def set_item_location(gameworld, item_entity, posx, posy):
        item_location_component = gameworld.component_for_entity(item_entity, items.Location)
        item_location_component.x = posx
        item_location_component.y = posy

    @staticmethod
    def get_item_components(gameworld, entity):
        item_components_component = gameworld.component_for_entity(entity, items.Material)
        return item_components_component.component1, item_components_component.component2, item_components_component.component3

    @staticmethod
    def get_item_can_be_rendered(gameworld, entity):
        item_render_component = gameworld.component_for_entity(entity, items.RenderItem)
        return item_render_component.is_true

    @staticmethod
    def get_item_quality(gameworld, entity):
        item_quality_component = gameworld.component_for_entity(entity, items.Quality)
        return item_quality_component.level

    @staticmethod
    def delete_item(gameworld, entity):
        world.delete_entity(gameworld=gameworld, entity=entity)

    @staticmethod
    def remove_item_from_inventory(gameworld, mobile, entity):
        mobile_inventory_component = gameworld.component_for_entity(mobile, mobiles.Inventory)
        mobile_inventory_component.items.remove(entity)

    @staticmethod
    def add_previously_equipped_item_to_inventory(gameworld, mobile, item_to_inventory):
        mobile_inventory_component = gameworld.component_for_entity(mobile, mobiles.Inventory)
        mobile_inventory_component.items.append(item_to_inventory)

####################################################
#
#   WEAPONS
#
####################################################

    @staticmethod
    def get_equipped_weapon_for_enemy(gameworld, weapons_equipped):
        weapon_id = 0

        if len(weapons_equipped) == 0:
            logger.warning('NO WEAPONS EQUIPPED')
            return weapon_id
        if weapons_equipped[0] > 0:
            weapon_id = weapons_equipped[0]
        elif weapons_equipped[1] > 0:
            weapon_id = weapons_equipped[1]
        else:
            weapon_id = weapons_equipped[2]

        weapon_type = ItemUtilities.get_item_name(gameworld=gameworld, entity=weapon_id)

        return weapon_type


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
    def get_weapon_held_in_hand(gameworld, entity):
        wielded_component = gameworld.component_for_entity(entity, items.Wielded)
        if wielded_component.both_hands != 0:
            return 'both hands'
        if wielded_component.main_hand != 0:
            return 'main hand'
        if wielded_component.off_hand != 0:
            return 'off hand'
        return 'unknown'

    @staticmethod
    def get_weapon_experience_values(gameworld, entity):
        experience_component = gameworld.component_for_entity(entity, items.Experience)
        levels = [experience_component.current_level, experience_component.max_level]
        return levels

    @staticmethod
    def get_weapon_hallmarks(gameworld, entity):
        hallmarks_component = gameworld.component_for_entity(entity,items.Hallmarks)
        hallmarks = [hallmarks_component.hallmark_slot_one, hallmarks_component.hallmark_slot_two]
        return hallmarks

    @staticmethod
    def get_weapon_spell_slot_one_entity(gameworld, weapon_entity):
        slot_component = gameworld.component_for_entity(weapon_entity, items.Spells)
        spell_entity = slot_component.slot_one
        return int(spell_entity)

    @staticmethod
    def get_weapon_spell_slot_two_entity(gameworld, weapon_entity):
        slot_component = gameworld.component_for_entity(weapon_entity, items.Spells)
        spell_entity = slot_component.slot_two
        return int(spell_entity)

    @staticmethod
    def get_weapon_spell_slot_three_entity(gameworld, weapon_entity):
        slot_component = gameworld.component_for_entity(weapon_entity, items.Spells)
        spell_entity = slot_component.slot_three
        return int(spell_entity)

    @staticmethod
    def get_weapon_spell_slot_four_entity(gameworld, weapon_entity):
        slot_component = gameworld.component_for_entity(weapon_entity, items.Spells)
        spell_entity = slot_component.slot_four
        return int(spell_entity)

    @staticmethod
    def get_weapon_spell_slot_five_entity(gameworld, weapon_entity):
        slot_component = gameworld.component_for_entity(weapon_entity, items.Spells)
        spell_entity = slot_component.slot_five
        return int(spell_entity)

    @staticmethod
    def get_weapon_damage_ranges(gameworld, weapon):
        return gameworld.component_for_entity(weapon, items.DamageRange).ranges

    @staticmethod
    def calculate_weapon_strength(gameworld, weapon):
        weapon_level = ItemUtilities.get_weapon_experience_values(gameworld=gameworld, entity=weapon)
        current_weapon_level = weapon_level[0]

        weapon_strength = ItemUtilities.get_weapon_strength(gameworld=gameworld, weapon=weapon, weapon_level=current_weapon_level)

        return weapon_strength

    @staticmethod
    def get_weapon_strength(gameworld, weapon, weapon_level):
        wpn_dmg_min = 0
        wpn_dmg_max = 0
        range_chosen = False
        weapon_damage_range = ItemUtilities.get_weapon_damage_ranges(gameworld=gameworld, weapon=weapon)

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


####################################################
#
#   ARMOUR
#
####################################################
    @staticmethod
    def get_armour_defense_value(gameworld, entity):
        return gameworld.component_for_entity(entity, items.Defense).value

    @staticmethod
    def get_armour_set_name(gameworld, entity):
        return gameworld.component_for_entity(entity, items.ArmourSet).name

    @staticmethod
    def get_armour_piece_weight(gameworld, entity):
        return gameworld.component_for_entity(entity, items.Weight).label

    @staticmethod
    def get_armour_major_attributes(gameworld, entity):
        armour_attributes_component = gameworld.component_for_entity(entity, items.AttributeBonus)
        major = [armour_attributes_component.major_name, armour_attributes_component.major_bonus]

        return major

    @staticmethod
    def get_armour_minor_attributes(gameworld, entity):
        armour_attributes_component = gameworld.component_for_entity(entity, items.AttributeBonus)
        minor = [armour_attributes_component.minor_one_name, armour_attributes_component.minor_one_bonus]
        return minor

    @staticmethod
    def get_armour_being_worn_status(gameworld, piece_of_armour):
        armour_worn_component = gameworld.component_for_entity(piece_of_armour, items.ArmourBeingWorn)
        return armour_worn_component.status

    @staticmethod
    def set_armour_being_worn_status_to_true(gameworld, entity):
        gameworld.component_for_entity(entity, items.ArmourBeingWorn).status = True

    @staticmethod
    def set_armour_being_worn_status_to_false(gameworld, entity):
        gameworld.component_for_entity(entity, items.ArmourBeingWorn).status = False

    @staticmethod
    def get_armour_entity_from_body_location(gameworld, entity, bodylocation):
        armour_worn = 0
        if bodylocation == 'head':
            armour_worn = gameworld.component_for_entity(entity, mobiles.Armour).head
        if bodylocation == 'chest':
            armour_worn = gameworld.component_for_entity(entity, mobiles.Armour).chest
        if bodylocation == 'hands':
            armour_worn = gameworld.component_for_entity(entity, mobiles.Armour).hands
        if bodylocation == 'legs':
            armour_worn = gameworld.component_for_entity(entity, mobiles.Armour).legs
        if bodylocation == 'feet':
            armour_worn = gameworld.component_for_entity(entity, mobiles.Armour).feet

        return armour_worn

    @staticmethod
    def get_armour_body_location(gameworld, armour_piece):
        body_location = ''
        if gameworld.component_for_entity(armour_piece, items.ArmourBodyLocation).head > 0:
            return 'head'
        if gameworld.component_for_entity(armour_piece, items.ArmourBodyLocation).chest > 0:
            return 'chest'
        if gameworld.component_for_entity(armour_piece, items.ArmourBodyLocation).hands > 0:
            return 'hands'
        if gameworld.component_for_entity(armour_piece, items.ArmourBodyLocation).legs > 0:
            return 'legs'
        if gameworld.component_for_entity(armour_piece, items.ArmourBodyLocation).feet > 0:
            return 'feet'

        return body_location


    @staticmethod
    def equip_piece_of_armour(gameworld, entity, piece_of_armour, bodylocation):
        # logger.info('Armour entity is {} / mobile entity is {} / body location is {}', piece_of_armour, entity, bodylocation)
        # is_armour_being_worn = ItemUtilities.get_armour_being_worn_status(gameworld, piece_of_armour)
        # if not is_armour_being_worn:
        if bodylocation == 'head':
            gameworld.component_for_entity(entity, mobiles.Armour).head = piece_of_armour
        if bodylocation == 'chest':
            gameworld.component_for_entity(entity, mobiles.Armour).chest = piece_of_armour
        if bodylocation == 'hands':
            gameworld.component_for_entity(entity, mobiles.Armour).hands = piece_of_armour
        if bodylocation == 'legs':
            gameworld.component_for_entity(entity, mobiles.Armour).legs = piece_of_armour
        if bodylocation == 'feet':
            gameworld.component_for_entity(entity, mobiles.Armour).feet = piece_of_armour

    @staticmethod
    def unequip_piece_of_armour(gameworld, entity, bodylocation):
        # armour_is_already_worn = ItemUtilities.get_armour_being_worn_status(gameworld, entity)
        # if armour_is_already_worn:
        if bodylocation == 'head':
            gameworld.component_for_entity(entity, mobiles.Armour).head = 0
        if bodylocation == 'chest':
            gameworld.component_for_entity(entity, mobiles.Armour).chest = 0
        if bodylocation == 'hands':
            gameworld.component_for_entity(entity, mobiles.Armour).hands = 0
        if bodylocation == 'legs':
            gameworld.component_for_entity(entity, mobiles.Armour).legs = 0
        if bodylocation == 'feet':
            gameworld.component_for_entity(entity, mobiles.Armour).feet = 0

    @staticmethod
    def equip_full_set_of_armour(gameworld, entity, armourset):

        if armourset[0] > 0:
            ItemUtilities.equip_piece_of_armour(gameworld, entity, armourset[0], 'head')
        if armourset[1] > 0:
            ItemUtilities.equip_piece_of_armour(gameworld, entity, armourset[1], 'chest')
        if armourset[2] > 0:
            ItemUtilities.equip_piece_of_armour(gameworld, entity, armourset[2], 'hands')
        if armourset[3] > 0:
            ItemUtilities.equip_piece_of_armour(gameworld, entity, armourset[3], 'legs')
        if armourset[4] > 0:
            ItemUtilities.equip_piece_of_armour(gameworld, entity, armourset[4], 'feet')

    @staticmethod
    def add_spell_to_armour_piece(gameworld, armour_entity, spell_entity):
        gameworld.add_component(armour_entity, items.ArmourSpell(entity=spell_entity))

    @staticmethod
    def set_spell_cooldown_status_on_armour_piece(gameworld, armour_entity, cool_down_status):
        gameworld.add_component(armour_entity, items.ArmourSpell(on_cool_down=cool_down_status))


####################################################
#
#   JEWELLERY
#
####################################################

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
        jewellery_body_location_component = gameworld.component_for_entity(jewellery_entity, items.JewelleryBodyLocation)
        loc =[jewellery_body_location_component.ears, jewellery_body_location_component.fingers, jewellery_body_location_component.neck]
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
        is_jewellery_equipped = ItemUtilities.get_jewellery_already_equipped_status(gameworld, jewellery_entity=trinket)
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

            ItemUtilities.set_jewellery_equipped_status_to_true(gameworld, jewellery_entity=trinket)

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

        ItemUtilities.set_jewellery_equipped_status_to_false(gameworld=gameworld, jewellery_entity=entity)

    @staticmethod
    def add_jewellery_benefit(gameworld, entity, statbonus):

        stat = statbonus[0]
        benefit = statbonus[1]

        if stat.lower() == 'condition damage':
            current_stat_bonus = gameworld.component_for_entity(entity, mobiles.SecondaryAttributes).condition_damage
            new_stat_bonus = current_stat_bonus + benefit
            gameworld.component_for_entity(entity, mobiles.SecondaryAttributes).condition_damage=new_stat_bonus

        if stat.lower() == 'power':
            current_stat_bonus = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).power
            new_stat_bonus = current_stat_bonus + benefit
            gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).power=new_stat_bonus

        if stat.lower() == 'vitality':
            current_stat_bonus = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).vitality
            new_stat_bonus = current_stat_bonus + benefit
            gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).vitality=new_stat_bonus

        if stat.lower() == 'toughness':
            current_stat_bonus = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).toughness
            new_stat_bonus = current_stat_bonus + benefit
            gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).toughness=new_stat_bonus

        if stat.lower() == 'healing power':
            current_stat_bonus = gameworld.component_for_entity(entity, mobiles.SecondaryAttributes).healing_power
            new_stat_bonus = current_stat_bonus + benefit
            gameworld.component_for_entity(entity, mobiles.SecondaryAttributes).healing_power=new_stat_bonus

        if stat.lower() == 'precision':
            current_stat_bonus = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).precision
            new_stat_bonus = current_stat_bonus + benefit
            gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).precision=new_stat_bonus

    @staticmethod
    def add_spell_to_jewellery(gameworld, piece_of_jewellery, spell_entity):
        gameworld.add_component(piece_of_jewellery, items.JewellerySpell(entity=spell_entity))

    @staticmethod
    def get_spell_from_item(gameworld, item_entity):
        item_type_component = gameworld.component_for_entity(item_entity, items.TypeOfItem)

        if item_type_component.label == 'jewellery':
            spell_entity = gameworld.component_for_entity(item_entity, items.JewellerySpell).entity
            return spell_entity

        if item_type_component.label == 'armour':
            spell_entity = gameworld.component_for_entity(item_entity, items.ArmourSpell).entity
            return spell_entity
