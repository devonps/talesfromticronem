
from loguru import logger
from components import mobiles


class ArmourClass:

    @staticmethod
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
