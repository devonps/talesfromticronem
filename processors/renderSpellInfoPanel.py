import random

import esper
from bearlibterminal import terminal

from components import spells
from utilities import configUtilities, formulas, world
from utilities.common import CommonUtils
from utilities.display import set_both_hands_weapon_string_es, set_main_hand_weapon_string_es, \
    set_off_hand_weapon_string_es, set_jewellery_left_ear_string, set_jewellery_right_ear_string, \
    set_jewellery_left_hand_string, set_jewellery_right_hand_string, set_jewellery_neck_string, get_head_armour_details, \
    get_chest_armour_details, get_hands_armour_details, get_legs_armour_details, get_feet_armour_details
from utilities.mobileHelp import MobileUtilities
from utilities.spellHelp import SpellUtilities


class RenderSpellInfoPanel(esper.Processor):
    def __init__(self, gameworld):
        self.gameworld = gameworld
        self.game_config = configUtilities.load_config()

    def process(self, game_config):
        self.render_spell_info_outer_frame()
        self.render_equipped_items()
        self.render_energy_bars(game_config=game_config)
        # self.render_class_mechanics(game_config=game_config)
        self.render_spell_bar()
        self.render_utility_spells()
        # self.render_player_status_effects(game_config=game_config)

    def render_player_status_effects(self, game_config):

        player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=game_config)
        player_boons = MobileUtilities.get_current_boons_applied_to_mobile(gameworld=self.gameworld,
                                                                           entity=player_entity)
        player_conditions = MobileUtilities.get_current_condis_applied_to_mobile(gameworld=self.gameworld,
                                                                                 entity=player_entity)

        self.render_boons(list_of_boons=player_boons, game_config=game_config)
        self.render_conditions(list_of_conditions=player_conditions, game_config=game_config)

    def render_equipped_items(self):

        self.render_equipped_weapons()
        self.render_equipped_jewellery()
        self.render_equipped_armour()

    def render_energy_bars(self, game_config):
        self.render_health(self, game_config=game_config)
        self.render_mana(self, game_config=game_config)

    @staticmethod
    def render_boons(list_of_boons, game_config):
        boon_start_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                       parameter='STATUS_EFFECTS_START_X')

        boon_start_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                       parameter='STATUS_EFFECTS_START_Y')

        unicode_boon_string = '[font=dungeon][color=BOON_BASE_COLOUR]'

        boon_string = ''
        if len(list_of_boons) > 0:
            for z in list_of_boons:
                boon_string += z['shortcode'] + ' '

        terminal.printf(x=boon_start_x, y=boon_start_y, s=unicode_boon_string + 'Boons ' + boon_string)

    @staticmethod
    def render_conditions(list_of_conditions, game_config):
        condition_start_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                   parameter='STATUS_EFFECTS_START_X')

        condition_start_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                   parameter='STATUS_EFFECTS_START_Y') + 1

        unicode_condition_string = '[font=dungeon][color=CONDITION_BASE_COLOUR]'
        condition_string = ''

        if len(list_of_conditions) > 0:
            for z in list_of_conditions:
                condition_string += z['shortcode'] + ' '

        terminal.printf(x=condition_start_x, y=condition_start_y, s=unicode_condition_string + 'Conds ' + condition_string)

    @staticmethod
    def render_spell_info_outer_frame():

        unicode_string_to_print = '[font=dungeon][color=SPELLINFO_FRAME_COLOUR]['

        game_config = configUtilities.load_config()

        ascii_prefix = 'ASCII_SINGLE_'

        spell_infobox_start_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                            parameter='SI_START_X')

        spell_infobox_start_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                            parameter='SI_START_Y')

        spell_infobox_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                          parameter='SI_WIDTH')
        spell_infobox_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                           parameter='SI_DEPTH')

        items_start_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                            parameter='ITEMS_BAR_Y')

        class_start_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                            parameter='CLASS_BAR_Y')

        spell_info_top_left_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                      parameter=ascii_prefix + 'TOP_LEFT')

        spell_info_bottom_left_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                         parameter=ascii_prefix + 'BOTTOM_LEFT')

        spell_info_top_right_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                       parameter=ascii_prefix + 'TOP_RIGHT')

        spell_info_bottom_right_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                          parameter=ascii_prefix + 'BOTTOM_RIGHT')

        spell_info_horizontal = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                 parameter=ascii_prefix + 'HORIZONTAL')
        spell_info_vertical = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                               parameter=ascii_prefix + 'VERTICAL')

        items_splitter_left_t_junction = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                               parameter=ascii_prefix + 'LEFT_T_JUNCTION')
        items_splitter_right_t_junction = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                               parameter=ascii_prefix + 'RIGHT_T_JUNCTION')

        # render horizontal bottom
        for z in range(spell_infobox_start_x, (spell_infobox_start_x + spell_infobox_width)):
            terminal.printf(x=z, y=(spell_infobox_start_y + spell_infobox_height),
                            s=unicode_string_to_print + spell_info_horizontal + ']')
            terminal.printf(x=z, y=spell_infobox_start_y, s=unicode_string_to_print + spell_info_horizontal + ']')

        # render verticals
        for z in range(spell_infobox_start_y, (spell_infobox_start_y + spell_infobox_height) - 1):
            terminal.printf(x=spell_infobox_start_x, y=z + 1, s=unicode_string_to_print + spell_info_vertical + ']')
            terminal.printf(x=(spell_infobox_start_x + spell_infobox_width), y=z + 1,
                            s=unicode_string_to_print + spell_info_vertical + ']')

        # top left
        terminal.printf(x=spell_infobox_start_x, y=spell_infobox_start_y,
                        s=unicode_string_to_print + spell_info_top_left_corner + ']')
        # bottom left
        terminal.printf(x=spell_infobox_start_x, y=(spell_infobox_start_y + spell_infobox_height),
                        s=unicode_string_to_print + spell_info_bottom_left_corner + ']')
        # top right
        terminal.printf(x=(spell_infobox_start_x + spell_infobox_width), y=spell_infobox_start_y,
                        s=unicode_string_to_print + spell_info_top_right_corner + ']')
        # bottom right
        terminal.printf(x=(spell_infobox_start_x + spell_infobox_width),
                        y=(spell_infobox_start_y + spell_infobox_height),
                        s=unicode_string_to_print + spell_info_bottom_right_corner + ']')


        # render horizontal splitters
        for z in range(spell_infobox_start_x, (spell_infobox_start_x + spell_infobox_width)):
            terminal.printf(x=z, y=items_start_y,
                            s=unicode_string_to_print + spell_info_horizontal + ']')

            terminal.printf(x=z, y=class_start_y,
                            s=unicode_string_to_print + spell_info_horizontal + ']')

            terminal.printf(x=spell_infobox_start_x , y=items_start_y,
                            s=unicode_string_to_print + items_splitter_left_t_junction + ']')

            terminal.printf(x=(spell_infobox_start_x + spell_infobox_width), y=items_start_y,
                            s=unicode_string_to_print + items_splitter_right_t_junction + ']')

            terminal.printf(x=spell_infobox_start_x , y=class_start_y,
                            s=unicode_string_to_print + items_splitter_left_t_junction + ']')

            terminal.printf(x=(spell_infobox_start_x + spell_infobox_width), y=class_start_y,
                            s=unicode_string_to_print + items_splitter_right_t_junction + ']')

    def render_equipped_weapons(self):

        player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=self.game_config)

        start_list_x = configUtilities.get_config_value_as_integer(configfile=self.game_config, section='spellinfo',
                                                                   parameter='START_LIST_X')

        this_row = configUtilities.get_config_value_as_integer(configfile=self.game_config, section='spellinfo',
                                                                   parameter='START_LIST_Y')
        unicode_section_headers = '[font=dungeon][color=SPELLINFO_ITEM_EQUIPPED]'
        unicode_cooldown_disabled = '[font=dungeon][color=SPELLINFO_COOLDOWN_DISABLED]'
        unicode_cooldown_enabled = '[font=dungeon][color=SPELLINFO_COOLDOWN_ACTIVE]'
        unicode_white_colour = '[font=dungeon][color=SPELLINFO_HOTKEY_ACTIVE]'

        this_letter = 49
        terminal.printf(x=start_list_x, y=this_row, s=unicode_section_headers + 'Main Hand ')
        this_row += 2
        slot = 1
        cooldown_string_x = start_list_x + 1
        name_string_x = start_list_x + 4
        range_string_x = start_list_x + 31
        for _ in range(3):

            slot_spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=self.gameworld, slot=slot,
                                                                                   player_entity=player_entity)

            spell_name, spell_range, spell_cooldown_value = SpellUtilities.get_spell_info_details(gameworld=self.gameworld, spell_entity=slot_spell_entity)

            if spell_cooldown_value > 0:
                cooldown_colour = unicode_cooldown_enabled
            else:
                spell_cooldown_value = 0
                cooldown_colour = unicode_cooldown_disabled

            cooldown_string = cooldown_colour + ' ' + str(spell_cooldown_value)
            name_string = unicode_white_colour + spell_name
            range_string = unicode_white_colour + str(spell_range)

            terminal.printf(x=start_list_x, y=this_row, s=chr(this_letter))

            terminal.printf(x=cooldown_string_x, y=this_row, s=cooldown_string)
            terminal.printf(x=name_string_x, y=this_row, s=name_string)
            terminal.printf(x=range_string_x, y=this_row, s=range_string)
            this_row += 1
            this_letter += 1
            slot += 1

        this_row += 1
        terminal.printf(x=start_list_x, y=this_row, s=unicode_section_headers + 'Off Hand ')
        this_row += 2
        for _ in range(2):
            slot_spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=self.gameworld, slot=slot,
                                                                                   player_entity=player_entity)
            spell_name, spell_range, spell_cooldown_value = SpellUtilities.get_spell_info_details(gameworld=self.gameworld, spell_entity=slot_spell_entity)

            if spell_cooldown_value > 0:
                cooldown_colour = unicode_cooldown_enabled
            else:
                spell_cooldown_value = 0
                cooldown_colour = unicode_cooldown_disabled

            cooldown_string = cooldown_colour + ' ' + str(spell_cooldown_value)
            name_string = unicode_white_colour + spell_name
            range_string = unicode_white_colour + str(spell_range)

            terminal.printf(x=start_list_x, y=this_row, s=chr(this_letter))

            terminal.printf(x=cooldown_string_x, y=this_row, s=cooldown_string)
            terminal.printf(x=name_string_x, y=this_row, s=name_string)
            terminal.printf(x=range_string_x, y=this_row, s=range_string)
            this_row += 1
            this_letter += 1
            slot += 1

    def render_equipped_jewellery(self):

        player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=self.game_config)

        start_list_x = configUtilities.get_config_value_as_integer(configfile=self.game_config, section='spellinfo',
                                                                   parameter='START_LIST_X')

        this_row = configUtilities.get_config_value_as_integer(configfile=self.game_config, section='spellinfo',
                                                               parameter='JEWELLERY_SPELL_Y')
        unicode_section_headers = '[font=dungeon][color=SPELLINFO_ITEM_EQUIPPED]'

        this_letter = 70
        terminal.printf(x=start_list_x, y=this_row, s=unicode_section_headers + 'Jewellery')
        this_row += 2

        equipped_jewellery = MobileUtilities.get_jewellery_already_equipped(gameworld=self.gameworld, mobile=player_entity)
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


    @staticmethod
    def render_health(self, game_config):
        player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=game_config)
        health_start_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                            parameter='ENERGY_BARS_START_X')

        health_start_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                            parameter='ENERGY_BARS_START_Y')

        ascii_prefix = 'ASCII_SINGLE_'

        health_lost_fill = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'HEALTH_LOST')
        health_remiaing_fill = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'HEALTH_REMAINING')

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



    @staticmethod
    def render_mana(self, game_config):

        player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=game_config)
        mana_start_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                            parameter='ENERGY_BARS_START_X')

        mana_start_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                            parameter='ENERGY_BARS_START_Y') + 2

        ascii_prefix = 'ASCII_SINGLE_'

        mana_lost_fill = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'HEALTH_LOST')
        mana_remiaing_fill = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'HEALTH_REMAINING')

        unicode_mechanic_mana_lost = '[font=dungeon][color=ENERGY_MANA_LOST]['
        unicode_mechanic_mana_remaining = '[font=dungeon][color=ENERGY_MANA_REMAINING]['

        current_mana_value = MobileUtilities.get_mobile_derived_current_mana(gameworld=self.gameworld, entity=player_entity)
        max_mana_value = MobileUtilities.get_mobile_derived_maximum_mana(gameworld=self.gameworld, entity=player_entity)

        mana_split = formulas.calculate_percentage(low_number=current_mana_value, max_number=max_mana_value)

        # draw full lost mana bar
        terminal.printf(x=mana_start_x, y=mana_start_y, s="Mana ")
        for x in range(10):
            terminal.printf(x=(mana_start_x + 5) + x, y=mana_start_y,
                            s=unicode_mechanic_mana_lost + mana_lost_fill + ']')

        # now draw mana remaining on top of the above bar
        split_mana = int(mana_split / 10)
        for x in range(split_mana):
            terminal.printf(x=(mana_start_x + 5) + x, y=mana_start_y,
                            s=unicode_mechanic_mana_remaining + mana_remiaing_fill + ']')

    #
    # formally known as the F1 bar
    #
    def render_class_mechanics(self, game_config):
        plpayer_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=game_config)

        mechanic_start_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                            parameter='MECHANIC_START_X')

        mechanic_start_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                            parameter='MECHANIC_START_Y')

        ascii_prefix = 'ASCII_SINGLE_'

        mechanic_info_top_left_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                      parameter=ascii_prefix + 'TOP_LEFT')

        mechanic_info_bottom_left_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                         parameter=ascii_prefix + 'BOTTOM_LEFT')

        mechanic_info_top_right_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                       parameter=ascii_prefix + 'TOP_RIGHT')

        mechanic_info_bottom_right_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                          parameter=ascii_prefix + 'BOTTOM_RIGHT')

        mechanic_info_horizontal = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                 parameter=ascii_prefix + 'HORIZONTAL')
        mechanic_info_vertical = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                               parameter=ascii_prefix + 'VERTICAL')

        mechanic_ascii_one = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'ONE')
        mechanic_ascii_two = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'TWO')
        mechanic_ascii_three = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'THREE')
        mechanic_ascii_four = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'FOUR')
        mechanic_background_fill = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'MECHANIC_FILL')
        mechanic_f_key = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'MECHANIC_F')

        mechanic_depth = 1
        mechanic_width = 5
        unicode_mechanic_frame_enabled = '[font=dungeon][color=CLASS_MECHANIC_FRAME_COLOUR]['
        unicode_mechanic_id = '[font=dungeon][color=CLASS_MECHANIC_DISABLED]['
        unicode_mechanic_partial = '[font=dungeon][color=CLASS_MECHANIC_PARTIAL]['

        for loop in range (4):
            unicode_mechanic_frame = unicode_mechanic_id if loop < 2 else unicode_mechanic_frame_enabled
            # verticals
            for d in range(mechanic_depth):
                terminal.printf(x=mechanic_start_x, y=(mechanic_start_y + 1) + d,
                                s=unicode_mechanic_frame + mechanic_info_vertical + ']')

                terminal.printf(x=(mechanic_start_x + mechanic_width) + 1, y=(mechanic_start_y + 1) + d,
                                s=unicode_mechanic_frame + mechanic_info_vertical + ']')

            # horizontal
            for a in range(mechanic_width):
                terminal.printf(x=(mechanic_start_x + a) + 1, y=mechanic_start_y,
                                s=unicode_mechanic_frame + mechanic_info_horizontal + ']')
                terminal.printf(x=(mechanic_start_x + a) + 1, y=((mechanic_start_y + mechanic_depth) + 1),
                                s=unicode_mechanic_frame + mechanic_info_horizontal + ']')

            # top left
            terminal.printf(x=mechanic_start_x, y=mechanic_start_y,
                            s=unicode_mechanic_frame + mechanic_info_top_left_corner + ']')
            # bottom left
            terminal.printf(x=mechanic_start_x, y=((mechanic_start_y + mechanic_depth) + 1),
                            s=unicode_mechanic_frame + mechanic_info_bottom_left_corner + ']')
            # top right
            terminal.printf(x=(mechanic_start_x + mechanic_width) + 1, y=mechanic_start_y,
                            s=unicode_mechanic_frame + mechanic_info_top_right_corner + ']')
            # bottom right
            terminal.printf(x=(mechanic_start_x + mechanic_width) + 1, y=((mechanic_start_y + mechanic_depth) + 1),
                            s=unicode_mechanic_frame + mechanic_info_bottom_right_corner + ']')

            # mechanic partially filled - measured in 20% blocks
            xx = random.randrange(1, 4)
            for zz in range(xx):
                terminal.printf(x=mechanic_start_x + 1 + zz, y=mechanic_start_y + 1, s=unicode_mechanic_partial + mechanic_background_fill + ']')

            # mechanic ID
            if loop == 0:
                mechanic_id = mechanic_ascii_one
            elif loop == 1:
                mechanic_id = mechanic_ascii_two
            elif loop == 2:
                mechanic_id = mechanic_ascii_three
            else:
                mechanic_id = mechanic_ascii_four

            terminal.printf(x=mechanic_start_x + 3, y=mechanic_start_y + 3, s=unicode_mechanic_frame + mechanic_f_key + '][' + mechanic_id + ']')

            mechanic_start_x += 8

    def render_equipped_armour(self):
        player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=self.game_config)

        start_list_x = configUtilities.get_config_value_as_integer(configfile=self.game_config, section='spellinfo',
                                                                   parameter='START_LIST_X')

        this_row = configUtilities.get_config_value_as_integer(configfile=self.game_config, section='spellinfo',
                                                               parameter='ARMOUR_SPELL_Y')
        unicode_section_headers = '[font=dungeon][color=SPELLINFO_ITEM_EQUIPPED]'
        unicode_cooldown_disabled = '[font=dungeon][color=SPELLINFO_COOLDOWN_DISABLED]'
        unicode_cooldown_enabled = '[font=dungeon][color=SPELLINFO_COOLDOWN_ACTIVE]'
        unicode_white_colour = '[font=dungeon][color=SPELLINFO_HOTKEY_ACTIVE]'

        this_letter = 65
        slot = 1
        cooldown_string_x = start_list_x + 1
        name_string_x = start_list_x + 4
        range_string_x = start_list_x + 31

        terminal.printf(x=start_list_x, y=this_row, s=unicode_section_headers + 'Armour ')
        this_row += 2

        items = get_head_armour_details(gameworld=self.gameworld, entity_id=player_entity)
        if len(items) == 1:
            str_to_print = items[0]
        else:
            str_to_print = items[0] + items[2]

        terminal.print_(x=start_list_x, y=this_row, s=chr(this_letter) + ' ' + str_to_print)
        this_row += 1
        this_letter += 1
        items = get_chest_armour_details(gameworld=self.gameworld, entity_id=player_entity)
        if len(items) == 1:
            str_to_print = items[0]
        else:
            str_to_print = items[0] + items[2]

        terminal.print_(x=start_list_x, y=this_row, s=chr(this_letter) + ' ' + str_to_print)
        this_row += 1
        this_letter += 1

        items = get_hands_armour_details(gameworld=self.gameworld, entity_id=player_entity)
        if len(items) == 1:
            str_to_print = items[0]
        else:
            str_to_print = items[0] + items[2]

        terminal.print_(x=start_list_x, y=this_row, s=chr(this_letter) + ' ' + str_to_print)
        this_row += 1
        this_letter += 1

        items = get_legs_armour_details(gameworld=self.gameworld, entity_id=player_entity)
        if len(items) == 1:
            str_to_print = items[0]
        else:
            str_to_print = items[0] + items[2]
        terminal.print_(x=start_list_x, y=this_row, s=chr(this_letter) + ' ' + str_to_print)
        this_row += 1
        this_letter += 1

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
        unicode_section_headers = '[font=dungeon][color=SPELLINFO_ITEM_EQUIPPED]'
        unicode_cooldown_disabled = '[font=dungeon][color=SPELLINFO_COOLDOWN_DISABLED]'
        unicode_cooldown_enabled = '[font=dungeon][color=SPELLINFO_COOLDOWN_ACTIVE]'
        unicode_white_colour = '[font=dungeon][color=SPELLINFO_HOTKEY_ACTIVE]'
        cooldown_string_x = start_list_x + 1
        name_string_x = start_list_x + 4
        range_string_x = start_list_x + 31

        this_letter = 55
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
                range_string = unicode_white_colour + str(spell_range)

                terminal.printf(x=cooldown_string_x, y=this_row, s=cooldown_string)
                terminal.printf(x=range_string_x, y=this_row, s=range_string)
            terminal.printf(x=start_list_x, y=this_row, s=chr(this_letter))
            terminal.printf(x=name_string_x, y=this_row, s=name_string)
            this_row += 1
            this_letter += 1
            slot += 1

    def render_spell_bar(self):
        player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=self.game_config)
        start_list_x = configUtilities.get_config_value_as_integer(configfile=self.game_config, section='spellinfo',
                                                                   parameter='START_LIST_X')

        this_row = configUtilities.get_config_value_as_integer(configfile=self.game_config, section='spellinfo',
                                                                   parameter='HEALING_SPELL_Y')
        unicode_section_headers = '[font=dungeon][color=SPELLINFO_ITEM_EQUIPPED]'
        unicode_cooldown_disabled = '[font=dungeon][color=SPELLINFO_COOLDOWN_DISABLED]'
        unicode_cooldown_enabled = '[font=dungeon][color=SPELLINFO_COOLDOWN_ACTIVE]'
        unicode_white_colour = '[font=dungeon][color=SPELLINFO_HOTKEY_ACTIVE]'
        cooldown_string_x = start_list_x + 1
        name_string_x = start_list_x + 4
        range_string_x = start_list_x + 31

        this_letter = 54
        terminal.printf(x=start_list_x, y=this_row, s=unicode_section_headers + 'Healing ')
        this_row += 2
        # spell name
        slot_spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=self.gameworld, slot=6,
                                                                               player_entity=player_entity)
        spell_name = SpellUtilities.get_spell_name(gameworld=self.gameworld, spell_entity=slot_spell_entity)
        # spell range
        if world.check_if_entity_has_component(gameworld=self.gameworld, entity=slot_spell_entity, component=spells.MaxRange):
            spell_range = SpellUtilities.get_spell_max_range(gameworld=self.gameworld, spell_entity=slot_spell_entity)
        else:
            spell_range = '-'
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
        range_string = unicode_white_colour + str(spell_range)

        terminal.printf(x=start_list_x, y=this_row, s=chr(this_letter))

        terminal.printf(x=cooldown_string_x, y=this_row, s=cooldown_string)
        terminal.printf(x=name_string_x, y=this_row, s=name_string)
        terminal.printf(x=range_string_x, y=this_row, s=range_string)
        this_row += 1
        this_letter += 1
        this_row += 1



        #
        # this_row = 45
        # terminal.printf(x=start_list_x, y=this_row, s='p')
        # this_row += 1
        # terminal.printf(x=start_list_x, y=this_row, s='b')
        # this_row += 1
        # for _ in range(10):
        #     terminal.printf(x=start_list_x, y=this_row, s='b1b')
        #     terminal.printf(x=start_list_x + 6, y=this_row, s='b2b')
        #     terminal.printf(x=start_list_x + 14, y=this_row, s='b3b')
        #     terminal.printf(x=start_list_x + 22, y=this_row, s='b4b')
        #
        #     this_row += 1
        #
        # terminal.printf(x=start_list_x, y=this_row, s='b')
        # this_row += 1
        # terminal.printf(x=start_list_x, y=this_row, s='p')