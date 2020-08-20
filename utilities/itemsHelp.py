from components import items, mobiles
from utilities import world


class ItemUtilities:

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

    @staticmethod
    def get_spell_from_item(gameworld, item_entity):
        item_type_component = gameworld.component_for_entity(item_entity, items.TypeOfItem)

        if item_type_component.label == 'jewellery':
            spell_entity = gameworld.component_for_entity(item_entity, items.JewellerySpell).entity
            return spell_entity

        if item_type_component.label == 'armour':
            spell_entity = gameworld.component_for_entity(item_entity, items.ArmourSpell).entity
            return spell_entity
