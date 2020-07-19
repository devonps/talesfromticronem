from bearlibterminal import terminal
from loguru import logger

from utilities import configUtilities
from utilities.common import CommonUtils
from utilities.externalfileutilities import Externalfiles
from utilities.input_handlers import handle_game_keys
from utilities.itemsHelp import ItemUtilities
from utilities.spellHelp import SpellUtilities


def process(menu_selection, gameworld, player_entity):
    logger.info('Items and spells info panel accessed')
    game_config = configUtilities.load_config()
    armour_map = {"A": "head", "B": "chest", "C": "hands", "D": "legs", "E": "feet"}
    jewellery_map = {"F": "lear", "G": "rear", "H": "lhand", "I": "rhand", "J": "neck"}

    portraits_folder = configUtilities.get_config_value_as_string(configfile=game_config,
                                                                        section='files', parameter='PORTRAITSFOLDER')

    hardcoded_item_portrait_file = 'short-sleeve-shirt.txt'
    hardoced_armour_portrait_file = 'cap.txt'

    armour_selection_keys = configUtilities.get_config_value_as_list(configfile=game_config, section='spellInfoPopup',
                                                                   parameter='ARMOUR_KEYS')

    jewellery_selection_keys = configUtilities.get_config_value_as_list(configfile=game_config, section='spellInfoPopup',
                                                                   parameter='JEWELLERY_KEYS')

    spell_selection_keys = configUtilities.get_config_value_as_list(configfile=game_config, section='spellInfoPopup',
                                                                    parameter='SPELL_KEYS')

    spell_item_info_start_x = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                          section='spellInfoPopup',
                                                                          parameter='SP_START_X')

    spell_item_info_start_y = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                          section='spellInfoPopup',
                                                                          parameter='SP_START_Y')
    spell_item_info_item_horz = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                            section='spellInfoPopup',
                                                                            parameter='SP_PORTRAIT_BAR')
    spell_item_info_width = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                        section='spellInfoPopup',
                                                                        parameter='SP_WIDTH')
    spell_item_info_depth = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                        section='spellInfoPopup',
                                                                        parameter='SP_DEPTH')

    spell_item_info_item_imp_text_x = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                                  section='spellInfoPopup',
                                                                                  parameter='SP_IMPORTANT_TEXT_X')

    spell_item_info_item_imp_text = spell_item_info_item_horz + 2

    ascii_prefix = 'ASCII_SINGLE_'
    spell_item_info_left_t_junction = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                       parameter=ascii_prefix + 'LEFT_T_JUNCTION')

    spell_item_info_right_t_junction = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                        parameter=ascii_prefix + 'RIGHT_T_JUNCTION')
    spell_item_info_bottom_right_t_junction = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                               parameter=ascii_prefix + 'BOTTOM_T_JUNCTION')

    spell_item_info_top_left_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                       parameter=ascii_prefix + 'TOP_LEFT')

    spell_item_info_cross_junction = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                      parameter=ascii_prefix + 'CROSS_JUNCTION')

    spell_item_info_bottom_left_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                          parameter=ascii_prefix + 'BOTTOM_LEFT')

    spell_item_info_horizontal = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                  parameter=ascii_prefix + 'HORIZONTAL')
    spell_item_info_vertical = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                parameter=ascii_prefix + 'VERTICAL')

    # unicode strings of colours
    unicode_frame_colour = '[font=dungeon][color=SPELLINFO_FRAME_COLOUR]['

    # clear the area under the panel
    terminal.clear_area(spell_item_info_start_x, spell_item_info_start_y, spell_item_info_width,
                        spell_item_info_depth)

    # draw outer frame

    # draw top/bottom horizontals
    for z in range(spell_item_info_start_x, (spell_item_info_start_x + spell_item_info_width)):
        terminal.printf(x=z, y=spell_item_info_start_y,
                        s=unicode_frame_colour + spell_item_info_horizontal + ']')

        terminal.printf(x=z, y=(spell_item_info_start_y + spell_item_info_depth) - 1,
                        s=unicode_frame_colour + spell_item_info_horizontal + ']')

    # draw left vertical
    for zz in range(spell_item_info_depth - 1):
        terminal.printf(x=spell_item_info_start_x, y=spell_item_info_start_y + zz,
                        s=unicode_frame_colour + spell_item_info_vertical + ']')

        # draw corners
        terminal.printf(x=spell_item_info_start_x, y=spell_item_info_start_y,
                        s=unicode_frame_colour + spell_item_info_top_left_corner + ']')

        terminal.printf(x=spell_item_info_start_x, y=(spell_item_info_start_y + spell_item_info_depth) - 1,
                        s=unicode_frame_colour + spell_item_info_bottom_left_corner + ']')

        terminal.printf(x=(spell_item_info_start_x + spell_item_info_width), y=spell_item_info_start_y,
                        s=unicode_frame_colour + spell_item_info_cross_junction + ']')

        terminal.printf(x=(spell_item_info_start_x + spell_item_info_width),
                        y=(spell_item_info_start_y + spell_item_info_depth) - 1,
                        s=unicode_frame_colour + spell_item_info_bottom_right_t_junction + ']')

    # display control message
    terminal.printf(x=spell_item_info_start_x + 2, y=(spell_item_info_start_y + spell_item_info_depth) - 2,
                    s='Press Escape to return')

    key_colour_string = "[color=DISPLAY_ITEM_EQUIPPED]"
    value_colour_string = "[/color][color=PLAYER_DEBUG]"

    item_entity = 0
    spell_entity = 0

    #
    # DISPLAY SPELL INFORMATION
    #
    if str(menu_selection) in spell_selection_keys:
        logger.info('Spell selected')

        spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=gameworld, slot=menu_selection,
                                                                          player_entity=player_entity)
        spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=spell_entity)
        spell_cooldown = SpellUtilities.get_spell_cooldown_remaining_turns(gameworld=gameworld,
                                                                           spell_entity=spell_entity)
        spell_type = SpellUtilities.get_spell_type(gameworld=gameworld, spell_entity=spell_entity)
        spell_range = SpellUtilities.get_spell_max_range(gameworld=gameworld, spell_entity=spell_entity)
        spell_description = SpellUtilities.get_spell_description(gameworld=gameworld, spell_entity=spell_entity)
        spell_condi_effects_list = SpellUtilities.get_all_condis_for_spell(gameworld=gameworld,
                                                                           spell_entity=spell_entity)
        spell_boon_effects_list = SpellUtilities.get_all_boons_for_spell(gameworld=gameworld, spell_entity=spell_entity)

        spell_resources_list = SpellUtilities.get_all_resources_for_spell(gameworld=gameworld,
                                                                          spell_entity=spell_entity)
        spell_no_targets = SpellUtilities.get_spell_max_targets(gameworld=gameworld, spell_entity=spell_entity)

        y_pos = spell_item_info_start_y + 1

        terminal.print_(x=spell_item_info_item_imp_text_x, y=y_pos, width=spell_item_info_width,
                        height=1, align=terminal.TK_ALIGN_CENTER, s=value_colour_string + spell_name)

        y_pos += 2
        terminal.printf(x=spell_item_info_item_imp_text_x, y=y_pos, s=key_colour_string + 'Type: ' + value_colour_string + spell_type)

        cooldown_string = format_cooldown_string(spell_cooldown)

        y_pos += 1
        terminal.printf(x=spell_item_info_item_imp_text_x, y=y_pos,
                        s=key_colour_string + 'On cooldown: ' + value_colour_string + cooldown_string)

        y_pos += 1
        if spell_range == 1:
            tile_string = ' tile'
        else:
            tile_string = ' tiles'
        terminal.printf(x=spell_item_info_item_imp_text_x, y=y_pos,
                        s=key_colour_string + 'Max Range: ' + value_colour_string + str(spell_range) + tile_string)

        y_pos += 1
        terminal.printf(x=spell_item_info_item_imp_text_x, y=y_pos,
                        s=key_colour_string + 'No Targets: ' + value_colour_string + str(spell_no_targets))

        y_pos += 2
        terminal.printf(x=spell_item_info_item_imp_text_x, y=y_pos, s=key_colour_string + 'Effects...')

        condi_string = get_condis_as_string(condi_list=spell_condi_effects_list)
        boon_string = get_boons_as_string(boon_list=spell_boon_effects_list)
        resource_string = get_resources_as_string(spell_resources_list)

        y_pos += 1
        terminal.printf(x=spell_item_info_item_imp_text_x, y=y_pos,
                        s=key_colour_string + 'Causes: ' + value_colour_string + condi_string)
        y_pos += 1
        terminal.printf(x=spell_item_info_item_imp_text_x, y=y_pos,
                        s=key_colour_string + 'Gives: ' + value_colour_string + boon_string + resource_string)

        # draw fluff text
        y_pos += 3
        draw_fluff_text(x=spell_item_info_item_imp_text_x, y=y_pos, width=spell_item_info_width,
                        fluff_text=spell_description, key_colour_string=key_colour_string,
                        value_colour_string=value_colour_string)
    #
    # DISPLAY ARMOUR INFORMATION
    #
    elif menu_selection in armour_selection_keys:
        logger.info('Armour selected')
        item_entity = ItemUtilities.get_armour_entity_from_body_location(gameworld=gameworld, entity=player_entity,
                                                                         bodylocation=armour_map[menu_selection])
        if item_entity > 0:
            logger.debug('Armour entity is {}', item_entity)
            # draw portrait
            filepath = portraits_folder + hardoced_armour_portrait_file

            file_content = Externalfiles.load_existing_file(filename=filepath)
            posy = spell_item_info_start_y + 3
            for row in file_content:
                terminal.printf(x=spell_item_info_item_imp_text_x + 7, y=posy, s=row)
                posy += 1

            # draw middle horizontal line
            draw_horizontal_line_after_portrait(x=spell_item_info_start_x, y=spell_item_info_item_horz,
                                                w=spell_item_info_width, string_colour=unicode_frame_colour,
                                                horiz_glyph=spell_item_info_horizontal,
                                                left_t_glyph=spell_item_info_left_t_junction,
                                                right_t_glyph=spell_item_info_right_t_junction)

            # draw armour stuff
            defense_value = ItemUtilities.get_armour_defense_value(gameworld=gameworld, entity=item_entity)
            armourset_value = ItemUtilities.get_armour_set_name(gameworld=gameworld, entity=item_entity)
            quality_value = ItemUtilities.get_item_quality(gameworld=gameworld, entity=item_entity)
            spell_entity = ItemUtilities.get_spell_from_item(gameworld=gameworld, item_entity=item_entity)
            if spell_entity is None:
                spell_entity = -99
            armour_description_value = ItemUtilities.get_item_description(gameworld=gameworld, entity=item_entity)

            terminal.printf(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 1,
                            s=key_colour_string + 'Defense:' + value_colour_string + str(defense_value))
            terminal.printf(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 3,
                            s=key_colour_string + 'Armourset:' + value_colour_string + armourset_value)
            terminal.printf(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 4,
                            s=key_colour_string + 'Quality:' + value_colour_string + quality_value)
            terminal.printf(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 6,
                            s=key_colour_string + 'Embedded Spell Info...')
            if spell_entity == 0:
                terminal.printf(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 7,
                                s='No embedded spell')
            else:
                spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=spell_entity)
                spell_cooldown = SpellUtilities.get_spell_cooldown_remaining_turns(gameworld=gameworld,
                                                                                   spell_entity=spell_entity)
                spell_range = SpellUtilities.get_spell_max_range(gameworld=gameworld, spell_entity=spell_entity)
                spell_condi_effects_list = SpellUtilities.get_all_condis_for_spell(gameworld=gameworld,
                                                                                   spell_entity=spell_entity)
                spell_boon_effects_list = SpellUtilities.get_all_boons_for_spell(gameworld=gameworld,
                                                                                 spell_entity=spell_entity)
                terminal.printf(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 7,
                                s=key_colour_string + 'Name:' + value_colour_string + spell_name)
                terminal.printf(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 8,
                                s=key_colour_string + 'Cooldown:' + value_colour_string + str(spell_cooldown))
                terminal.printf(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 9,
                                s=key_colour_string + 'Range:' + value_colour_string + str(spell_range))
                terminal.printf(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 11,
                                s=key_colour_string + 'Effects...')

                condi_string = get_condis_as_string(condi_list=spell_condi_effects_list)
                boon_string = get_boons_as_string(boon_list=spell_boon_effects_list)

                terminal.printf(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 13,
                                s=key_colour_string + 'Causes: ' + value_colour_string + condi_string)

                terminal.printf(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 14,
                                s=key_colour_string + 'Gives: ' + value_colour_string + boon_string)

            # draw fluff text
            draw_fluff_text(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 16,
                            width=spell_item_info_width, fluff_text=armour_description_value,
                            key_colour_string=key_colour_string, value_colour_string=value_colour_string)

    #
    # DISPLAY JEWELLERY INFORMATION
    #
    elif menu_selection in jewellery_selection_keys:
        item_entity = ItemUtilities.get_jewellery_entity_from_body_location(gameworld=gameworld,
                                                                            entity=player_entity,
                                                                            bodylocation=jewellery_map[
                                                                                menu_selection])
        # draw portrait
        filepath = portraits_folder + hardcoded_item_portrait_file

        file_content = Externalfiles.load_existing_file(filename=filepath)
        posy = spell_item_info_start_y + 3
        for row in file_content:
            terminal.printf(x=spell_item_info_item_imp_text_x + 7, y=posy, s=row)
            posy += 1

        # draw middle horizontal line
        draw_horizontal_line_after_portrait(x=spell_item_info_start_x, y=spell_item_info_item_horz,
                                            w=spell_item_info_width, string_colour=unicode_frame_colour,
                                            horiz_glyph=spell_item_info_horizontal,
                                            left_t_glyph=spell_item_info_left_t_junction,
                                            right_t_glyph=spell_item_info_right_t_junction)

        # draw important text
        jewellery_statbonus = ItemUtilities.get_jewellery_stat_bonus(gameworld=gameworld,
                                                                     jewellery_entity=item_entity)
        spell_entity = ItemUtilities.get_spell_from_item(gameworld=gameworld, item_entity=item_entity)
        jewellery_description = ItemUtilities.get_item_description(gameworld=gameworld, entity=item_entity)

        # draw jewellery stuff
        terminal.printf(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 1,
                        s=key_colour_string + 'Bonus to:' + value_colour_string + jewellery_statbonus[0])
        terminal.printf(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 2,
                        s=key_colour_string + 'Attribute type:' + value_colour_string + 'Primary')
        terminal.printf(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 3,
                        s=key_colour_string + 'Bonus:' + value_colour_string + '+' + str(jewellery_statbonus[1]))

        # embedded spell
        spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=spell_entity)
        spell_cooldown = SpellUtilities.get_spell_cooldown_remaining_turns(gameworld=gameworld,
                                                                           spell_entity=spell_entity)
        spell_range = SpellUtilities.get_spell_max_range(gameworld=gameworld, spell_entity=spell_entity)
        spell_condi_effects_list = SpellUtilities.get_all_condis_for_spell(gameworld=gameworld,
                                                                           spell_entity=spell_entity)
        spell_boon_effects_list = SpellUtilities.get_all_boons_for_spell(gameworld=gameworld,
                                                                         spell_entity=spell_entity)

        terminal.printf(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 5,
                        s=key_colour_string + 'Embedded Spell:...')
        terminal.printf(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 6,
                        s=key_colour_string + 'Name:' + value_colour_string + spell_name)
        terminal.printf(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 7,
                        s=key_colour_string + 'Cooldown:' + value_colour_string + str(spell_cooldown))
        terminal.printf(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 8,
                        s=key_colour_string + 'Range:' + value_colour_string + str(spell_range))
        terminal.printf(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 10,
                        s=key_colour_string + 'Effects...')

        condi_string = get_condis_as_string(condi_list=spell_condi_effects_list)
        boon_string = get_boons_as_string(boon_list=spell_boon_effects_list)

        terminal.printf(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 12,
                        s=key_colour_string + 'Causes: ' + value_colour_string + condi_string)

        terminal.printf(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 13,
                        s=key_colour_string + 'Gives: ' + value_colour_string + boon_string)
        # draw fluff text
        draw_fluff_text(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 15,
                        width=spell_item_info_width, fluff_text=jewellery_description,
                        key_colour_string=key_colour_string, value_colour_string=value_colour_string)
    else:
        return
    selected_entity = item_entity + spell_entity
    if selected_entity > 0:
        # blit the terminal
        terminal.refresh()

        # wait for escape key
        player_not_pressed_a_key = True
        while player_not_pressed_a_key:
            event_to_be_processed, event_action = handle_game_keys()
            if event_to_be_processed == 'keypress':
                logger.info('event action is {}', event_action)
                if event_action == 'quit':
                    player_not_pressed_a_key = False


def draw_fluff_text(x, y, key_colour_string, value_colour_string, width, fluff_text):
    terminal.printf(x=x, y=y,
                    s=key_colour_string + 'Description...')
    terminal.print_(x=x, y=y + 1,
                    width=width, height=5, align=terminal.TK_ALIGN_LEFT,
                    s=value_colour_string + fluff_text.capitalize())


def format_cooldown_string(spell_cooldown):
    if spell_cooldown > 0:
        cooldown_string = 'Yes (' + str(spell_cooldown) + ') turns remaining'
    else:
        cooldown_string = 'No'
    return cooldown_string


def get_resources_as_string(resource_list):
    resource_string = 'Nothing'
    if len(resource_list) > 0:
        resource_string = ''
        cnt = 0
        for _ in resource_list:
            resource_string += resource_list[cnt].capitalize() + ' '
            cnt += 1
    return resource_string


def get_boons_as_string(boon_list):
    boon_string = 'Nothing'
    if len(boon_list) > 0:
        boon_string = ''
        cnt = 0
        for _ in boon_list:
            boon_string += boon_list[cnt].capitalize() + ' '
            cnt += 1
    return boon_string


def get_condis_as_string(condi_list):
    condi_string = 'Nothing'
    if len(condi_list) > 0:
        condi_string = ''
        cnt = 0
        for _ in condi_list:
            condi_string += condi_list[cnt].capitalize() + ' '
            cnt += 1
    return condi_string


def draw_horizontal_line_after_portrait(x, y, w, string_colour, horiz_glyph, left_t_glyph, right_t_glyph):
    for z in range(x, (x + w)):
        terminal.printf(x=z, y=y,
                        s=string_colour + horiz_glyph + ']')

    terminal.printf(x=x, y=y,
                    s=string_colour + left_t_glyph + ']')
    terminal.printf(x=x + w, y=y,
                    s=string_colour + right_t_glyph + ']')
