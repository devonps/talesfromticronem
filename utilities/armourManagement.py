from components import items, mobiles


class ArmourUtilities:
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

    @staticmethod
    def set_spell_cooldown_status_on_armour_piece(gameworld, armour_entity, cool_down_status):
        gameworld.add_component(armour_entity, items.ArmourSpell(on_cool_down=cool_down_status))

