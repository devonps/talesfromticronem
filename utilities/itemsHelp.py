from loguru import logger

from components import items


class ItemUtilities:

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
    def get_item_quality(gameworld, entity):
        item_quality_component = gameworld.component_for_entity(entity, items.Quality)
        return item_quality_component.level

    @staticmethod
    def get_spell_from_item(gameworld, item_entity):
        item_type_component = gameworld.component_for_entity(item_entity, items.TypeOfItem)

        if item_type_component.label == 'jewellery':
            spell_entity = gameworld.component_for_entity(item_entity, items.JewellerySpell).entity
            return spell_entity

        if item_type_component.label == 'armour':
            spell_entity = gameworld.component_for_entity(item_entity, items.ArmourSpell).entity
            return spell_entity
