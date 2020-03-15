from components import mobiles, items, spellBar
from loguru import logger
from utilities.itemsHelp import ItemUtilities, display_inspect_panel
from utilities import world
from utilities import configUtilities, colourUtilities

import numbers
import tcod


class MobileUtilities(numbers.Real):

    #
    # general methods
    #

    @staticmethod
    def create_armour_for_npc(gameworld, entity_id, armour_modifier, px_bonus):
        if armour_modifier.lower() == 'healer':
            current_healingpower = MobileUtilities.get_mobile_healing_power(gameworld=gameworld, entity=entity_id)
            new_bonus = current_healingpower + px_bonus
            MobileUtilities.set_mobile_healing_power(gameworld=gameworld, entity=entity_id, value=new_bonus)

        if armour_modifier.lower() == 'malign':
            current_condidamage = MobileUtilities.get_mobile_condition_damage(gameworld=gameworld, entity=entity_id)
            new_bonus = current_condidamage + px_bonus
            MobileUtilities.set_mobile_condition_damage(gameworld=gameworld, entity=entity_id, value=new_bonus)

        if armour_modifier.lower() == 'mighty':
            current_power = MobileUtilities.get_mobile_power(gameworld=gameworld, entity=entity_id)
            new_bonus = current_power + px_bonus
            MobileUtilities.set_mobile_power(gameworld=gameworld, entity=entity_id, value=new_bonus)

        if armour_modifier.lower() == 'precise':
            current_precision = MobileUtilities.get_mobile_precision(gameworld=gameworld, entity=entity_id)
            new_bonus = current_precision + px_bonus
            MobileUtilities.set_mobile_precision(gameworld=gameworld, entity=entity_id, value=new_bonus)

        if armour_modifier.lower() == 'resilient':
            current_toughness = MobileUtilities.get_mobile_toughness(gameworld=gameworld, entity=entity_id)
            new_bonus = current_toughness + px_bonus
            MobileUtilities.set_mobile_toughness(gameworld=gameworld, entity=entity_id, value=new_bonus)

        if armour_modifier.lower() == 'vital':
            current_vitality = MobileUtilities.get_mobile_vitality(gameworld=gameworld, entity=entity_id)
            new_bonus = current_vitality + px_bonus
            MobileUtilities.set_mobile_vitality(gameworld=gameworld, entity=entity_id, value=new_bonus)

    @staticmethod
    def set_player_gender(gameworld, entity, gender):
        describable_component = gameworld.component_for_entity(entity, mobiles.Describable)
        describable_component.gender = gender

    @staticmethod
    def get_player_gender(gameworld, entity):
        gender = gameworld.component_for_entity(entity, mobiles.Describable).gender
        return gender

    @staticmethod
    def setup_racial_attributes(gameworld, player, selected_race, race_size, bg):
        describable_component = gameworld.component_for_entity(player, mobiles.Describable)
        describable_component.background = bg
        race_component = gameworld.component_for_entity(player, mobiles.Race)
        race_component.label = selected_race
        race_component.size = race_size

    @staticmethod
    def setup_class_attributes(gameworld, player, selected_class, health, spellfile):

        gameworld.component_for_entity(player, mobiles.CharacterClass).label = selected_class
        gameworld.component_for_entity(player, mobiles.CharacterClass).spellfile = spellfile
        gameworld.component_for_entity(player, mobiles.CharacterClass).baseHealth = health

    @staticmethod
    def get_player_entity(gameworld, game_config):
        player_ai = configUtilities.get_config_value_as_integer(configfile=game_config, section='game',
                                                                parameter='AI_LEVEL_PLAYER')

        player = 0
        for ent, ai in gameworld.get_component(mobiles.AI):
            if ai.ailevel == player_ai:
                player = ent

        return player

    @staticmethod
    def get_number_as_a_percentage(lower_value, maximum_value):
        return int((lower_value / maximum_value) * 100)

    @staticmethod
    def get_bar_count(lower_value, bar_depth):
        return (lower_value / 100) * bar_depth

    @staticmethod
    def has_player_moved(gameworld, game_config):
        entity = MobileUtilities.get_player_entity(gameworld, game_config)

        position_component = gameworld.component_for_entity(entity, mobiles.Position)

        return position_component.hasMoved

    @staticmethod
    def set_mobile_position(gameworld, entity, posx, posy):
        gameworld.add_component(entity, mobiles.Position(x=posx, y=posy, hasMoved=True))

    @staticmethod
    def get_mobile_x_position(gameworld, entity):
        position_component = gameworld.component_for_entity(entity, mobiles.Position)

        return position_component.x

    @staticmethod
    def get_mobile_y_position(gameworld, entity):
        position_component = gameworld.component_for_entity(entity, mobiles.Position)

        return position_component.y

    @staticmethod
    def set_player_velocity(gameworld, player_entity, direction, speed):
        player_velocity_component = gameworld.component_for_entity(player_entity, mobiles.Velocity)
        dx = 0
        dy = 0
        if direction == 'left':
            dx = -speed
            dy = 0
        if direction == 'right':
            dx = speed
            dy = 0
        if direction == 'up':
            dx = 0
            dy = -speed
        if direction == 'down':
            dx = 0
            dy = speed
        player_velocity_component.dx = dx
        player_velocity_component.dy = dy

    @staticmethod
    def get_player_velocity(gameworld, player_entity):
        player_velocity_component = gameworld.component_for_entity(player_entity, mobiles.Velocity)
        return player_velocity_component.dx, player_velocity_component.dy

    @staticmethod
    def set_mobile_has_moved(gameworld, mobile, status):
        position_component = gameworld.component_for_entity(mobile, mobiles.Position)
        position_component.hasMoved = status

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
    def set_mobile_first_name(gameworld, entity, name):
        firstname_component = gameworld.component_for_entity(entity, mobiles.Name)
        firstname_component.first = name

    @staticmethod
    def set_mobile_last_name(gameworld, entity, name):
        firstname_component = gameworld.component_for_entity(entity, mobiles.Name)
        firstname_component.suffix = name

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
    def calculate_mobile_personality(gameworld, game_config):
        player_entity = MobileUtilities.get_player_entity(gameworld, game_config)

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
    def unequip_all_weapons(gameworld, entity):
        MobileUtilities.unequip_weapon(gameworld, entity, 'main')
        MobileUtilities.unequip_weapon(gameworld, entity, 'off')
        MobileUtilities.unequip_weapon(gameworld, entity, 'both')

    @staticmethod
    def unequip_weapon(gameworld, entity, hand):

        if hand == 'main':
            gameworld.component_for_entity(entity, mobiles.Equipped).main_hand = 0
        if hand == 'off':
            gameworld.component_for_entity(entity, mobiles.Equipped).off_hand = 0
        if hand == 'both':
            gameworld.component_for_entity(entity, mobiles.Equipped).both_hands = 0

    @staticmethod
    def get_next_entity_id(gameworld):
        entity = world.get_next_entity_id(gameworld=gameworld)

        return entity

    @staticmethod
    def create_base_mobile(gameworld, game_config, entity_id):
        ai = configUtilities.get_config_value_as_integer(configfile=game_config, section='game',
                                                         parameter='AI_LEVEL_NONE')

        gameworld.add_component(entity_id, mobiles.Describable(description='', glyph='',
                                                               foreground=colourUtilities.get('WHITE'),
                                                               background=colourUtilities.get('BLACK'),
                                                               personality='', gender='', image=0))
        gameworld.add_component(entity_id,
                                mobiles.CharacterClass(label='', base_health=0, style='balanced', spellfile=''))
        gameworld.add_component(entity_id, mobiles.AI(ailevel=ai))
        gameworld.add_component(entity_id, mobiles.Inventory())
        gameworld.add_component(entity_id, mobiles.Armour())
        gameworld.add_component(entity_id, mobiles.Jewellery())
        gameworld.add_component(entity_id, mobiles.Equipped())
        gameworld.add_component(entity_id, mobiles.Velocity())
        gameworld.add_component(entity_id, mobiles.ManaPool(current=500, maximum=1000))
        gameworld.add_component(entity_id, mobiles.Renderable(is_visible=True))
        gameworld.add_component(entity_id, mobiles.StatusEffects())
        gameworld.add_component(entity_id, mobiles.PrimaryAttributes())
        gameworld.add_component(entity_id, mobiles.SecondaryAttributes())
        gameworld.add_component(entity_id, mobiles.DerivedAttributes())
        gameworld.add_component(entity_id, mobiles.SpellBar(entityId=0))
        gameworld.add_component(entity_id, mobiles.Race(race='', size=''))
        gameworld.add_component(entity_id, mobiles.Position())
        gameworld.add_component(entity_id, mobiles.Name())

    @staticmethod
    def create_player_character(gameworld, game_config, player_entity):
        player_ai = configUtilities.get_config_value_as_integer(configfile=game_config, section='game',
                                                                parameter='AI_LEVEL_PLAYER')
        gameworld.add_component(player_entity, mobiles.Describable(description='something', glyph='@',
                                                                   foreground=colourUtilities.get('ORANGE'),
                                                                   background=colourUtilities.get('BLACK'),
                                                                   personality='Unpredictable', gender='neutral',
                                                                   image=11))
        gameworld.add_component(player_entity,
                                mobiles.CharacterClass(label='', base_health=0, style='balanced', spellfile=''))
        gameworld.add_component(player_entity, mobiles.Name(first='', suffix=''))
        gameworld.add_component(player_entity, mobiles.AI(ailevel=player_ai))
        gameworld.add_component(player_entity, mobiles.Personality())
        gameworld.add_component(player_entity, mobiles.SpecialBar(valuecurrent=10, valuemaximum=100))
        gameworld.add_component(player_entity, mobiles.SpellBar(entityId=0))
        gameworld.add_component(player_entity,
                                mobiles.ClothingImage(head=0, back=21, front=22, feet=23, weapon=24, hands=0, shield=0,
                                                      legs=0, chest=0, shoulders=0))

    @staticmethod
    def set_mobile_visible(gameworld, entity):
        gameworld.add_component(entity, mobiles.Renderable(is_visible=True))

    @staticmethod
    def set_mobile_invisible(gameworld, entity):
        gameworld.add_component(entity, mobiles.Renderable(is_visible=False))

    @staticmethod
    def get_mobile_renderstate(gameworld, entity):
        render_component = gameworld.component_for_entity(entity, mobiles.Renderable)
        return render_component.is_visible

    @staticmethod
    def set_mobile_description(gameworld, entity, value):
        gameworld.component_for_entity(entity, mobiles.Describable).description = value

    @staticmethod
    def set_mobile_glyph(gameworld, entity, value):
        gameworld.component_for_entity(entity, mobiles.Describable).glyph = value

    @staticmethod
    def get_mobile_glyph(gameworld, entity):
        describe_component = gameworld.component_for_entity(entity, mobiles.Describable)

        return describe_component.glyph

    @staticmethod
    def get_mobile_fg_render_colour(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.Describable).foreground

    @staticmethod
    def get_mobile_bg_render_colour(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.Describable).background

    @staticmethod
    def set_mobile_fg_render_colour(gameworld, entity, value):
        gameworld.component_for_entity(entity, mobiles.Describable).foreground = colourUtilities.get(value)

    @staticmethod
    def set_mobile_bg_render_colour(gameworld, entity, value):
        gameworld.component_for_entity(entity, mobiles.Describable).background = colourUtilities.get(value)

    @staticmethod
    def set_mobile_render_image(gameworld, entity, value):
        gameworld.component_for_entity(entity, mobiles.Describable).image = value

    @staticmethod
    def set_entity_ai(gameworld, entity, value):
        gameworld.component_for_entity(entity, mobiles.AI).ailevel = value

    @staticmethod
    def create_spell_bar_as_entity(gameworld):
        spell_bar = MobileUtilities.get_next_entity_id(gameworld=gameworld)

        gameworld.add_component(spell_bar, spellBar.SlotOne())
        gameworld.add_component(spell_bar, spellBar.SlotTwo())
        gameworld.add_component(spell_bar, spellBar.SlotThree())
        gameworld.add_component(spell_bar, spellBar.SlotFour())
        gameworld.add_component(spell_bar, spellBar.SlotFive())
        gameworld.add_component(spell_bar, spellBar.SlotSix())
        gameworld.add_component(spell_bar, spellBar.SlotSeven())
        gameworld.add_component(spell_bar, spellBar.SlotEight())
        gameworld.add_component(spell_bar, spellBar.SlotNine())
        gameworld.add_component(spell_bar, spellBar.SlotTen())

        return spell_bar

    @staticmethod
    def set_spellbar_for_entity(gameworld, entity, spellbarEntity):
        gameworld.add_component(entity, mobiles.SpellBar(entityId=spellbarEntity))

    @staticmethod
    def get_spellbar_id_for_entity(gameworld, entity):
        spellbar_component = gameworld.component_for_entity(entity, mobiles.SpellBar)

        return spellbar_component.entityId

    @staticmethod
    def set_viewport_for_player(gameworld, entity, viewportId):
        gameworld.add_component(entity, mobiles.Viewport(entityId=viewportId))

    @staticmethod
    def get_viewport_id(gameworld, entity):
        viewport_component = gameworld.component_for_entity(entity, mobiles.Viewport)

        return viewport_component.entityId

    @staticmethod
    def set_MessageLog_for_player(gameworld, entity, logid):
        gameworld.add_component(entity, mobiles.MessageLog(entityId=logid))

    @staticmethod
    def get_MessageLog_id(gameworld, entity):
        messagelog_component = gameworld.component_for_entity(entity, mobiles.MessageLog)

        return messagelog_component.entityId

    @staticmethod
    def describe_the_mobile(gameworld, entity):
        player_name_component = gameworld.component_for_entity(entity, mobiles.Name)
        player_race_component = gameworld.component_for_entity(entity, mobiles.Race)
        player_class = MobileUtilities.get_character_class(gameworld, entity)
        player_gender = MobileUtilities.get_player_gender(gameworld, entity)
        player_style = MobileUtilities.get_character_style(gameworld, entity)

        return player_name_component.first + ' is a ' + player_gender + ' ' + player_race_component.label + ' ' + player_class + ' ( ' + player_style + ' )'

    @staticmethod
    def get_character_style(gameworld, entity):
        player_character_style_component = gameworld.component_for_entity(entity, mobiles.CharacterClass)
        return player_character_style_component.style

    @staticmethod
    def get_character_class(gameworld, entity):
        player_class_component = gameworld.component_for_entity(entity, mobiles.CharacterClass)
        return player_class_component.label

    @staticmethod
    def get_character_class_spellfilename(gameworld, entity):
        player_class_component = gameworld.component_for_entity(entity, mobiles.CharacterClass)
        return player_class_component.spellfile

    #
    # Mobile actions
    #

    # inspect an item
    @staticmethod
    def inspect_item(gameworld, item_entity, game_config):
        display_inspect_panel(gameworld=gameworld, display_mode='inspect', item_entity=item_entity,
                              game_config=game_config)

    # pick up item from dungeon floor
    @staticmethod
    def mobile_pick_up_item(gameworld, mobile):
        px, py = MobileUtilities.get_mobile_current_location(gameworld=gameworld, mobile=mobile)
        mobile_inventory_component = gameworld.component_for_entity(mobile, mobiles.Inventory)
        for ent, (rend, loc, desc) in gameworld.get_components(items.RenderItem, items.Location, items.Describable):
            if loc.x == px and loc.y == py:
                if rend.isTrue:
                    # check if mobile has enough space in their inventory
                    # remove item location data
                    gameworld.remove_component(ent, items.Location)
                    # add item entity to mobiles' inventory
                    mobile_inventory_component.items.append(ent)
                    logger.info('{} has been picked up', desc.name)

    # drop item from inventory
    @staticmethod
    def drop_item_from_inventory(gameworld, mobile, entity):
        # is item in inventory
        # add dungeon position component
        ItemUtilities.add_dungeon_position_component(gameworld=gameworld, entity=entity)

        # set item location to mobile's location
        px, py = MobileUtilities.get_mobile_current_location(gameworld=gameworld, mobile=mobile)
        ItemUtilities.set_item_location(gameworld=gameworld, item_entity=entity, posx=px, posy=py)

        # remove item from inventory component
        ItemUtilities.remove_item_from_inventory(gameworld, mobile, entity)

    # destroy item from inventory
    @staticmethod
    def destroy_item_from_inventory(gameworld, mobile, entity):

        # remove item from inventory component
        ItemUtilities.remove_item_from_inventory(gameworld, mobile, entity)

        # remove entity from gameworld
        ItemUtilities.delete_item(gameworld=gameworld, entity=entity)

    # equip armour from inventory
    @staticmethod
    def equip_armour_from_inventory(gameworld, mobile, armour_piece):
        # worn_body_armour = 0
        # determine body location from armour piece
        body_location = ItemUtilities.get_armour_body_location(gameworld=gameworld, armour_piece=armour_piece)

        # if there's any armour already being worn then store that entity
        worn_body_armour = ItemUtilities.get_armour_entity_from_body_location(gameworld=gameworld, entity=mobile,
                                                                              bodylocation=body_location)

        # unequip current armour from body location
        ItemUtilities.unequip_piece_of_armour(gameworld=gameworld, entity=mobile, bodylocation=body_location)

        # remove unequipped armour from inventory component
        ItemUtilities.remove_item_from_inventory(gameworld, mobile, armour_piece)

        # equip new armour to body location
        ItemUtilities.equip_piece_of_armour(gameworld=gameworld, entity=mobile, piece_of_armour=armour_piece,
                                            bodylocation=body_location)

        # add original armour to the inventory
        if worn_body_armour != 0:
            mobile_inventory_component = gameworld.component_for_entity(mobile, mobiles.Inventory)
            mobile_inventory_component.items.append(worn_body_armour)

        # # determine which body location is being swapped out
        # if body_location == 'head':
        #     # Is armour already being worn here
        #     ap = MobileUtilities.is_entity_wearing_head_armour(gameworld=gameworld, entity=mobile)
        #     if ap != 0:
        #         worn_body_armour = ItemUtilities.get_armour_entity_from_body_location(gameworld=gameworld, entity=mobile, bodylocation='head')
        #         ItemUtilities.unequip_piece_of_armour(gameworld=gameworld,entity=mobile, bodylocation='head')
        #     ItemUtilities.equip_piece_of_armour(gameworld=gameworld, entity=mobile,piece_of_armour=armour_piece, bodylocation=body_location)
        #
        # if body_location == 'chest':
        #     ap = MobileUtilities.is_entity_wearing_chest_armour(gameworld=gameworld, entity=mobile)
        #     if ap != 0:
        #         worn_body_armour = ItemUtilities.get_armour_entity_from_body_location(gameworld=gameworld,
        #                                                                               entity=mobile,
        #                                                                               bodylocation='chest')
        #         ItemUtilities.unequip_piece_of_armour(gameworld=gameworld,entity=mobile, bodylocation='chest')
        # if body_location == 'hands':
        #     ap = MobileUtilities.is_entity_wearing_hands_armour(gameworld=gameworld, entity=mobile)
        #     if ap != 0:
        #         worn_body_armour = ItemUtilities.get_armour_entity_from_body_location(gameworld=gameworld, entity=mobile, bodylocation='hands')
        #         ItemUtilities.unequip_piece_of_armour(gameworld=gameworld,entity=mobile, bodylocation='hands')
        #
        # if body_location == 'legs':
        #     ap = MobileUtilities.is_entity_wearing_legs_armour(gameworld=gameworld, entity=mobile)
        #     if ap != 0:
        #         worn_body_armour = ItemUtilities.get_armour_entity_from_body_location(gameworld=gameworld, entity=mobile, bodylocation='legs')
        #         ItemUtilities.unequip_piece_of_armour(gameworld=gameworld,entity=mobile, bodylocation='legs')
        #
        # if body_location == 'feet':
        #     ap = MobileUtilities.is_entity_wearing_feet_armour(gameworld=gameworld, entity=mobile)
        #     if ap != 0:
        #         worn_body_armour = ItemUtilities.get_armour_entity_from_body_location(gameworld=gameworld, entity=mobile, bodylocation='feet')
        #         ItemUtilities.unequip_piece_of_armour(gameworld=gameworld,entity=mobile, bodylocation='feet')
        #
        #
        # # equip new piece of armour
        #
        # # add original armour to the inventory
        # if worn_body_armour != 0:
        #     mobile_inventory_component = gameworld.component_for_entity(mobile, mobiles.Inventory)
        #     mobile_inventory_component.items.append(worn_body_armour)

    @staticmethod
    def wield_weapon_from_inventory(gameworld, mobile, entity):

        # get list of weapons currently equipped as a list of entities
        equipped_weapons = MobileUtilities.get_weapons_equipped(gameworld, mobile)

        # remove unequipped weapon from inventory component
        ItemUtilities.remove_item_from_inventory(gameworld, mobile, entity)

        # determine which hand the weapon can be equipped in
        hand_to_wield = ItemUtilities.get_hand_weapon_can_be_wielded_in(gameworld=gameworld, weapon_entity=entity)

        if hand_to_wield == 'main':
            MobileUtilities.equip_weapon(gameworld=gameworld, entity=mobile, weapon=entity, hand=hand_to_wield)
            # add previously equipped weapon (item) to the inventory
            mobile_inventory_component = gameworld.component_for_entity(mobile, mobiles.Inventory)
            # add item entity to mobiles' inventory
            mobile_inventory_component.items.append(equipped_weapons[0])
            # check for holding a 2-handed weapon
            if equipped_weapons[2] > 0:
                gameworld.component_for_entity(mobile, mobiles.Equipped).both_hands = 0
                mobile_inventory_component.items.append(equipped_weapons[2])

        if hand_to_wield == 'off':
            MobileUtilities.equip_weapon(gameworld=gameworld, entity=mobile, weapon=entity, hand=hand_to_wield)
            # add previously equipped weapon (item) to the inventory
            mobile_inventory_component = gameworld.component_for_entity(mobile, mobiles.Inventory)
            # add item entity to mobiles' inventory
            mobile_inventory_component.items.append(equipped_weapons[1])
            # check for holding a 2-handed weapon
            if equipped_weapons[2] > 0:
                gameworld.component_for_entity(mobile, mobiles.Equipped).both_hands = 0
                mobile_inventory_component.items.append(equipped_weapons[2])

        if hand_to_wield == 'both':
            MobileUtilities.equip_weapon(gameworld=gameworld, entity=mobile, weapon=entity, hand=hand_to_wield)
            # add previously equipped weapon (item) to the inventory
            mobile_inventory_component = gameworld.component_for_entity(mobile, mobiles.Inventory)
            # add both items entities to mobiles' inventory
            # is there a weapon in either the main or off hand - that's not a 2-handed weapon
            if equipped_weapons[0] > 0:
                mobile_inventory_component.items.append(equipped_weapons[0])
                gameworld.component_for_entity(mobile, mobiles.Equipped).main_hand = 0
            if equipped_weapons[1] > 0:
                mobile_inventory_component.items.append(equipped_weapons[1])
                gameworld.component_for_entity(mobile, mobiles.Equipped).off_hand = 0
            elif equipped_weapons[2] > 0:
                mobile_inventory_component.items.append(equipped_weapons[2])

    @staticmethod
    def wear_jewellery_from_inventory(gameworld, mobile, jewellery_entity):
        # get list of currently equipped jewellery
        equipped_jewellery = MobileUtilities.get_jewellery_already_equipped(gameworld, mobile)

        # remove unequipped jewelery from inventory
        ItemUtilities.remove_item_from_inventory(gameworld, mobile, jewellery_entity)

        # equip jewellery in correct location
        body_location = ItemUtilities.get_jewellery_valid_body_location(gameworld=gameworld, entity=jewellery_entity)

        if body_location[0]:
            if equipped_jewellery[0] == 0:
                ItemUtilities.equip_jewellery(gameworld=gameworld, mobile=mobile, bodylocation='left ear',
                                              trinket=jewellery_entity)
            if equipped_jewellery[1] == 0:
                ItemUtilities.equip_jewellery(gameworld=gameworld, mobile=mobile, bodylocation='right ear',
                                              trinket=jewellery_entity)
            if equipped_jewellery[0] != 0 and equipped_jewellery[1] != 0:
                ItemUtilities.equip_jewellery(gameworld=gameworld, mobile=mobile, bodylocation='left ear',
                                              trinket=jewellery_entity)
                ItemUtilities.add_previously_equipped_item_to_inventory(gameworld=gameworld, mobile=mobile,
                                                                        item_to_inventory=equipped_jewellery[0])

        if body_location[1]:
            if equipped_jewellery[2] == 0:
                ItemUtilities.equip_jewellery(gameworld=gameworld, mobile=mobile, bodylocation='left hand',
                                              trinket=jewellery_entity)
            if equipped_jewellery[3] == 0:
                ItemUtilities.equip_jewellery(gameworld=gameworld, mobile=mobile, bodylocation='right hand',
                                              trinket=jewellery_entity)
            if equipped_jewellery[2] != 0 and equipped_jewellery[3] != 0:
                ItemUtilities.equip_jewellery(gameworld=gameworld, mobile=mobile, bodylocation='left hand',
                                              trinket=jewellery_entity)
                ItemUtilities.add_previously_equipped_item_to_inventory(gameworld=gameworld, mobile=mobile,
                                                                        item_to_inventory=equipped_jewellery[2])

        if body_location[2]:
            ItemUtilities.equip_jewellery(gameworld=gameworld, mobile=mobile, bodylocation='neck',
                                          trinket=jewellery_entity)
            if equipped_jewellery[4] != 0:
                ItemUtilities.add_previously_equipped_item_to_inventory(gameworld=gameworld, mobile=mobile,
                                                                        item_to_inventory=equipped_jewellery[4])

    @staticmethod
    def get_jewellery_already_equipped(gameworld, mobile):
        equipped = [gameworld.component_for_entity(mobile, mobiles.Jewellery).left_ear,
                    gameworld.component_for_entity(mobile, mobiles.Jewellery).right_ear,
                    gameworld.component_for_entity(mobile, mobiles.Jewellery).left_hand,
                    gameworld.component_for_entity(mobile, mobiles.Jewellery).right_hand,
                    gameworld.component_for_entity(mobile, mobiles.Jewellery).neck]

        return equipped

    @staticmethod
    def generate_list_of_random_names(gameworld, game_config, entity, gender, race):

        base_file_name = 'NAMESFILE'
        race_file = race.upper() + base_file_name
        race_name_file = configUtilities.get_config_value_as_string(configfile=game_config, section='default',
                                                                    parameter=race_file)
        tcod.namegen_parse(race_name_file)

        nameList = []

        for randomName in range(10):
            if gender == 1:
                sn = tcod.namegen_generate('male')
            else:
                sn = tcod.namegen_generate('female')

            nameList.append(sn.capitalize())
        tcod.namegen_destroy()
        return nameList

    @staticmethod
    def choose_random_name(gameworld, game_config, entity, gender, race):
        base_file_name = 'NAMESFILE'
        race_file = race.upper() + base_file_name
        race_name_file = configUtilities.get_config_value_as_string(configfile=game_config, section='default',
                                                                    parameter=race_file)
        tcod.namegen_parse(race_name_file)

        if gender == 1:
            sn = tcod.namegen_generate('male')
        else:
            sn = tcod.namegen_generate('female')

        selected_name = sn.capitalize()
        tcod.namegen_destroy()

        return selected_name

    @staticmethod
    def stop_double_casting_same_spell(gameworld, entity):
        gameworld.remove_component(entity, mobiles.SpellCast)

    #
    # Get primary attributes
    #
    @staticmethod
    def get_mobile_power(gameworld, entity):
        primary_components = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes)
        return primary_components.power

    @staticmethod
    def set_mobile_power(gameworld, entity, value):
        gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).power = value

    @staticmethod
    def get_mobile_precision(gameworld, entity):
        primary_components = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes)
        return primary_components.precision

    @staticmethod
    def set_mobile_precision(gameworld, entity, value):
        gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).precision = value

    @staticmethod
    def get_mobile_toughness(gameworld, entity):
        primary_components = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes)
        return primary_components.toughness

    @staticmethod
    def set_mobile_toughness(gameworld, entity, value):
        gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).toughness = value

    @staticmethod
    def get_mobile_vitality(gameworld, entity):
        primary_components = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes)
        return primary_components.vitality

    @staticmethod
    def set_mobile_vitality(gameworld, entity, value):
        gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).vitality = value

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
    def set_mobile_condition_damage(gameworld, entity, value):
        gameworld.component_for_entity(entity, mobiles.SecondaryAttributes).conditionDamage = value

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
    def set_mobile_healing_power(gameworld, entity, value):
        gameworld.component_for_entity(entity, mobiles.SecondaryAttributes).healingPower = value

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
        MobileUtilities.calculate_special_bar_current_value(gameworld, entity)

    @staticmethod
    def calculate_special_bar_current_value(gameworld, entity):
        pass

    @staticmethod
    def calculate_armour_attribute(gameworld, entity):
        """
        Need to calculate the 'defense' value first
        Then get the toughness attribute value
        :param gameworld: object: the game world
        :param entity: integer: represents the entity in the gameworld
        :return: None
        """
        # entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=gameconfig)
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
            def_chest_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, entity=chest)
        else:
            def_chest_value = 0

        if head != 0:
            def_head_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, entity=head)
        else:
            def_head_value = 0

        if legs != 0:
            def_legs_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, entity=legs)
        else:
            def_legs_value = 0

        if feet != 0:
            def_feet_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, entity=feet)
        else:
            def_feet_value = 0

        if hands != 0:
            def_hands_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, entity=hands)
        else:
            def_hands_value = 0

        defense_value = def_chest_value + def_head_value + def_legs_value + def_feet_value + def_hands_value

        return defense_value

    @staticmethod
    def calculate_boon_duration(gameworld, entity):

        # entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=gameconfig)
        entity_secondary_component = gameworld.component_for_entity(entity, mobiles.SecondaryAttributes)

        concentration_value = entity_secondary_component.concentration

        boon_duration_value = min(100, int(concentration_value / 15))

        gameworld.component_for_entity(entity, mobiles.DerivedAttributes).boonDuration = boon_duration_value

    @staticmethod
    def calculate_critical_hit_chance(gameworld, entity):

        # entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=gameconfig)
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

        # entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=gameconfig)
        base_value = 150
        entity_secondary_component = gameworld.component_for_entity(entity, mobiles.SecondaryAttributes)

        ferocity_value = entity_secondary_component.ferocity

        critical_damage_bonus = int(ferocity_value / 15)

        critical_damage_value = base_value + critical_damage_bonus

        gameworld.component_for_entity(entity, mobiles.DerivedAttributes).criticalDamage = critical_damage_value

    @staticmethod
    def calculate_condition_duration(gameworld, entity):

        # entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=gameconfig)
        entity_secondary_component = gameworld.component_for_entity(entity, mobiles.SecondaryAttributes)
        expertise_value = entity_secondary_component.expertise

        cond_duration = int(expertise_value / 15)

        cond_duration_bonus = min(100, cond_duration)
        gameworld.component_for_entity(entity, mobiles.DerivedAttributes).conditionDuration = cond_duration_bonus

    @staticmethod
    def calculate_max_health(gameworld, entity):

        # get primary attributes component
        primary_attribute_component = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes)
        vitality_value = primary_attribute_component.vitality

        # get character class attributes component
        entity_class_component = gameworld.component_for_entity(entity, mobiles.CharacterClass)
        class_base_health = entity_class_component.baseHealth

        vitality_calculated_health = vitality_value * 10

        health_value = vitality_calculated_health + class_base_health
        gameworld.component_for_entity(entity, mobiles.DerivedAttributes).maximumHealth = health_value

    @staticmethod
    def calculate_current_health(gameworld, entity):

        current_health = 0
        maximum_health = gameworld.component_for_entity(entity, mobiles.DerivedAttributes).maximumHealth
        # check boons --> increase health
        # check conditions --> reduce health
        # check controls --> can affect it either way
        # check traits
        # check jewellery
        # check armour
        # check weapons

        gameworld.component_for_entity(entity, mobiles.DerivedAttributes).currentHealth = maximum_health

    @staticmethod
    def calculate_current_mana(gameworld, gameconfig):

        entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=gameconfig)

        current_mana = MobileUtilities.get_derived_current_mana(gameworld=gameworld, entity=entity)
        # check boons
        # check conditions
        # check controls
        # check traits
        # check equipped items (armour, jewellery)
        # check weapons
        return current_mana

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

    @staticmethod
    def get_derived_special_bar_current_value(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.SpecialBar).currentvalue

    @staticmethod
    def get_derived_special_bar_max_value(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.SpecialBar).maximumvalue

    @staticmethod
    def get_combat_status(gameworld, entity):
        status_effects_component = gameworld.component_for_entity(entity, mobiles.StatusEffects)
        return status_effects_component.inCombat

    #
    # Set derived attributes
    #
    @staticmethod
    def set_current_health_during_combat(gameworld, entity, damageToApply):
        target_current_health = MobileUtilities.get_derived_current_health(gameworld=gameworld, entity=entity)
        target_new_health = target_current_health - damageToApply
        gameworld.component_for_entity(entity, mobiles.DerivedAttributes).currentHealth = target_new_health

    @staticmethod
    def set_combat_status_to_true(gameworld, entity):
        status_effects_component = gameworld.component_for_entity(entity, mobiles.StatusEffects)
        status_effects_component.inCombat = True

    @staticmethod
    def set_combat_status_to_false(gameworld, entity):
        status_effects_component = gameworld.component_for_entity(entity, mobiles.StatusEffects)
        status_effects_component.inCombat = False

    @staticmethod
    def get_current_condis_applied_to_mobile(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.StatusEffects).conditions

    @staticmethod
    def get_current_boons_applied_to_mobile(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.StatusEffects).boons

    @staticmethod
    def get_current_controls_applied_to_mobile(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.StatusEffects).controls

