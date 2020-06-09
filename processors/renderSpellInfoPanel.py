import esper
from bearlibterminal import terminal

from utilities import configUtilities
from utilities.common import CommonUtils
from utilities.display import set_both_hands_weapon_string_es, set_main_hand_weapon_string_es, \
    set_off_hand_weapon_string_es, set_jewellery_left_ear_string, set_jewellery_right_ear_string, \
    set_jewellery_left_hand_string, set_jewellery_right_hand_string, set_jewellery_neck_string, get_head_armour_details, \
    get_chest_armour_details, get_hands_armour_details, get_legs_armour_details, get_feet_armour_details
from utilities.itemsHelp import ItemUtilities
from utilities.mobileHelp import MobileUtilities
from utilities.spellHelp import SpellUtilities


class RenderSpellInfoPanel(esper.Processor):
    def __init__(self, gameworld):
        self.gameworld = gameworld
        self.game_config = configUtilities.load_config()

    def process(self, game_config):
        self.render_spell_info_outer_frame()
        self.render_equipped_items()
        self.render_energy_bars()
        self.render_player_status_effects(game_config=game_config)
        self.render_class_mechanics()
        self.render_spell_bar()

    def render_player_status_effects(self, game_config):

        player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=game_config)
        player_boons = MobileUtilities.get_current_boons_applied_to_mobile(gameworld=self.gameworld,
                                                                           entity=player_entity)
        player_conditions = MobileUtilities.get_current_condis_applied_to_mobile(gameworld=self.gameworld,
                                                                                 entity=player_entity)

        self.render_boons(list_of_boons=player_boons)
        self.render_conditions(list_of_conditions=player_conditions)

    def render_equipped_items(self):
        self.render_equipped_weapons(gameworld=self.gameworld, game_config=self.game_config)
        self.render_equipped_jewellery(gameworld=self.gameworld, game_config=self.game_config)
        self.render_equipped_armour(gameworld=self.gameworld, game_config=self.game_config)

    def render_energy_bars(self):
        self.render_health()
        self.render_mana()

    @staticmethod
    def render_boons(list_of_boons):

        for boon in list_of_boons:
            pass

    @staticmethod
    def render_conditions(list_of_conditions):

        for condition in list_of_conditions:
            pass

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

    @staticmethod
    def render_equipped_weapons(gameworld,game_config):

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
    def render_equipped_jewellery(gameworld,game_config):
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
    def render_health():
        return True

    @staticmethod
    def render_mana():
        return True

    #
    # formally known as the F1 bar
    #
    def render_class_mechanics(self):
        return True

    @staticmethod
    def render_equipped_armour(gameworld, game_config):
        plpayer_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
        spell_infobox_start_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                            parameter='SI_START_X')

        spell_infobox_start_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                            parameter='SI_START_Y')

        # title bar
        terminal.printf(x=spell_infobox_start_x + 60, y=spell_infobox_start_y + 1, s='Armour')

        items = get_head_armour_details(gameworld=gameworld, entity_id=plpayer_entity)
        if len(items) == 1:
            str_to_print = items[0]
        else:
            str_to_print = items[0] + items[2]
        terminal.print_(x=spell_infobox_start_x + 60, y=spell_infobox_start_y + 2, s=str_to_print)

        items = get_chest_armour_details(gameworld=gameworld, entity_id=plpayer_entity)
        if len(items) == 1:
            str_to_print = items[0]
        else:
            str_to_print = items[0] + items[2]

        terminal.print_(x=spell_infobox_start_x + 60, y=spell_infobox_start_y + 3, s=str_to_print)

        items = get_hands_armour_details(gameworld=gameworld, entity_id=plpayer_entity)
        if len(items) == 1:
            str_to_print = items[0]
        else:
            str_to_print = items[0] + items[2]

        terminal.print_(x=spell_infobox_start_x + 60, y=spell_infobox_start_y + 4, s=str_to_print)

        items = get_legs_armour_details(gameworld=gameworld, entity_id=plpayer_entity)
        if len(items) == 1:
            str_to_print = items[0]
        else:
            str_to_print = items[0] + items[2]

        terminal.print_(x=spell_infobox_start_x + 60, y=spell_infobox_start_y + 5, s=str_to_print)

        items = get_feet_armour_details(gameworld=gameworld, entity_id=plpayer_entity)
        if len(items) == 1:
            str_to_print = items[0]
        else:
            str_to_print = items[0] + items[2]
        terminal.print_(x=spell_infobox_start_x + 60, y=spell_infobox_start_y + 6, s=str_to_print)

    def render_spell_bar(self):
        return True
