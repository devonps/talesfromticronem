from loguru import logger
from components import jewellery, mobiles
from utilities.jsonUtilities import read_json_file
from newGame import constants


class Trinkets:

    def create_earring(gameworld, e_setting, e_hook, e_activator):
        """
        Will create an earring the e_setting informs the tier, e.g. copper is only used in Tier 1 jewellery
        The e_activator is the gemstone - this drives the attribute bonuses
        :param e_setting:
        :param e_hook:
        :param e_activator:
        :return:
        """
        if e_setting == '' or e_activator == '' or e_hook == '':
            logger.debug('Earring - at least one base component is missing')
            return 0
        if e_setting != e_hook:
            logger.debug("Earring - setting and hook base metals don't match")
            return 0
        logger.info('Creating earring')
        earring = gameworld.create_entity()

        gameworld.add_component(earring, jewellery.Type(label='earring'))
        gameworld.add_component(earring, jewellery.Material(label=e_setting))

        gemstone_file = read_json_file(constants.JSONFILEPATH + 'gemstones.json')
        ab = 1

        for gemstone in gemstone_file['gemstones']:
            if gemstone['Gemstone'] == e_activator:
                if ab == 3:
                    gameworld.add_component(earring, jewellery.ImprovementTo(stat3name=gemstone['Attribute'],
                                                                             stat3bonus=gemstone['Earring']))
                    ab += 1
                if ab == 2:
                    gameworld.add_component(earring, jewellery.ImprovementTo(stat2name=gemstone['Attribute'],
                                                                             stat2bonus=gemstone['Earring']))
                    ab += 1
                if ab == 1:
                    gameworld.add_component(earring, jewellery.ImprovementTo(stat1name=gemstone['Attribute'],
                                                                             stat1bonus=gemstone['Earring']))
                    ab += 1

        gameworld.add_component(earring, jewellery.Describable(
            component1=e_hook,
            component2=e_setting,
            component3=e_activator))
        gameworld.add_component(earring, jewellery.Equipped(isequipped=False))

        return earring

    def create_amulet(gameworld, e_setting, e_hook, e_activator):
        if e_setting == '' or e_activator == '' or e_hook == '':
            logger.debug('Amulet - at least one base component is missing')
            return 0
        if e_setting != e_hook:
            logger.debug("Amulet - setting and hook base metals don't match")
            return 0
        logger.info('Creating Amulet')
        amulet = gameworld.create_entity()

        gameworld.add_component(amulet, jewellery.Type(label='amulet'))
        gameworld.add_component(amulet, jewellery.Material(label=e_setting))

        gemstone_file = read_json_file(constants.JSONFILEPATH + 'gemstones.json')
        ab = 1

        for gemstone in gemstone_file['gemstones']:
            if gemstone['Gemstone'] == e_activator:
                if ab == 3:
                    gameworld.add_component(amulet, jewellery.ImprovementTo(stat3name=gemstone['Attribute'],
                                                                             stat3bonus=gemstone['Amulet']))
                    ab += 1
                if ab == 2:
                    gameworld.add_component(amulet, jewellery.ImprovementTo(stat2name=gemstone['Attribute'],
                                                                             stat2bonus=gemstone['Amulet']))
                    ab += 1
                if ab == 1:
                    gameworld.add_component(amulet, jewellery.ImprovementTo(stat1name=gemstone['Attribute'],
                                                                             stat1bonus=gemstone['Amulet']))
                    ab += 1

        gameworld.add_component(amulet, jewellery.Describable(
            component1=e_hook,
            component2=e_setting,
            component3=e_activator))
        gameworld.add_component(amulet, jewellery.Equipped(isequipped=False))

        return amulet

    def create_ring(gameworld, e_setting, e_hook, e_activator):
        if e_setting == '' or e_activator == '' or e_hook == '':
            logger.debug('Ring - at least one base component is missing')
            return 0
        if e_setting != e_hook:
            logger.debug("Ring - setting and hook base metals don't match")
            return 0
        logger.info('Creating Ring')
        ring = gameworld.create_entity()

        gameworld.add_component(ring, jewellery.Type(label='ring'))
        gameworld.add_component(ring, jewellery.Material(label=e_setting))

        gemstone_file = read_json_file(constants.JSONFILEPATH + 'gemstones.json')
        ab = 1

        for gemstone in gemstone_file['gemstones']:
            if gemstone['Gemstone'] == e_activator:
                if ab == 3:
                    gameworld.add_component(ring, jewellery.ImprovementTo(stat3name=gemstone['Attribute'],
                                                                             stat3bonus=gemstone['Ring']))
                    ab += 1
                if ab == 2:
                    gameworld.add_component(ring, jewellery.ImprovementTo(stat2name=gemstone['Attribute'],
                                                                             stat2bonus=gemstone['Ring']))
                    ab += 1
                if ab == 1:
                    gameworld.add_component(ring, jewellery.ImprovementTo(stat1name=gemstone['Attribute'],
                                                                             stat1bonus=gemstone['Ring']))
                    ab += 1

        gameworld.add_component(ring, jewellery.Describable(
            component1=e_hook,
            component2=e_setting,
            component3=e_activator))
        gameworld.add_component(ring, jewellery.Equipped(isequipped=False))

        return ring

    def equip_piece_of_jewellery(gameworld, mobile, bodylocation, trinket):

        trinket_type_component = gameworld.component_for_entity(trinket, jewellery.Type)
        equipped = gameworld.component_for_entity(trinket, jewellery.Equipped)
        if not equipped.label:
            logger.info('Equipping {}', trinket_type_component.label)

            if bodylocation == 'left ear':
                gameworld.component_for_entity(mobile, mobiles.Jewellery).ear_one = trinket
                gameworld.component_for_entity(trinket, jewellery.Equipped).isequipped = True
            if bodylocation == 'right ear':
                gameworld.component_for_entity(mobile, mobiles.Jewellery).ear_two = trinket
                gameworld.component_for_entity(trinket, jewellery.Equipped).isequipped = True
            if bodylocation == 'left hand':
                gameworld.component_for_entity(mobile, mobiles.Jewellery).ring_one = trinket
                gameworld.component_for_entity(trinket, jewellery.Equipped).isequipped = True
            if bodylocation == 'right hand':
                gameworld.component_for_entity(mobile, mobiles.Jewellery).ring_two = trinket
                gameworld.component_for_entity(trinket, jewellery.Equipped).isequipped = True
            if bodylocation == 'neck':
                gameworld.component_for_entity(mobile, mobiles.Jewellery).amulet = trinket
                gameworld.component_for_entity(trinket, jewellery.Equipped).isequipped = True
        else:
            logger.info('{} is already equipped.', trinket_type_component.label)

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

    def get_jewellery_attribute_bonus(gameworld, piece_of_jewellery):

        bonus = {}

        attribute_component = gameworld.component_for_entity(piece_of_jewellery, jewellery.ImprovementTo)
        stat1_name = attribute_component.stat1name
        stat1_bonus = attribute_component.stat1bonus
        stat2_name = attribute_component.stat1name
        stat2_bonus = attribute_component.stat1bonus
        stat3_name = attribute_component.stat1name
        stat3_bonus = attribute_component.stat1bonus

        if stat1_name != '':
            bonus[stat1_name] = stat1_bonus
        if stat2_name != '':
            bonus[stat2_name] = stat2_bonus
        if stat3_name != '':
            bonus[stat3_name] = stat3_bonus

        return bonus

    def describe_piece_of_jewellery(gameworld, piece_of_jewellery):
        gemstone_component = gameworld.component_for_entity(piece_of_jewellery, jewellery.Describable)
        material_component = gameworld.component_for_entity(piece_of_jewellery, jewellery.Material)
        type_component = gameworld.component_for_entity(piece_of_jewellery, jewellery.Type)

        return gemstone_component.component3 + ' ' + material_component.label + ' ' + type_component.label