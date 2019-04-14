
from loguru import logger
from components import mobiles


class ArmourClass:

    def get_armour_piece_from_body_location(gameworld, entity, bodylocation):

        armour_entity = 0
        logger.info('fetching armour for entity {} from the {}', entity, bodylocation)

        if bodylocation == 'head':
            piece_of_armour_component = gameworld.component_for_entity(entity, mobiles.Armour)
            armour_entity = piece_of_armour_component.head
        if bodylocation == 'chest':
            piece_of_armour_component = gameworld.component_for_entity(entity, mobiles.Armour)
            armour_entity = piece_of_armour_component.chest
        if bodylocation == 'hands':
            piece_of_armour_component = gameworld.component_for_entity(entity, mobiles.Armour)
            armour_entity = piece_of_armour_component.hands
        if bodylocation == 'legs':
            piece_of_armour_component = gameworld.component_for_entity(entity, mobiles.Armour)
            armour_entity = piece_of_armour_component.legs
        if bodylocation == 'feet':
            piece_of_armour_component = gameworld.component_for_entity(entity, mobiles.Armour)
            armour_entity = piece_of_armour_component.feet

        return armour_entity

    def equip_full_set_of_armour(gameworld, entity, armourset):

        if armourset[0] > 0:
            gameworld.component_for_entity(entity, mobiles.Armour).chest = armourset[0]
        if armourset[1] > 0:
            gameworld.component_for_entity(entity, mobiles.Armour).head = armourset[1]
        if armourset[2] > 0:
            gameworld.component_for_entity(entity, mobiles.Armour).hands = armourset[2]
        if armourset[3] > 0:
            gameworld.component_for_entity(entity, mobiles.Armour).legs = armourset[3]
        if armourset[4] > 0:
            gameworld.component_for_entity(entity, mobiles.Armour).feet = armourset[4]

    def equip_single_piece_of_armour(gameworld, entity, piece_of_armour, bodylocation):
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

    def unequip_piece_of_armour(gameworld, entity, bodylocation):
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