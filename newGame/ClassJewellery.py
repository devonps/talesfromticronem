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

    def get_jewellery_at_bodylocation(self):
        pass

    def equip_piece_of_jewellery(gameworld, mobile, trinket):

        trinket_type_component = gameworld.component_for_entity(trinket, jewellery.Type)
        equipped = gameworld.component_for_entity(trinket, jewellery.Equipped)
        if not equipped.label:
            logger.info('Equipping {}', trinket_type_component.label)
            if trinket_type_component.label == 'earring':
                left_ear = Trinkets.get_jewellery_entity_at_bodylocation(gameworld, mobile, 'left ear')
                right_ear = Trinkets.get_jewellery_entity_at_bodylocation(gameworld, mobile, 'right ear')

                if left_ear == 0:
                    gameworld.component_for_entity(mobile, mobiles.Jewellery).ear_one=trinket
                    gameworld.component_for_entity(trinket, jewellery.Equipped).isequipped=True
                    logger.info('The earring is in the left ear')
                elif right_ear == 0:
                    gameworld.component_for_entity(mobile, mobiles.Jewellery).ear_two=trinket
                    gameworld.component_for_entity(trinket, jewellery.Equipped).isequipped=True
                    logger.info('The earring is in the right ear')

            if trinket_type_component.label == 'ring':
                left_ring = Trinkets.get_jewellery_entity_at_bodylocation(gameworld, mobile, 'left hand')
                right_ring = Trinkets.get_jewellery_entity_at_bodylocation(gameworld, mobile, 'right hand')

                if left_ring == 0:
                    gameworld.component_for_entity(mobile, mobiles.Jewellery).ring_one=trinket
                    gameworld.component_for_entity(trinket, jewellery.Equipped).isequipped=True
                    logger.info('Equipping ring onto the left hand')
                elif right_ring == 0:
                    gameworld.component_for_entity(mobile, mobiles.Jewellery).ring_two=trinket
                    gameworld.component_for_entity(trinket, jewellery.Equipped).isequipped=True
                    logger.info('Equipping ring onto the right hand')

            if trinket_type_component.label == 'amulet':
                amulet = Trinkets.get_jewellery_entity_at_bodylocation(gameworld, mobile, 'neck')

                if amulet == 0:
                    gameworld.component_for_entity(mobile, mobiles.Jewellery).amulet = trinket
                    gameworld.component_for_entity(trinket, jewellery.Equipped).isequipped = True
        else:
            logger.info('{} is already equipped.', trinket_type_component.label)

    def unequp_piece_of_jewellery(gameworld, entity, trinket, bodylocaton):
        pass

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


