import random

import esper
from bearlibterminal import terminal

from utilities import configUtilities, formulas
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
        # self.render_equipped_items()
        self.render_energy_bars(game_config=game_config)
        # self.render_class_mechanics(game_config=game_config)
        # self.render_spell_bar(game_config=game_config)
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
        minimal_display = configUtilities.get_config_value_as_string(configfile=self.game_config, section='spellinfo',
                                                                       parameter='MINIMAL_DISPLAY_ENABLED')
        if minimal_display != 'True':
            self.render_equipped_weapons(gameworld=self.gameworld, game_config=self.game_config)
            self.render_equipped_jewellery(gameworld=self.gameworld, game_config=self.game_config)
            self.render_equipped_armour(gameworld=self.gameworld, game_config=self.game_config)

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

        start_list_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                            parameter='START_LIST_X')

        start_list_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                            parameter='START_LIST_Y')
        z = 0
        for letter in range(26):
            terminal.printf(x=start_list_x, y=start_list_y + letter,
                            s=chr(65+letter) + ' 9 Glyph of Lesser Elementals 10')
            z+= 1
            if z == 5:
                start_list_y += 1
                z = 1

    @staticmethod
    def render_equipped_weapons(gameworld, game_config):

        plpayer_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
        spell_infobox_start_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                            parameter='SI_START_X')

        spell_infobox_start_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                            parameter='SI_START_Y')

        weapons_list = MobileUtilities.get_weapons_equipped(gameworld=gameworld, entity=plpayer_entity)

        both_hands = set_both_hands_weapon_string_es(gameworld=gameworld, both_weapon=weapons_list[2])
        main_hand = set_main_hand_weapon_string_es(main_weapon=weapons_list[0], gameworld=gameworld)
        off_hand = set_off_hand_weapon_string_es(off_weapon=weapons_list[1], gameworld=gameworld)

        # title bar
        terminal.printf(x=spell_infobox_start_x + 3, y=spell_infobox_start_y + 1, s='Weapons')

        terminal.print_(x=spell_infobox_start_x + 1, y=spell_infobox_start_y + 2, s=both_hands)
        terminal.print_(x=spell_infobox_start_x + 1, y=spell_infobox_start_y + 3, s=main_hand)
        terminal.print_(x=spell_infobox_start_x + 1, y=spell_infobox_start_y + 4, s=off_hand)

    @staticmethod
    def render_equipped_jewellery(gameworld, game_config):
        plpayer_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
        spell_infobox_start_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                            parameter='SI_START_X')

        spell_infobox_start_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                            parameter='SI_START_Y')

        equipped_jewellery = MobileUtilities.get_jewellery_already_equipped(gameworld=gameworld, mobile=plpayer_entity)
        left_ear = set_jewellery_left_ear_string(gameworld=gameworld, left_ear=equipped_jewellery[0])
        right_ear = set_jewellery_right_ear_string(gameworld=gameworld, right_ear=equipped_jewellery[1])
        left_hand = set_jewellery_left_hand_string(gameworld=gameworld, left_hand=equipped_jewellery[2])
        right_hand = set_jewellery_right_hand_string(gameworld=gameworld, right_hand=equipped_jewellery[3])
        neck = set_jewellery_neck_string(gameworld=gameworld, neck=equipped_jewellery[4])

        # title bar
        terminal.printf(x=spell_infobox_start_x + 3, y=spell_infobox_start_y + 7, s='Jewellery')

        terminal.print_(x=spell_infobox_start_x + 1, y=spell_infobox_start_y + 8, s=left_ear)
        terminal.print_(x=spell_infobox_start_x + 1, y=spell_infobox_start_y + 9, s=right_ear)
        terminal.print_(x=spell_infobox_start_x + 1, y=spell_infobox_start_y + 10, s=left_hand)
        terminal.print_(x=spell_infobox_start_x + 1, y=spell_infobox_start_y + 11, s=right_hand)
        terminal.print_(x=spell_infobox_start_x + 1, y=spell_infobox_start_y + 12, s=neck)

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

    @staticmethod
    def render_equipped_armour(gameworld, game_config):
        plpayer_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)

        spell_infobox_start_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                            parameter='SI_START_Y')

        armour_pos_x = 60
        # title bar
        terminal.printf(x=armour_pos_x + 5, y=spell_infobox_start_y + 1, s='Armour')

        items = get_head_armour_details(gameworld=gameworld, entity_id=plpayer_entity)
        if len(items) == 1:
            str_to_print = items[0]
        else:
            str_to_print = items[0] + items[2]
        terminal.print_(x=armour_pos_x, y=spell_infobox_start_y + 2, s=str_to_print)

        items = get_chest_armour_details(gameworld=gameworld, entity_id=plpayer_entity)
        if len(items) == 1:
            str_to_print = items[0]
        else:
            str_to_print = items[0] + items[2]

        terminal.print_(x=armour_pos_x, y=spell_infobox_start_y + 3, s=str_to_print)

        items = get_hands_armour_details(gameworld=gameworld, entity_id=plpayer_entity)
        if len(items) == 1:
            str_to_print = items[0]
        else:
            str_to_print = items[0] + items[2]

        terminal.print_(x=armour_pos_x, y=spell_infobox_start_y + 4, s=str_to_print)

        items = get_legs_armour_details(gameworld=gameworld, entity_id=plpayer_entity)
        if len(items) == 1:
            str_to_print = items[0]
        else:
            str_to_print = items[0] + items[2]

        terminal.print_(x=armour_pos_x, y=spell_infobox_start_y + 5, s=str_to_print)

        items = get_feet_armour_details(gameworld=gameworld, entity_id=plpayer_entity)
        if len(items) == 1:
            str_to_print = items[0]
        else:
            str_to_print = items[0] + items[2]
        terminal.print_(x=armour_pos_x, y=spell_infobox_start_y + 6, s=str_to_print)

    def render_spell_bar(self, game_config):

        plpayer_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=game_config)

        spell_infobox_start_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                            parameter='SI_START_X')

        spell_infobox_start_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                            parameter='SI_START_Y')

        ascii_prefix = 'ASCII_SINGLE_'

        spell_info_top_t_junction = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                     parameter=ascii_prefix + 'TOP_T_JUNCTION')

        spell_info_bottom_t_junction = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                        parameter=ascii_prefix + 'BOTTOM_T_JUNCTION')

        spell_info_bottom_left_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                         parameter=ascii_prefix + 'BOTTOM_LEFT')

        spell_info_bottom_right_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                          parameter=ascii_prefix + 'BOTTOM_RIGHT')

        spell_info_horizontal = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                 parameter=ascii_prefix + 'HORIZONTAL')
        spell_info_vertical = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                               parameter=ascii_prefix + 'VERTICAL')

        spell_ascii_one = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'ONE')
        spell_ascii_two = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'TWO')
        spell_ascii_three = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'THREE')
        spell_ascii_four = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'FOUR')
        spell_ascii_five = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'FIVE')
        spell_ascii_six = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'SIX')
        spell_ascii_seven = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'SEVEN')
        spell_ascii_eight = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'EIGHT')
        spell_ascii_nine = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'NINE')
        spell_ascii_zero = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'ZERO')

        spell_button_width = 5
        spell_button_depth = 3
        unicode_string_to_print = '[font=dungeon][color=SPELLINFO_FRAME_COLOUR]['
        unicode_cooldown_disabled = '[font=dungeon][color=SPELLINFO_COOLDOWN_DISABLED]['
        unicode_cooldown_enabled = '[font=dungeon][color=SPELLINFO_COOLDOWN_ACTIVE]['
        unicode_spell_hotkey_enabled = '[font=dungeon][color=SPELLINFO_HOTKEY_ACTIVE]['
        unicode_spell_hotkey_disabled = '[font=dungeon][color=SPELLINFO_HOTKEY_DISABLED]['

        spell_button_original_x = spell_infobox_start_x + 17

        spell_button_start_x = spell_button_original_x
        spell_button_end_y = (spell_infobox_start_y + spell_button_depth)
        spell_cooldown_counter_start_x = spell_button_start_x + 1

        cool_down_dict = {
            '0': spell_ascii_zero,
            '1': spell_ascii_one,
            '2': spell_ascii_two,
            '3': spell_ascii_three,
            '4': spell_ascii_four,
            '5': spell_ascii_five,
            '6': spell_ascii_six,
            '7': spell_ascii_seven,
            '8': spell_ascii_eight,
            '9': spell_ascii_nine
        }

        spell_on_cooldown = False
        slotid = 1
        for hotkey in range(10):

            # render horizontal bottom
            for z in range(spell_button_width):
                terminal.printf(x=spell_button_start_x + z, y=spell_button_end_y,
                                s=unicode_string_to_print + spell_info_horizontal + ']')

            # render verticals
            for zz in range(spell_button_depth - 1):
                terminal.printf(x=spell_button_start_x, y=(spell_infobox_start_y + 1) + zz,
                                s=unicode_string_to_print + spell_info_vertical + ']')
                terminal.printf(x=(spell_button_start_x + spell_button_width) - 1, y=(spell_infobox_start_y + 1) + zz,
                                s=unicode_string_to_print + spell_info_vertical + ']')

            # bottom left
            if hotkey == 0:
                terminal.printf(x=spell_button_start_x, y=spell_button_end_y,
                                s=unicode_string_to_print + spell_info_bottom_left_corner + ']')

            # top t-junctions
            terminal.printf(x=spell_button_start_x, y=spell_infobox_start_y,
                            s=unicode_string_to_print + spell_info_top_t_junction + ']')

            # spell activation checks/display

            slot_spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=self.gameworld,
                                                                                   slot=slotid,
                                                                                   player_entity=plpayer_entity)
            if slot_spell_entity > 0:
                spell_on_cooldown = SpellUtilities.get_spell_cooldown_status(gameworld=self.gameworld,
                                                                             spell_entity=slot_spell_entity)

            # cooldown counter
            if spell_on_cooldown:
                spell_cooldown = unicode_cooldown_enabled
                spell_hotkey_print = unicode_spell_hotkey_disabled
                cooldown_value = SpellUtilities.get_spell_cooldown_remaining_turns(gameworld=self.gameworld,
                                                                        spell_entity=slot_spell_entity)
            else:
                spell_cooldown = unicode_cooldown_disabled
                spell_hotkey_print = unicode_spell_hotkey_enabled
                cooldown_value = 0

            cc = list(CommonUtils.format_number_as_string(base_number=cooldown_value, base_string='000'))

            down_cool = []

            for a in range(len(cc)):
                for key in cool_down_dict:
                    if key == cc[a]:
                        down_cool.append(cool_down_dict[key])

            terminal.printf(x=spell_cooldown_counter_start_x, y=spell_infobox_start_y + 1,
                            s=spell_cooldown + down_cool[0] + '][' + down_cool[1] + '][' + down_cool[2] + ']')

            # spell hotkey
            if hotkey == 0:
                spell_hotkey = spell_ascii_one
            elif hotkey == 1:
                spell_hotkey = spell_ascii_two
            elif hotkey == 2:
                spell_hotkey = spell_ascii_three
            elif hotkey == 3:
                spell_hotkey = spell_ascii_four
            elif hotkey == 4:
                spell_hotkey = spell_ascii_five
            elif hotkey == 5:
                spell_hotkey = spell_ascii_six
            elif hotkey == 6:
                spell_hotkey = spell_ascii_seven
            elif hotkey == 7:
                spell_hotkey = spell_ascii_eight
            elif hotkey == 8:
                spell_hotkey = spell_ascii_nine
            else:
                spell_hotkey = spell_ascii_zero

            terminal.printf(x=spell_button_start_x + 2, y=spell_infobox_start_y + 2,
                            s=spell_hotkey_print + spell_hotkey + ']')
            spell_button_start_x += 4
            spell_cooldown_counter_start_x += 4
            slotid += 1

            br = spell_button_original_x
            for xx in range(10):
                # bottom right
                if xx < 9:
                    bottom_corner = spell_info_bottom_t_junction
                else:
                    bottom_corner = spell_info_bottom_right_corner

                terminal.printf(x=(br + spell_button_width) - 1, y=spell_button_end_y,
                                s=unicode_string_to_print + bottom_corner + ']')
                terminal.printf(x=(br + spell_button_width) - 1, y=spell_infobox_start_y,
                                s=unicode_string_to_print + spell_info_top_t_junction + ']')

                br += 4
