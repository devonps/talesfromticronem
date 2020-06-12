from bearlibterminal import terminal
from loguru import logger

from utilities import configUtilities
from utilities.common import CommonUtils
from utilities.input_handlers import handle_game_keys
from utilities.spellHelp import SpellUtilities


def spell_pop_up(game_config, slot, gameworld, player):

    logger.info('Spell pop up')

    spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=gameworld, slot=slot,
                                                                      player_entity=player)

    is_spell_on_cooldown = SpellUtilities.get_spell_cooldown_status(gameworld=gameworld, spell_entity=spell_entity)

    spell_popup_start_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellpopup',
                                                                        parameter='SP_START_X')

    spell_popup_start_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellpopup',
                                                                        parameter='SP_START_Y')

    ascii_prefix = 'ASCII_SINGLE_'

    spell_popup_left_t_junction = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                 parameter=ascii_prefix + 'LEFT_T_JUNCTION')

    spell_popup_right_t_junction = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                 parameter=ascii_prefix + 'RIGHT_T_JUNCTION')

    spell_popup_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellpopup',
                                                                      parameter='SP_WIDTH')
    spell_popup_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellpopup',
                                                                       parameter='SP_DEPTH')
    spell_popup_top_left_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                  parameter=ascii_prefix + 'TOP_LEFT')

    spell_popup_bottom_left_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                     parameter=ascii_prefix + 'BOTTOM_LEFT')

    spell_popup_top_right_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                   parameter=ascii_prefix + 'TOP_RIGHT')

    spell_popup_bottom_right_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                      parameter=ascii_prefix + 'BOTTOM_RIGHT')

    spell_popup_horizontal = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                             parameter=ascii_prefix + 'HORIZONTAL')
    spell_popup_vertical = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                           parameter=ascii_prefix + 'VERTICAL')

    # unicode strings of colours
    unicode_frame_colour = '[font=dungeon][color=SPELLINFO_FRAME_COLOUR]['

    # draw frame for spell pop up
    spell_popup_start_x += ((slot -1) * 4)

    # draw verticals
    for zz in range(spell_popup_height - 1):
        terminal.printf(x=spell_popup_start_x, y=(spell_popup_start_y + - 1) - zz,
                        s=unicode_frame_colour + spell_popup_vertical + ']')

        terminal.printf(x=(spell_popup_start_x + spell_popup_width) - 1, y=(spell_popup_start_y + - 2) - zz,
                        s=unicode_frame_colour + spell_popup_vertical + ']')

    # draw top horizontal
    for zz in range(spell_popup_width - 2):
        terminal.printf(x=(spell_popup_start_x + 1) + zz, y=(spell_popup_start_y - spell_popup_height) - 1,
                        s=unicode_frame_colour + spell_popup_horizontal + ']')

    # draw bottom open corners
    # left open
    terminal.printf(x=spell_popup_start_x, y=(spell_popup_start_y),
                    s=unicode_frame_colour + spell_popup_right_t_junction + ']')
    # right open
    terminal.printf(x=spell_popup_start_x + 4, y=(spell_popup_start_y),
                    s=unicode_frame_colour + spell_popup_left_t_junction + ']')

    # draw top left corner to link
    terminal.printf(x=spell_popup_start_x + 4, y=(spell_popup_start_y - 1),
                    s=unicode_frame_colour + spell_popup_top_left_corner + ']')

    # draw from right cross point to right hand vertical
    for zz in range(spell_popup_width -6):
        terminal.printf(x=(spell_popup_start_x + 5) + zz, y=(spell_popup_start_y + - 1),
                        s=unicode_frame_colour + spell_popup_horizontal + ']')

    # blank out horizontal spell button
    for zz in range(3):
        terminal.printf(x=(spell_popup_start_x + 1) + zz, y=spell_popup_start_y, s=' ')

    # bottom right corner
    terminal.printf(x=(spell_popup_start_x + spell_popup_width) - 1, y=(spell_popup_start_y + - 1),
                    s=unicode_frame_colour + spell_popup_bottom_right_corner + ']')

    # top right corner
    terminal.printf(x=(spell_popup_start_x + spell_popup_width) - 1, y=(spell_popup_start_y - spell_popup_height) - 1,
                    s=unicode_frame_colour + spell_popup_top_right_corner + ']')

    # top left corner
    terminal.printf(x=spell_popup_start_x, y=(spell_popup_start_y - spell_popup_height) - 1,
                    s=unicode_frame_colour + spell_popup_top_left_corner + ']')
    # extra step covers odd vertical count
    terminal.printf(x=spell_popup_start_x, y=(spell_popup_start_y - spell_popup_height) ,
                    s=unicode_frame_colour + spell_popup_vertical + ']')

    # spell name
    # spell description
    # spell type
    # spell range
    # spell cooldown
    # spell status effects
    # spell direct damage
    # spell AoE radius
    # user instructions
    if is_spell_on_cooldown:
        # don't display the cast option
        pass
    else:
        # display the cast option
        pass
    # display the quit option

    # blit the terminal
    terminal.refresh()

    # wait for user key press
    player_not_pressed_a_key = True
    while player_not_pressed_a_key:
        event_to_be_processed, event_action = handle_game_keys()
        if event_to_be_processed == 'keypress':
            if event_action == 'quit':
                player_not_pressed_a_key = False

            if event_action == 'a' and not is_spell_on_cooldown:
                # cast the spell
                player_not_pressed_a_key = False

