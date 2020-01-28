import random

from loguru import logger

from components import items, mobiles
from utilities import formulas, world
from utilities.spellHelp import SpellUtilities


def display_inspect_panel(gameworld, display_mode, item_entity, game_config):
    """

    :param gameworld:
    :param display_mode: inspect = full info, look = generic info, partial=limited
    :param item_entity:
    :return:
    """

    disp_inspect_panel = True
    spell_display_index = 0
    spell_display_index_max = 3

    spell_display_mode = ['cast time  ','cool down  ','max targets','max range  ']

    item_type = ItemUtilities.get_item_type(gameworld=gameworld, entity=item_entity)

    insp_panel_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='inspect', parameter='INSP_PANEL_MAX_WIDTH')
    insp_panel_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='inspect', parameter='INSP_PANEL_MAX_HEIGHT')
    insp_panel_start_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='inspect', parameter='INSP_PANEL_LEFT_X')
    insp_panel_start_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='inspect', parameter='INSP_PANEL_LEFT_Y')
    other_game_state = configUtilities.get_config_value_as_integer(configfile=game_config, section='game', parameter='DISPLAY_GAME_MAP')
    portrait_start_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='inspect', parameter='INSP_PANEL_ITEM_PORTRAIT_X')
    portrait_start_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='inspect', parameter='INSP_PANEL_ITEM_PORTRAIT_Y')
    portrait_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='inspect', parameter='INSP_PANEL_ITEM_PORTRAIT_WIDTH')
    portrait_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='inspect', parameter='INSP_PANEL_ITEM_PORTRAIT_HEIGHT')

    # create console & draw pretty frame
    inspect_panel = tcod.console_new(insp_panel_width, insp_panel_height)
    panel_msg = 'ESC to quit'

    if display_mode == 'inspect':
        panel_msg += ', arrows to change info'

    while disp_inspect_panel:

        draw_colourful_frame(console=inspect_panel, game_config=game_config, startx=0, starty=0,
                             width=insp_panel_width, height=insp_panel_height,
                             title='Inspect', title_loc='right', corner_decorator='',
                             corner_studs='round', msg=panel_msg)

        # draw item portrait
        inspect_panel.draw_frame(x=portrait_start_x, y=portrait_start_y, width=portrait_width, height=portrait_height, title='Item', clear=True, fg=colourUtilities.GREENYELLOW, bg=colourUtilities.BLACK)
        # display general item properties
        item_display_name = ItemUtilities.get_item_displayname(gameworld=gameworld, entity=item_entity)
        item_description = ItemUtilities.get_item_description(gameworld=gameworld, entity=item_entity)
        item_texture = ItemUtilities.get_item_texture(gameworld=gameworld, entity=item_entity)

        item_general_info_x = portrait_start_x + portrait_width + 2

        inspect_panel.print(x=item_general_info_x, y=portrait_start_y, string=item_display_name)
        inspect_panel.print(x=item_general_info_x, y=portrait_start_y + 1, string=item_description)
        inspect_panel.print(x=item_general_info_x, y=portrait_start_y + 2, string=item_texture)

        # display specific item properties - defense values, bonuses,
        if item_type == 'armour':
            am_set_name = ItemUtilities.get_armour_set_name(gameworld=gameworld, entity=item_entity)
            am_quality_level = ItemUtilities.get_item_quality(gameworld=gameworld, entity=item_entity)
            am_weight = ItemUtilities.get_armour_piece_weight(gameworld=gameworld, entity=item_entity)
            am_defense_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, body_location=item_entity)
            am_major_attributes = ItemUtilities.get_armour_major_attributes(gameworld=gameworld, entity=item_entity)
            am_minor_attributes = ItemUtilities.get_armour_minor_attributes(gameworld=gameworld, entity=item_entity)

            major_attr = am_major_attributes[0] + ' +' + str(am_major_attributes[1])
            minor_attr = am_minor_attributes[0] + ' +' + str(am_minor_attributes[1])

            inspect_panel.print(x=item_general_info_x, y=portrait_start_y + 4, string=am_set_name)
            inspect_panel.print(x=item_general_info_x, y=portrait_start_y + 5, string=am_quality_level)
            inspect_panel.print(x=item_general_info_x, y=portrait_start_y + 6, string=am_weight)
            inspect_panel.print(x=item_general_info_x, y=portrait_start_y + 7, string=str(am_defense_value))
            inspect_panel.print(x=item_general_info_x, y=portrait_start_y + 8, string=major_attr)
            inspect_panel.print(x=item_general_info_x, y=portrait_start_y + 9, string=minor_attr)

        if item_type == 'jewellery':
            jw_stat_bonus = ItemUtilities.get_jewellery_stat_bonus(gameworld=gameworld, entity=item_entity)

            jewel_stat_bonus = jw_stat_bonus[0] + ' +' + str(jw_stat_bonus[1])
            inspect_panel.print(x=item_general_info_x, y=portrait_start_y + 4, string=jewel_stat_bonus)
        if item_type == 'weapon':
            spell_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='inspect', parameter='INSP_PANEL_SPELL_Y')
            spell_name_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='inspect', parameter='INSP_PANEL_SPELL_NAME')
            spell_info_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='inspect', parameter='INSP_PANEL_SPELL_INFO')

            wp_hallmarks = ItemUtilities.get_weapon_hallmarks(gameworld=gameworld, entity=item_entity)
            hallmarks = 'no hallmarks'
            wp_experience = ItemUtilities.get_weapon_experience_values(gameworld=gameworld, entity=item_entity)

            wp_cur_exp_level = wp_experience[0]
            wp_max_exp_level = wp_experience[1]

            wp_exp = str(wp_cur_exp_level) + '/' + str(wp_max_exp_level)
            inspect_panel.print(x=item_general_info_x, y=portrait_start_y + 4, string=wp_exp)
            inspect_panel.print(x=item_general_info_x, y=portrait_start_y + 5, string=hallmarks)

            inspect_panel.print(x=portrait_start_x, y=spell_y, string='Spell Slots', fg=colourUtilities.BLUE, bg=colourUtilities.BLACK)
            inspect_panel.print(x=spell_info_x, y=spell_y, string=spell_display_mode[spell_display_index], fg=colourUtilities.YELLOW1, bg=colourUtilities.BLACK)

            spell_slot_one = ItemUtilities.get_weapon_spell_slot_one_entity(gameworld=gameworld, entity=item_entity)
            spell_y += 1
            if spell_slot_one > 0:
                slot_one_spell_name = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=gameworld, weapon_equipped=item_entity, slotid=1)
                spell_information = str(get_spell_additional_information(gameworld=gameworld, spell_entity=spell_slot_one, display_mode=spell_display_index))

                inspect_panel.print(x=spell_name_x, y=spell_y, string='1. ' + slot_one_spell_name)
                inspect_panel.print(x=spell_info_x, y=spell_y, string=spell_information)
            else:
                inspect_panel.print(x=spell_name_x, y=spell_y, string='1. No spell')

            spell_slot_two = ItemUtilities.get_weapon_spell_slot_two_entity(gameworld=gameworld, entity=item_entity)
            spell_y += 1
            if spell_slot_two > 0:
                slot_two_spell_name = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=gameworld, weapon_equipped=item_entity, slotid=2)
                spell_information = str(get_spell_additional_information(gameworld=gameworld, spell_entity=spell_slot_two, display_mode=spell_display_index))

                inspect_panel.print(x=spell_name_x, y=spell_y, string='2. ' + slot_two_spell_name)
                inspect_panel.print(x=spell_info_x, y=spell_y, string=spell_information)
            else:
                inspect_panel.print(x=portrait_start_x, y=spell_y, string='2. No spell')

            spell_slot_three = ItemUtilities.get_weapon_spell_slot_three_entity(gameworld=gameworld, entity=item_entity)
            spell_y += 1
            if spell_slot_three > 0:
                slot_three_spell_name = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=gameworld, weapon_equipped=item_entity, slotid=3)
                spell_information = str(get_spell_additional_information(gameworld=gameworld, spell_entity=spell_slot_three, display_mode=spell_display_index))

                inspect_panel.print(x=spell_name_x, y=spell_y, string='3. ' + slot_three_spell_name)
                inspect_panel.print(x=spell_info_x, y=spell_y, string=spell_information)
            else:
                inspect_panel.print(x=spell_name_x, y=spell_y, string='3. No spell')

            spell_slot_four = ItemUtilities.get_weapon_spell_slot_four_entity(gameworld=gameworld, entity=item_entity)
            spell_y += 1
            if spell_slot_four > 0:
                slot_four_spell_name = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=gameworld, weapon_equipped=item_entity, slotid=4)
                spell_information = str(get_spell_additional_information(gameworld=gameworld, spell_entity=spell_slot_four, display_mode=spell_display_index))

                inspect_panel.print(x=spell_name_x, y=spell_y, string='4. ' + slot_four_spell_name)
                inspect_panel.print(x=spell_info_x, y=spell_y, string=spell_information)
            else:
                inspect_panel.print(x=spell_name_x, y=spell_y, string='4. No spell')

            spell_slot_five = ItemUtilities.get_weapon_spell_slot_five_entity(gameworld=gameworld, entity=item_entity)
            spell_y += 1
            if spell_slot_five > 0:
                slot_five_spell_name = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=gameworld, weapon_equipped=item_entity, slotid=5)
                spell_information = str(get_spell_additional_information(gameworld=gameworld, spell_entity=spell_slot_five, display_mode=spell_display_index))

                inspect_panel.print(x=spell_name_x, y=spell_y, string='5. ' + slot_five_spell_name)
                inspect_panel.print(x=spell_info_x, y=spell_y, string=spell_information)
            else:
                inspect_panel.print(x=spell_name_x, y=spell_y, string='5. No spell')

        # display dynamic item properties

        tcod.console_blit(inspect_panel, 0, 0, insp_panel_width, insp_panel_height, 0, insp_panel_start_x, insp_panel_start_y)

        tcod.console_flush()

        event_to_be_processed, event_action = handle_game_keys()
        if event_action != '':
            if event_action == 'quit':
                disp_inspect_panel = False
                configUtilities.write_config_value(configfile=game_config, section='game',
                                                   parameter='DISPLAY_GAME_STATE', value=str(other_game_state))
            if event_action == 'left':
                spell_display_index -= 1
            if event_action == 'right':
                spell_display_index += 1

            if spell_display_index > spell_display_index_max:
                spell_display_index = 0
            if spell_display_index < 0:
                spell_display_index = spell_display_index_max

    tcod.console_blit(inspect_panel, 0, 0, insp_panel_width, insp_panel_height, 0, insp_panel_start_x, 10)

    tcod.console_flush()


class ItemUtilities:
    ####################################################
    #
    #   Methods applicable to all types of items
    #
    ####################################################
    @staticmethod
    def get_item_type(gameworld, entity):
        item_type_component = gameworld.component_for_entity(entity, items.TypeOfItem)
        return item_type_component.label

    @staticmethod
    def get_item_actions(gameworld, entity):
        item_actions_component = gameworld.component_for_entity(entity, items.Actionlist)
        return item_actions_component.actions

    @staticmethod
    def get_item_name(gameworld, entity):
        item_described_component = gameworld.component_for_entity(entity, items.Describable)
        return item_described_component.name

    @staticmethod
    def get_item_material(gameworld, entity):
        item_material_component = gameworld.component_for_entity(entity, items.Material)
        return item_material_component.texture

    @staticmethod
    def get_item_displayname(gameworld, entity):
        item_described_component = gameworld.component_for_entity(entity, items.Describable)
        return item_described_component.displayname

    @staticmethod
    def get_item_description(gameworld, entity):
        item_described_component = gameworld.component_for_entity(entity, items.Describable)
        return item_described_component.description

    @staticmethod
    def get_item_glyph(gameworld, entity):
        item_described_component = gameworld.component_for_entity(entity, items.Describable)
        return item_described_component.glyph

    @staticmethod
    def get_item_colours(gameworld, entity):
        describeable_component = gameworld.component_for_entity(entity,items.Describable)
        colours = [describeable_component.fg, describeable_component.bg]
        return colours

    @staticmethod
    def get_item_fg_colour(gameworld, entity):
        item_described_component = gameworld.component_for_entity(entity, items.Describable)
        return item_described_component.fg

    @staticmethod
    def get_item_bg_colour(gameworld, entity):
        item_described_component = gameworld.component_for_entity(entity, items.Describable)
        return item_described_component.bg

    @staticmethod
    def get_item_location(gameworld, entity):
        item_location_component = gameworld.component_for_entity(entity, items.Location)
        return item_location_component.x, item_location_component.y

    @staticmethod
    def add_dungeon_position_component(gameworld, entity):
        gameworld.add_component(entity, items.Location(x=0, y=0))


    @staticmethod
    def set_item_location(gameworld, item_entity, posx, posy):
        item_location_component = gameworld.component_for_entity(item_entity, items.Location)
        item_location_component.x = posx
        item_location_component.y = posy

    @staticmethod
    def get_item_texture(gameworld, entity):
        item_material_component = gameworld.component_for_entity(entity, items.Material)
        return item_material_component.texture

    @staticmethod
    def get_item_components(gameworld, entity):
        item_components_component = gameworld.component_for_entity(entity, items.Material)
        return item_components_component.component1, item_components_component.component2, item_components_component.component3

    @staticmethod
    def get_item_can_be_rendered(gameworld, entity):
        item_render_component = gameworld.component_for_entity(entity, items.RenderItem)
        return item_render_component.isTrue

    @staticmethod
    def get_item_quality(gameworld, entity):
        item_quality_component = gameworld.component_for_entity(entity, items.Quality)
        return item_quality_component.level

    @staticmethod
    def delete_item(gameworld, entity):
        world.delete_entity(gameworld=gameworld, entity=entity)

    @staticmethod
    def remove_item_from_inventory(gameworld, mobile, entity):
        mobile_inventory_component = gameworld.component_for_entity(mobile, mobiles.Inventory)
        mobile_inventory_component.items.remove(entity)

    @staticmethod
    def add_previously_equipped_item_to_inventory(gameworld, mobile, item_to_inventory):
        mobile_inventory_component = gameworld.component_for_entity(mobile, mobiles.Inventory)
        mobile_inventory_component.items.append(item_to_inventory)

####################################################
#
#   BAGS
#
####################################################
    @staticmethod
    def get_bag_size(gameworld, entity):
        bag_size_component = gameworld.component_for_entity(entity, items.SlotSize)
        return bag_size_component.maxsize

    @staticmethod
    def get_bag_is_populated(gameworld, entity):
        bag_populated_component = gameworld.component_for_entity(entity, items.SlotSize)
        return bag_populated_component.populated

####################################################
#
#   WEAPONS
#
####################################################

    @staticmethod
    def get_is_weapon_wielded(gameworld, weapon_entity):
        wielded_component = gameworld.component_for_entity(weapon_entity, items.Wielded)
        return wielded_component.true_or_false

    @staticmethod
    def get_hand_weapon_can_be_wielded_in(gameworld, weapon_entity):
        wielded_component = gameworld.component_for_entity(weapon_entity, items.Wielded)
        return wielded_component.hands

    @staticmethod
    def get_weapon_type(gameworld, weapon_entity):
        weapon_type_component = gameworld.component_for_entity(weapon_entity, items.WeaponType)
        return weapon_type_component.label

    @staticmethod
    def get_weapon_held_in_hand(gameworld, entity):
        wielded_component = gameworld.component_for_entity(entity, items.Wielded)
        if wielded_component.both_hands != 0:
            return 'both hands'
        if wielded_component.main_hand != 0:
            return 'main hand'
        if wielded_component.off_hand != 0:
            return 'off hand'
        return 'unknown'

    @staticmethod
    def get_weapon_experience_values(gameworld, entity):
        experience_component = gameworld.component_for_entity(entity, items.Experience)
        levels = [experience_component.current_level, experience_component.max_level]
        return levels

    @staticmethod
    def get_weapon_hallmarks(gameworld, entity):
        hallmarks_component = gameworld.component_for_entity(entity,items.Hallmarks)
        hallmarks = [hallmarks_component.hallmark_slot_one, hallmarks_component.hallmark_slot_two]
        return hallmarks

    @staticmethod
    def get_weapon_spell_slot_one_entity(gameworld, entity):
        slot_component = gameworld.component_for_entity(entity,items.Spells)
        slot = slot_component.slot_one
        return int(slot)

    @staticmethod
    def get_weapon_spell_slot_two_entity(gameworld, entity):
        slot_component = gameworld.component_for_entity(entity,items.Spells)
        slot = slot_component.slot_two
        return int(slot)

    @staticmethod
    def get_weapon_spell_slot_three_entity(gameworld, entity):
        slot_component = gameworld.component_for_entity(entity, items.Spells)
        slot = slot_component.slot_three
        return int(slot)

    @staticmethod
    def get_weapon_spell_slot_four_entity(gameworld, entity):
        slot_component = gameworld.component_for_entity(entity,items.Spells)
        slot = slot_component.slot_four
        return int(slot)

    @staticmethod
    def get_weapon_spell_slot_five_entity(gameworld, entity):
        slot_component = gameworld.component_for_entity(entity,items.Spells)
        slot = slot_component.slot_five
        return int(slot)

    @staticmethod
    def get_weapon_damage_ranges(gameworld, weapon):
        return gameworld.component_for_entity(weapon, items.DamageRange).ranges

    @staticmethod
    def get_weapon_outgoing_damage(gameworld, weapon, power, slot):
        weapon_level = ItemUtilities.get_weapon_experience_values(gameworld=gameworld, entity=weapon)
        current_weapon_level = weapon_level[0]

        weapon_strength = ItemUtilities.get_weapon_strength(gameworld=gameworld, weapon=weapon, weapon_level=current_weapon_level)

        spell_entity = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld=gameworld, weapon_equipped=weapon, slotid=slot)

        spell_coeff = float(SpellUtilities.get_spell_DamageCoeff(gameworld=gameworld, spell_entity=spell_entity))

        outgoing_base_damage = formulas.outgoing_base_damage(weapon_strength=weapon_strength, power=power, spell_coefficient=spell_coeff)

        # outgoing_base_damage = weapon_strength * power * spell_coeff

        # logger.debug('weapon strength {}', weapon_strength)
        # logger.debug('spell entity {}', spell_entity)
        # logger.debug('spell coeff {}', spell_coeff)
        # logger.debug('base damage {}', int(outgoing_base_damage))

        return outgoing_base_damage

    @staticmethod
    def get_weapon_strength(gameworld, weapon, weapon_level):
        wpn_dmg_min = 0
        wpn_dmg_max = 0
        range_chosen = False
        weapon_damage_range = ItemUtilities.get_weapon_damage_ranges(gameworld=gameworld, weapon=weapon)
        weapon_type = ItemUtilities.get_weapon_type(gameworld=gameworld, weapon_entity=weapon)

        for lvl in weapon_damage_range:
            wid = lvl['id']
            if int(wid) > (weapon_level - 1) and range_chosen is False:
                range_chosen = True
                wpn_dmg_min = int(lvl['min'])
                wpn_dmg_max = int(lvl['max'])
                logger.info('Weapon damage range found: min {} max {}', str(wpn_dmg_min), str(wpn_dmg_max))

        if wpn_dmg_min == 0 or wpn_dmg_max == 0:
            # raise logger warning
            # return 0 damage
            return 0
        else:
            return random.randrange(wpn_dmg_min, wpn_dmg_max)






####################################################
#
#   ARMOUR
#
####################################################
    @staticmethod
    def get_armour_defense_value(gameworld, entity):
        return gameworld.component_for_entity(entity, items.Defense).value

    @staticmethod
    def get_armour_set_name(gameworld, entity):
        return gameworld.component_for_entity(entity, items.ArmourSet).name

    @staticmethod
    def get_armour_piece_weight(gameworld, entity):
        return gameworld.component_for_entity(entity, items.Weight).label

    @staticmethod
    def get_armour_major_attributes(gameworld, entity):
        armour_attributes_component = gameworld.component_for_entity(entity, items.AttributeBonus)
        major = [armour_attributes_component.majorName, armour_attributes_component.majorBonus]

        return major

    @staticmethod
    def get_armour_minor_attributes(gameworld, entity):
        armour_attributes_component = gameworld.component_for_entity(entity, items.AttributeBonus)
        minor = [armour_attributes_component.minorOneName, armour_attributes_component.minorOneBonus]
        return minor

    @staticmethod
    def get_armour_being_worn_status(gameworld, piece_of_armour):
        armour_worn_component = gameworld.component_for_entity(piece_of_armour, items.ArmourBeingWorn)
        return armour_worn_component.status

    @staticmethod
    def set_armour_being_worn_status_to_true(gameworld, entity):
        gameworld.component_for_entity(entity, items.ArmourBeingWorn).status = True

    @staticmethod
    def set_armour_being_worn_status_to_false(gameworld, entity):
        gameworld.component_for_entity(entity, items.ArmourBeingWorn).status = False

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
    def get_armour_body_location(gameworld, armour_piece):
        body_location = ''
        if gameworld.component_for_entity(armour_piece, items.ArmourBodyLocation).head > 0:
            return 'head'
        if gameworld.component_for_entity(armour_piece, items.ArmourBodyLocation).chest > 0:
            return 'chest'
        if gameworld.component_for_entity(armour_piece, items.ArmourBodyLocation).hands > 0:
            return 'hands'
        if gameworld.component_for_entity(armour_piece, items.ArmourBodyLocation).legs > 0:
            return 'legs'
        if gameworld.component_for_entity(armour_piece, items.ArmourBodyLocation).feet > 0:
            return 'feet'

        return body_location


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
    def unequip_piece_of_armour(gameworld, entity, bodylocation):
        # armour_is_already_worn = ItemUtilities.get_armour_being_worn_status(gameworld, entity)
        # if armour_is_already_worn:
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

    @staticmethod
    def equip_full_set_of_armour(gameworld, entity, armourset):

        if armourset[0] > 0:
            ItemUtilities.equip_piece_of_armour(gameworld, entity, armourset[0], 'head')
        if armourset[1] > 0:
            ItemUtilities.equip_piece_of_armour(gameworld, entity, armourset[1], 'chest')
        if armourset[2] > 0:
            ItemUtilities.equip_piece_of_armour(gameworld, entity, armourset[2], 'hands')
        if armourset[3] > 0:
            ItemUtilities.equip_piece_of_armour(gameworld, entity, armourset[3], 'legs')
        if armourset[4] > 0:
            ItemUtilities.equip_piece_of_armour(gameworld, entity, armourset[4], 'feet')

####################################################
#
#   JEWELLERY
#
####################################################

    @staticmethod
    def get_jewellery_stat_bonus(gameworld, entity):
        jewellery_statbonus_component = gameworld.component_for_entity(entity, items.JewelleryStatBonus)
        statbonus = [jewellery_statbonus_component.statName, jewellery_statbonus_component.statBonus]
        return statbonus

    @staticmethod
    def get_jewellery_valid_body_location(gameworld, entity):
        jewellery_body_location_component = gameworld.component_for_entity(entity, items.JewelleryBodyLocation)
        loc =[jewellery_body_location_component.ears, jewellery_body_location_component.fingers, jewellery_body_location_component.neck]
        return loc

    @staticmethod
    def get_jewellery_already_equipped_status(gameworld, entity):
        jewellery_equipped_component = gameworld.component_for_entity(entity, items.JewelleryEquipped)
        return jewellery_equipped_component.istrue

    @staticmethod
    def set_jewellery_equipped_status_to_true(gameworld, entity):
        gameworld.component_for_entity(entity, items.JewelleryEquipped).istrue = True

    @staticmethod
    def set_jewellery_equipped_status_to_false(gameworld, entity):
        gameworld.component_for_entity(entity, items.JewelleryEquipped).istrue = False

    @staticmethod
    def equip_jewellery(gameworld, mobile, bodylocation, trinket):
        is_jewellery_equipped = ItemUtilities.get_jewellery_already_equipped_status(gameworld, entity=trinket)
        if not is_jewellery_equipped:
            if bodylocation == 'left ear':
                gameworld.component_for_entity(mobile, mobiles.Jewellery).left_ear = trinket
            if bodylocation == 'right ear':
                gameworld.component_for_entity(mobile, mobiles.Jewellery).right_ear = trinket
            if bodylocation == 'left hand':
                gameworld.component_for_entity(mobile, mobiles.Jewellery).left_hand = trinket
            if bodylocation == 'right hand':
                gameworld.component_for_entity(mobile, mobiles.Jewellery).right_hand = trinket
            if bodylocation == 'neck':
                gameworld.component_for_entity(mobile, mobiles.Jewellery).neck = trinket

            ItemUtilities.set_jewellery_equipped_status_to_true(gameworld, entity=trinket)

    @staticmethod
    def unequp_piece_of_jewellery(gameworld, entity, bodylocation):

        if bodylocation == 'left ear':
            gameworld.component_for_entity(entity, mobiles.Jewellery).left_ear = 0
        if bodylocation == 'right ear':
            gameworld.component_for_entity(entity, mobiles.Jewellery).right_ear = 0
        if bodylocation == 'left hand':
            gameworld.component_for_entity(entity, mobiles.Jewellery).left_hand = 0
        if bodylocation == 'right hand':
            gameworld.component_for_entity(entity, mobiles.Jewellery).right_hand = 0
        if bodylocation == 'neck':
            gameworld.component_for_entity(entity, mobiles.Jewellery).neck = 0

        ItemUtilities.set_jewellery_equipped_status_to_false(gameworld, entity=entity)

    @staticmethod
    def add_jewellery_benefit(gameworld, entity, statbonus):

        stat = statbonus[0]
        benefit = statbonus[1]

        if stat.lower() == 'condition damage':
            currentStatBonus = gameworld.component_for_entity(entity, mobiles.SecondaryAttributes).conditionDamage
            newStatBonus = currentStatBonus + benefit
            gameworld.component_for_entity(entity, mobiles.SecondaryAttributes).conditionDamage=newStatBonus

        if stat.lower() == 'power':
            currentStatBonus = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).power
            newStatBonus = currentStatBonus + benefit
            gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).power=newStatBonus

        if stat.lower() == 'vitality':
            currentStatBonus = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).vitality
            newStatBonus = currentStatBonus + benefit
            gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).vitality=newStatBonus

        if stat.lower() == 'toughness':
            currentStatBonus = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).toughness
            newStatBonus = currentStatBonus + benefit
            gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).toughness=newStatBonus

        if stat.lower() == 'healing power':
            currentStatBonus = gameworld.component_for_entity(entity, mobiles.SecondaryAttributes).healingPower
            newStatBonus = currentStatBonus + benefit
            gameworld.component_for_entity(entity, mobiles.SecondaryAttributes).healingPower=newStatBonus

        if stat.lower() == 'precision':
            currentStatBonus = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).precision
            newStatBonus = currentStatBonus + benefit
            gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).precision=newStatBonus
