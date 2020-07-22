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
    # unicode strings of colours
    unicode_frame_colour = '[font=dungeon][color=SPELLINFO_FRAME_COLOUR]['
    key_colour_string = "[color=DISPLAY_ITEM_EQUIPPED]"
    value_colour_string = "[/color][color=PLAYER_DEBUG]"

    item_entity = 0
    spell_entity = 0

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
    spell_item_info_width = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                        section='spellInfoPopup',
                                                                        parameter='SP_WIDTH')
    spell_item_info_depth = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                        section='spellInfoPopup',
                                                                        parameter='SP_DEPTH')


    # clear the area under the panel
    terminal.clear_area(spell_item_info_start_x, spell_item_info_start_y, spell_item_info_width,
                        spell_item_info_depth)

    # draw outer frame

    draw_outer_frame(startx=spell_item_info_start_x, starty=spell_item_info_start_y, width=spell_item_info_width, frame_colour=unicode_frame_colour, game_config=game_config, depth=spell_item_info_depth)

    # display control message
    terminal.printf(x=spell_item_info_start_x + 2, y=(spell_item_info_start_y + spell_item_info_depth) - 2,
                    s='Press Escape to return')

    #
    # DISPLAY SPELL INFORMATION
    #
    if str(menu_selection) in spell_selection_keys:
        logger.info('Spell selected')
        spell_entity = display_spell_information(gameworld=gameworld, game_config=game_config, player_entity=player_entity, menu_selection=menu_selection, key_colour=key_colour_string, value_colour=value_colour_string)
    #
    # DISPLAY ARMOUR INFORMATION
    #
    elif menu_selection in armour_selection_keys:
        logger.info('Armour selected')

        item_entity = display_armour_information(gameworld=gameworld, game_config=game_config, player_entity=player_entity, bodylocation=armour_map[menu_selection], key_colour=key_colour_string, value_colour=value_colour_string, frame_colour=unicode_frame_colour)

    #
    # DISPLAY JEWELLERY INFORMATION
    #
    elif menu_selection in jewellery_selection_keys:

        item_entity = display_jewellery_information(gameworld=gameworld, game_config=game_config, player_entity=player_entity, bodylocation=jewellery_map[menu_selection], key_colour=key_colour_string, value_colour=value_colour_string, frame_colour=unicode_frame_colour)

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
    resource_string = ' '
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


def draw_outer_frame(startx, width, starty, frame_colour, game_config, depth):
    ascii_prefix = 'ASCII_SINGLE_'
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
    # draw top/bottom horizontals
    for z in range(startx, (startx + width)):
        terminal.printf(x=z, y=starty, s=frame_colour + spell_item_info_horizontal + ']')

        terminal.printf(x=z, y=(starty + depth) - 1, s=frame_colour + spell_item_info_horizontal + ']')

    # draw left vertical
    for zz in range(depth - 1):
        terminal.printf(x=startx, y=starty + zz, s=frame_colour + spell_item_info_vertical + ']')

        # draw corners
        terminal.printf(x=startx, y=starty, s=frame_colour + spell_item_info_top_left_corner + ']')

        terminal.printf(x=startx, y=(starty + depth) - 1, s=frame_colour + spell_item_info_bottom_left_corner + ']')

        terminal.printf(x=(startx + width), y=starty, s=frame_colour + spell_item_info_cross_junction + ']')

        terminal.printf(x=(startx + width), y=(starty + depth) - 1, s=frame_colour + spell_item_info_bottom_right_t_junction + ']')


def is_tile_string_plural(spell_range):
    if spell_range == 1:
        tile_string = ' tile'
    else:
        tile_string = ' tiles'

    return tile_string


def draw_portrait(startx, starty, game_config, portrait_file):

    portraits_folder = configUtilities.get_config_value_as_string(configfile=game_config,
                                                                        section='files', parameter='PORTRAITSFOLDER')

    filepath = portraits_folder + portrait_file
    font_string = "[font=portrait]"

    file_content = Externalfiles.load_existing_file(filename=filepath)
    posy = starty + 2
    for row in file_content:
        terminal.printf(x=startx + 7, y=posy, s=font_string + row)
        posy += 1


def draw_spell_info(startx, starty, gameworld, spell_entity):

    key_colour_string = "[color=DISPLAY_ITEM_EQUIPPED]"
    value_colour_string = "[/color][color=PLAYER_DEBUG]"
    effects_title = key_colour_string + 'Effects...'
    status_effects_condi_list_title = key_colour_string + 'Causes: ' + value_colour_string
    status_effects_boon_title = key_colour_string + 'Gives: ' + value_colour_string

    terminal.printf(x=startx, y=starty + 6, s=key_colour_string + 'Embedded Spell Info...')
    if spell_entity == 0:
        terminal.printf(x=startx, y=starty + 7, s='No embedded spell')
    else:
        spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=spell_entity)
        spell_cooldown = SpellUtilities.get_spell_cooldown_remaining_turns(gameworld=gameworld,
                                                                           spell_entity=spell_entity)
        spell_range = SpellUtilities.get_spell_max_range(gameworld=gameworld, spell_entity=spell_entity)
        spell_condi_effects_list = SpellUtilities.get_all_condis_for_spell(gameworld=gameworld,
                                                                           spell_entity=spell_entity)
        spell_boon_effects_list = SpellUtilities.get_all_boons_for_spell(gameworld=gameworld,
                                                                         spell_entity=spell_entity)
        terminal.printf(x=startx, y=starty + 7, s=key_colour_string + 'Name:' + value_colour_string + spell_name)
        terminal.printf(x=startx, y=starty + 8, s=key_colour_string + 'Cooldown:' + value_colour_string + str(spell_cooldown))
        terminal.printf(x=startx, y=starty + 9, s=key_colour_string + 'Range:' + value_colour_string + str(spell_range))
        terminal.printf(x=startx, y=starty + 11, s=effects_title)

        condi_string = get_condis_as_string(condi_list=spell_condi_effects_list)
        boon_string = get_boons_as_string(boon_list=spell_boon_effects_list)

        terminal.printf(x=startx, y=starty + 13, s=status_effects_condi_list_title + condi_string)

        terminal.printf(x=startx, y=starty + 14, s=status_effects_boon_title + boon_string)


def display_spell_information(gameworld, menu_selection, player_entity, game_config, key_colour, value_colour):

    spell_key_colour_string = key_colour
    spell_value_colour_string = value_colour
    effects_title = spell_key_colour_string + 'Effects...'
    status_effects_condi_list_title = spell_key_colour_string + 'Causes: ' + spell_value_colour_string
    status_effects_boon_title = spell_key_colour_string + 'Gives: ' + spell_value_colour_string
    spell_type_string = spell_key_colour_string + 'Type: ' + spell_value_colour_string
    spell_cooldown_string = spell_key_colour_string + 'On cooldown: ' + spell_value_colour_string
    spell_range_string = spell_key_colour_string + 'Max Range: ' + spell_value_colour_string
    spell_targets_string = spell_key_colour_string + 'No Targets: ' + spell_value_colour_string

    spell_item_info_item_imp_text_x = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                                  section='spellInfoPopup',
                                                                                  parameter='SP_IMPORTANT_TEXT_X')

    spell_item_info_start_y = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                          section='spellInfoPopup',
                                                                          parameter='SP_START_Y')
    spell_item_info_width = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                        section='spellInfoPopup',
                                                                        parameter='SP_WIDTH')

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
                    height=1, align=terminal.TK_ALIGN_CENTER, s=spell_value_colour_string + spell_name)

    y_pos += 2
    terminal.printf(x=spell_item_info_item_imp_text_x, y=y_pos,
                    s=spell_type_string + spell_type)

    cooldown_string = format_cooldown_string(spell_cooldown)

    y_pos += 1
    terminal.printf(x=spell_item_info_item_imp_text_x, y=y_pos,
                    s=spell_cooldown_string + cooldown_string)

    y_pos += 1

    tile_string = is_tile_string_plural(spell_range=spell_range)

    terminal.printf(x=spell_item_info_item_imp_text_x, y=y_pos,
                    s=spell_range_string + str(spell_range) + tile_string)

    y_pos += 1
    terminal.printf(x=spell_item_info_item_imp_text_x, y=y_pos,
                    s=spell_targets_string + str(spell_no_targets))

    y_pos += 2
    terminal.printf(x=spell_item_info_item_imp_text_x, y=y_pos, s=effects_title)

    condi_string = get_condis_as_string(condi_list=spell_condi_effects_list)
    boon_string = get_boons_as_string(boon_list=spell_boon_effects_list)
    resource_string = get_resources_as_string(spell_resources_list)

    y_pos += 1
    terminal.printf(x=spell_item_info_item_imp_text_x, y=y_pos,
                    s=status_effects_condi_list_title + condi_string)
    y_pos += 1
    terminal.printf(x=spell_item_info_item_imp_text_x, y=y_pos,
                    s=status_effects_boon_title + boon_string + resource_string)

    # draw fluff text
    y_pos += 3
    draw_fluff_text(x=spell_item_info_item_imp_text_x, y=y_pos, width=spell_item_info_width,
                    fluff_text=spell_description, key_colour_string=spell_key_colour_string,
                    value_colour_string=spell_value_colour_string)

    return spell_entity


def display_armour_information(gameworld, game_config, player_entity, bodylocation, key_colour, value_colour, frame_colour):
    armour_key_colour_string = key_colour
    armour_value_colour_string = value_colour
    armour_ascii_prefix = 'ASCII_SINGLE_'
    # unicode strings of colours
    unicode_frame_colour = frame_colour
    armour_defense_string = armour_key_colour_string + 'Defense:' + armour_value_colour_string
    armour_armourset_string = armour_key_colour_string + 'Armourset:' + armour_value_colour_string
    armour_quality_string = armour_key_colour_string + 'Quality:' + armour_value_colour_string

    spell_item_info_item_imp_text_x = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                                  section='spellInfoPopup',
                                                                                  parameter='SP_IMPORTANT_TEXT_X')
    spell_item_info_start_x = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                          section='spellInfoPopup',
                                                                          parameter='SP_START_X')

    spell_item_info_start_y = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                          section='spellInfoPopup',
                                                                          parameter='SP_START_Y')
    spell_item_info_width = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                        section='spellInfoPopup',
                                                                        parameter='SP_WIDTH')
    spell_item_info_item_horz = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                            section='spellInfoPopup',
                                                                            parameter='SP_PORTRAIT_BAR')

    spell_item_info_item_imp_text = spell_item_info_item_horz + 2

    spell_item_info_left_t_junction = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                       parameter=armour_ascii_prefix + 'LEFT_T_JUNCTION')

    spell_item_info_right_t_junction = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                        parameter=armour_ascii_prefix + 'RIGHT_T_JUNCTION')

    spell_item_info_horizontal = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                  parameter=armour_ascii_prefix + 'HORIZONTAL')

    item_entity = ItemUtilities.get_armour_entity_from_body_location(gameworld=gameworld, entity=player_entity,
                                                                     bodylocation=bodylocation)
    if item_entity > 0:
        logger.debug('Armour entity is {}', item_entity)
        # draw portrait
        item_displayname = ItemUtilities.get_item_displayname(gameworld=gameworld, entity=item_entity)
        portrait_file = item_displayname + '.txt'
        draw_portrait(startx=spell_item_info_item_imp_text_x, starty=spell_item_info_start_y, game_config=game_config,
                      portrait_file=portrait_file)

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
        armour_description_value = ItemUtilities.get_item_description(gameworld=gameworld, entity=item_entity)

        terminal.printf(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 1,
                        s=armour_defense_string + str(defense_value))
        terminal.printf(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 3,
                        s=armour_armourset_string + armourset_value)
        terminal.printf(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 4,
                        s=armour_quality_string + quality_value)

        draw_spell_info(startx=spell_item_info_item_imp_text_x, starty=spell_item_info_item_imp_text,
                        gameworld=gameworld, spell_entity=spell_entity)

        # draw fluff text
        draw_fluff_text(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 16,
                        width=spell_item_info_width, fluff_text=armour_description_value,
                        key_colour_string=armour_key_colour_string, value_colour_string=armour_value_colour_string)

    return item_entity


def display_jewellery_information(gameworld, game_config, player_entity, bodylocation, key_colour, value_colour, frame_colour):
    jewellery_key_colour_string = key_colour
    jewellery_value_colour_string = value_colour
    jewellery_ascii_prefix = 'ASCII_SINGLE_'
    # unicode strings of colours
    unicode_frame_colour = frame_colour
    jewellery_bonus_string = jewellery_key_colour_string + 'Bonus to:' + jewellery_value_colour_string
    jewellery_attribute_string = jewellery_key_colour_string + 'Attribute type:' + jewellery_value_colour_string
    jewellery_att_bonus_string = jewellery_key_colour_string + 'Bonus:' + jewellery_value_colour_string

    spell_item_info_item_imp_text_x = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                                  section='spellInfoPopup',
                                                                                  parameter='SP_IMPORTANT_TEXT_X')
    spell_item_info_start_x = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                          section='spellInfoPopup',
                                                                          parameter='SP_START_X')

    spell_item_info_start_y = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                          section='spellInfoPopup',
                                                                          parameter='SP_START_Y')
    spell_item_info_width = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                        section='spellInfoPopup',
                                                                        parameter='SP_WIDTH')
    spell_item_info_item_horz = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                            section='spellInfoPopup',
                                                                            parameter='SP_PORTRAIT_BAR')

    spell_item_info_item_imp_text = spell_item_info_item_horz + 2

    spell_item_info_left_t_junction = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                       parameter=jewellery_ascii_prefix + 'LEFT_T_JUNCTION')

    spell_item_info_right_t_junction = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                        parameter=jewellery_ascii_prefix + 'RIGHT_T_JUNCTION')

    spell_item_info_horizontal = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                  parameter=jewellery_ascii_prefix + 'HORIZONTAL')

    item_entity = ItemUtilities.get_jewellery_entity_from_body_location(gameworld=gameworld,
                                                                        entity=player_entity,
                                                                        bodylocation=bodylocation)
    if item_entity > 0:
        # draw portrait
        item_displayname = ItemUtilities.get_item_name(gameworld=gameworld, entity=item_entity)
        portrait_file = item_displayname + '.txt'
        draw_portrait(startx=spell_item_info_item_imp_text_x, starty=spell_item_info_start_y, game_config=game_config,
                      portrait_file=portrait_file)

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
                        s=jewellery_bonus_string + jewellery_statbonus[0])
        terminal.printf(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 2,
                        s=jewellery_attribute_string + 'Primary')
        terminal.printf(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 3,
                        s=jewellery_att_bonus_string + '+' + str(jewellery_statbonus[1]))

        # embedded spell
        draw_spell_info(startx=spell_item_info_item_imp_text_x, starty=spell_item_info_item_imp_text, gameworld=gameworld,
                        spell_entity=spell_entity)

        # draw fluff text
        draw_fluff_text(x=spell_item_info_item_imp_text_x, y=spell_item_info_item_imp_text + 15,
                        width=spell_item_info_width, fluff_text=jewellery_description,
                        key_colour_string=jewellery_key_colour_string, value_colour_string=jewellery_value_colour_string)
    return item_entity
