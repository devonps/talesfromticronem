from components import mobiles, userInput, items
from loguru import logger
from newGame import constants
from utilities.itemsHelp import ItemUtilities
from utilities import world
import numbers


class MobileUtilities(numbers.Real):

    #
    # general methods
    #
    @staticmethod
    def get_player_entity(gameworld):
        player = 0
        for ent, ai in gameworld.get_component(mobiles.AI):
            if ai.ailevel == constants.AI_LEVEL_PLAYER:
                player = ent

        return player

    @staticmethod
    def get_number_as_a_percentage(lower_value, maximum_value):
        return int((lower_value / maximum_value) * 100)

    @staticmethod
    def get_bar_count(lower_value):
        return (lower_value / 100) * constants.V_BAR_DEPTH

    @staticmethod
    def create_player_input_entity(gameworld):
        ent = gameworld.create_entity()
        gameworld.add_component(ent, userInput.Keyboard())
        gameworld.add_component(ent, userInput.Mouse())

    @staticmethod
    def has_player_moved(gameworld):
        entity = MobileUtilities.get_player_entity(gameworld)

        position_component = gameworld.component_for_entity(entity, mobiles.Position)

        return position_component.hasMoved

    @staticmethod
    def get_mobile_current_location(gameworld, mobile):
        location_component = gameworld.component_for_entity(mobile, mobiles.Position)
        return location_component.x, location_component.y

    @staticmethod
    def get_mobile_name_details(gameworld, entity):
        name_component = gameworld.component_for_entity(entity, mobiles.Name)
        names = [name_component.first, name_component.suffix]
        return names

    @staticmethod
    def get_mobile_race_details(gameworld, entity):
        race_component = gameworld.component_for_entity(entity, mobiles.Race)
        racial = [race_component.label, race_component.size]
        return racial

    @staticmethod
    def get_mobile_personality_title(gameworld, entity):
        describeable_component = gameworld.component_for_entity(entity, mobiles.Describable)
        return describeable_component.personality_title

    @staticmethod
    def calculate_mobile_personality(gameworld):
        player_entity = MobileUtilities.get_player_entity(gameworld)

        player_current_personality_component = gameworld.component_for_entity(player_entity, mobiles.Personality)
        player_describable_personality_component = gameworld.component_for_entity(player_entity, mobiles.Describable)

        player_personality = player_describable_personality_component.personality_title

        # get current personality trait values
        charm_level = player_current_personality_component.charm_level
        dignity_level = player_current_personality_component.dignity_level
        ferocity_level = player_current_personality_component.ferocity_level

        if charm_level == 12.5 and dignity_level == 75 and ferocity_level == 12.5:
            player_personality = 'Noble'
        if charm_level == 75 and dignity_level == 12.5 and ferocity_level == 12.5:
            player_personality = 'Captivating'
        if charm_level == 12.5 and dignity_level == 12.5 and ferocity_level == 175:
            player_personality = 'Barbaric'
        if charm_level == 45 and dignity_level == 45 and ferocity_level == 10:
            player_personality = 'Diplomatic'
        if charm_level == 10 and dignity_level == 45 and ferocity_level == 45:
            player_personality = 'Militant'
        if charm_level == 45 and dignity_level == 10 and ferocity_level == 45:
            player_personality = 'Scoundrel'
        if charm_level == 33 and dignity_level == 33 and ferocity_level == 33:
            player_personality = 'Unpredictable'
        if charm_level == 50 and dignity_level == 25 and ferocity_level == 25:
            player_personality = 'Charming'
        if charm_level == 25 and dignity_level == 50 and ferocity_level == 25:
            player_personality = 'Honourable'
        if charm_level == 25 and dignity_level == 25 and ferocity_level == 50:
            player_personality = 'Brute'

        player_describable_personality_component.personality_title = player_personality

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

    @staticmethod
    def generate_base_mobile(gameworld):
        mobile = world.get_next_entity_id(gameworld=gameworld)
        logger.info('Base mobile entity ID ' + str(mobile))
        gameworld.add_component(mobile, mobiles.Name(first='xyz', suffix=''))
        gameworld.add_component(mobile, mobiles.Describable())
        gameworld.add_component(mobile, mobiles.CharacterClass())
        gameworld.add_component(mobile, mobiles.AI(ailevel=constants.AI_LEVEL_NONE))

        return mobile

    @staticmethod
    def describe_the_mobile(gameworld, entity):
        player_name_component = gameworld.component_for_entity(entity, mobiles.Name)
        player_race_component = gameworld.component_for_entity(entity, mobiles.Race)
        player_class_component = gameworld.component_for_entity(entity, mobiles.CharacterClass)
        player_gender_component = gameworld.component_for_entity(entity, mobiles.Describable)

        return player_name_component.first + ' is a ' + player_gender_component.gender + ' ' + player_race_component.label + ' ' + player_class_component.label

    #
    # Mobile actions
    #

    # pick up item from dungeon floor
    def mobile_pick_up_item(gameworld, mobile):
        px, py = MobileUtilities.get_mobile_current_location(gameworld=gameworld, mobile=mobile)
        mobile_inventory_component = gameworld.component_for_entity(mobile, mobiles.Inventory)
        for ent, (rend, loc, desc) in gameworld.get_components(items.RenderItem, items.Location, items.Describable):
            if loc.posx == px and loc.posy == py:
                if rend.isTrue:
                    pass
                    # check if mobile has enough space in their inventory
                    # remove item location data
                    gameworld.remove_component(ent, items.Location)
                    # add item entity to mobile inventory
                    mobile_inventory_component.items.append(ent)
                    logger.info('{} has been picked up', desc.name)

        mobile_inventory_component = gameworld.component_for_entity(mobile, mobiles.Inventory)
        inventory_items = mobile_inventory_component.items
        logger.info('Inventory consists of {}', inventory_items)


    # drop item to dungeon floor



    # add item, once picked up, to inventory




    #
    # Get primary attributes
    #
    @staticmethod
    def get_mobile_power(gameworld, entity):
        primary_components = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes)
        return primary_components.power
    @staticmethod
    def get_mobile_precision(gameworld, entity):
        primary_components = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes)
        return primary_components.precision
    @staticmethod
    def get_mobile_toughness(gameworld, entity):
        primary_components = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes)
        return primary_components.toughness
    @staticmethod
    def get_mobile_vitality(gameworld, entity):
        primary_components = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes)
        return primary_components.vitality

    #
    # Get secondary attributes
    #
    @staticmethod
    def get_mobile_concentration(gameworld, entity):
        secondary_components = gameworld.component_for_entity(entity, mobiles.SecondaryAttributes)
        return secondary_components.concentration

    @staticmethod
    def get_mobile_condition_damage(gameworld, entity):
        secondary_components = gameworld.component_for_entity(entity, mobiles.SecondaryAttributes)
        return secondary_components.conditionDamage

    @staticmethod
    def get_mobile_expertise(gameworld, entity):
        secondary_components = gameworld.component_for_entity(entity, mobiles.SecondaryAttributes)
        return secondary_components.expertise

    @staticmethod
    def get_mobile_ferocity(gameworld, entity):
        secondary_components = gameworld.component_for_entity(entity, mobiles.SecondaryAttributes)
        return secondary_components.ferocity

    @staticmethod
    def get_mobile_healing_power(gameworld, entity):
        secondary_components = gameworld.component_for_entity(entity, mobiles.SecondaryAttributes)
        return secondary_components.healingPower

    @staticmethod
    def is_entity_wearing_armour(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.DerivedAttributes).armour

    @staticmethod
    def is_entity_wearing_head_armour(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.Armour).head
    @staticmethod
    def is_entity_wearing_chest_armour(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.Armour).chest

    @staticmethod
    def is_entity_wearing_legs_armour(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.Armour).legs

    @staticmethod
    def is_entity_wearing_feet_armour(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.Armour).feet

    @staticmethod
    def is_entity_wearing_hands_armour(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.Armour).hands

#
# Calculate derived attributes
#
    @staticmethod
    def calculate_derived_attributes(gameworld, entity):
        MobileUtilities.calculate_armour_attribute(gameworld, entity)
        MobileUtilities.calculate_boon_duration(gameworld, entity)
        MobileUtilities.calculate_condition_duration(gameworld, entity)
        MobileUtilities.calculate_critical_damage(gameworld, entity)
        MobileUtilities.calculate_critical_hit_chance(gameworld, entity)
        MobileUtilities.calculate_max_health(gameworld, entity)
        MobileUtilities.calculate_current_health(gameworld, entity)

    @staticmethod
    def calculate_armour_attribute(gameworld, entity):
        """
        Need to calculate the 'defense' value first
        Then get the toughness attribute value
        :param gameworld: object: the game world
        :param entity: integer: represents the entity in the gameworld
        :return: None
        """

        # get toughness value from primary attributes
        primary_attribute_component = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes)
        toughness_value = primary_attribute_component.toughness

        # get defense values based on equipped pieces of armour
        defense_value = MobileUtilities.get_current_armour_based_defense_value(gameworld=gameworld, entity=entity)

        armour_value = defense_value + toughness_value

        gameworld.component_for_entity(entity, mobiles.DerivedAttributes).armour = armour_value

    @staticmethod
    def get_current_armour_based_defense_value(gameworld, entity):

        head = MobileUtilities.is_entity_wearing_head_armour(gameworld=gameworld, entity=entity)
        chest = MobileUtilities.is_entity_wearing_chest_armour(gameworld=gameworld, entity=entity)
        legs = MobileUtilities.is_entity_wearing_legs_armour(gameworld=gameworld, entity=entity)
        feet = MobileUtilities.is_entity_wearing_feet_armour(gameworld=gameworld, entity=entity)
        hands = MobileUtilities.is_entity_wearing_hands_armour(gameworld=gameworld, entity=entity)

        if chest != 0:
            def_chest_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, body_location=chest)
        else:
            def_chest_value = 0

        if head != 0:
            def_head_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, body_location=head)
        else:
            def_head_value = 0

        if legs != 0:
            def_legs_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, body_location=legs)
        else:
            def_legs_value = 0

        if feet != 0:
            def_feet_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, body_location=feet)
        else:
            def_feet_value = 0

        if hands != 0:
            def_hands_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, body_location=hands)
        else:
            def_hands_value = 0

        defense_value = def_chest_value + def_head_value + def_legs_value + def_feet_value + def_hands_value

        return defense_value

    @staticmethod
    def calculate_boon_duration(gameworld, entity):
        """
        calculates the duration of the boon(s) when they are applied to the target entity
        :param gameworld: object: the game world
        :param entity: integer: represents the mobile in the gameworld
        :return: None
        """
        entity_secondary_component = gameworld.component_for_entity(entity, mobiles.SecondaryAttributes)

        concentration_value = entity_secondary_component.concentration

        boon_duration_value = min(100, int(concentration_value / 15))

        gameworld.component_for_entity(entity, mobiles.DerivedAttributes).boonDuration = boon_duration_value

    @staticmethod
    def calculate_critical_hit_chance(gameworld, entity):
        """
        calculates the chance the entity has to generate a critical hit.
        The boon 'fury' gives a flat 20% increase
        Precision, traits, spells, and weapons can all affect the value

        :param gameword:
        :param entity:
        :return: None
        """
        base_value = 5  # every hit has a 5% chance of causing a critical hit

        status_effects_component = gameworld.component_for_entity(entity, mobiles.StatusEffects)
        primary_attribute_component = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes)

        precision_value = primary_attribute_component.precision
        applied_boons = status_effects_component.boons
        # now cycle through the list of applied_boons looking for fury
        boon_fury_bonus = 0

        # check the traits (currently not implemented)
        trait_bonus = 0

        precision_bonus = int(precision_value / 21)

        critical_chance_value = min(100, base_value + boon_fury_bonus + trait_bonus + precision_value)

        gameworld.component_for_entity(entity, mobiles.DerivedAttributes).criticalChance = critical_chance_value

    @staticmethod
    def calculate_critical_damage(gameworld, entity):
        """
        calculates the damage caused when a critical hit has landed
        :param gameworld:
        :param entity:
        :return:
        """

        base_value = 150
        entity_secondary_component = gameworld.component_for_entity(entity, mobiles.SecondaryAttributes)

        ferocity_value = entity_secondary_component.ferocity

        critical_damage_bonus = int(ferocity_value / 15)

        critical_damage_value = base_value + critical_damage_bonus

        gameworld.component_for_entity(entity, mobiles.DerivedAttributes).criticalDamage = critical_damage_value

    @staticmethod
    def calculate_condition_duration(gameworld, entity):
        """
        caluclates the duration for conditions when they are applied to the target
        :param gameworld:
        :param entity:
        :return:
        """
        entity_secondary_component = gameworld.component_for_entity(entity, mobiles.SecondaryAttributes)
        expertise_value = entity_secondary_component.expertise

        cond_duration = int(expertise_value / 15)

        cond_duration_bonus = min(100, cond_duration)
        gameworld.component_for_entity(entity, mobiles.DerivedAttributes).conditionDuration = cond_duration_bonus

    @staticmethod
    def calculate_max_health(gameworld, entity):
        """
        Calculates the health of the entity. Base health is based on character class & vitality.
        Health value can be affected by traits, boons, conditions, etc.

        :param gameworld:
        :param entity:
        :return:
        """
        primary_attribute_component = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes)
        entity_class_component = gameworld.component_for_entity(entity, mobiles.CharacterClass)
        vitality_value = primary_attribute_component.vitality
        class_base_health = entity_class_component.baseHealth

        vitality_calculated_health = vitality_value * 10

        health_value = vitality_calculated_health + class_base_health
        gameworld.component_for_entity(entity, mobiles.DerivedAttributes).maximumHealth = health_value

    @staticmethod
    def calculate_current_health(gameworld, entity):
        """
        This method will take everything into account that could affect the entities health, and calculate
        the current health
        :param gameworld:
        :param entity:
        :return:
        """
        current_health = 0
        maximum_health = gameworld.component_for_entity(entity, mobiles.DerivedAttributes).maximumHealth
        # check boons
        # check conditions
        # check controls
        # check traits
        # check equipped items (armour, jewellery)
        # check weapons

        gameworld.component_for_entity(entity, mobiles.DerivedAttributes).currentHealth = maximum_health

    #
    # Get derived attributes
    #

    @staticmethod
    def get_derived_armour_value(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.DerivedAttributes).armour

    @staticmethod
    def get_derived_boon_duration(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.DerivedAttributes).boonDuration

    @staticmethod
    def get_derived_critical_hit_chance(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.DerivedAttributes).criticalChance

    @staticmethod
    def get_derived_critical_damage(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.DerivedAttributes).criticalDamage

    @staticmethod
    def get_derived_condition_duration(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.DerivedAttributes).conditionDuration

    @staticmethod
    def get_derived_maximum_health(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.DerivedAttributes).maximumHealth

    @staticmethod
    def get_derived_current_health(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.DerivedAttributes).currentHealth

    @staticmethod
    def get_derived_current_mana(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.ManaPool).current

    @staticmethod
    def get_derived_maximum_mana(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.ManaPool).maximum
