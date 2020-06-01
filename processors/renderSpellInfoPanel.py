import esper
from bearlibterminal import terminal

from utilities import configUtilities, formulas
from utilities.common import CommonUtils
from utilities.mobileHelp import MobileUtilities
from utilities.spellHelp import SpellUtilities


class RenderSpellInfoPanel(esper.Processor):
    def __init__(self, gameworld):
        self.gameworld = gameworld

    def process(self, game_config):
        self.render_spell_infobox()
        # self.render_player_status_effects(game_config=game_config)
        # self.render_spell_info_panel(game_config=game_config)
        # self.render_player_vitals(game_config=game_config)

    def render_player_status_effects(self, game_config):
        image_y_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='map_Yscale')

        statusbox_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                       parameter='STATUSBOX_HEIGHT')

        player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=game_config)
        player_boons = MobileUtilities.get_current_boons_applied_to_mobile(gameworld=self.gameworld,
                                                                           entity=player_entity)
        player_conditions = MobileUtilities.get_current_condis_applied_to_mobile(gameworld=self.gameworld,
                                                                                 entity=player_entity)

        self.render_boons(posx=1, posy=statusbox_height * image_y_scale, list_of_boons=player_boons)
        self.render_conditions(posx=11, posy=statusbox_height * image_y_scale,
                               list_of_conditions=player_conditions)

    @staticmethod
    def render_boons(posx, posy, list_of_boons):
        image_count = 0
        image_scale_factor = 2

        for boon in list_of_boons:
            boon_image_id = int(boon['image'])
            terminal.put(x=(posx + image_count) * image_scale_factor, y=posy, c=0xE600 + boon_image_id)
            image_count += 1

    @staticmethod
    def render_conditions(posx, posy, list_of_conditions):

        image_count = 0
        image_scale_factor = 2

        for condition in list_of_conditions:
            condition_image_id = int(condition['image'])
            terminal.put(x=(posx + image_count) * image_scale_factor, y=posy, c=0xE630 + condition_image_id)
            image_count += 1

    @staticmethod
    def render_spell_infobox():

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
        spell_info_top_left_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'TOP_LEFT')

        spell_info_bottom_left_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                        parameter=ascii_prefix + 'BOTTOM_LEFT')

        spell_info_top_right_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                      parameter=ascii_prefix + 'TOP_RIGHT')

        spell_info_bottom_right_corner = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                                         parameter=ascii_prefix + 'BOTTOM_RIGHT')

        spell_info_horizontal = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'HORIZONTAL')
        spell_info_vertical = CommonUtils.get_ascii_to_unicode(game_config=game_config, parameter=ascii_prefix + 'VERTICAL')

        # render horizontal bottom
        for z in range(spell_infobox_start_x, (spell_infobox_start_x + spell_infobox_width)):
            terminal.printf(x=z, y=(spell_infobox_start_y + spell_infobox_height), s=unicode_string_to_print + spell_info_horizontal + ']')
            terminal.printf(x=z, y=spell_infobox_start_y, s=unicode_string_to_print + spell_info_horizontal + ']')

        # render verticals
        for z in range(spell_infobox_start_y, (spell_infobox_start_y + spell_infobox_height) - 1):
            terminal.printf(x=spell_infobox_start_x, y=z + 1, s=unicode_string_to_print + spell_info_vertical + ']')
            terminal.printf(x=(spell_infobox_start_x + spell_infobox_width), y=z + 1, s=unicode_string_to_print + spell_info_vertical + ']')


        # top left
        terminal.printf(x=spell_infobox_start_x, y=spell_infobox_start_y, s=unicode_string_to_print + spell_info_top_left_corner + ']')
        # bottom left
        terminal.printf(x=spell_infobox_start_x, y=(spell_infobox_start_y + spell_infobox_height), s=unicode_string_to_print + spell_info_bottom_left_corner + ']')
        # top right
        terminal.printf(x=(spell_infobox_start_x + spell_infobox_width), y=spell_infobox_start_y, s=unicode_string_to_print + spell_info_top_right_corner + ']')
        # bottom right
        terminal.printf(x=(spell_infobox_start_x + spell_infobox_width), y=(spell_infobox_start_y + spell_infobox_height), s=unicode_string_to_print + spell_info_bottom_right_corner + ']')

    def render_spell_info_panel(self, game_config):
        image_y_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='map_Yscale')
        statusbox_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                       parameter='STATUSBOX_HEIGHT')
        player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=game_config)

        ac = 1
        sc = 5
        y = statusbox_height + 1

        # spell bar slots are drawn first
        for a in range(10):
            terminal.put(x=(ac + a) * sc, y=y * image_y_scale, c=0xE500 + 0)
        # now the spells based on the spell bar entities -- currently loads slots 1 - 6
        slotid = 1
        for spell_slot in range(6):
            SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=self.gameworld, slot=slotid,
                                                               player_entity=player_entity)
            spell_image = 0

            terminal.put(x=(ac + spell_slot) * sc, y=y * image_y_scale, c=0xE400 + spell_image)
            slotid += 1

        # and finally the utility spells

    def render_player_vitals(self, game_config):

        self.render_health(game_config=game_config)
        self.render_mana(game_config=game_config)
        self.render_special_power(game_config=game_config)

    def render_health(self, game_config):

        statusbox_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                       parameter='STATUSBOX_HEIGHT')

        player_entity = MobileUtilities.get_player_entity(self.gameworld, game_config)
        current_health = MobileUtilities.get_mobile_derived_current_health(gameworld=self.gameworld,
                                                                           entity=player_entity)
        maximum_health = MobileUtilities.get_mobile_derived_maximum_health(gameworld=self.gameworld,
                                                                           entity=player_entity)

        str_to_print = "[color=red]Health[/color]"

        self.render_bar(print_string=str_to_print, low_number=current_health, high_number=maximum_health,
                        posy=statusbox_height + 3, posx=6, sprite_ref=0xE770, game_config=game_config)

    def render_mana(self, game_config):

        statusbox_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                       parameter='STATUSBOX_HEIGHT')

        player_entity = MobileUtilities.get_player_entity(self.gameworld, game_config)
        current_mana = MobileUtilities.get_mobile_derived_current_mana(gameworld=self.gameworld, entity=player_entity)
        max_mana = MobileUtilities.get_mobile_derived_maximum_mana(gameworld=self.gameworld, entity=player_entity)
        str_to_print = "[color=blue]Mana[/color]"

        self.render_bar(print_string=str_to_print, low_number=current_mana, high_number=max_mana,
                        posy=statusbox_height + 4, posx=6, sprite_ref=0xE800, game_config=game_config)

    def render_special_power(self, game_config):

        statusbox_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                       parameter='STATUSBOX_HEIGHT')

        player_entity = MobileUtilities.get_player_entity(self.gameworld, game_config)
        current_f1_power = MobileUtilities.get_mobile_derived_special_bar_current_value(gameworld=self.gameworld,
                                                                                        entity=player_entity)
        max_f1_power = MobileUtilities.get_mobile_derived_special_bar_max_value(gameworld=self.gameworld,
                                                                                entity=player_entity)

        str_to_print = "[color=green]Power[/color]"

        self.render_bar(print_string=str_to_print, low_number=current_f1_power, high_number=max_f1_power,
                        posy=statusbox_height + 5, posx=6, sprite_ref=0xE880, game_config=game_config)

    @staticmethod
    def render_bar(print_string, low_number, high_number, posy, posx, sprite_ref, game_config):

        image_y_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='map_Yscale')
        image_x_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='map_Xscale')

        display_percentage = formulas.calculate_percentage(low_number, high_number)
        tens = int(display_percentage / 10)
        units = display_percentage % 10
        px = 0

        if print_string != "":
            terminal.printf(4, posy * image_y_scale, print_string)

        for a in range(tens):
            terminal.put(x=(a + posx) * image_x_scale, y=posy * image_y_scale, c=sprite_ref + 0)
            px += 1

        if units > 0:
            if units < 5:
                terminal.put(x=(px + posx) * image_x_scale, y=posy * image_y_scale, c=sprite_ref + 3)

            if units == 5:
                terminal.put(x=(px + posx) * image_x_scale, y=posy * image_y_scale, c=sprite_ref + 2)

            if units > 5:
                terminal.put(x=(px + posx) * image_x_scale, y=posy * image_y_scale, c=sprite_ref + 1)
