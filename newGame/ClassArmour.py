
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

    def create_full_armour_set(gameworld, armourset):
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

        armour_set_file = read_json_file(constants.JSONFILEPATH + 'armoursets.json')

        full_armour_set = []

        for armour in armour_set_file['armoursets']:
            if armour['setname'] == armourset:
                gm = gameworld
                bodylocation = armour['location']
                quality = armour['basic']
                weight = armour['weight']
                setname = armourset
                prefix = armour['prefix']
                location_aka = armour['location aka']
                level = armour['level']
                defense = armour['defense']
                majorname = armour['majorname']
                majorbonus = armour['majorbonus']
                minoronename = armour['minoronename']
                minoronebonus = armour['minoronebonus']
                minortwoname = armour['minortwoname']
                minortwobonus = armour['minortwobonus']

                piece_of_Armour = ArmourClass.create_piece_of_armour(gameworld, bodylocation, quality, weight, setname, prefix,
                                                   location_aka, level, defense,majorname, majorbonus, minoronename,
                                                   minoronebonus, minortwoname, minortwobonus)

                full_armour_set.append(piece_of_Armour)

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


