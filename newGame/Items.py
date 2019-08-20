
from components import items
from utilities import world, jsonUtilities
from utilities.itemsHelp import ItemUtilities
from utilities.mobileHelp import MobileUtilities
from utilities import configUtilities
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

    def create_weapon(gameworld, weapon_type, game_config):
        """
        Currently this creates a new weapon using the information in an external file
        :type gameworld: esper.world
        :type weapon_type: the type of weapon to be created, e.g. sword
        """
        weapon_file_path = configUtilities.get_config_value_as_string(configfile=game_config, section='default', parameter='WEAPONSFILE')
        weapon_action_list = configUtilities.get_config_value_as_list(configfile=game_config, section='game', parameter='ITEM_WEAPON_ACTIONS')

        weapon_file = jsonUtilities.read_json_file(weapon_file_path)
        for weapon in weapon_file['weapons']:
            if weapon['name'] == weapon_type:
                myweapon = world.get_next_entity_id(gameworld=gameworld)
                # generate common item components
                gameworld.add_component(myweapon, items.TypeOfItem(label='weapon'))
                gameworld.add_component(myweapon, items.Material(texture='wooden'))
                gameworld.add_component(myweapon, items.Actionlist(action_list=weapon_action_list))
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
                    hands=weapon['wielded_hands'],
                    true_or_false=True))

                gameworld.add_component(myweapon, items.Experience(current_level=1))

                gameworld.add_component(myweapon, items.Hallmarks(
                    hallmark_slot_one=weapon['hallmark_slot_one'],
                    hallmark_slot_two=weapon['hallmark_slot_two']))

                logger.info('Entity {} has been created using the {} template', myweapon, weapon['name'])
                return myweapon  # this is the entity id for the newly created weapon

    @staticmethod
    def create_piece_of_armour(gameworld, bodylocation, setname, prefix, game_config):

        armour_action_list = configUtilities.get_config_value_as_list(configfile=game_config, section='game',
                                                                      parameter='ITEM_ARMOUR_ACTIONS')

        armour_set_path = configUtilities.get_config_value_as_string(configfile=game_config, section='default',
                                                                     parameter='ARMOURSETFILE')

        armour_set_file = jsonUtilities.read_json_file(armour_set_path)

        armour_piece = world.get_next_entity_id(gameworld=gameworld)

        pxstring = 'prefix'
        attnamestring = 'attributename'
        attvaluestring = 'attributebonus'
        display = ''
        defense = ''

        for armourset in armour_set_file['armoursets']:
            if armourset['displayname'] == setname:
                as_display_name = (armourset['displayname'])
                as_weight = (armourset['weight'])
                as_quality = armourset['quality']
                as_flavour = (armourset['flavour'])
                as_material = (armourset['material'])
                prefix_count = armourset['prefixcount']
                attribute_bonus_count = armourset['attributebonuscount']
                if bodylocation == 'head':
                    gameworld.add_component(armour_piece, items.ArmourBodyLocation(head=True))
                    display = armourset['head']['display']
                    defense = armourset['head']['defense']
                if bodylocation == 'chest':
                    gameworld.add_component(armour_piece, items.ArmourBodyLocation(chest=True))
                    display = armourset['chest']['display']
                    defense = armourset['chest']['defense']
                if bodylocation == 'hands':
                    gameworld.add_component(armour_piece, items.ArmourBodyLocation(hands=True))
                    display = armourset['hands']['display']
                    defense = armourset['hands']['defense']
                if bodylocation == 'feet':
                    gameworld.add_component(armour_piece, items.ArmourBodyLocation(feet=True))
                    display = armourset['feet']['display']
                    defense = armourset['feet']['defense']
                if bodylocation == 'legs':
                    gameworld.add_component(armour_piece, items.ArmourBodyLocation(legs=True))
                    display = armourset['legs']['display']
                    defense = armourset['legs']['defense']

                for px in range(1, prefix_count + 1):
                    prefix_string = pxstring + str(px)
                    if armourset[prefix_string]['name'] == prefix:
                        as_prefix = prefix
                        if attribute_bonus_count > 1:
                            att_bonus_string = attvaluestring + str(px)
                            att_name_string = attnamestring + str(px)
                        else:
                            att_bonus_string = attvaluestring + str(1)
                            att_name_string = attnamestring + str(1)

                        px_att_bonus = armourset[prefix_string][att_bonus_string]
                        px_att_name = armourset[prefix_string][att_name_string]

        # generate common item components
        gameworld.add_component(armour_piece, items.TypeOfItem(label='armour'))
        gameworld.add_component(armour_piece, items.Material(texture=as_material))
        gameworld.add_component(armour_piece, items.Actionlist(action_list=armour_action_list))
        gameworld.add_component(armour_piece, items.Describable(
            name=bodylocation + ' armour',
            glyph=")",
            description='a ' + display + ' made from ' + as_material,
            fg=tcod.white,
            bg=tcod.black,
            displayname=display))
        gameworld.add_component(armour_piece, items.RenderItem(istrue=True))
        gameworld.add_component(armour_piece, items.Quality(level=as_quality))

        # generate armour specifics
        gameworld.add_component(armour_piece, items.Weight(label=as_weight))
        gameworld.add_component(armour_piece, items.Defense(value=int(defense)))

        gameworld.add_component(armour_piece, items.AttributeBonus(
            majorname=px_att_name,
            majorbonus=int(px_att_bonus),
            minoronename='',
            minoronebonus=0))

        gameworld.add_component(armour_piece, items.ArmourSet(label=setname, prefix=prefix, level=0))
        gameworld.add_component(armour_piece, items.ArmourBeingWorn(status=False))

        return armour_piece

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

        head_armour = ItemManager.create_piece_of_armour(gameworld=gameworld, game_config=game_config,
                                                         setname=armourset, prefix=prefix, bodylocation='head')
        full_armour_set.append(head_armour)

        chest_armour = ItemManager.create_piece_of_armour(gameworld=gameworld, game_config=game_config,
                                                          setname=armourset, prefix=prefix, bodylocation='chest')
        full_armour_set.append(chest_armour)

        hands_armour = ItemManager.create_piece_of_armour(gameworld=gameworld, game_config=game_config,
                                                          setname=armourset, prefix=prefix, bodylocation='hands')
        full_armour_set.append(hands_armour)

        legs_armour = ItemManager.create_piece_of_armour(gameworld=gameworld, game_config=game_config,
                                                         setname=armourset, prefix=prefix, bodylocation='legs')
        full_armour_set.append(legs_armour)

        feet_armour = ItemManager.create_piece_of_armour(gameworld=gameworld, game_config=game_config,
                                                         setname=armourset, prefix=prefix, bodylocation='feet')
        full_armour_set.append(feet_armour)

        return full_armour_set

    def create_bag(gameworld, game_config):

        bag_file_path = configUtilities.get_config_value_as_string(configfile=game_config, section='default',
                                                                      parameter='BAGSFILE')
        bag_action_list = configUtilities.get_config_value_as_list(configfile=game_config, section='game',
                                                                      parameter='ITEM_ARMOUR_ACTIONS')

        bags_file = jsonUtilities.read_json_file(bag_file_path)
        bag_count = 0
        for this_bag in bags_file['bags']:
            new_bag = world.get_next_entity_id(gameworld=gameworld)
            bag_count += 1

            # generate common item components
            gameworld.add_component(new_bag, items.TypeOfItem(label='bag'))
            gameworld.add_component(new_bag, items.Actionlist(action_list=bag_action_list))
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

    def create_jewellery(gameworld, bodylocation, e_setting, e_hook, e_activator, game_config):
        """
        Will create a piece of jewellery the e_setting informs the tier, e.g. copper is only used in Tier 1 jewellery
        The e_activator is the gemstone - this drives the attribute bonuses

        :param bodylocation:
        :param e_setting: the quality level of the jewellery and the base metal used, e.g. copper
        :param e_hook: a 3rd component used in crafting
        :param e_activator: the gemstone used in the jewellery, drives the attribute bonus
        :return:
        """
        trinket_setting = e_setting.lower()
        trinket_hook = e_hook.lower()
        trinket_activator = e_activator.lower()

        gemstones_file_path = configUtilities.get_config_value_as_string(configfile=game_config, section='default',
                                                                      parameter='GEMSTONESFILE')
        jewellery_action_list = configUtilities.get_config_value_as_list(configfile=game_config, section='game',
                                                                      parameter='ITEM_JEWELLERY_ACTIONS')
        if trinket_setting == '' or trinket_activator == '' or trinket_hook == '':
            logger.debug('At least one base component is missing')
            return 0
        if trinket_setting != trinket_hook:
            logger.debug("Jewellery setting and hook base metals don't match")
            return 0

        gemstone_file = jsonUtilities.read_json_file(gemstones_file_path)

        for gemstone in gemstone_file['gemstones']:
            file_gemstone = gemstone['Stone'].lower()
            if file_gemstone == trinket_activator:
                piece_of_jewellery = world.get_next_entity_id(gameworld=gameworld)
                # generate common item components
                gameworld.add_component(piece_of_jewellery, items.TypeOfItem(label='jewellery'))
                gameworld.add_component(piece_of_jewellery, items.Material(texture=trinket_setting))
                gameworld.add_component(piece_of_jewellery, items.RenderItem(istrue=True))
                gameworld.add_component(piece_of_jewellery, items.Quality(level='common'))
                gameworld.add_component(piece_of_jewellery, items.Actionlist(action_list=jewellery_action_list))

                # create jewellery specific components
                gameworld.add_component(piece_of_jewellery, items.JewelleryEquipped(istrue=False))
                desc = 'a ' + trinket_setting
                nm = ''

                if 'ear' in bodylocation:
                    # create an earring
                    desc += ' earring, offset with a ' + trinket_activator + ' gemstone.'
                    nm = 'earring'
                    gameworld.add_component(piece_of_jewellery, items.JewelleryBodyLocation(ears=True))
                    gameworld.add_component(piece_of_jewellery, items.JewelleryStatBonus(
                        statname=gemstone['Attribute'],
                        statbonus=gemstone['Earring']))
                elif bodylocation == 'neck':
                    # create an amulet
                    desc += ' amulet, offset with a ' + trinket_activator + ' gemstone.'
                    nm = 'amulet'
                    gameworld.add_component(piece_of_jewellery, items.JewelleryBodyLocation(neck=True))
                    gameworld.add_component(piece_of_jewellery, items.JewelleryStatBonus(
                        statname=gemstone['Attribute'],
                        statbonus=gemstone['Amulet']))
                else:
                    # create a ring
                    desc += ' ring, offset with a ' + trinket_activator + ' gemstone.'
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
                    displayname=trinket_activator + ' ' + nm))
                logger.info('Created {}', desc)
                return piece_of_jewellery

    def place_item_in_dungeon(gameworld, item_to_be_placed, game_map, game_config):
        """

        :param game_map: holds the current view of the world
        :param item_to_be_placed: gameworld.entity
        :return:

        This method will look for a suitable location in the dungeon to place an item.
        Over time I imagine this will evolve into lots of constraints and possibly be removed
        in favour of something else. 22/4/19
        """
        map_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='game', parameter='MAP_WIDTH')
        map_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='game', parameter='MAP_HEIGHT')
        tile_type_floor = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon', parameter='TILE_TYPE_FLOOR')

        if item_to_be_placed == 0:
            return False
        # logger.info('Placing {} in the dungeon', item_to_be_placed)

        # get player entity
        player_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
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
                ix = random.randrange(1, map_width)
                iy = random.randrange(1, map_height)
                tile = GameMap.get_type_of_tile(game_map, ix, iy)
                if tile == tile_type_floor:
                    ItemUtilities.set_item_location(gameworld=gameworld, item_entity=item_to_be_placed, posx=ix, posy=iy)
                    # logger.info('...at location {} / {}', ix, iy)
                    # logger.info('Player located at {}/{}', player_pos_x, player_pos_y)
                    attempts = 499
                    item_has_been_placed = True
                attempts += 1

        return item_has_been_placed




