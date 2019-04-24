from newGame import constants
from components import items
from utilities import world, jsonUtilities
from utilities.itemsHelp import ItemUtilities
from utilities.mobileHelp import MobileUtilities
from loguru import logger
from mapRelated.gameMap import GameMap

import random
import tcod


class ItemManager:

    """
    The purpose of the ItemManager class is to:
    Create ALL items in the game
    Delete ALL items from the game
    Place items in the dungeon

    """

    def create_weapon(gameworld, weapon_type):
        """
        Currently this creates a new weapon using the information in an external file
        :type gameworld: esper.world
        :type weapon_type: the type of weapon to be created, e.g. sword
        """
        weapon_file = jsonUtilities.read_json_file(constants.JSONFILEPATH + 'weapons.json')
        for weapon in weapon_file['weapons']:
            if weapon['name'] == weapon_type:
                myweapon = world.get_next_entity_id(gameworld=gameworld)
                # generate common item components
                gameworld.add_component(myweapon, items.TypeOfItem(label='weapon'))
                gameworld.add_component(myweapon, items.Material)
                gameworld.add_component(myweapon, items.Describable(
                    description=weapon['description'],
                    name=weapon['display_name'],
                    glyph=weapon['glyph'],
                    fg=tcod.white,
                    bg=tcod.black,
                    displayname='wooden ' + weapon_type
                    # fg=weapon['fg_colour'],
                    # bg=weapon['bg_colour']
                ))
                # gameworld.add_component(myweapon, items.Location(x=0, y=0))
                gameworld.add_component(myweapon, items.RenderItem(istrue=True))
                gameworld.add_component(myweapon, items.Quality(level=weapon['quality_level']))

                # generate weapon specific components
                gameworld.add_component(myweapon, items.WeaponType(label=weapon_type))
                gameworld.add_component(myweapon, items.Spells(
                    slot_one=weapon['spell_slot_one'],
                    slot_two=weapon['spell_slot_two'],
                    slot_three=weapon['spell_slot_three'],
                    slot_four=weapon['spell_slot_four'],
                    slot_five=weapon['spell_slot_five']))

                gameworld.add_component(myweapon, items.Wielded(
                    main_hand=weapon['wielded_main_hand'],
                    off_hand=weapon['wielded_off_hand'],
                    both_hands=weapon['wielded_both_hands'],
                    true_or_false=True))

                gameworld.add_component(myweapon, items.Experience(current_level=1))

                gameworld.add_component(myweapon, items.Hallmarks(
                    hallmark_slot_one=weapon['hallmark_slot_one'],
                    hallmark_slot_two=weapon['hallmark_slot_two']))

                logger.info('Entity {} has been created using the {} template', myweapon, weapon['name'])
                return myweapon  # this is the entity id for the newly created weapon

    def create_piece_of_armour(gameworld, bodylocation, quality, setname, prefix, level, majorname, majorbonus, minoronename, minoronebonus):
        """
        This method creates a gameworld entity that's used as a piece of armour. It uses the Json file
        to create the 'base' entity - it's up to other methods to add flesh to these bones.
        :param setname:
        :param prefix:
        :param level:
        :param majorname:
        :param majorbonus:
        :param minoronename:
        :param minoronebonus:
        :param bodylocation:
        :param quality:
        :param gameworld:

        """
        armour_file = jsonUtilities.read_json_file(constants.JSONFILEPATH + 'armour.json')
        for piece_of_armour in armour_file['armour']:
            if piece_of_armour['location'] == bodylocation and piece_of_armour['quality'] == quality:
                armour_piece = world.get_next_entity_id(gameworld=gameworld)

                # generate common item components
                gameworld.add_component(armour_piece, items.TypeOfItem(label='armour'))
                gameworld.add_component(armour_piece, items.Describable(
                    name=piece_of_armour['location'] + ' armour',
                    glyph=piece_of_armour['glyph'],
                    description=piece_of_armour['location'] + ' armour',
                    fg=tcod.white,
                    bg=tcod.black,
                    displayname='cloth ' + piece_of_armour['type']))

                # gameworld.add_component(armour_piece, items.Location)
                gameworld.add_component(armour_piece, items.Material)
                gameworld.add_component(armour_piece, items.RenderItem(istrue=True))
                gameworld.add_component(armour_piece, items.Quality(level=piece_of_armour['quality']))

                # generate armour specifics
                gameworld.add_component(armour_piece, items.Weight(label=piece_of_armour['weight']))
                gameworld.add_component(armour_piece, items.Defense(value=piece_of_armour['defense']))

                if bodylocation == 'head':
                    gameworld.add_component(armour_piece, items.ArmourBodyLocation(head=True))

                if bodylocation == 'chest':
                    gameworld.add_component(armour_piece, items.ArmourBodyLocation(chest=True))

                if bodylocation == 'hands':
                    gameworld.add_component(armour_piece, items.ArmourBodyLocation(hands=True))

                if bodylocation == 'feet':
                    gameworld.add_component(armour_piece, items.ArmourBodyLocation(feet=True))

                if bodylocation == 'legs':
                    gameworld.add_component(armour_piece, items.ArmourBodyLocation(legs=True))

                gameworld.add_component(armour_piece, items.AttributeBonus(
                    majorname=majorname,
                    majorbonus=majorbonus,
                    minoronename=minoronename,
                    minoronebonus=minoronebonus))

                gameworld.add_component(armour_piece, items.ArmourSet(
                    label=setname,
                    prefix=prefix,
                    level=level))

                gameworld.add_component(armour_piece, items.ArmourBeingWorn(status=False))

                logger.info('Entity {} has been created as a piece of {} armour', armour_piece, bodylocation)

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
        armour_set_file = jsonUtilities.read_json_file(constants.JSONFILEPATH + 'armoursets.json')

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

                        piece_of_armour = ItemManager.create_piece_of_armour(gameworld, bodylocation, quality,
                                            setname, prefix, level, majorname, majorbonus, minoronename, minoronebonus)

                        full_armour_set.append(piece_of_armour)

        return full_armour_set

    def create_bag(gameworld):
        bags_file = jsonUtilities.read_json_file(constants.JSONFILEPATH + 'bags.json')
        bag_count = 0
        for this_bag in bags_file['bags']:
            new_bag = world.get_next_entity_id(gameworld=gameworld)
            bag_count += 1

            # generate common item components
            gameworld.add_component(new_bag, items.TypeOfItem(label='bag'))
            gameworld.add_component(new_bag, items.Describable(
                description=this_bag['description'],
                name=this_bag['description'],
                glyph=this_bag['glyph'],
                fg=tcod.white,
                bg=tcod.black))
            # gameworld.add_component(new_bag, items.Location(x=0, y=0))
            gameworld.add_component(new_bag, items.Material(texture=this_bag['material']))
            gameworld.add_component(new_bag, items.RenderItem)
            gameworld.add_component(new_bag, items.Quality(level=this_bag['quality']))

            # generate bag specific components
            gameworld.add_component(new_bag, items.SlotSize(maxsize=this_bag['slots'], populated=0))
            # gameworld.add_component(new_bag, items.Owner(entity))
            # gameworld.add_component(new_bag, items.BagBeingUsed)
            logger.info('New bag created as entity {} and a description of {}', new_bag, this_bag['description'])

            return new_bag

    def create_jewellery(gameworld, bodylocation, e_setting, e_hook, e_activator):
        """
        Will create a piece of jewellery the e_setting informs the tier, e.g. copper is only used in Tier 1 jewellery
        The e_activator is the gemstone - this drives the attribute bonuses

        :param bodylocation:
        :param e_setting: the quality level of the jewellery and the base metal used, e.g. copper
        :param e_hook: a 3rd component used in crafting
        :param e_activator: the gemstone used in the jewellery, drives the attribute bonus
        :return:
        """
        if e_setting == '' or e_activator == '' or e_hook == '':
            logger.debug('At least one base component is missing')
            return 0
        if e_setting != e_hook:
            logger.debug("Jewellery setting and hook base metals don't match")
            return 0

        gemstone_file = jsonUtilities.read_json_file(constants.JSONFILEPATH + 'gemstones.json')

        for gemstone in gemstone_file['gemstones']:
            if gemstone['Stone'] == e_activator:
                piece_of_jewellery = world.get_next_entity_id(gameworld=gameworld)
                # generate common item components
                gameworld.add_component(piece_of_jewellery, items.TypeOfItem(label='jewellery'))
                gameworld.add_component(piece_of_jewellery, items.Material(texture=e_setting))
                gameworld.add_component(piece_of_jewellery, items.RenderItem(istrue=True))
                gameworld.add_component(piece_of_jewellery, items.Quality(level='common'))

                # create jewellery specific components
                gameworld.add_component(piece_of_jewellery, items.JewelleryEquipped(istrue=False))
                desc = 'a ' + e_setting
                nm = ''

                if bodylocation == 'ear':
                    # create an earring
                    desc += ' earring, offset with a ' + e_activator + ' gemstone.'
                    nm = 'earring'
                    gameworld.add_component(piece_of_jewellery, items.JewelleryBodyLocation(ears=True))
                    gameworld.add_component(piece_of_jewellery, items.JewelleryStatBonus(
                        statname=gemstone['Attribute'],
                        statbonus=gemstone['Earring']))
                elif bodylocation == 'neck':
                    # create an amulet
                    desc += ' amulet, offset with a ' + e_activator + ' gemstone.'
                    nm = 'amulet'
                    gameworld.add_component(piece_of_jewellery, items.JewelleryBodyLocation(neck=True))
                    gameworld.add_component(piece_of_jewellery, items.JewelleryStatBonus(
                        statname=gemstone['Attribute'],
                        statbonus=gemstone['Amulet']))
                else:
                    # create a ring
                    desc += ' ring, offset with a ' + e_activator + ' gemstone.'
                    nm = 'ring'
                    gameworld.add_component(piece_of_jewellery, items.JewelleryBodyLocation(fingers=True))
                    gameworld.add_component(piece_of_jewellery, items.JewelleryStatBonus(
                        statname=gemstone['Attribute'],
                        statbonus=gemstone['Ring']))

                gameworld.add_component(piece_of_jewellery, items.Describable(
                    description=desc,
                    name=nm,
                    glyph=gemstone['glyph'],
                    fg=tcod.blue,
                    bg=tcod.black,
                    displayname=e_activator + ' ' + nm))
                logger.info('Created {}', desc)
                return piece_of_jewellery

    def place_item_in_dungeon(gameworld, item_to_be_placed, game_map):
        """

        :param game_map: holds the current view of the world
        :param item_to_be_placed: gameworld.entity
        :return:

        This method will look for a suitable location in the dungeon to place an item.
        Over time I imagine this will evolve into lots of constraints and possibly be removed
        in favour of something else. 22/4/19
        """

        if item_to_be_placed == 0:
            return False
        logger.info('Placing {} in the dungeon', item_to_be_placed)

        # get player entity
        player_entity = MobileUtilities.get_player_entity(gameworld=gameworld)
        if player_entity == 0:
            logger.warning('Cannot resolve player entity')
            return False

        # lets take the simple approach - place items near player start position
        # and on the dungeon floor. Plus no more than one item per dungeon location

        # Check if item can be rendered on to the dungeon
        can_be_rendered = ItemUtilities.get_item_can_be_rendered(gameworld=gameworld, entity=item_to_be_placed)
        gameworld.add_component(item_to_be_placed, items.Location(x=0, y=0))
        item_has_been_placed = False
        if can_be_rendered:

            # get items current location --> if already exists then it is already placed in the dungeon
            item_dungeon_posx, item_dungeon_posy = ItemUtilities.get_item_location(gameworld=gameworld, entity=item_to_be_placed)
            if item_dungeon_posx > 0 or item_dungeon_posy > 0:
                logger.info('Item is already in the dungeon, cannot place twice')
                return False
            # get player current location
            player_pos_x, player_pos_y = MobileUtilities.get_mobile_current_location(gameworld=gameworld, mobile=player_entity)
            if player_pos_x == 0 or player_pos_y == 0:
                logger.warning('Cannot resolve players current position')
                return False
            # pick random location in the dungeon --> that's near the player location but not in a wall
            max_attempts = 500
            attempts = 0
            while not item_has_been_placed and attempts < max_attempts:
                ix = random.randrange(1, constants.MAP_WIDTH)
                iy = random.randrange(1, constants.MAP_HEIGHT)
                tile = GameMap.get_type_of_tile(game_map, ix, iy)
                if tile == constants.TILE_TYPE_FLOOR:
                    ItemUtilities.set_item_location(gameworld=gameworld, entity=item_to_be_placed, posx=ix, posy=iy)
                    logger.info('...at location {} / {}', ix, iy)
                    logger.info('Player located at {}/{}', player_pos_x, player_pos_y)
                    attempts = 499
                    item_has_been_placed = True
                attempts += 1

        return item_has_been_placed




