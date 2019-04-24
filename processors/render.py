import esper
import tcod

from loguru import logger
from newGame import constants
from components import mobiles, items
from utilities.display import menu
from utilities.mobileHelp import MobileUtilities
from utilities.spellHelp import SpellUtilities
from utilities import configUtilities


class RenderConsole(esper.Processor):
    def __init__(self, con, game_map, gameworld, fov_compute, fov_object, spell_bar, message_log):
        super().__init__()
        self.con = con
        self.game_map = game_map
        self.gameworld = gameworld
        self.fov_compute = fov_compute
        self.fov_object = fov_object
        self.spell_bar = spell_bar
        self.message_log = message_log

    def process(self, game_config):
        # GUI viewport and message box borders
        self.render_viewport(game_config)
        self.render_message_box(game_config)
        self.render_spell_bar(game_config)
        self.render_player_status_effects(game_config)
        self.render_player_vitals(game_config)

        # render the game map
        self.render_map()

        # draw the entities
        self.render_items(game_config)
        self.render_entities(game_config)

        # blit the console
        self.blit_the_console(game_config)
        # clear the entity
        self.clear_entity()

    def blit_the_console(self, game_config):
        # update console with latest changes
        scr_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='tcod', parameter='SCREEN_WIDTH')
        scr_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='tcod', parameter='SCREEN_HEIGHT')

        tcod.console_blit(self.con, 0, 0, scr_width, scr_height, 0, 0, 0)

    def render_player_status_effects(self, game_config):
        # draw the boon, condition, and control bar borders (horizontal)
        self.render_boons(game_config)
        self.render_conditions(game_config)
        self.render_controls(game_config)

    def render_player_vitals(self, game_config):
        player_entity = MobileUtilities.get_player_entity(self.gameworld)
        player_derived_attributes_component = self.gameworld.component_for_entity(player_entity,
                                                                                  mobiles.DerivedAttributes)

        self.render_health_bar(player_derived_attributes_component, game_config)
        self.render_mana_bar(player_entity, game_config)

        self.render_f1_bar(player_entity, game_config)

    def render_spell_bar(self, game_config):
        spell_box_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='SPELL_BOX_WIDTH')
        spell_bar_across = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='SPELL_BAR_X')
        spell_bar_down = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='SPELL_BAR_Y')
        spell_bar_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='SPELL_BAR_WIDTH')
        spell_bar_depth = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='SPELL_BOX_DEPTH')
        spell_slots = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='SPELL_SLOTS')

        tcod.console_set_default_foreground(self.con, tcod.yellow)
        for spellSlot in range(1, spell_slots):
            spell_slot_posx = spell_bar_across + (spellSlot * spell_box_width)
            tcod.console_print_frame(self.con,
                                     x=spell_slot_posx,
                                     y=spell_bar_down,
                                     w=spell_bar_width,
                                     h=spell_bar_depth,
                                     clear=False,
                                     flag=tcod.BKGND_DEFAULT,
                                     fmt='')
            slot_component = SpellUtilities.get_spell_bar_slot_componet(self.gameworld, spell_bar=self.spell_bar, slotid=spellSlot)
            if slot_component == -1:
                logger.warning('Could not get slot component from spell bar')
            else:
                tcod.console_put_char_ex(self.con, spell_slot_posx + 1, spell_bar_down, str(slot_component.sid), tcod.white, tcod.black)
                tcod.console_put_char_ex(self.con, spell_slot_posx + 2, spell_bar_down + 1, '&', tcod.yellow, tcod.black)
                tcod.console_put_char_ex(self.con, spell_slot_posx + 3, spell_bar_down, '*', tcod.white, tcod.black)

    def render_map(self):
        thisplayer = MobileUtilities.get_player_entity(self.gameworld)
        player_position_component = self.gameworld.component_for_entity(thisplayer, mobiles.Position)
        # fov_map = self.fov_object.create_fov_map_via_raycasting(player_position_component.x, player_position_component.y)

        has_player_moved = MobileUtilities.has_player_moved(self.gameworld)
        # has_player_moved = True

        if has_player_moved:
            # calculate FOV
            # fov_map = self.fov_object.create_fov_map_via_raycasting(player_position_component.x, player_position_component.y)
            # GameMap.calculate_fov(self.fov_map, player_position_component.x, player_position_component.y, constants.FOV_RADIUS, constants.FOV_LIGHT_WALLS,constants.FOV_ALGORITHM)

            for y in range(self.game_map.height):
                for x in range(self.game_map.width):
                    isVisible = True
                    draw_pos_x = constants.MAP_VIEW_DRAW_X + x
                    draw_pos_y = constants.MAP_VIEW_DRAW_Y + y
                    tile = self.game_map.tiles[x][y].type_of_tile
                    if isVisible:
                        if tile == constants.TILE_TYPE_WALL:
                            tcod.console_put_char_ex(self.con, draw_pos_x, draw_pos_y, constants.DNG_WALL, constants.colors.get('light_wall'), tcod.black)
                        elif tile == constants.TILE_TYPE_FLOOR:
                            tcod.console_put_char_ex(self.con, draw_pos_x, draw_pos_y, constants.DNG_FLOOR, constants.colors.get('light_ground'),tcod.black)
                        elif tile == constants.TILE_TYPE_DOOR:
                            tcod.console_put_char_ex(self.con, draw_pos_x, draw_pos_y, constants.DNG_DOOR, constants.colors.get('light_ground'),tcod.black)
                        elif tile == constants.TILE_TYPE_CORRIDOR:
                            tcod.console_put_char_ex(self.con, draw_pos_x, draw_pos_y, constants.DNG_FLOOR, constants.colors.get('light_ground'),tcod.black)
                        # tile += constants.TILE_TYPE_EXPLORED

                    else:
                        if tile == constants.TILE_TYPE_WALL:
                            tcod.console_put_char_ex(self.con, draw_pos_x, draw_pos_y, constants.DNG_WALL,
                                                     constants.colors.get('dark_wall'), tcod.black)
                        elif tile == constants.TILE_TYPE_FLOOR:
                            tcod.console_put_char_ex(self.con, draw_pos_x, draw_pos_y, constants.DNG_FLOOR,
                                                     constants.colors.get('dark_ground'), tcod.black)
                        elif tile == constants.TILE_TYPE_DOOR:
                            tcod.console_put_char_ex(self.con, draw_pos_x, draw_pos_y, constants.DNG_DOOR,
                                                     constants.colors.get('dark_ground'), tcod.black)
                        elif tile == constants.TILE_TYPE_CORRIDOR:
                            tcod.console_put_char_ex(self.con, draw_pos_x, draw_pos_y, constants.DNG_FLOOR,
                                                     constants.colors.get('dark_ground'), tcod.black)

    def render_entities(self, game_config):
        px = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MAP_VIEW_DRAW_X')
        py = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MAP_VIEW_DRAW_Y')

        for ent, (rend, pos, desc) in self.world.get_components(mobiles.Renderable, mobiles.Position, mobiles.Describable):
            if rend.isVisible:
                draw_pos_x = px + pos.x
                draw_pos_y = py + pos.y
                self.render_entity(draw_pos_x, draw_pos_y, desc.glyph, desc.foreground, desc.background)

    def render_items(self, game_config):
        px = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MAP_VIEW_DRAW_X')
        py = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MAP_VIEW_DRAW_Y')

        for ent, (rend, loc, desc) in self.world.get_components(items.RenderItem, items.Location, items.Describable):
            if rend.isTrue:
                draw_pos_x = px + loc.posx
                draw_pos_y = py + loc.posy
                self.render_entity(draw_pos_x, draw_pos_y, desc.glyph, desc.fg, desc.bg)

    def render_boons(self, game_config):
        self.render_h_bar(posy=0, border_colour=tcod.darker_gray, game_config=game_config)
        self.render_player_status_effects_content(0, tcod.CHAR_SUBP_DIAG, tcod.green, game_config)

    def render_conditions(self, game_config):
        self.render_h_bar(posy=3, border_colour=tcod.darker_gray, game_config=game_config)
        self.render_player_status_effects_content(3, chr(9), tcod.red, game_config)

    def render_controls(self, game_config):
        self.render_h_bar(posy=6, border_colour=tcod.darker_gray, game_config=game_config)
        self.render_player_status_effects_content(6, chr(10), tcod.white, game_config)

    def render_health_bar(self, player_derived_attributes_component, game_config):

        px = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='V_BAR_X')
        py = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='V_BAR_Y')
        bd2 = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='V_BAR_D')
        current_health = player_derived_attributes_component.currentHealth
        maximum_health = player_derived_attributes_component.maximumHealth
        current_health_percentage = MobileUtilities.get_number_as_a_percentage(current_health, maximum_health)

        self.render_v_bar(posx=px, posy=py, depth=bd2, border_colour=tcod.darker_gray)
        self.render_player_vertical_bar_content(0, current_health_percentage, tcod.red, tcod.black, game_config)

    def render_mana_bar(self, player_entity, game_config):

        px = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='V_BAR_X')
        py = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='V_BAR_Y')
        bd2 = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='V_BAR_D')
        player_current_mana = MobileUtilities.calculate_current_mana(self.gameworld, player_entity)
        player_maximum_mana = MobileUtilities.get_derived_maximum_mana(self.gameworld, player_entity)

        current_mana_percentage = MobileUtilities.get_number_as_a_percentage(player_current_mana, player_maximum_mana)

        self.render_v_bar(posx=px + 3, posy=py, depth=bd2, border_colour=tcod.darker_gray)
        self.render_player_vertical_bar_content(3, current_mana_percentage, tcod.blue, tcod.black, game_config)

    def render_f1_bar(self, player_entity, game_config):
        px = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='V_BAR_X')
        py = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='V_BAR_Y')
        bd2 = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='V_BAR_D')
        psc = MobileUtilities.get_derived_special_bar_current_value(self.gameworld, player_entity)
        psm = MobileUtilities.get_derived_special_bar_max_value(self.gameworld, player_entity)

        current_special_percentage = MobileUtilities.get_number_as_a_percentage(psc, psm)

        self.render_player_vertical_bar_content(6, current_special_percentage, tcod.white, tcod.black, game_config)
        self.render_v_bar(posx=px + 6, posy=py, depth=bd2, border_colour=tcod.darker_gray)

    def render_viewport(self, game_config):
        # draw the outer bounds of the map viewport

        viewport_across = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='VIEWPORT_START_X')
        viewport_down = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='VIEWPORT_START_Y')
        viewport_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='VIEWPORT_WIDTH')
        viewport_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='VIEWPORT_HEIGHT')

        tcod.console_set_default_foreground(self.con, tcod.yellow)

        tcod.console_print_frame(self.con,
                                 x=viewport_across,
                                 y=viewport_down,
                                 w=viewport_width,
                                 h=viewport_height,
                                 clear=False,
                                 flag=tcod.BKGND_DEFAULT,
                                 fmt='')

    def render_message_box(self, game_config):
        msg_start_across = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MSG_PANEL_START_X')
        msg_start_down = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MSG_PANEL_START_Y')
        msg_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MSG_PANEL_WIDTH')
        msg_depth = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MSG_PANEL_DEPTH')

        # draw the message box area

        tcod.console_set_default_foreground(self.con, tcod.yellow)

        tcod.console_print_frame(self.con,
                                 x=msg_start_across,
                                 y=msg_start_down,
                                 w=msg_width,
                                 h=msg_depth,
                                 clear=False,
                                 flag=tcod.BKGND_DEFAULT,
                                 fmt='')
        # render messages in message log
        y = 1
        for message in self.message_log.messages:
            tcod.console_set_default_foreground(self.con, message.color)
            tcod.console_print_ex(self.con, 1, msg_start_down + y, tcod.BKGND_NONE, tcod.LEFT, message.text)
            y += 1

    def render_v_bar(self, posx, posy, depth, border_colour):

        tcod.console_set_default_foreground(self.con, border_colour)
        tcod.console_print_frame(self.con, x=posx, y=posy, w=3, h=depth, clear=False, flag=tcod.BKGND_DEFAULT,
                                 fmt='')

    def render_h_bar(self, posy, border_colour, game_config):

        px = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='H_BAR_X')
        py = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='H_BAR_Y')
        rs = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='BCC_BAR_RIGHT_SIDE')

        tcod.console_set_default_foreground(self.con, border_colour)
        tcod.console_print_frame(self.con, x=px, y=py + posy, w=rs, h=3, clear=False, flag=tcod.BKGND_DEFAULT, fmt='')

    def render_entity(self, posx, posy, glyph, fg, bg):
        tcod.console_put_char_ex(self.con, posx, posy, glyph, fg, bg)

    # clear the entity from the screen - this is used in conjunction with the Renderable component
    def clear_entity(self):
        for ent, (rend, pos, desc) in self.world.get_components(mobiles.Renderable, mobiles.Position, mobiles.Describable):
            if rend.isVisible:
                self.render_entity(pos.x, pos.y, ' ', desc.foreground, desc.background)

    def render_player_status_effects_content(self, posy, glyph, foreground, game_config):
        px = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='H_BAR_X')
        py = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='H_BAR_Y') + posy

        x = 0
        for a in range(10):
            self.render_entity(1 + px + x, py + 1, glyph, foreground, tcod.black)
            if a < 9:
                x += 1
                self.render_entity(1 + px + x, py + 1, chr(179), tcod.darker_gray, tcod.black)
            x += 1

    def render_player_vertical_bar_content(self, x, current_value, foreground, background, game_config):

        px = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='V_BAR_X')
        posx = 1 + px + x
        py = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='V_BAR_Y')
        bar_depth = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='V_BAR_DEPTH')
        posy = py + bar_depth

        bar_count = int(MobileUtilities.get_bar_count(current_value))

        for y in range(bar_count):
            tcod.console_put_char_ex(self.con, posx, posy - y, chr(176), foreground, background)


class RenderGameStartScreen(esper.Processor):
    def __init__(self, con, image, key, mouse, gameworld):
        self.title = constants.GAME_WINDOW_TITLE
        self.author = '(c) 2019 Steven Devonport'
        self.con = con
        self.image = image
        self.key = key
        self.mouse = mouse
        self.gameworld = gameworld
        super().__init__()

    def process(self):
        # get opening image & blit it
        tcod.image_blit_2x(self.image, self.con, 0, 0)

        self.render_game_info()

        # display game options
        menu(self.con, header='Game Start',
            options=['New Game', 'Continue', 'Save', 'Set Seed', 'Replay', 'Quit'],
            width=24, screen_width=constants.SCREEN_WIDTH, screen_height=constants.SCREEN_HEIGHT, posx=10, posy=26,
            foreground=tcod.yellow,
            key=self.key,
            mouse=self.mouse,
            gameworld=self.gameworld)

    def render_game_info(self):
        # display Game information
        tcod.console_set_default_foreground(self.con, tcod.yellow)
        tcod.console_print_ex(self.con, 10, 10, tcod.BKGND_NONE, tcod.LEFT, self.title)
        tcod.console_print_ex(self.con, 10, 42, tcod.BKGND_NONE, tcod.LEFT, self.author)
        tcod.console_blit(self.con, 0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, 0, 0, 0)
