from loguru import logger

from components import items, mobiles, spells
from utilities import configUtilities, jsonUtilities, world, colourUtilities
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
    def apply_major_attribute_bonus_to_full_armourset(gameworld, player_entity, attribute_name, attribute_bonus):

        if MobileUtilities.is_entity_wearing_head_armour(gameworld=gameworld, entity=player_entity):
            armour_entity = ArmourUtilities.get_armour_entity_from_body_location(gameworld=gameworld,
                                                                                 entity=player_entity,
                                                                                 bodylocation='head')

            ArmourUtilities.add_major_attribute_bonus_to_piece_of_armour(gameworld=gameworld,
                                                                         armour_entity=armour_entity,
                                                                         attribute_name=attribute_name,
                                                                         attribute_bonus=attribute_bonus)
            MobileUtilities.add_armour_modifier(gameworld=gameworld, entity_id=player_entity,
                                                armour_modifier=attribute_name, px_bonus=attribute_bonus)

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
            MobileUtilities.add_armour_modifier(gameworld=gameworld, entity_id=player_entity,
                                                armour_modifier=attribute_name, px_bonus=attribute_bonus)

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
            MobileUtilities.add_armour_modifier(gameworld=gameworld, entity_id=player_entity,
                                                armour_modifier=attribute_name, px_bonus=attribute_bonus)

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
            MobileUtilities.add_armour_modifier(gameworld=gameworld, entity_id=player_entity,
                                                armour_modifier=attribute_name, px_bonus=attribute_bonus)

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
            MobileUtilities.add_armour_modifier(gameworld=gameworld, entity_id=player_entity,
                                                armour_modifier=attribute_name, px_bonus=attribute_bonus)

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
    def get_spell_entity_from_armour_piece(gameworld, armour_entity):
        spell_component = gameworld.component_for_entity(armour_entity, items.ArmourSpell)
        return spell_component.entity

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

    @staticmethod
    def get_current_armour_based_defense_value(gameworld, entity):

        head = MobileUtilities.is_entity_wearing_head_armour(gameworld=gameworld, entity=entity)
        chest = MobileUtilities.is_entity_wearing_chest_armour(gameworld=gameworld, entity=entity)
        legs = MobileUtilities.is_entity_wearing_legs_armour(gameworld=gameworld, entity=entity)
        feet = MobileUtilities.is_entity_wearing_feet_armour(gameworld=gameworld, entity=entity)
        hands = MobileUtilities.is_entity_wearing_hands_armour(gameworld=gameworld, entity=entity)

        if chest != 0:
            def_chest_value = ArmourUtilities.get_armour_defense_value(gameworld=gameworld, entity=chest)

        else:
            def_chest_value = 0

        if head != 0:
            def_head_value = ArmourUtilities.get_armour_defense_value(gameworld=gameworld, entity=head)
        else:
            def_head_value = 0

        if legs != 0:
            def_legs_value = ArmourUtilities.get_armour_defense_value(gameworld=gameworld, entity=legs)
        else:
            def_legs_value = 0

        if feet != 0:
            def_feet_value = ArmourUtilities.get_armour_defense_value(gameworld=gameworld, entity=feet)
        else:
            def_feet_value = 0

        if hands != 0:
            def_hands_value = ArmourUtilities.get_armour_defense_value(gameworld=gameworld, entity=hands)
        else:
            def_hands_value = 0

        defense_value = def_chest_value + def_head_value + def_legs_value + def_feet_value + def_hands_value

        return defense_value

    @staticmethod
    def set_mobile_derived_armour_attribute(gameworld, entity):
        """
        Need to calculate the 'defense' value first
        Then get the toughness attribute value
        :param gameworld: object: the game world
        :param entity: integer: represents the entity in the gameworld
        :return: None
        """
        # get toughness value from primary attributes
        toughness_value = MobileUtilities.get_mobile_primary_toughness(gameworld=gameworld, entity=entity)
        # get defense values based on equipped pieces of armour
        defense_value = ArmourUtilities.get_current_armour_based_defense_value(gameworld=gameworld, entity=entity)
        armour_value = defense_value + toughness_value

        gameworld.component_for_entity(entity, mobiles.DerivedAttributes).armour = armour_value

    @staticmethod
    def create_and_equip_armourset_for_npc(gameworld, as_display_name, armour_modifier, entity_id):
        game_config = configUtilities.load_config()
        this_armourset = ArmourUtilities.create_full_armour_set(gameworld=gameworld, armourset=as_display_name,
                                                                prefix=armour_modifier, game_config=game_config)

        ArmourUtilities.equip_full_set_of_armour(gameworld=gameworld, entity=entity_id, armourset=this_armourset)

    @staticmethod
    def create_full_armour_set(gameworld, armourset, prefix, game_config):
        """
        This method creates a full set of armour (as game entities), it calls the method create_piece_of_armour
        to create the actual piece of armour.

        Why do I need to create a full armour set?
        1. An NPC could wear it
        2. NPC's could drop multiple pieces of the same set
        3. The PC could wear it
        4. A full set may be available to purchase or craft by the PC

        :return: a list of entities created in the order [head, chest, hands, legs, feet]
        """
        full_armour_set = []

        head_armour = ArmourUtilities.create_piece_of_armour(gameworld=gameworld, game_config=game_config,
                                                             setname=armourset, prefix=prefix, bodylocation='head')
        full_armour_set.append(head_armour)

        chest_armour = ArmourUtilities.create_piece_of_armour(gameworld=gameworld, game_config=game_config,
                                                              setname=armourset, prefix=prefix, bodylocation='chest')
        full_armour_set.append(chest_armour)

        hands_armour = ArmourUtilities.create_piece_of_armour(gameworld=gameworld, game_config=game_config,
                                                              setname=armourset, prefix=prefix, bodylocation='hands')
        full_armour_set.append(hands_armour)

        legs_armour = ArmourUtilities.create_piece_of_armour(gameworld=gameworld, game_config=game_config,
                                                             setname=armourset, prefix=prefix, bodylocation='legs')
        full_armour_set.append(legs_armour)

        feet_armour = ArmourUtilities.create_piece_of_armour(gameworld=gameworld, game_config=game_config,
                                                             setname=armourset, prefix=prefix, bodylocation='feet')
        full_armour_set.append(feet_armour)

        return full_armour_set

    @staticmethod
    def create_piece_of_armour(gameworld, bodylocation, setname, prefix, game_config):

        armour_action_list = configUtilities.get_config_value_as_list(configfile=game_config, section='game',
                                                                      parameter='ITEM_ARMOUR_ACTIONS')

        armour_set_path = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                     parameter='ARMOURSETFILE')

        armour_set_file = jsonUtilities.read_json_file(armour_set_path)

        armour_piece = world.get_next_entity_id(gameworld=gameworld)

        pxstring = 'prefix'
        attnamestring = 'attributename'
        attvaluestring = 'attributebonus'
        piece_of_armour = ''
        defense = ''
        as_material = ''
        as_quality = ''
        as_weight = ''
        px_att_name = ''
        px_att_bonus = ''

        for armourset in armour_set_file['armoursets']:
            if armourset['displayname'] == setname:
                as_weight = (armourset['weight'])
                as_quality = armourset['quality']
                as_material = (armourset['material'])
                prefix_count = armourset['prefixcount']
                attribute_bonus_count = armourset['attributebonuscount']
                piece_of_armour, defense = ArmourUtilities.process_armour_bodylocation(gameworld=gameworld,
                                                                                       bodylocation=bodylocation,
                                                                                       armour_piece=armour_piece,
                                                                                       armourset=armourset)

                for px in range(1, prefix_count + 1):
                    prefix_string = pxstring + str(px)
                    if armourset[prefix_string]['name'].lower() == prefix.lower():
                        att_bonus_string, att_name_string = ArmourUtilities.process_armour_attribute_bonus(
                            attribute_bonus_count=attribute_bonus_count, attvaluestring=attvaluestring, px=px,
                            attnamestring=attnamestring)
                        px_att_bonus = armourset[prefix_string][att_bonus_string]
                        px_att_name = armourset[prefix_string][att_name_string]

        # generate common item components
        gameworld.add_component(armour_piece, items.TypeOfItem(label='armour'))
        gameworld.add_component(armour_piece, items.Material(texture=as_material))
        gameworld.add_component(armour_piece, items.Actionlist(action_list=armour_action_list))
        gameworld.add_component(armour_piece, items.Describable(
            name=bodylocation + ' armour',
            glyph=")",
            description='a ' + piece_of_armour + ' made from ' + as_material,
            fg=colourUtilities.get('WHITE'),
            bg=colourUtilities.get('BLACK'),
            displayname=piece_of_armour))
        gameworld.add_component(armour_piece, items.RenderItem(istrue=True))
        gameworld.add_component(armour_piece, items.Quality(level=as_quality))
        gameworld.add_component(armour_piece, items.ArmourSpell(entity=0, on_cool_down=False))

        # generate armour specifics
        gameworld.add_component(armour_piece, items.Weight(label=as_weight))
        gameworld.add_component(armour_piece, items.Defense(value=int(defense)))
        if prefix == '':
            px_att_bonus = 0
        gameworld.add_component(armour_piece, items.AttributeBonus(
            majorname=px_att_name,
            majorbonus=int(px_att_bonus),
            minoronename='',
            minoronebonus=0))

        gameworld.add_component(armour_piece, items.ArmourSet(label=setname, prefix=prefix, level=0))
        gameworld.add_component(armour_piece, items.ArmourBeingWorn(status=False))

        # add spell to piece of armour
        player = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
        player_class = MobileUtilities.get_character_class(gameworld, player)
        ArmourUtilities.add_spell_to_piece_of_armour(gameworld=gameworld, bodylocation=bodylocation,
                                                     armour_piece=armour_piece, playable_class=player_class)

        return armour_piece

    @staticmethod
    def process_armour_attribute_bonus(attribute_bonus_count, attvaluestring, px, attnamestring):
        if attribute_bonus_count > 1:
            att_bonus_string = attvaluestring + str(px)
            att_name_string = attnamestring + str(px)
        else:
            att_bonus_string = attvaluestring + str(1)
            att_name_string = attnamestring + str(1)
        return att_bonus_string, att_name_string

    @staticmethod
    def add_spell_to_piece_of_armour(gameworld, bodylocation, armour_piece, playable_class):
        for spell_entity, (name, location, spell_type, item_type, spclass) in gameworld.get_components(spells.Name,
                                                                                                       spells.ItemLocation,
                                                                                                       spells.SpellType,
                                                                                                       spells.ItemType,
                                                                                                       spells.ClassName):
            if spclass.label == playable_class and spell_type.label == 'utility' and item_type.label == 'armour' and location.label == bodylocation:
                ArmourUtilities.add_spell_to_armour_piece(gameworld=gameworld, armour_entity=armour_piece,
                                                          spell_entity=spell_entity)

    @staticmethod
    def process_armour_bodylocation(gameworld, bodylocation, armour_piece, armourset):
        piece_of_armour = ''
        defense = 0
        if bodylocation == 'head':
            gameworld.add_component(armour_piece, items.ArmourBodyLocation(head=True))
            piece_of_armour = armourset['head']['display']
            defense = armourset['head']['defense']
        if bodylocation == 'chest':
            gameworld.add_component(armour_piece, items.ArmourBodyLocation(chest=True))
            piece_of_armour = armourset['chest']['display']
            defense = armourset['chest']['defense']
        if bodylocation == 'hands':
            gameworld.add_component(armour_piece, items.ArmourBodyLocation(hands=True))
            piece_of_armour = armourset['hands']['display']
            defense = armourset['hands']['defense']
        if bodylocation == 'feet':
            gameworld.add_component(armour_piece, items.ArmourBodyLocation(feet=True))
            piece_of_armour = armourset['feet']['display']
            defense = armourset['feet']['defense']
        if bodylocation == 'legs':
            gameworld.add_component(armour_piece, items.ArmourBodyLocation(legs=True))
            piece_of_armour = armourset['legs']['display']
            defense = armourset['legs']['defense']
        return piece_of_armour, defense
