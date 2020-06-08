import esper
from bearlibterminal import terminal

from utilities import configUtilities, formulas
from utilities.common import CommonUtils
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
        self.render_equipped_jewellery()
        self.render_equipped_armour()

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
        equipped_weapons = MobileUtilities.get_weapons_equipped(gameworld=gameworld, entity=plpayer_entity)
        print_col_no_item = "[color=SPELLINFO_NO_ITEM_EQUIPPED]"
        print_col_item = "[color=SPELLINFO_ITEM_EQUIPPED]"

        # title bar
        terminal.printf(x=spell_infobox_start_x + 3, y=spell_infobox_start_y + 1, s='Weapons')

        # main hand
        if equipped_weapons[0] == 0:
            str_to_print = print_col_no_item + "Main:"
        else:
            str_to_print = print_col_item + "Main:" + ItemUtilities.get_item_name(gameworld=gameworld, entity=equipped_weapons[0])
        terminal.printf(x=spell_infobox_start_x + 1, y=spell_infobox_start_y + 2, s=str_to_print)

        # off hand
        if equipped_weapons[1] == 0:
            str_to_print = print_col_no_item + "Off:"
        else:
            str_to_print = print_col_item + "Off:" + ItemUtilities.get_item_name(gameworld=gameworld, entity=equipped_weapons[1])
        terminal.printf(x=spell_infobox_start_x + 1, y=spell_infobox_start_y + 3, s=str_to_print)

        # both hands
        if equipped_weapons[2] == 0:
            str_to_print = print_col_no_item + "Both:"
        else:
            str_to_print = print_col_item + "Both:" + ItemUtilities.get_item_name(gameworld=gameworld, entity=equipped_weapons[2])
        terminal.printf(x=spell_infobox_start_x + 1, y=spell_infobox_start_y + 4, s=str_to_print)

    @staticmethod
    def render_equipped_jewellery():
        return True

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
    def render_equipped_armour():
        return True

    def render_spell_bar(self):
        return True
