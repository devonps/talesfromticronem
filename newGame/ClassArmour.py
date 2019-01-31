
from utilities.jsonUtilities import read_json_file
from loguru import logger
from components import armour, mobiles
from newGame import constants


class ArmourClass:

    def create_piece_of_armour(gameworld, bodylocation, quality, weight, setname, prefix, location_aka, level, defense,
                               majorname, majorbonus, minoronename, minoronebonus, minortwoname, minortwobonus):
        """
                This method creates a gameworld entity that's used as a piece of armour. It uses the Json file
        to create the 'base' entity - it's up to other methods to add flesh to these bones.
        :param bodylocation:
        :param quality:
        :param weight:
        :param setname:
        :param prefix:
        :param location_aka:
        :param level:
        :param defense:
        :param majorname:
        :param majorbonus:
        :param minoronename:
        :param minoronebonus:
        :param minortwoname:
        :param minortwobonus:
        :return:
        """
        armour_piece = gameworld.create_entity()
        logger.info('Entity {} has been created as a piece of {} armour', armour_piece, bodylocation)
        gameworld.add_component(armour_piece, armour.Location(bodylocation))
        gameworld.add_component(armour_piece, armour.LocationAKA(location_aka))
        gameworld.add_component(armour_piece, armour.Set(setname))
        gameworld.add_component(armour_piece, armour.Quality(quality))
        gameworld.add_component(armour_piece, armour.Weight(weight))
        gameworld.add_component(armour_piece, armour.Defense(defense))
        gameworld.add_component(armour_piece, armour.Describable(prefix=prefix, location_aka=location_aka,level=level))
        gameworld.add_component(armour_piece, armour.AttributeBonus(
            majorname=majorname,
            majorbonus=majorbonus,
            minoronename=minoronename,
            minoronebonus=minoronebonus,
            minortwoname=minortwoname,
            minortwobonus=minortwobonus))

        return armour_piece

    def create_full_armour_set(gameworld, armourset, level, quality):
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
        print(armourset, level, quality)
        armour_set_file = read_json_file(constants.JSONFILEPATH + 'armoursets.json')

        full_armour_set = []

        for this_armour in armour_set_file['armoursets']:
            if this_armour['setname'] == armourset:
                if this_armour['level'] == level:
                    if this_armour['quality'] == quality:
                        bodylocation = this_armour['location']
                        quality = quality
                        weight = this_armour['weight']
                        setname = armourset
                        prefix = this_armour['prefix']
                        location_aka = this_armour['location aka']
                        level = level
                        defense = this_armour['defense']
                        majorname = this_armour['majorname']
                        majorbonus = this_armour['majorbonus']
                        minoronename = this_armour['minoronename']
                        minoronebonus = this_armour['minoronebonus']
                        minortwoname = this_armour['minortwoname']
                        minortwobonus = this_armour['minortwobonus']

                        piece_of_armour = ArmourClass.create_piece_of_armour(gameworld, bodylocation, quality,
                                        weight,setname, prefix,location_aka, level, defense,majorname,
                                        majorbonus, minoronename, minoronebonus, minortwoname, minortwobonus)

                        full_armour_set.append(piece_of_armour)

        return full_armour_set

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

    def describe_armour_at_bodylocation(gameworld, entity, bodylocation):
        """
        This method returns a string (see below)
        :param entity: the entity (mobile) to interrogate
        :param bodylocation: armour slot to interrogate
        :return: set name + ' ' + body locationAKA (alternate description)
        """
        armour_piece = ArmourClass.get_armour_piece_from_body_location(gameworld, entity, bodylocation)

        set_component = gameworld.component_for_entity(armour_piece, armour.Set)
        locationAKA_component = gameworld.component_for_entity(armour_piece, armour.LocationAKA)

        return set_component.label + ' ' + locationAKA_component.label

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