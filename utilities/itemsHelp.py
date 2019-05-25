from components import items, mobiles
from utilities import world
from loguru import logger


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
        return item_location_component.posx, item_location_component.posy

    @staticmethod
    def add_dungeon_position_component(gameworld, entity):
        gameworld.add_component(entity, items.Location(x=0, y=0))


    @staticmethod
    def set_item_location(gameworld, item_entity, posx, posy):
        item_location_component = gameworld.component_for_entity(item_entity, items.Location)
        item_location_component.posx = posx
        item_location_component.posy = posy

    @staticmethod
    def get_item_texture(gameworld, entity):
        item_material_component = gameworld.component_for_entity(entity, items.Material)
        return item_material_component.texture

    @staticmethod
    def get_item_components(gameworld, entity):
        item_components_component = gameworld.component_for_entity(entity, items.Material)
        return item_components_component.component1, item_components_component.component2, item_components_component.component3

    @staticmethod
    def get_item_can_be_rendered(gameworld, entity):
        item_render_component = gameworld.component_for_entity(entity, items.RenderItem)
        return item_render_component.isTrue

    @staticmethod
    def get_item_quality(gameworld, entity):
        item_quality_component = gameworld.component_for_entity(entity, items.Quality)
        return item_quality_component.level

    @staticmethod
    def delete_item(gameworld, entity):
        gameworld.delete_entity(entity=entity, immediate=True)

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
#   BAGS
#
####################################################
    @staticmethod
    def get_bag_size(gameworld, entity):
        bag_size_component = gameworld.component_for_entity(entity, items.SlotSize)
        return bag_size_component.maxsize

    @staticmethod
    def get_bag_is_populated(gameworld, entity):
        bag_populated_component = gameworld.component_for_entity(entity, items.SlotSize)
        return bag_populated_component.populated

####################################################
#
#   WEAPONS
#
####################################################

    @staticmethod
    def get_is_weapon_wielded(gameworld, weapon_entity):
        wielded_component = gameworld.component_for_entity(weapon_entity, items.Wielded)
        return wielded_component.true_or_false

    @staticmethod
    def get_hand_weapon_can_be_wielded_in(gameworld, weapon_entity):
        wielded_component = gameworld.component_for_entity(weapon_entity, items.Wielded)
        return wielded_component.hands

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
    def get_weapon_spell_slot_one_information(gameworld, entity):
        slot_component = gameworld.component_for_entity(entity,items.Spells)
        slot = [slot_component.slot_one, slot_component.slot_one_disabled]
        return slot

    @staticmethod
    def get_weapon_spell_slot_two_information(gameworld, entity):
        slot_component = gameworld.component_for_entity(entity,items.Spells)
        slot = [slot_component.slot_two, slot_component.slot_two_disabled]
        return slot

    @staticmethod
    def get_weapon_spell_slot_three_information(gameworld, entity):
        slot_component = gameworld.component_for_entity(entity, items.Spells)
        slot = [slot_component.slot_three, slot_component.slot_three_disabled]
        return slot

    @staticmethod
    def get_weapon_spell_lot_four_information(gameworld, entity):
        slot_component = gameworld.component_for_entity(entity,items.Spells)
        slot = [slot_component.slot_four, slot_component.slot_four_disabled]
        return slot

    @staticmethod
    def get_weapon_spell_slot_five_information(gameworld, entity):
        slot_component = gameworld.component_for_entity(entity,items.Spells)
        slot = [slot_component.slot_five, slot_component.slot_five_disabled]
        return slot

####################################################
#
#   ARMOUR
#
####################################################
    @staticmethod
    def get_armour_defense_value(gameworld, body_location):
        return gameworld.component_for_entity(body_location, items.Defense).value

    @staticmethod
    def get_armour_set_name(gameworld, entity):
        return gameworld.component_for_entity(entity, items.ArmourSet).name

    @staticmethod
    def get_armour_piece_weight(gameworld, entity):
        return gameworld.component_for_entity(entity, items.Weight).label

    @staticmethod
    def get_armour_major_attributes(gameworld, entity):
        armour_attributes_component = gameworld.component_for_entity(entity, items.AttributeBonus)
        major = [armour_attributes_component.majorName, armour_attributes_component.majorBonus]

        return major

    @staticmethod
    def get_armour_minor_attributes(gameworld, entity):
        armour_attributes_component = gameworld.component_for_entity(entity, items.AttributeBonus)
        minor = [armour_attributes_component.minorOneName, armour_attributes_component.minorOneBonus]
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

    def equip_piece_of_armour(gameworld, entity, piece_of_armour, bodylocation):
        logger.info('Armour entity is {} / mobile entity is {} / body location is {}', piece_of_armour, entity, bodylocation)
        is_armour_being_worn = ItemUtilities.get_armour_being_worn_status(gameworld, piece_of_armour)
        if not is_armour_being_worn:
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

            ItemUtilities.set_armour_being_worn_status_to_true(gameworld, piece_of_armour)

    def unequip_piece_of_armour(gameworld, entity, bodylocation):
        armour_is_already_worn = ItemUtilities.get_armour_being_worn_status(gameworld, entity)
        if armour_is_already_worn:
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

            ItemUtilities.set_armour_being_worn_status_to_false(gameworld, entity)

    def equip_full_set_of_armour(gameworld, entity, armourset):

        if armourset[0] > 0:
            # gameworld.component_for_entity(entity, mobiles.Armour).chest = armourset[0]
            ItemUtilities.equip_piece_of_armour(gameworld, entity, armourset[0], 'chest')
        if armourset[1] > 0:
            # gameworld.component_for_entity(entity, mobiles.Armour).head = armourset[1]
            ItemUtilities.equip_piece_of_armour(gameworld, entity, armourset[1], 'head')
        if armourset[2] > 0:
            # gameworld.component_for_entity(entity, mobiles.Armour).hands = armourset[2]
            ItemUtilities.equip_piece_of_armour(gameworld, entity, armourset[2], 'hands')
        if armourset[3] > 0:
            # gameworld.component_for_entity(entity, mobiles.Armour).legs = armourset[3]
            ItemUtilities.equip_piece_of_armour(gameworld, entity, armourset[3], 'legs')
        if armourset[4] > 0:
            # gameworld.component_for_entity(entity, mobiles.Armour).feet = armourset[4]
            ItemUtilities.equip_piece_of_armour(gameworld, entity, armourset[4], 'feet')

####################################################
#
#   JEWELLERY
#
####################################################

    @staticmethod
    def get_jewellery_stat_bonus(gameworld, entity):
        jewellery_statbonus_component = gameworld.component_for_entity(entity, items.JewelleryStatBonus)
        statbonus = [jewellery_statbonus_component.statName, jewellery_statbonus_component.statBonus]
        return statbonus

    @staticmethod
    def get_jewellery_valid_body_location(gameworld, entity):
        jewellery_body_location_component = gameworld.component_for_entity(entity, items.JewelleryBodyLocation)
        loc =[jewellery_body_location_component.ears, jewellery_body_location_component.fingers, jewellery_body_location_component.neck]
        return loc

    @staticmethod
    def get_jewellery_already_equipped_status(gameworld, entity):
        jewellery_equipped_component = gameworld.component_for_entity(entity, items.JewelleryEquipped)
        return jewellery_equipped_component.istrue

    @staticmethod
    def set_jewellery_equipped_status_to_true(gameworld, entity):
        gameworld.component_for_entity(entity, items.JewelleryEquipped).istrue = True

    @staticmethod
    def set_jewellery_equipped_status_to_false(gameworld, entity):
        gameworld.component_for_entity(entity, items.JewelleryEquipped).istrue = False

    @staticmethod
    def equip_jewellery(gameworld, mobile, bodylocation, trinket):
        is_jewellery_equipped = ItemUtilities.get_jewellery_already_equipped_status(gameworld, entity=trinket)
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

            ItemUtilities.set_jewellery_equipped_status_to_true(gameworld, entity=trinket)

            # if world.does_entity_have_component(gameworld=gameworld, entity=trinket, component=items.Location):
            #     world.remove_component_from_entity(gameworld=gameworld, entity=trinket, component=items.Location)

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

        ItemUtilities.set_jewellery_equipped_status_to_false(gameworld, entity=entity)
