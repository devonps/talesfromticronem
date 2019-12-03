import esper

from bearlibterminal import terminal

from components import mobiles, items
from utilities import configUtilities
from utilities.mobileHelp import MobileUtilities
from loguru import logger
from mapRelated.gameMap import RenderLayer


class RenderGameMap(esper.Processor):
    def __init__(self, game_map, gameworld):
        self.game_map = game_map
        self.gameworld = gameworld

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
        # render the game map
        self.render_map(self.gameworld, game_config, self.game_map)
        # draw the entities
        # self.render_items(game_config, self.gameworld)
        self.render_mobiles(game_config, self.gameworld)

        # GUI viewport
        # self.render_viewport(game_config)
        # self.render_message_box(self.con, game_config, self.gameworld)
        self.render_spell_bar(self)
        # self.render_player_status_effects(self, game_config)
        # self.render_player_vitals(self, self.con, game_config)

        # blit the console
        terminal.refresh()

    @staticmethod
    def clear_map_layer():
        prev_layer = terminal.state(terminal.TK_LAYER)
        terminal.layer(RenderLayer.MAP.value)
        terminal.bkcolor('black')
        terminal.clear_area(0, 0, terminal.state(terminal.TK_WIDTH), terminal.state(terminal.TK_HEIGHT))

        terminal.layer(prev_layer)

    @staticmethod
    def render_map(gameworld, game_config, game_map):
        image_x_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='map_Xscale')
        image_y_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='map_Yscale')

        player_has_moved = MobileUtilities.has_player_moved(gameworld, game_config)
        player_entity = MobileUtilities.get_player_entity(gameworld, game_config)

        y_offset = 0
        x_offset = 0

        x_min, x_max, y_min, y_max = RenderGameMap.get_viewport_boundary(gameworld=gameworld, game_map=game_map,
                                                                         game_config=game_config,
                                                                         player_entity=player_entity)
        if player_has_moved:
            RenderGameMap.clear_map_layer()

        scry = 0

        for y in range(y_min, y_max):
            scrx = 0
            for x in range(x_min, x_max):
                image = game_map.tiles[x][y].image
                tile = game_map.tiles[x][y].type_of_tile
                if tile > 0:
                    terminal.put(x=(scrx + x_offset) * image_x_scale, y=(scry + y_offset) * image_y_scale,
                                 c=0xE300 + image)
                scrx += 1
            scry += 1

    @staticmethod
    def get_viewport_boundary(gameworld, player_entity, game_config, game_map):

        viewport_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                     parameter='VIEWPORT_WIDTH')
        viewport_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='VIEWPORT_HEIGHT')

        map_x, map_y = MobileUtilities.get_mobile_current_location(gameworld=gameworld, mobile=player_entity)
        logger.info('player map pos x/y {}/{}', map_x, map_y)

        if map_x <= (viewport_width // 2):
            viewport_x_min = 0
            viewport_x_max = viewport_width
        else:
            viewport_x_min = map_x - (viewport_width // 2)
            viewport_x_max = map_x + (viewport_width // 2)

        if map_y <= (viewport_height // 2):
            viewport_y_min = 0
            viewport_y_max = viewport_height
        else:
            viewport_y_min = map_y - (viewport_height // 2)
            viewport_y_max = map_y + (viewport_height // 2)
        if viewport_x_max >= game_map.width:
            viewport_x_max = game_map.width

        if viewport_y_max > game_map.height:
            viewport_y_max = game_map.height

        logger.info('viewport x min/max: {}/{}', viewport_x_min, viewport_x_max)
        logger.info('viewport y min/max: {}/{}', viewport_y_min, viewport_y_max)
        logger.info('viewport y max - min is {}', viewport_y_max - viewport_y_min)
        logger.info('viewport width/height {}/{}', viewport_width, viewport_height)
        return viewport_x_min, viewport_x_max, viewport_y_min, viewport_y_max

    @staticmethod
    def render_mobiles(game_config, gameworld):
        image_x_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='map_Xscale')
        image_y_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='map_Yscale')
        term_pos_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                 parameter='TERMINAL_POS_X')
        term_pos_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                 parameter='TERMINAL_POS_Y')
        viewport_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                     parameter='VIEWPORT_WIDTH')
        viewport_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='VIEWPORT_HEIGHT')

        terminal.layer(RenderLayer.ENTITIES.value)

        for ent, (rend, pos, desc) in gameworld.get_components(mobiles.Renderable, mobiles.Position,
                                                               mobiles.Describable):
            if rend.isVisible:
                if pos.x <= (viewport_width // 2):
                    draw_pos_x = pos.x
                else:
                    draw_pos_x = term_pos_x
                if pos.y <= (viewport_height // 2):
                    draw_pos_y = pos.y
                else:
                    draw_pos_y = term_pos_y
                RenderGameMap.render_entity(draw_pos_x, draw_pos_y, desc.image, image_x_scale, image_y_scale)

    @staticmethod
    def render_items(game_config, gameworld):
        map_view_across = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='MAP_VIEW_DRAW_X')
        map_view_down = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='MAP_VIEW_DRAW_Y')

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
        characterbits = [cloak, glyph, robe, shoes, weapon]

        for cell in characterbits:
            terminal.put(x=posx * image_x_scale, y=posy * image_y_scale, c=0xE300 + cell)

    @staticmethod
    def render_viewport(game_config):
        pass

    @staticmethod
    def render_message_box(con, game_config, gameworld):
        pass

    @staticmethod
    def render_player_status_effects(self, game_config):
        pass

    @staticmethod
    def render_boons(self, game_config):
        pass

    @staticmethod
    def render_conditions(self, game_config):
        pass

    @staticmethod
    def render_controls(self, game_config):
        pass

    @staticmethod
    def render_player_status_effects_content(self, posy, glyph, foreground, game_config):
        pass

    @staticmethod
    def render_h_bar(posy, border_colour, game_config):
        pass

    @staticmethod
    def render_player_vitals(self, game_config):
        pass

    @staticmethod
    def render_health_bar(self, player_derived_attributes_component, game_config):
        pass

    @staticmethod
    def render_mana_bar(self, player_entity, game_config):
        pass

    @staticmethod
    def render_f1_bar(self, player_entity, game_config):
        pass

    @staticmethod
    def render_v_bar(con, posx, posy, depth, border_colour):
        pass

    @staticmethod
    def render_player_vertical_bar_content(self, x, current_value, foreground, background, game_config):
        pass

    @staticmethod
    def render_spell_bar(self):

        game_config = configUtilities.load_config()

        spell_box_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='SPELL_BOX_WIDTH')
        spell_bar_across = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                       parameter='SPELL_BOX_X')
        spell_bar_down = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                     parameter='SPELL_BAR_Y')
        spell_bar_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='SPELL_BAR_WIDTH')
        spell_bar_depth = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='SPELL_BOX_DEPTH')
        spell_slots = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                  parameter='SPELL_SLOTS')

        image_x_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='map_Xscale')
        image_y_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='map_Yscale')

        viewport_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='VIEWPORT_HEIGHT')

        player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=game_config)
        weapons_list = MobileUtilities.get_weapons_equipped(gameworld=self.gameworld, entity=player_entity)
        main_weapon = weapons_list[0]
        off_weapon = weapons_list[1]
        both_weapon = weapons_list[2]
        slot = ['NO SPEL'] * 10
        ac = 4
        sc = 3
        y = viewport_height

        prev_layer = terminal.state(terminal.TK_LAYER)
        terminal.layer(RenderLayer.SPELLBAR.value)
        terminal.composition(terminal.TK_ON)
        terminal.color_from_name('blue')

        # spell bar slots are drawn first
        for a in range(10):
            terminal.put(x=(ac + a) * sc, y=y * image_y_scale, c=0xE500 + 0)
        # then the spell images themselves
        for a in range(4):
            terminal.put(x=(ac + a) * sc, y=y * image_y_scale, c=0xE400 + a)

        terminal.layer(prev_layer)

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
