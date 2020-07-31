from bearlibterminal import terminal
from loguru import logger

from utilities import configUtilities, formulas
from utilities.common import CommonUtils
from utilities.input_handlers import handle_game_keys
from utilities.itemsHelp import ItemUtilities
from utilities.mobileHelp import MobileUtilities
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
    spell_popup_start_x += ((slot - 1) * 4)

    draw_verticals(spell_popup_height=spell_popup_height, spell_popup_start_x=spell_popup_start_x,
                   spell_popup_start_y=spell_popup_start_y, unicode_frame_colour=unicode_frame_colour,
                   spell_popup_vertical=spell_popup_vertical, spell_popup_width=spell_popup_width)

    draw_horizontals(spell_popup_width=spell_popup_width, spell_popup_start_x=spell_popup_start_x, spell_popup_start_y=spell_popup_start_y, spell_popup_height=spell_popup_height, unicode_frame_colour=unicode_frame_colour, spell_popup_horizontal=spell_popup_horizontal)

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
    for zz in range(spell_popup_width - 6):
        terminal.printf(x=(spell_popup_start_x + 5) + zz, y=(spell_popup_start_y + - 1),
                        s=unicode_frame_colour + spell_popup_horizontal + ']')

    draw_blank_buttons(spell_popup_start_x=spell_popup_start_x, spell_popup_start_y=spell_popup_start_y)

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
    terminal.printf(x=spell_popup_start_x, y=(spell_popup_start_y - spell_popup_height),
                    s=unicode_frame_colour + spell_popup_vertical + ']')

    top_of_popup = spell_popup_start_y - spell_popup_height
    # spell name
    slot_spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=gameworld, slot=slot,
                                                                           player_entity=player)
    spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=slot_spell_entity)
    terminal.printf(x=spell_popup_start_x + 1, y=top_of_popup, s=spell_name.title())

    # spell description
    spell_description = SpellUtilities.get_spell_short_description(gameworld=gameworld, spell_entity=slot_spell_entity)
    terminal.printf(x=spell_popup_start_x + 1, y=top_of_popup + 1, s=spell_description)

    # spell type
    spell_type = SpellUtilities.get_spell_type(gameworld=gameworld, spell_entity=slot_spell_entity)
    terminal.printf(x=spell_popup_start_x + 1, y=top_of_popup + 2, s='Type:' + spell_type)

    # spell range
    spell_range = SpellUtilities.get_spell_max_range(gameworld=gameworld, spell_entity=slot_spell_entity)
    terminal.printf(x=spell_popup_start_x + 1, y=top_of_popup + 3, s='Range:' + str(spell_range))
    # spell cooldown
    spell_cooldown_value = SpellUtilities.get_spell_cooldown_time(gameworld=gameworld, spell_entity=slot_spell_entity)
    terminal.printf(x=spell_popup_start_x + 1, y=top_of_popup + 4, s='Cooldown turns:' + str(spell_cooldown_value))
    # spell status effects
    condi_effects = SpellUtilities.get_all_condis_for_spell(gameworld=gameworld, spell_entity=slot_spell_entity)
    boon_effects = SpellUtilities.get_all_boons_for_spell(gameworld=gameworld, spell_entity=slot_spell_entity)
    other_effects = SpellUtilities.get_all_resources_for_spell(gameworld=gameworld, spell_entity=slot_spell_entity)
    terminal.printf(x=spell_popup_start_x + 1, y=top_of_popup + 5, s='Boons:' + str(boon_effects))
    terminal.printf(x=spell_popup_start_x + 1, y=top_of_popup + 6, s='Conds:' + str(condi_effects))
    terminal.printf(x=spell_popup_start_x + 1, y=top_of_popup + 7, s='resources:' + str(other_effects))

    # spell direct damage
    equipped_weapons = MobileUtilities.get_weapons_equipped(gameworld=gameworld, entity=player)
    caster_power = MobileUtilities.get_mobile_primary_power(gameworld=gameworld, entity=player)
    spell_coeff = float(SpellUtilities.get_spell_damage_coeff(gameworld=gameworld, spell_entity=slot_spell_entity))

    weapon = which_weapon(equipped_weapons=equipped_weapons, slot=slot)

    weapon_strength = ItemUtilities.calculate_weapon_strength(gameworld=gameworld, weapon=weapon)
    outgoing_base_damage = formulas.outgoing_base_damage(weapon_strength=weapon_strength, power=caster_power,
                                                         spell_coefficient=spell_coeff)
    terminal.printf(x=spell_popup_start_x + 1, y=top_of_popup + 8, s='Base Damage:' + str(outgoing_base_damage))
    # spell AoE radius
    spell_use_aoe = SpellUtilities.get_spell_aoe_status(gameworld=gameworld, spell_entity=slot_spell_entity)
    if spell_use_aoe == 'True':
        aoe_radius = SpellUtilities.get_spell_aoe_size(gameworld=gameworld, spell_entity=slot_spell_entity)
        terminal.printf(x=spell_popup_start_x + 1, y=top_of_popup + 9, s='AoE Radius:' + str(aoe_radius))
    else:
        terminal.printf(x=spell_popup_start_x + 1, y=top_of_popup + 9, s='No AoE')

    # user instructions
    if is_spell_on_cooldown:
        # don't display the cast option
        pass
    else:
        # display the cast option
        terminal.printf(x=spell_popup_start_x + 1, y=top_of_popup + 10, s='(a) Cast (ESC) quit')
    # display the quit option

    # blit the terminal
    terminal.refresh()

    # wait for user key press
    player_not_pressed_a_key = True
    while player_not_pressed_a_key:
        event_to_be_processed, event_action = handle_game_keys()
        if event_to_be_processed == 'keypress':
            logger.info('event action is {}', event_action)
            if event_action == 'quit':
                player_not_pressed_a_key = False

            if event_action == 0 and not is_spell_on_cooldown:
                # cast the spell
                player_not_pressed_a_key = False
                SpellUtilities.cast_spell(slot=slot, gameworld=gameworld, player=player, game_config=game_config)


def draw_blank_buttons(spell_popup_start_x, spell_popup_start_y):
    # blank out horizontal spell button
    for zz in range(3):
        terminal.printf(x=(spell_popup_start_x + 1) + zz, y=spell_popup_start_y, s=' ')


def draw_verticals(spell_popup_height, spell_popup_start_x, spell_popup_start_y, unicode_frame_colour,
                   spell_popup_vertical, spell_popup_width):
    # draw verticals
    for zz in range(spell_popup_height - 1):
        terminal.printf(x=spell_popup_start_x, y=(spell_popup_start_y + - 1) - zz,
                        s=unicode_frame_colour + spell_popup_vertical + ']')

        terminal.printf(x=(spell_popup_start_x + spell_popup_width) - 1, y=(spell_popup_start_y + - 2) - zz,
                        s=unicode_frame_colour + spell_popup_vertical + ']')


def draw_horizontals(spell_popup_width, spell_popup_start_x, spell_popup_start_y, spell_popup_height,
                     unicode_frame_colour, spell_popup_horizontal):
    # draw top horizontal
    for zz in range(spell_popup_width - 2):
        terminal.printf(x=(spell_popup_start_x + 1) + zz, y=(spell_popup_start_y - spell_popup_height) - 1,
                        s=unicode_frame_colour + spell_popup_horizontal + ']')


def which_weapon(equipped_weapons, slot):
    weapon = 0
    if equipped_weapons[2] != 0:
        weapon = equipped_weapons[2]
    else:
        if slot <= 2:
            weapon = equipped_weapons[0]
        else:
            weapon = equipped_weapons[1]

    return weapon
