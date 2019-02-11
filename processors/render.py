import esper
import tcod

from loguru import logger
from newGame import constants
from components import mobiles, weapons, spells, spellBar
from utilities.display import menu
from utilities.mobileHelp import MobileUtilities
from utilities.spellHelp import SpellUtilities
from map_objects.gameMap import GameMap


class RenderConsole(esper.Processor):
    def __init__(self, con, game_map, gameworld, fov_compute, fov_map, spell_bar):
        super().__init__()
        self.con = con
        self.game_map = game_map
        self.gameworld = gameworld
        self.fov_compute = fov_compute
        self.fov_map = fov_map
        self.spell_bar = spell_bar

    def process(self):
        # GUI viewport and message box borders
        self.render_viewport()
        self.render_message_box()
        self.render_spell_bar()

        # draw the boon, condition, and control bar borders (horizontal)
        self.render_boons()
        self.render_conditions()
        self.render_controls()

        # draw the health, mana and F1 bar borders (vertical)
        self.render_health_bar()
        self.render_mana_bar()
        self.render_f1_bar()

        # render player effects...
        player_entity = MobileUtilities.get_player_entity(self.gameworld)

        # life
        player_current_health_component = self.gameworld.component_for_entity(player_entity, mobiles.Health)
        current_health_percentage = MobileUtilities.get_number_as_a_percentage(player_current_health_component.current, player_current_health_component.maximum)
        self.render_player_vertical_bar_content(constants.V_BAR_X, constants.V_BAR_Y, current_health_percentage, tcod.red, tcod.black)

        # mana
        player_current_mana_component = self.gameworld.component_for_entity(player_entity, mobiles.ManaPool)
        current_mana_percentage = MobileUtilities.get_number_as_a_percentage(player_current_mana_component.current, player_current_mana_component.maximum)
        self.render_player_vertical_bar_content(constants.V_BAR_X + 3, constants.V_BAR_Y, current_mana_percentage, tcod.blue, tcod.black)
        logger.info('mana percentage set to {}', current_mana_percentage)
        # F1 bar
        player_current_special_component = self.gameworld.component_for_entity(player_entity, mobiles.SpecialBar)
        current_special_percentage = MobileUtilities.get_number_as_a_percentage(player_current_special_component.valuecurrent, player_current_special_component.valuemaximum)
        self.render_player_vertical_bar_content(constants.V_BAR_X + 6, constants.V_BAR_Y, current_special_percentage, tcod.white, tcod.black)

        # boons
        self.render_player_status_effects_content(constants.H_BAR_X, constants.H_BAR_Y, tcod.CHAR_SUBP_DIAG, tcod.green)

        # conditions
        self.render_player_status_effects_content(constants.H_BAR_X, constants.H_BAR_Y + 3, chr(9), tcod.red)

        # controls
        self.render_player_status_effects_content(constants.H_BAR_X, constants.H_BAR_Y + 6, chr(10), tcod.white)

        # render the game map
        self.render_game_map()

        # draw the entities
        self.render_entities()

        # blit the console
        self.blit_the_console()
        # clear the entity
        self.clear_entity()

    def blit_the_console(self):
        # update console with latest changes
        tcod.console_blit(self.con, 0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, 0, 0, 0)

    def render_spell_bar(self):
        tcod.console_set_default_foreground(self.con, tcod.yellow)
        for spellSlot in range(1, constants.SPELL_SLOTS):
            tcod.console_print_frame(self.con,
                                     x=constants.SPELL_BAR_X + (spellSlot * constants.SPELL_BOX_WIDTH),
                                     y=constants.SPELL_BAR_Y,
                                     w=constants.SPELL_BOX_WIDTH,
                                     h=constants.SPELL_BOX_DEPTH,
                                     clear=False,
                                     flag=tcod.BKGND_DEFAULT,
                                     fmt='')
            slot_component = SpellUtilities.get_spell_bar_slot_componet(self.gameworld, spell_bar=self.spell_bar, slotid=spellSlot)
            if slot_component == -1:
                logger.warning('Could not get slot component from spell bar')
            else:
                tcod.console_put_char_ex(self.con, constants.SPELL_BAR_X + (spellSlot * constants.SPELL_BOX_WIDTH) + 1, constants.SPELL_SLOTS_Y, str(slot_component.sid), tcod.white, tcod.black)
                tcod.console_put_char_ex(self.con, constants.SPELL_BAR_X + (spellSlot * constants.SPELL_BOX_WIDTH) + 2, constants.SPELL_SLOTS_Y + 1, '&', tcod.yellow, tcod.black)
                tcod.console_put_char_ex(self.con, constants.SPELL_BAR_X + (spellSlot * constants.SPELL_BOX_WIDTH) + 3, constants.SPELL_SLOTS_Y, '*', tcod.white, tcod.black)

    def render_game_map(self):

        thisplayer = MobileUtilities.get_player_entity(self.gameworld)
        player_position_component = self.gameworld.component_for_entity(thisplayer, mobiles.Position)

        has_player_moved = MobileUtilities.has_player_moved(self.gameworld)

        if has_player_moved:
            GameMap.calculate_fov(self.fov_map, player_position_component.x, player_position_component.y, constants.FOV_RADIUS, constants.FOV_LIGHT_WALLS,
                                  constants.FOV_ALGORITHM)

            for map_cell_y in range(self.game_map.height):
                for map_cell_x in range(self.game_map.width):
                    isVisible = tcod.map_is_in_fov(self.fov_map, map_cell_x, map_cell_y)
                    wall = self.game_map.tiles[map_cell_x][map_cell_y].block_path

                    draw_pos_x = constants.MAP_VIEW_DRAW_X + map_cell_x
                    draw_pos_y = constants.MAP_VIEW_DRAW_Y + map_cell_y

                    if isVisible:
                        if wall:
                            #tcod.console_set_char_background(self.con, draw_pos_x, draw_pos_y, constants.colors.get('light_wall'), tcod.BKGND_SET)
                            tcod.console_put_char_ex(self.con, draw_pos_x, draw_pos_y, '#', constants.colors.get('light_wall'), tcod.black)
                        else:
                            #tcod.console_set_char_background(self.con, draw_pos_x, draw_pos_y, constants.colors.get('light_ground'), tcod.BKGND_SET)
                            tcod.console_put_char_ex(self.con, draw_pos_x, draw_pos_y, '.', constants.colors.get('light_ground'),tcod.black)
                        self.game_map.tiles[map_cell_x][map_cell_y].explored = True
                    elif self.game_map.tiles[map_cell_x][map_cell_y].explored:
                        if wall:
                            #tcod.console_set_char_background(self.con, draw_pos_x, draw_pos_y, constants.colors.get('dark_wall'), tcod.BKGND_SET)
                            tcod.console_put_char_ex(self.con, draw_pos_x, draw_pos_y, '#', constants.colors.get('dark_wall'), tcod.black)
                        else:
                            #tcod.console_set_char_background(self.con, draw_pos_x, draw_pos_y, constants.colors.get('dark_ground'), tcod.BKGND_SET)
                            tcod.console_put_char_ex(self.con, draw_pos_x, draw_pos_y, '.', constants.colors.get('dark_ground'),tcod.black)

    def render_entities(self):
        for ent, (rend, pos, desc) in self.world.get_components(mobiles.Renderable, mobiles.Position, mobiles.Describable):
            if rend.isVisible:
                draw_pos_x = constants.MAP_VIEW_DRAW_X + pos.x
                draw_pos_y = constants.MAP_VIEW_DRAW_Y + pos.y
                self.render_entity(draw_pos_x, draw_pos_y, desc.glyph, desc.foreground, desc.background)

    def render_boons(self):
        self.render_h_bar(posx=constants.H_BAR_X, posy=constants.H_BAR_Y, right_side=constants.BCC_BAR_RIGHT_SIDE,border_colour=tcod.darker_gray)

    def render_conditions(self):
        self.render_h_bar(posx=constants.H_BAR_X, posy=constants.H_BAR_Y + 3, right_side=constants.BCC_BAR_RIGHT_SIDE, border_colour=tcod.darker_gray)

    def render_controls(self):
        self.render_h_bar(posx=constants.H_BAR_X, posy=constants.H_BAR_Y + 6, right_side=constants.BCC_BAR_RIGHT_SIDE, border_colour=tcod.darker_gray)

    def render_health_bar(self):
        self.render_v_bar(posx=constants.V_BAR_X, posy=constants.V_BAR_Y, depth=constants.V_BAR_D, border_colour=tcod.darker_gray)

    def render_mana_bar(self):
        self.render_v_bar(posx=constants.V_BAR_X + 3, posy=constants.V_BAR_Y, depth=constants.V_BAR_D, border_colour=tcod.darker_gray)

    def render_f1_bar(self):
        self.render_v_bar(posx=constants.V_BAR_X + 6, posy=constants.V_BAR_Y, depth=constants.V_BAR_D, border_colour=tcod.darker_gray)

    def render_viewport(self):
        # draw the outer bounds of the map viewport
        tcod.console_set_default_foreground(self.con, tcod.yellow)

        tcod.console_print_frame(self.con,
                                 x=constants.VIEWPORT_START_X,
                                 y=constants.VIEWPORT_START_Y,
                                 w=constants.VIEWPORT_WIDTH,
                                 h=constants.VIEWPORT_HEIGHT,
                                 clear=False,
                                 flag=tcod.BKGND_DEFAULT,
                                 fmt='')

    def render_message_box(self):
        # draw the message box area

        tcod.console_set_default_foreground(self.con, tcod.yellow)

        tcod.console_print_frame(self.con,
                                 x=constants.MSG_PANEL_START_X,
                                 y=constants.MSG_PANEL_START_Y,
                                 w=constants.MSG_PANEL_WIDTH,
                                 h=constants.MSG_PANEL_DEPTH,
                                 clear=False,
                                 flag=tcod.BKGND_DEFAULT,
                                 fmt='')
        # test code - to be deleted
        tcod.console_set_default_foreground(self.con, tcod.light_blue)
        for y in range(constants.MSG_PANEL_LINES):
            tcod.console_print_ex(self.con, 1, 1 + constants.MSG_PANEL_START_Y + y, tcod.BKGND_NONE, tcod.LEFT,
                                  'Message line ' + str(y))

    def render_v_bar(self, posx, posy, depth, border_colour):

        tcod.console_set_default_foreground(self.con, border_colour)
        tcod.console_print_frame(self.con, x=posx, y=posy, w=3, h=depth, clear=False, flag=tcod.BKGND_DEFAULT,
                                 fmt='')

    def render_h_bar(self, posx, posy, right_side, border_colour):

        tcod.console_set_default_foreground(self.con, border_colour)
        tcod.console_print_frame(self.con, x=posx, y=posy, w=right_side, h=3, clear=False, flag=tcod.BKGND_DEFAULT,
                                 fmt='')

    def render_entity(self, posx, posy, glyph, fg, bg):
        tcod.console_put_char_ex(self.con, posx, posy, glyph, fg, bg)

    # clear the entity from the screen - this is used in conjunction with the Renderable component
    def clear_entity(self):
        for ent, (rend, pos, desc) in self.world.get_components(mobiles.Renderable, mobiles.Position, mobiles.Describable):
            if rend.isVisible:
                self.render_entity(pos.x, pos.y, ' ', desc.foreground, desc.background)

    def render_player_status_effects_content(self, posx, posy, glyph, foreground):
        x = 0
        for a in range(10):
            self.render_entity(1 + posx + x, posy + 1, glyph, foreground, tcod.black)
            if a < 9:
                x += 1
                self.render_entity(1 + posx + x, posy + 1, chr(179), tcod.darker_gray, tcod.black)
            x += 1

    def render_player_vertical_bar_content(self, posx, posy, current_value, foreground, background):
        bar_count = int(MobileUtilities.get_bar_count(current_value))
        logger.info('bar count set to {}', bar_count)

        for y in range(bar_count):
            tcod.console_put_char_ex(self.con, posx + 1, (posy + constants.V_BAR_DEPTH) - y, chr(176), foreground, background)


class RenderInventory(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        pass


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
            options=['New Game', 'Continue', 'Save', 'Quit'],
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


class RenderPlayerCharacterScreen(esper.Processor):
    def __init__(self, ):
        super().__init__()

    def process(self):
        pass
