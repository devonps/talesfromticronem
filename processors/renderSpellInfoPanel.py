import random

import esper
from bearlibterminal import terminal

from components import spells, spellBar
from utilities import configUtilities, formulas, world
from utilities.common import CommonUtils
from utilities.display import set_both_hands_weapon_string_es, set_main_hand_weapon_string_es, \
    set_off_hand_weapon_string_es, set_jewellery_left_ear_string, set_jewellery_right_ear_string, \
    set_jewellery_left_hand_string, set_jewellery_right_hand_string, set_jewellery_neck_string, get_head_armour_details, \
    get_chest_armour_details, get_hands_armour_details, get_legs_armour_details, get_feet_armour_details
from utilities.mobileHelp import MobileUtilities
from utilities.spellHelp import SpellUtilities


class RenderSpellInfoPanel(esper.Processor):
    def __init__(self, gameworld, game_map):
        self.gameworld = gameworld
        self.game_map = game_map
        self.game_config = configUtilities.load_config()

    def process(self, game_config):
        self.render_spell_info_outer_frame()
        self.render_equipped_items()
        self.render_energy_bars()
        self.render_class_mechanics()
        self.render_healing_spell()
        self.render_utility_spells()
        self.render_player_status_effects()

    def render_player_status_effects(self):
        self.render_boons()
        self.render_conditions()

    def render_equipped_items(self):

        self.render_equipped_weapons()
        self.render_equipped_jewellery()
        self.render_equipped_armour()

    def render_energy_bars(self):
        self.render_health()

    def render_boons(self):
        player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=self.game_config)
        list_of_boons = MobileUtilities.get_current_boons_applied_to_mobile(gameworld=self.gameworld,
                                                                           entity=player_entity)
        boon_start_x = configUtilities.get_config_value_as_integer(configfile=self.game_config, section='spellinfo',
                                                                       parameter='STATUS_EFFECTS_START_X')

        boon_start_y = configUtilities.get_config_value_as_integer(configfile=self.game_config, section='spellinfo',
                                                                       parameter='STATUS_EFFECTS_START_Y')

        no_boons = configUtilities.get_config_value_as_string(configfile=self.game_config, section='colorCodes', parameter='NO_STATUS_EFFECT')
        unicode_boon_string = no_boons

        boon_string = 'Boons: '
        if len(list_of_boons) > 0:
            unicode_boon_string = '[font=dungeon][color=BOON_BASE_COLOUR]'
            for z in list_of_boons:
                boon_string += z['shortcode'] + ' '

        terminal.printf(x=boon_start_x, y=boon_start_y, s=unicode_boon_string + boon_string)

    def render_conditions(self):

        player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=self.game_config)

        list_of_conditions = MobileUtilities.get_current_condis_applied_to_mobile(gameworld=self.gameworld,
                                                                                 entity=player_entity)
        condition_start_x = configUtilities.get_config_value_as_integer(configfile=self.game_config, section='spellinfo',
                                                                   parameter='STATUS_EFFECTS_START_X')

        condition_start_y = configUtilities.get_config_value_as_integer(configfile=self.game_config, section='spellinfo',
                                                                   parameter='STATUS_EFFECTS_START_Y') + 1
        no_condis = configUtilities.get_config_value_as_string(configfile=self.game_config, section='colorCodes', parameter='NO_STATUS_EFFECT')
        unicode_condition_string = no_condis
        condition_string = 'Condis: '

        if len(list_of_conditions) > 0:
            unicode_condition_string = '[font=dungeon][color=CONDITION_BASE_COLOUR]'
            for z in list_of_conditions:
                condition_string += z['shortcode'] + ' '

        terminal.printf(x=condition_start_x, y=condition_start_y, s=unicode_condition_string + condition_string)

    def render_spell_info_outer_frame(self):
        CommonUtils.render_ui_framework(game_config=self.game_config)

    def render_equipped_weapons(self):

        player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=self.game_config)

        this_row = configUtilities.get_config_value_as_integer(configfile=self.game_config, section='spellinfo',
                                                                   parameter='START_LIST_Y')

        this_row, this_letter = SpellUtilities.render_main_hand_spells(gameworld=self.gameworld, game_config=self.game_config, this_row=this_row, player_entity=player_entity)

        SpellUtilities.render_off_hand_spells(gameworld=self.gameworld, game_config=self.game_config, this_row=this_row, player_entity=player_entity)

    def render_equipped_jewellery(self):

        player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=self.game_config)

        start_list_x = configUtilities.get_config_value_as_integer(configfile=self.game_config, section='spellinfo',
                                                                   parameter='START_LIST_X')

        this_row = configUtilities.get_config_value_as_integer(configfile=self.game_config, section='spellinfo',
                                                               parameter='JEWELLERY_SPELL_Y')

        unicode_section_headers = configUtilities.get_config_value_as_string(configfile=self.game_config, section='colorCodes', parameter='SPELL_UI_SECTION_HEADERS')

        this_letter = 70
        this_row += 1
        terminal.printf(x=start_list_x, y=this_row, s=unicode_section_headers + 'Jewellery')
        this_row += 2
        left_ear = 'nothing'
        right_ear = 'nothing'
        left_hand = 'nothing'
        right_hand = 'nothing'
        neck = 'nothing'

        equipped_jewellery = MobileUtilities.get_jewellery_already_equipped(gameworld=self.gameworld, mobile=player_entity)
        if len(equipped_jewellery) > 0:
            left_ear = set_jewellery_left_ear_string(gameworld=self.gameworld, left_ear=equipped_jewellery[0])
            right_ear = set_jewellery_right_ear_string(gameworld=self.gameworld, right_ear=equipped_jewellery[1])
            left_hand = set_jewellery_left_hand_string(gameworld=self.gameworld, left_hand=equipped_jewellery[2])
            right_hand = set_jewellery_right_hand_string(gameworld=self.gameworld, right_hand=equipped_jewellery[3])
            neck = set_jewellery_neck_string(gameworld=self.gameworld, neck=equipped_jewellery[4])

        terminal.print_(x=start_list_x, y=this_row, s=chr(this_letter) + ' ' + left_ear)
        this_row += 1
        this_letter += 1
        terminal.print_(x=start_list_x, y=this_row, s=chr(this_letter) + ' ' + right_ear)
        this_row += 1
        this_letter += 1
        terminal.print_(x=start_list_x, y=this_row, s=chr(this_letter) + ' ' + left_hand)
        this_row += 1
        this_letter += 1
        terminal.print_(x=start_list_x, y=this_row, s=chr(this_letter) + ' ' + right_hand)
        this_row += 1
        this_letter += 1
        terminal.print_(x=start_list_x, y=this_row, s=chr(this_letter) + ' ' + neck)

    def render_health(self):
        player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=self.game_config)
        health_start_x = configUtilities.get_config_value_as_integer(configfile=self.game_config, section='spellinfo',
                                                                            parameter='ENERGY_BARS_START_X')

        health_start_y = configUtilities.get_config_value_as_integer(configfile=self.game_config, section='spellinfo',
                                                                            parameter='ENERGY_BARS_START_Y')

        debug_mode = configUtilities.get_config_value_as_integer(configfile=self.game_config, section='logging',
                                                    parameter='PLAYER_DEBUG')

        ascii_prefix = 'ASCII_SINGLE_'

        health_lost_fill = CommonUtils.get_ascii_to_unicode(game_config=self.game_config, parameter=ascii_prefix + 'HEALTH_LOST')
        health_remiaing_fill = CommonUtils.get_ascii_to_unicode(game_config=self.game_config, parameter=ascii_prefix + 'HEALTH_REMAINING')

        unicode_mechanic_health_lost = '[font=dungeon][color=ENERGY_HEALTH_LOST]['
        unicode_mechanic_health_remaining = '[font=dungeon][color=ENERGY_HEALTH_REMAINING]['

        current_health_value = MobileUtilities.get_mobile_derived_current_health(gameworld=self.gameworld, entity=player_entity)
        max_health_value = MobileUtilities.get_mobile_derived_maximum_health(gameworld=self.gameworld, entity=player_entity)

        health_split = formulas.calculate_percentage(low_number=current_health_value, max_number=max_health_value)

        # draw full lost health bar
        terminal.printf(x=health_start_x, y=health_start_y, s="Health ")
        for x in range(10):
            terminal.printf(x=(health_start_x + 8) + x, y=health_start_y, s=unicode_mechanic_health_lost + health_lost_fill + ']')

        # now draw health remaining on top of the above bar
        split_health = int(health_split / 10)
        for x in range(split_health):
            terminal.printf(x=(health_start_x + 8) + x, y=health_start_y,
                            s=unicode_mechanic_health_remaining + health_remiaing_fill + ']')

        if debug_mode:
            px = MobileUtilities.get_mobile_x_position(gameworld=self.gameworld, entity=player_entity)
            py = MobileUtilities.get_mobile_y_position(gameworld=self.gameworld, entity=player_entity)

            terminal.printf(x=health_start_x, y=health_start_y + 2,
                            s='map x:' + str(px) + ' map y:' + str(py))

    #
    # formally known as the F1 bar
    #
    def render_class_mechanics(self):

        start_list_x = configUtilities.get_config_value_as_integer(configfile=self.game_config, section='spellinfo',
                                                                   parameter='MECHANIC_START_X')

        start_x = configUtilities.get_config_value_as_integer(configfile=self.game_config,
                                                              section='newCharacter', parameter='NC_START_X')
        width = configUtilities.get_config_value_as_integer(configfile=self.game_config,
                                                            section='newCharacter', parameter='NC_WIDTH')

        this_row = configUtilities.get_config_value_as_integer(configfile=self.game_config, section='spellinfo',
                                                               parameter='MECHANIC_START_Y')
        dungeon_font = '[font=dungeon]'

        ascii_prefix = 'ASCII_SINGLE_'

        mechanic_left_t_junction_char = CommonUtils.get_ascii_to_unicode(game_config=self.game_config,
                                                                parameter=ascii_prefix + 'LEFT_T_JUNCTION')
        mechanic_right_t_junction_char = CommonUtils.get_ascii_to_unicode(game_config=self.game_config,
                                                                 parameter=ascii_prefix + 'RIGHT_T_JUNCTION')

        mechanic_info_top_left_corner = CommonUtils.get_ascii_to_unicode(game_config=self.game_config,
                                                                      parameter=ascii_prefix + 'TOP_LEFT')

        mechanic_info_bottom_left_corner = CommonUtils.get_ascii_to_unicode(game_config=self.game_config,
                                                                         parameter=ascii_prefix + 'BOTTOM_LEFT')

        mechanic_info_top_right_corner = CommonUtils.get_ascii_to_unicode(game_config=self.game_config,
                                                                       parameter=ascii_prefix + 'TOP_RIGHT')

        mechanic_info_bottom_right_corner = CommonUtils.get_ascii_to_unicode(game_config=self.game_config,
                                                                          parameter=ascii_prefix + 'BOTTOM_RIGHT')

        mechanic_info_horizontal = CommonUtils.get_ascii_to_unicode(game_config=self.game_config,
                                                                 parameter=ascii_prefix + 'HORIZONTAL')
        mechanic_info_vertical = CommonUtils.get_ascii_to_unicode(game_config=self.game_config,
                                                               parameter=ascii_prefix + 'VERTICAL')

        mechanic_background_fill = CommonUtils.get_ascii_to_unicode(game_config=self.game_config, parameter=ascii_prefix + 'MECHANIC_FILL')

        mechanic_depth = 10
        mechanic_width = 1
        unicode_mechanic_frame_enabled = dungeon_font + '[color=CLASS_MECHANIC_FRAME_COLOUR]['
        unicode_mechanic_id = dungeon_font + '[color=CLASS_MECHANIC_DISABLED]['
        unicode_mechanic_partial = dungeon_font + '[color=CLASS_MECHANIC_PARTIAL]['

        start_here = this_row
        for z in range(start_x, (start_x + width)):
            terminal.printf(x=z, y=this_row - 1,
                            s=unicode_mechanic_frame_enabled + mechanic_info_horizontal + ']')

        terminal.printf(x=start_x, y=this_row - 1,
                        s=unicode_mechanic_frame_enabled + mechanic_left_t_junction_char + ']')

        terminal.printf(x=(start_x + width), y=this_row - 1,
                        s=unicode_mechanic_frame_enabled + mechanic_right_t_junction_char + ']')

        for loop in range(4):
            unicode_mechanic_frame = unicode_mechanic_id if loop < 2 else unicode_mechanic_frame_enabled
            unicode_class_id = dungeon_font + '[color=CLASS_MECHANIC_DISABLED]' if loop < 2 else dungeon_font + '[color=CLASS_MECHANIC_FRAME_COLOUR]'
            # top left
            terminal.printf(x=start_list_x, y=this_row + 1,
                            s=unicode_mechanic_frame + mechanic_info_top_left_corner + ']')
            # bottom left
            terminal.printf(x=start_list_x, y=((this_row + mechanic_depth) + 2),
                            s=unicode_mechanic_frame + mechanic_info_bottom_left_corner + ']')
            # top right
            terminal.printf(x=(start_list_x + mechanic_width) + 1, y=this_row + 1,
                            s=unicode_mechanic_frame + mechanic_info_top_right_corner + ']')
            # bottom right
            terminal.printf(x=(start_list_x + mechanic_width) + 1, y=((this_row + mechanic_depth) + 2),
                            s=unicode_mechanic_frame + mechanic_info_bottom_right_corner + ']')

            # Class buttons
            terminal.printf(x=start_list_x, y=this_row, s=unicode_class_id + 'F' + str(loop + 1))
            # verticals
            for d in range(mechanic_depth):
                terminal.printf(x=start_list_x, y=this_row + d + 2,
                                s=unicode_mechanic_frame + mechanic_info_vertical + ']')

                terminal.printf(x=(start_list_x + mechanic_width) + 1, y=this_row + d + 2,
                                s=unicode_mechanic_frame + mechanic_info_vertical + ']')

            # horizontal
            for a in range(mechanic_width):
                terminal.printf(x=(start_list_x + a) + 1, y=this_row + 1,
                                s=unicode_mechanic_frame + mechanic_info_horizontal + ']')
                terminal.printf(x=(start_list_x + a) + 1, y=((this_row + mechanic_depth) + 2),
                                s=unicode_mechanic_frame + mechanic_info_horizontal + ']')


            # mechanic partially filled - measured in 10% blocks
            xx = random.randrange(1, 10)
            for zz in range(xx):
                terminal.printf(x=start_list_x + 1, y=(mechanic_depth + this_row + 1) - zz, s=unicode_mechanic_partial + mechanic_background_fill + ']')

            start_list_x += 6
            this_row = start_here

    def render_equipped_armour(self):
        player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=self.game_config)

        start_list_x = configUtilities.get_config_value_as_integer(configfile=self.game_config, section='spellinfo',
                                                                   parameter='START_LIST_X')

        this_row = configUtilities.get_config_value_as_integer(configfile=self.game_config, section='spellinfo',
                                                               parameter='ARMOUR_SPELL_Y')

        unicode_section_headers = configUtilities.get_config_value_as_string(configfile=self.game_config, section='colorCodes', parameter='SPELL_UI_SECTION_HEADERS')

        this_letter = 65
        this_row += 1
        terminal.printf(x=start_list_x, y=this_row, s=unicode_section_headers + 'Armour ')
        this_row += 2

        # head armour
        items = get_head_armour_details(gameworld=self.gameworld, entity_id=player_entity)
        if len(items) == 1:
            str_to_print = items[0]
        else:
            str_to_print = items[0] + items[2]

        terminal.print_(x=start_list_x, y=this_row, s=chr(this_letter) + ' ' + str_to_print)
        this_row += 1
        this_letter += 1

        # chest armour
        items = get_chest_armour_details(gameworld=self.gameworld, entity_id=player_entity)
        if len(items) == 1:
            str_to_print = items[0]
        else:
            str_to_print = items[0] + items[2]

        terminal.print_(x=start_list_x, y=this_row, s=chr(this_letter) + ' ' + str_to_print)
        this_row += 1
        this_letter += 1

        # hands armour
        items = get_hands_armour_details(gameworld=self.gameworld, entity_id=player_entity)
        if len(items) == 1:
            str_to_print = items[0]
        else:
            str_to_print = items[0] + items[2]

        terminal.print_(x=start_list_x, y=this_row, s=chr(this_letter) + ' ' + str_to_print)
        this_row += 1
        this_letter += 1

        # legs armour
        items = get_legs_armour_details(gameworld=self.gameworld, entity_id=player_entity)
        if len(items) == 1:
            str_to_print = items[0]
        else:
            str_to_print = items[0] + items[2]
        terminal.print_(x=start_list_x, y=this_row, s=chr(this_letter) + ' ' + str_to_print)
        this_row += 1
        this_letter += 1

        # feet armour
        items = get_feet_armour_details(gameworld=self.gameworld, entity_id=player_entity)
        if len(items) == 1:
            str_to_print = items[0]
        else:
            str_to_print = items[0] + items[2]
        terminal.print_(x=start_list_x, y=this_row, s=chr(this_letter) + ' ' + str_to_print)

    def render_utility_spells(self):
        player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=self.game_config)
        start_list_x = configUtilities.get_config_value_as_integer(configfile=self.game_config, section='spellinfo',
                                                                   parameter='START_LIST_X')

        this_row = configUtilities.get_config_value_as_integer(configfile=self.game_config, section='spellinfo',
                                                                   parameter='UTILITY_SPELL_Y')

        unicode_section_headers = configUtilities.get_config_value_as_string(configfile=self.game_config, section='colorCodes', parameter='SPELL_UI_SECTION_HEADERS')
        unicode_cooldown_disabled = '[font=dungeon][color=SPELLINFO_COOLDOWN_DISABLED]'
        unicode_cooldown_enabled = '[font=dungeon][color=SPELLINFO_COOLDOWN_ACTIVE]'
        unicode_white_colour = '[font=dungeon][color=SPELLINFO_HOTKEY_ACTIVE]'
        cooldown_string_x = start_list_x + 1
        name_string_x = start_list_x + 4

        this_letter = 55
        this_row += 1
        terminal.printf(x=start_list_x, y=this_row, s=unicode_section_headers + 'Utility ')
        this_row += 2
        slot = 7
        for _ in range(3):
            name_string = unicode_cooldown_disabled + 'nothing selected'
            slot_spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=self.gameworld, slot=slot,
                                                                                       player_entity=player_entity)
            if slot_spell_entity > 0:

                spell_name, spell_range, spell_cooldown_value = SpellUtilities.get_spell_info_details(
                    gameworld=self.gameworld, spell_entity=slot_spell_entity)

                if spell_cooldown_value > 0:
                    cooldown_colour = unicode_cooldown_enabled
                else:
                    spell_cooldown_value = 0
                    cooldown_colour = unicode_cooldown_disabled

                cooldown_string = cooldown_colour + ' ' + str(spell_cooldown_value)
                name_string = unicode_white_colour + spell_name

                terminal.printf(x=cooldown_string_x, y=this_row, s=cooldown_string)
            terminal.printf(x=start_list_x, y=this_row, s=chr(this_letter))
            terminal.printf(x=name_string_x, y=this_row, s=name_string)
            this_row += 1
            this_letter += 1
            slot += 1

    def render_healing_spell(self):
        player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=self.game_config)
        start_list_x = configUtilities.get_config_value_as_integer(configfile=self.game_config, section='spellinfo',
                                                                   parameter='START_LIST_X')

        this_row = configUtilities.get_config_value_as_integer(configfile=self.game_config, section='spellinfo',
                                                                   parameter='HEALING_SPELL_Y')

        unicode_section_headers = configUtilities.get_config_value_as_string(configfile=self.game_config, section='colorCodes', parameter='SPELL_UI_SECTION_HEADERS')
        unicode_cooldown_disabled = '[font=dungeon][color=SPELLINFO_COOLDOWN_DISABLED]'
        unicode_cooldown_enabled = '[font=dungeon][color=SPELLINFO_COOLDOWN_ACTIVE]'
        unicode_white_colour = '[font=dungeon][color=SPELLINFO_HOTKEY_ACTIVE]'
        cooldown_string_x = start_list_x + 1
        name_string_x = start_list_x + 4

        this_letter = 54
        this_row += 1
        terminal.printf(x=start_list_x, y=this_row, s=unicode_section_headers + 'Healing ')
        this_row += 1
        # spell name
        slot_spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=self.gameworld, slot=6,
                                                                               player_entity=player_entity)

        if slot_spell_entity > 0:
            spell_name = SpellUtilities.get_spell_name(gameworld=self.gameworld, spell_entity=slot_spell_entity)

            # spell cooldown
            spell_is_on_cooldown = SpellUtilities.get_spell_cooldown_status(gameworld=self.gameworld,
                                                                            spell_entity=slot_spell_entity)
            if spell_is_on_cooldown:
                spell_cooldown_value = SpellUtilities.get_spell_cooldown_time(gameworld=self.gameworld,
                                                                              spell_entity=slot_spell_entity)
                cooldown_colur = unicode_cooldown_enabled
            else:
                spell_cooldown_value = 0
                cooldown_colur = unicode_cooldown_disabled

            cooldown_string = cooldown_colur + ' ' + str(spell_cooldown_value)
            name_string = unicode_white_colour + spell_name
            terminal.printf(x=cooldown_string_x, y=this_row, s=cooldown_string)
            terminal.printf(x=name_string_x, y=this_row, s=name_string)

        terminal.printf(x=start_list_x, y=this_row, s=chr(this_letter))
        this_row += 1
        this_letter += 1
        this_row += 1
