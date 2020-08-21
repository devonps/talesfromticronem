from loguru import logger

from components import items, mobiles
from utilities import configUtilities
from utilities.jsonUtilities import read_json_file
from utilities.mobileHelp import MobileUtilities


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
    def add_major_attribute_bonus_to_piece_of_armour(gameworld, armour_entity, attribute_name, attribute_bonus):
        armour_attributes_component = gameworld.component_for_entity(armour_entity, items.AttributeBonus)
        armour_attributes_component.major_name = attribute_name.lower()
        armour_attributes_component.major_bonus = attribute_bonus

    @staticmethod
    def add_major_attribute_bonus_to_full_armourset(gameworld, player_entity, attribute_name, attribute_bonus):

        if MobileUtilities.is_entity_wearing_head_armour(gameworld=gameworld, entity=player_entity):
            armour_entity = ArmourUtilities.get_armour_entity_from_body_location(gameworld=gameworld,
                                                                                 entity=player_entity,
                                                                                 bodylocation='head')

            ArmourUtilities.add_major_attribute_bonus_to_piece_of_armour(gameworld=gameworld,
                                                                         armour_entity=armour_entity,
                                                                         attribute_name=attribute_name,
                                                                         attribute_bonus=attribute_bonus)

            attribute_bonus_list = ArmourUtilities.get_armour_major_attributes(gameworld=gameworld,
                                                                               entity=armour_entity)
            logger.debug('head: Attribute bonus list {}', attribute_bonus_list)

        if MobileUtilities.is_entity_wearing_chest_armour(gameworld=gameworld, entity=player_entity):
            armour_entity = ArmourUtilities.get_armour_entity_from_body_location(gameworld=gameworld,
                                                                                 entity=player_entity,
                                                                                 bodylocation='chest')

            ArmourUtilities.add_major_attribute_bonus_to_piece_of_armour(gameworld=gameworld,
                                                                         armour_entity=armour_entity,
                                                                         attribute_name=attribute_name,
                                                                         attribute_bonus=attribute_bonus)

            attribute_bonus_list = ArmourUtilities.get_armour_major_attributes(gameworld=gameworld,
                                                                               entity=armour_entity)
            logger.debug('chest: Attribute bonus list {}', attribute_bonus_list)

        if MobileUtilities.is_entity_wearing_hands_armour(gameworld=gameworld, entity=player_entity):
            armour_entity = ArmourUtilities.get_armour_entity_from_body_location(gameworld=gameworld,
                                                                                 entity=player_entity,
                                                                                 bodylocation='hands')

            ArmourUtilities.add_major_attribute_bonus_to_piece_of_armour(gameworld=gameworld,
                                                                         armour_entity=armour_entity,
                                                                         attribute_name=attribute_name,
                                                                         attribute_bonus=attribute_bonus)

            attribute_bonus_list = ArmourUtilities.get_armour_major_attributes(gameworld=gameworld,
                                                                               entity=armour_entity)
            logger.debug('hands: Attribute bonus list {}', attribute_bonus_list)

        if MobileUtilities.is_entity_wearing_legs_armour(gameworld=gameworld, entity=player_entity):
            armour_entity = ArmourUtilities.get_armour_entity_from_body_location(gameworld=gameworld,
                                                                                 entity=player_entity,
                                                                                 bodylocation='legs')

            ArmourUtilities.add_major_attribute_bonus_to_piece_of_armour(gameworld=gameworld,
                                                                         armour_entity=armour_entity,
                                                                         attribute_name=attribute_name,
                                                                         attribute_bonus=attribute_bonus)

            attribute_bonus_list = ArmourUtilities.get_armour_major_attributes(gameworld=gameworld,
                                                                               entity=armour_entity)
            logger.debug('legs: Attribute bonus list {}', attribute_bonus_list)

        if MobileUtilities.is_entity_wearing_feet_armour(gameworld=gameworld, entity=player_entity):
            armour_entity = ArmourUtilities.get_armour_entity_from_body_location(gameworld=gameworld,
                                                                                 entity=player_entity,
                                                                                 bodylocation='feet')

            ArmourUtilities.add_major_attribute_bonus_to_piece_of_armour(gameworld=gameworld,
                                                                         armour_entity=armour_entity,
                                                                         attribute_name=attribute_name,
                                                                         attribute_bonus=attribute_bonus)

            attribute_bonus_list = ArmourUtilities.get_armour_major_attributes(gameworld=gameworld,
                                                                               entity=armour_entity)
            logger.debug('feet: Attribute bonus list {}', attribute_bonus_list)

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

    @staticmethod
    def get_all_armour_modifiers(game_config):
        armourset_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                    parameter='ARMOURSETFILE')
        armour_file = read_json_file(armourset_file)

        pxstring = 'prefix'
        attvaluestring = 'attributebonus'
        attnamestring = 'attributename'

        as_prefix_list = []
        px_flavour = []
        px_att_bonus = []
        armour_details = []
        px_att_name = []

        for armourset in armour_file['armoursets']:
            if armourset['startset'] == 'true':
                armour_details.append(armourset['displayname'])
                armour_details.append(armourset['material'])
                as_prefix_list = armourset['prefixlist'].split(",")
                prefix_count = armourset['prefixcount']
                attribute_bonus_count = armourset['attributebonuscount']

                for px in range(1, prefix_count + 1):
                    prefix_string = pxstring + str(px)
                    px_flavour.append(armourset[prefix_string]['flavour'])

                    if attribute_bonus_count > 1:
                        att_bonus_string = attvaluestring + str(px)
                        att_name_string = attnamestring + str(px)
                    else:
                        att_bonus_string = attvaluestring + str(1)
                        att_name_string = attnamestring + str(1)

                    px_att_bonus.append(armourset[prefix_string][att_bonus_string])
                    px_att_name.append(armourset[prefix_string][att_name_string])

        return armour_details, as_prefix_list, px_att_bonus, px_att_name, px_flavour
