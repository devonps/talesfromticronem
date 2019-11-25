import esper
import tcod

from bearlibterminal import terminal

from components import mobiles, items
from utilities import configUtilities, colourUtilities
from utilities.display import draw_simple_frame
from utilities.itemsHelp import ItemUtilities
from utilities.mobileHelp import MobileUtilities
from utilities.spellHelp import SpellUtilities
from loguru import logger
from mapRelated.gameMap import RenderLayer


class RenderGameMap(esper.Processor):
    def __init__(self, game_map, gameworld, camera):
        self.game_map = game_map
        self.gameworld = gameworld
        self.camera = camera

    def process(self, game_config):
        """
        Rendering during actual gameplay

        Render Order:
        1. game map                 dungeon floors, walls, furniture, spell effects??
        2. Entities                 player, enemies, items, etc
        3. HUD                      hp, mana, f1 bars, hotkeys, etc
        4. Spellbar                 spell bar
        5. Player status effects    effects player is suffering from

        """
        terminal.clear()
        # GUI viewport and message box borders
        # self.render_viewport(game_config)
        # self.render_message_box(self.con, game_config, self.gameworld)
        self.render_spell_bar(self)
        # self.render_player_status_effects(self, game_config)
        # self.render_player_vitals(self, self.con, game_config)

        # render the game map
        self.render_map(self.gameworld, game_config, self.game_map, self.camera)

        # draw the entities
        # self.render_items(game_config, self.gameworld)
        self.render_entities(game_config, self.gameworld)

        # blit the console
        terminal.refresh()

    @staticmethod
    def render_map(gameworld, game_config, game_map, camera):

        image_x_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='map_Xscale')
        image_y_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='map_Yscale')

        offset = 1

        player_has_moved = MobileUtilities.has_player_moved(gameworld, game_config)
        player_entity = MobileUtilities.get_player_entity(gameworld, game_config)
        # where is the player in terms of the game map
        playerx, playery = MobileUtilities.get_mobile_current_location(gameworld=gameworld, mobile=player_entity)

        camera_moved = camera.move_camera(playerx, playery, game_map)
        if camera_moved:
            # this is a hard hack - but it works
            # need to look at erasing
            terminal.clear()
        logger.info('camera newx/newy {}/{}', camera.topleft_x, camera.topleft_y)
        # draw what the camera can see
        for y in range(camera.height):
            for x in range(camera.width):
                map_x, map_y = camera.topleft_x + x, camera.topleft_y + y
                if (0 <= map_x < game_map.width) and (0 <= map_y < game_map.height):
                    image = game_map.tiles[map_x][map_y].image
                    tile = game_map.tiles[map_x][map_y].type_of_tile
                    if 0 < tile < 11:
                        terminal.put(x=(map_x + offset) * image_x_scale, y=(map_y + offset) * image_y_scale, c=0xE300 + image)

    @staticmethod
    def render_entities(game_config, gameworld):
        map_view_across = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MAP_VIEW_DRAW_X')
        map_view_down = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MAP_VIEW_DRAW_Y')
        image_x_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='map_Xscale')
        image_y_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='map_Yscale')

        for ent, (rend, pos, desc) in gameworld.get_components(mobiles.Renderable, mobiles.Position, mobiles.Describable):
            if rend.isVisible:
                draw_pos_x = map_view_across + pos.x
                draw_pos_y = map_view_down + pos.y
                RenderGameMap.render_entity(draw_pos_x, draw_pos_y, desc.image, image_x_scale, image_y_scale)

    @staticmethod
    def render_items(game_config, gameworld):
        map_view_across = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MAP_VIEW_DRAW_X')
        map_view_down = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MAP_VIEW_DRAW_Y')

        for ent, (rend, loc, desc) in gameworld.get_components(items.RenderItem, items.Location, items.Describable):
            if rend.isTrue:
                draw_pos_x = map_view_across + loc.x
                draw_pos_y = map_view_down + loc.y
                RenderGameMap.render_entity(draw_pos_x, draw_pos_y, desc.glyph, desc.fg, desc.bg)

    @staticmethod
    def render_entity(posx, posy, glyph, image_x_scale, image_y_scale):
        cloak = 21
        robe = 22
        shoes = 23
        weapon = 24
        logger.info('at map x/y {}/{}', posx, posy)
        characterbits = [cloak, glyph, robe, shoes, weapon]

        for cell in characterbits:
            terminal.put(x=posx * image_x_scale, y=posy * image_y_scale, c=0xE300 + cell)

    @staticmethod
    def render_viewport(game_config):
        # draw the outer bounds of the map viewport

        viewport_across = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='VIEWPORT_START_X')
        viewport_down = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='VIEWPORT_START_Y')
        viewport_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                     parameter='VIEWPORT_WIDTH')
        viewport_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='VIEWPORT_HEIGHT')
        draw_simple_frame(startx=viewport_across, starty=viewport_down, width=viewport_width, height=viewport_height, title='', fg=colourUtilities.get('YELLOW1'), bg=None)

    @staticmethod
    def render_message_box(con, game_config, gameworld):
        msg_start_across = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MSG_PANEL_START_X')
        msg_start_down = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MSG_PANEL_START_Y')
        msg_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MSG_PANEL_WIDTH')
        msg_depth = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MSG_PANEL_DEPTH')

        # draw the message box area
        con.draw_frame(
            x=msg_start_across,
            y=msg_start_down,
            width=msg_width,
            height=msg_depth,
            title='',
            clear=False,
            fg=tcod.yellow,
            bg_blend=tcod.BKGND_DEFAULT
        )

    @staticmethod
    def render_player_status_effects(self, game_config):
        # draw the boon, condition, and control bar borders (horizontal)
        self.render_boons(self, game_config)
        self.render_conditions(self, game_config)
        self.render_controls(self, game_config)

    @staticmethod
    def render_boons(self, game_config):
        self.render_h_bar(posy=0, border_colour=colourUtilities.get('GRAY'), game_config=game_config)
        self.render_player_status_effects_content(self, 0, '*', colourUtilities.get('GREEN'), game_config)

    @staticmethod
    def render_conditions(self, game_config):
        self.render_h_bar(posy=3, border_colour=colourUtilities.get('GRAY'), game_config=game_config)
        self.render_player_status_effects_content(self, 3, chr(9), colourUtilities.get('RED'), game_config)

    @staticmethod
    def render_controls(self, game_config):
        self.render_h_bar(posy=6, border_colour=colourUtilities.get('GRAY'), game_config=game_config)
        self.render_player_status_effects_content(self, 6, chr(10), colourUtilities.get('WHITE'), game_config)

    @staticmethod
    def render_player_status_effects_content(self, posy, glyph, foreground, game_config):
        px = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='H_BAR_X')
        py = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='H_BAR_Y') + posy

        x = 0
        bg = colourUtilities.get('BLACK')
        fg1 = foreground
        fg2 = colourUtilities.get('GRAY')
        for a in range(10):
            self.render_entity(1 + px + x, py + 1, glyph, fg1, bg)
            if a < 9:
                x += 1
                self.render_entity(1 + px + x, py + 1, '*', fg2, bg)
            x += 1

    @staticmethod
    def render_h_bar(posy, border_colour, game_config):

        px = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='H_BAR_X')
        py = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='H_BAR_Y')
        rs = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='BCC_BAR_RIGHT_SIDE')

        draw_simple_frame(startx=px, starty=py + posy, width=rs, height=3, title='', fg=border_colour, bg=None)
        # con.draw_frame(
        #     x=px,
        #     y=py + posy,
        #     width=rs,
        #     height=3,
        #     title='',
        #     fg=border_colour,
        #     bg_blend=tcod.BKGND_DEFAULT
        # )

    @staticmethod
    def render_player_vitals(self, game_config):
        player_entity = MobileUtilities.get_player_entity(self.gameworld, game_config)
        player_derived_attributes_component = self.gameworld.component_for_entity(player_entity,
                                                                                  mobiles.DerivedAttributes)

        self.render_health_bar(self, player_derived_attributes_component, game_config)
        self.render_mana_bar(self, player_entity, game_config)

        self.render_f1_bar(self, player_entity, game_config)

    @staticmethod
    def render_health_bar(self, player_derived_attributes_component, game_config):

        px = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='HEALTH_BAR_X')
        py = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='HEALTH_BAR_Y')
        wd = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='HEALTH_BAR_W')
        current_health = player_derived_attributes_component.currentHealth
        maximum_health = player_derived_attributes_component.maximumHealth
        current_health_percentage = MobileUtilities.get_number_as_a_percentage(current_health, maximum_health)

        self.con.draw_frame(x=px, y=py, width=wd, height=3, title='', fg=colourUtilities.WHITE, bg_blend=tcod.BKGND_DEFAULT)

        bar_count = int(MobileUtilities.get_bar_count(current_health_percentage, wd - 2))

        hlth = px + 1

        for x in range(bar_count):
            self.con.print(x=hlth + x, y=py + 1, string=chr(219), fg=colourUtilities.WHITE, bg=colourUtilities.RED)

        health = str(current_health) + ' / ' + str(maximum_health)
        self.con.print(x=int(wd/2), y=py + 1, string=health, fg=colourUtilities.WHITE, bg_blend=tcod.BKGND_SET)


    @staticmethod
    def render_mana_bar(self, player_entity, game_config):

        px = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MANA_BAR_X')
        py = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MANA_BAR_Y')
        wd = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MANA_BAR_W')
        player_current_mana = MobileUtilities.calculate_current_mana(self.gameworld, gameconfig=game_config)
        player_maximum_mana = MobileUtilities.get_derived_maximum_mana(self.gameworld, player_entity)

        current_mana_percentage = MobileUtilities.get_number_as_a_percentage(player_current_mana, player_maximum_mana)

        self.con.draw_frame(x=px, y=py, width=wd, height=3, title='', fg=colourUtilities.WHITE,
                            bg_blend=tcod.BKGND_DEFAULT)

        bar_count = int(MobileUtilities.get_bar_count(current_mana_percentage, wd - 2))

        hlth = px + 1

        for x in range(bar_count):
            self.con.print(x=hlth + x, y=py + 1, string=chr(219), fg=colourUtilities.WHITE, bg=colourUtilities.BLUE)

        mana = str(player_current_mana) + ' / ' + str(player_maximum_mana)
        self.con.print(x=px + int(wd / 2), y=py + 1, string=mana, fg=colourUtilities.WHITE, bg_blend=tcod.BKGND_SET)

    @staticmethod
    def render_f1_bar(self, player_entity, game_config):
        px = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='F1_BAR_X')
        py = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='F1_BAR_Y')
        wd = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='F1_BAR_W')
        psc = MobileUtilities.get_derived_special_bar_current_value(self.gameworld, gameconfig=game_config)
        psm = MobileUtilities.get_derived_special_bar_max_value(self.gameworld, player_entity)

        current_special_percentage = MobileUtilities.get_number_as_a_percentage(psc, psm)

        self.con.draw_frame(x=px, y=py, width=wd, height=3, title='', fg=colourUtilities.WHITE, bg_blend=tcod.BKGND_DEFAULT)

        bar_count = int(MobileUtilities.get_bar_count(current_special_percentage, wd - 2))

        hlth = px + 1

        for x in range(bar_count):
            self.con.print(x=hlth + x, y=py + 1, string=chr(219), fg=colourUtilities.WHITE, bg=colourUtilities.GREEN)

        mana = str(psc) + ' / ' + str(psm)
        self.con.print(x=px + int(wd / 2), y=py + 1, string=mana, fg=colourUtilities.WHITE, bg_blend=tcod.BKGND_SET)


    @staticmethod
    def render_v_bar(con, posx, posy, depth, border_colour):
        con.draw_frame(
            x=posx,
            y=posy,
            width=3,
            height=depth,
            title='',
            fg=border_colour,
            bg_blend=tcod.BKGND_DEFAULT
        )

    @staticmethod
    def render_player_vertical_bar_content(self, x, current_value, foreground, background, game_config):

        px = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='V_BAR_X')
        posx = 1 + px + x
        py = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='V_BAR_Y')
        bar_depth = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='V_BAR_DEPTH')
        posy = py + bar_depth

        bar_count = int(MobileUtilities.get_bar_count(current_value, bar_depth))

        for y in range(bar_count):
            tcod.console_put_char_ex(self.con, posx, posy - y, chr(176), foreground, background)

    @staticmethod
    def render_spell_bar(self):

        game_config = configUtilities.load_config()

        spell_box_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='SPELL_BOX_WIDTH')
        spell_bar_across = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='SPELL_BOX_X')
        spell_bar_down = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='SPELL_BAR_Y')
        spell_bar_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='SPELL_BAR_WIDTH')
        spell_bar_depth = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='SPELL_BOX_DEPTH')
        spell_slots = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='SPELL_SLOTS')

        image_x_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='map_Xscale')
        image_y_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='map_Yscale')

        player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=game_config)
        weapons_list = MobileUtilities.get_weapons_equipped(gameworld=self.gameworld, entity=player_entity)
        main_weapon = weapons_list[0]
        off_weapon = weapons_list[1]
        both_weapon = weapons_list[2]
        slot = ['NO SPEL'] * 10

        ac = 4
        for a in range(4):

            terminal.put(x=ac +a * image_x_scale, y=28 * image_y_scale, c=0xE400 + a)

        terminal.put(x=37 * image_x_scale, y=28 * image_y_scale, c=0xE400 + 0)

        # if both_weapon > 0:
        #     slot[0] = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=self.gameworld, weapon_equipped=both_weapon, slotid=1)
        #     slot[1] = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=self.gameworld, weapon_equipped=both_weapon, slotid=2)
        #     slot[2] = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=self.gameworld, weapon_equipped=both_weapon, slotid=3)
        #     slot[3] = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=self.gameworld, weapon_equipped=both_weapon, slotid=4)
        #     slot[4] = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=self.gameworld, weapon_equipped=both_weapon, slotid=5)
        #
        # else:
        #     slot[0] = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=self.gameworld, weapon_equipped=main_weapon, slotid=1)
        #     slot[1] = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=self.gameworld, weapon_equipped=main_weapon, slotid=2)
        #     slot[2] = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=self.gameworld, weapon_equipped=main_weapon, slotid=3)
        #     slot[3] = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=self.gameworld, weapon_equipped=off_weapon, slotid=4)
        #     slot[4] = SpellUtilities.get_spell_name_in_weapon_slot(gameworld=self.gameworld, weapon_equipped=off_weapon, slotid=5)
        #
        # ps = 1
        # fg = colourUtilities.get('YELLOW1')
        # bg = colourUtilities.get('GRAY')
        # for spellSlot in range(spell_slots):
        #     spell_slot_posx = spell_bar_across - 1
        #
        #     if spellSlot < 9:
        #         sp = str(ps)
        #     else:
        #         sp = str(ps)[-1:]
        #
        #     display_coloured_box(title=sp,
        #                          posx=spell_slot_posx, posy=spell_bar_down + 1,
        #                          width=spell_box_width, height=spell_bar_depth,
        #                          fg=fg, bg=bg)
        #     string_to_print = '[color=' + fg + ']' + slot[spellSlot][:7]
        #     terminal.print_(x=spell_slot_posx + 2, y=spell_bar_down + 3, width=spell_bar_width, height=spell_bar_depth, s=string_to_print)
        #
        #     spell_bar_across += spell_box_width
        #     ps += 1
        #