from loguru import logger
from components import mobiles
from utilities.itemsHelp import ItemUtilities


class Trinkets:

    def equip_piece_of_jewellery(gameworld, mobile, bodylocation, trinket):
        trinket_name = ItemUtilities.get_item_name(gameworld=gameworld, entity=trinket)
        is_jewellery_equipped = ItemUtilities.get_jewellery_already_equipped_status(gameworld=gameworld, entity=trinket)
        if not is_jewellery_equipped:
            logger.info('Equipping {}', trinket_name)
            if bodylocation == 'left ear':
                gameworld.component_for_entity(mobile, mobiles.Jewellery).ear_one = trinket
            if bodylocation == 'right ear':
                gameworld.component_for_entity(mobile, mobiles.Jewellery).ear_two = trinket
            if bodylocation == 'left hand':
                gameworld.component_for_entity(mobile, mobiles.Jewellery).ring_one = trinket
            if bodylocation == 'right hand':
                gameworld.component_for_entity(mobile, mobiles.Jewellery).ring_two = trinket
            if bodylocation == 'neck':
                gameworld.component_for_entity(mobile, mobiles.Jewellery).amulet = trinket

            ItemUtilities.set_jewellery_equipped_status_to_true(gameworld=gameworld, entity=trinket)
        else:
            logger.info('{} is already equipped.', trinket_name)

    def unequp_piece_of_jewellery(gameworld, entity, bodylocation):

        if bodylocation == 'left ear':
            gameworld.component_for_entity(entity, mobiles.Jewellery).ear_one = 0
        if bodylocation == 'right ear':
            gameworld.component_for_entity(entity, mobiles.Jewellery).ear_two = 0
        if bodylocation == 'left hand':
            gameworld.component_for_entity(entity, mobiles.Jewellery).ring_one = 0
        if bodylocation == 'right hand':
            gameworld.component_for_entity(entity, mobiles.Jewellery).ring_two = 0
        if bodylocation == 'neck':
            gameworld.component_for_entity(entity, mobiles.Jewellery).amulet = 0
        ItemUtilities.set_jewellery_equipped_status_to_false(gameworld=gameworld, entity=entity)

    def get_jewellery_entity_at_bodylocation(gameworld, entity, bodylocation):
        jewellery = 0
        if bodylocation == 'left ear':
            jewellery = gameworld.component_for_entity(entity, mobiles.Jewellery).ear_one
        if bodylocation == 'right ear':
            jewellery = gameworld.component_for_entity(entity, mobiles.Jewellery).ear_two
        if bodylocation == 'left hand':
            jewellery = gameworld.component_for_entity(entity, mobiles.Jewellery).ring_one
        if bodylocation == 'right hand':
            jewellery = gameworld.component_for_entity(entity, mobiles.Jewellery).ring_two
        if bodylocation == 'neck':
            jewellery = gameworld.component_for_entity(entity, mobiles.Jewellery).amulet

        return jewellery

