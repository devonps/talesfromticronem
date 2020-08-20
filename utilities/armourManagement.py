from components import items, mobiles


class ArmourUtilities:
    @staticmethod
    def get_armour_defense_value(gameworld, entity):
        return gameworld.component_for_entity(entity, items.Defense).value

    @staticmethod
    def get_armour_set_name(gameworld, entity):
        return gameworld.component_for_entity(entity, items.ArmourSet).name

    @staticmethod
    def get_armour_major_attributes(gameworld, entity):
        armour_attributes_component = gameworld.component_for_entity(entity, items.AttributeBonus)
        major = [armour_attributes_component.major_name, armour_attributes_component.major_bonus]

        return major


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
    def equip_full_set_of_armour(gameworld, entity, armourset):

        if armourset[0] > 0:
            ArmourUtilities.equip_piece_of_armour(gameworld, entity, armourset[0], 'head')
        if armourset[1] > 0:
            ArmourUtilities.equip_piece_of_armour(gameworld, entity, armourset[1], 'chest')
        if armourset[2] > 0:
            ArmourUtilities.equip_piece_of_armour(gameworld, entity, armourset[2], 'hands')
        if armourset[3] > 0:
            ArmourUtilities.equip_piece_of_armour(gameworld, entity, armourset[3], 'legs')
        if armourset[4] > 0:
            ArmourUtilities.equip_piece_of_armour(gameworld, entity, armourset[4], 'feet')

    @staticmethod
    def add_spell_to_armour_piece(gameworld, armour_entity, spell_entity):
        gameworld.add_component(armour_entity, items.ArmourSpell(entity=spell_entity))


