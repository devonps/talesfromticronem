from components import mobiles
from loguru import logger
from newGame import constants


class MobileUtilities:

    # check ALL hand combos: main, off, and both hands
    @staticmethod
    def get_weapons_equipped(gameworld, entity):
        """

        :param gameworld:
        :param entity:
        :return: List of items equipped in main, off, and both hands
        """
        equipped = []
        main_hand = gameworld.component_for_entity(entity, mobiles.Equipped).main_hand
        off_hand = gameworld.component_for_entity(entity, mobiles.Equipped).off_hand
        both_hands = gameworld.component_for_entity(entity, mobiles.Equipped).both_hands

        equipped.append(main_hand)
        equipped.append(off_hand)
        equipped.append(both_hands)

        return equipped

    # equip a weapon into a hand (main, off, both)
    @staticmethod
    def equip_weapon(gameworld, entity, weapon, hand):

        if hand == 'main':
            gameworld.component_for_entity(entity, mobiles.Equipped).main_hand = weapon
        if hand == 'off':
            gameworld.component_for_entity(entity, mobiles.Equipped).off_hand = weapon
        if hand == 'both':
            gameworld.component_for_entity(entity, mobiles.Equipped).both_hands = weapon

    def generate_base_mobile(gameworld):
        mobile = gameworld.create_entity()
        logger.info('Base mobile entity ID ' + str(mobile))
        gameworld.add_component(mobile, mobiles.Name(first='xyz', suffix=''))
        gameworld.add_component(mobile, mobiles.Describable())
        gameworld.add_component(mobile, mobiles.CharacterClass())
        gameworld.add_component(mobile, mobiles.AI(ailevel=constants.AI_LEVEL_NONE))

        return mobile

    def describe_the_mobile(gameworld, entity):
        player_name_component = gameworld.component_for_entity(entity, mobiles.Name)
        player_race_component = gameworld.component_for_entity(entity, mobiles.Race)
        player_class_component = gameworld.component_for_entity(entity, mobiles.CharacterClass)
        player_gender_component = gameworld.component_for_entity(entity, mobiles.Describable)

        return player_name_component.first + ' the ' + player_gender_component.gender + ' ' + player_race_component.label + ' ' + player_class_component.label

    @staticmethod
    def get_player_entity(gameworld):
        player = 0
        for ent, ai in gameworld.get_component(mobiles.AI):
            if ai.ailevel == constants.AI_LEVEL_PLAYER:
                player = ent

        return player

    def has_player_moved(gameworld):
        player_entity = MobileUtilities.get_player_entity(gameworld)

        position_component = gameworld.component_for_entity(player_entity, mobiles.Position)

        return position_component.hasMoved
