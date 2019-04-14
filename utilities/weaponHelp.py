from components import weapons, items


class WeaponUtilitiesXXX:

    @staticmethod
    def get_weapon_name(gameworld, entity):
        describeable_component = gameworld.component_for_entity(entity, items.Describable)
        return describeable_component.name

    @staticmethod
    def get_weapon_description(gameworld, entity):
        describeable_component = gameworld.component_for_entity(entity,items.Describable)
        return describeable_component.description

    @staticmethod
    def get_weapon_display_name(gameworld, entity):
        describeable_component = gameworld.component_for_entity(entity, items.Describable)
        return describeable_component.name

    @staticmethod
    def get_weapon_glyph(gameworld, entity):
        describeable_component = gameworld.component_for_entity(entity,items.Describable)
        return describeable_component.glyph

    @staticmethod
    def get_weapon_colours(gameworld, entity):
        describeable_component = gameworld.component_for_entity(entity,items.Describable)
        colours = [describeable_component.foreground, describeable_component.background]
        return colours

    @staticmethod
    def get_is_weapon_wielded(gameworld, weapon_entity):
        wielded_component = gameworld.component_for_entity(weapon_entity,items.Wielded)
        return wielded_component.true_or_false

    @staticmethod
    def get_hand_weapon_is_being_held(gameworld, entity):
        wielded_component = gameworld.component_for_entity(entity,items.Wielded)
        if wielded_component.both_hands != 0:
            return 'both hands'
        if wielded_component.main_hand != 0:
            return 'main hand'
        if wielded_component.off_hand != 0:
            return 'off hand'
        return 'unknown'

    @staticmethod
    def get_weapon_experience_values(gameworld, entity):
        experience_component = gameworld.component_for_entity(entity,items.Experience)
        levels = [experience_component.current_level, experience_component.max_level]
        return levels

    @staticmethod
    def get_weapon_hallmarks(gameworld, entity):
        hallmarks_component = gameworld.component_for_entity(entity,items.Hallmarks)
        hallmarks = [hallmarks_component.hallmark_slot_one, hallmarks_component.hallmark_slot_two]
        return hallmarks

    @staticmethod
    def get_can_weapon_be_rendered(gameworld, entity):
        return gameworld.component_for_entity(entity,items.Renderable).is_visible

    @staticmethod
    def get_weapon_quality_level(gameworld, entity):
        return gameworld.component_for_entity(entity,items.Quality).level

    @staticmethod
    def get_weapon_slot_one_information(gameworld, entity):
        slot_component = gameworld.component_for_entity(entity,items.Spells)
        slot = [slot_component.slot_one, slot_component.slot_one_disabled]
        return slot

    @staticmethod
    def get_weapon_slot_two_information(gameworld, entity):
        slot_component = gameworld.component_for_entity(entity,items.Spells)
        slot = [slot_component.slot_two, slot_component.slot_two_disabled]
        return slot

    @staticmethod
    def get_weapon_slot_three_information(gameworld, entity):
        slot_component = gameworld.component_for_entity(entity, items.Spells)
        slot = [slot_component.slot_three, slot_component.slot_three_disabled]
        return slot

    @staticmethod
    def get_weapon_slot_four_information(gameworld, entity):
        slot_component = gameworld.component_for_entity(entity,items.Spells)
        slot = [slot_component.slot_four, slot_component.slot_four_disabled]
        return slot

    @staticmethod
    def get_weapon_slot_five_information(gameworld, entity):
        slot_component = gameworld.component_for_entity(entity,items.Spells)
        slot = [slot_component.slot_five, slot_component.slot_five_disabled]
        return slot
