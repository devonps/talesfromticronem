from bearlibterminal import terminal
from loguru import logger

from utilities import configUtilities
from utilities.common import CommonUtils
from utilities.input_handlers import handle_game_keys


def process(menu_selection):
    logger.info('Items and spells info panel accessed')
    game_config = configUtilities.load_config()
    item_selection_keys = configUtilities.get_config_value_as_list(configfile=game_config, section='spellInfoPopup',
                                                                   parameter='ITEM_KEYS')
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

    ascii_prefix = 'ASCII_SINGLE_'
    spell_item_info_left_t_junction = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                       parameter=ascii_prefix + 'LEFT_T_JUNCTION')

    spell_item_info_right_t_junction = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                        parameter=ascii_prefix + 'RIGHT_T_JUNCTION')
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
                        s=unicode_frame_colour + spell_item_info_right_t_junction + ']')

    # display control message
    terminal.printf(x=spell_item_info_start_x + 2, y=(spell_item_info_start_y + spell_item_info_depth) - 2,
                    s='Press Escape to return')

    # determine which information is to be displayed
    logger.debug('raw menu selection is {}', menu_selection)
    logger.debug('STR menu selection is {}', str(menu_selection))

    if str(menu_selection) in spell_selection_keys:
        logger.info('Spell selected')

    elif menu_selection in item_selection_keys:
        logger.info('Item selected')
    else:
        return

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
