import esper
import tcod

from newGame import constants
from components import mobiles


class RenderConsole(esper.Processor):
    def __init__(self, con):
        super().__init__()
        self.con = con

    def process(self):
        # GUI viewport and message box borders
        self.render_viewport()
        self.render_message_box()

        # draw the spell bar borders

        # draw the boon, condition, and control bar borders (horizontal)
        self.render_boons()
        self.render_conditions()
        self.render_controls()

        # draw the health, mana and F1 bar borders (vertical)
        self.render_health_bar()
        self.render_mana_bar()
        self.render_f1_bar()

        # render the game map

        # render player effects...
        # life
        self.render_player_life_bar_content(constants.V_BAR_X, constants.V_BAR_Y, 15, tcod.red, tcod.black)
        # mana
        self.render_player_life_bar_content(constants.V_BAR_X + 3, constants.V_BAR_Y, 20, tcod.blue, tcod.black)
        # F1 bar
        self.render_player_life_bar_content(constants.V_BAR_X + 6, constants.V_BAR_Y, 1, tcod.white, tcod.black)
        # boons
        self.render_player_status_effects_content(constants.H_BAR_X, constants.H_BAR_Y, tcod.CHAR_SUBP_DIAG, tcod.green)
        # conditions
        self.render_player_status_effects_content(constants.H_BAR_X, constants.H_BAR_Y + 3, chr(9), tcod.red)
        # controls
        self.render_player_status_effects_content(constants.H_BAR_X, constants.H_BAR_Y + 6, chr(10), tcod.white)

        # draw the entities
        self.render_entities()

        # blit the console
        self.blit_the_console()
        # flush the console
        self.flush_console()
        # clear the entity
        self.clear_entity()

    @staticmethod
    def flush_console():
        tcod.console_flush()

    def blit_the_console(self):
        # update console with latest changes
        tcod.console_blit(self.con, 0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, 0, 0, 0)

    def render_entities(self):
        for ent, (rend, pos, desc) in self.world.get_components(mobiles.Renderable, mobiles.Position, mobiles.Describable):
            if rend.isVisible:
                self.render_entity(pos.x, pos.y, desc.glyph, desc.foreground, desc.background)

    def render_boons(self):
        self.render_h_bar(constants.H_BAR_X, constants.H_BAR_Y, constants.BCC_BAR_RIGHT_SIDE,tcod.darker_gray)

    def render_conditions(self):
        self.render_h_bar(constants.H_BAR_X, constants.H_BAR_Y + 3, constants.BCC_BAR_RIGHT_SIDE, tcod.darker_gray)

    def render_controls(self):
        self.render_h_bar(constants.H_BAR_X, constants.H_BAR_Y + 6, constants.BCC_BAR_RIGHT_SIDE, tcod.darker_gray)

    def render_health_bar(self):
        self.render_v_bar(constants.V_BAR_X, constants.V_BAR_Y, constants.V_BAR_D, tcod.darker_gray, tcod.red, 15)

    def render_mana_bar(self):
        self.render_v_bar(constants.V_BAR_X + 3, constants.V_BAR_Y, constants.V_BAR_D, tcod.darker_gray, tcod.blue, 6)

    def render_f1_bar(self):
        self.render_v_bar(constants.V_BAR_X + 6, constants.V_BAR_Y, constants.V_BAR_D, tcod.darker_gray, tcod.white, 9)

    def render_viewport(self):
        # draw the outer bounds of the map viewport
        tcod.console_set_default_foreground(self.con, tcod.red)

        for a in range(constants.VIEWPORT_WIDTH):
            for d in range(constants.VIEWPORT_HEIGHT):
                # top and bottom of viewport
                if a > 0 and (d == 0 or d == constants.VIEWPORT_HEIGHT - 1):
                    tcod.console_put_char(self.con, a, d, chr(196), tcod.BKGND_NONE)
                # top corners of viewport
                if a == 0 and d == 0:
                    tcod.console_put_char(self.con, a, 0, chr(218), tcod.BKGND_NONE)
                if a == constants.VIEWPORT_WIDTH - 1 and d == 0:
                    tcod.console_put_char(self.con, a, 0, chr(191), tcod.BKGND_NONE)

                # down sides of viewport
                if a == 0 and d > 0:
                    tcod.console_put_char(self.con, a, d, chr(179), tcod.BKGND_NONE)
                if a == constants.VIEWPORT_WIDTH - 1 and d > 0:
                    tcod.console_put_char(self.con, a, d, chr(179), tcod.BKGND_NONE)

                # bottom corners of viewport
                if a == 0 and d == constants.VIEWPORT_HEIGHT - 1:
                    tcod.console_put_char(self.con, a, d, chr(192), tcod.BKGND_NONE)
                if a == constants.VIEWPORT_WIDTH - 1 and d == constants.VIEWPORT_HEIGHT - 1:
                    tcod.console_put_char(self.con, a, d, chr(217), tcod.BKGND_NONE)

    def render_message_box(self):
        # draw the message box area

        foreground = tcod.yellow
        background = tcod.black

        for a in range(constants.MSG_PANEL_WIDTH):
            for d in range(constants.MSG_PANEL_DEPTH):
                # top and bottom of message box
                if a > 0 and (d == 0 or d == constants.MSG_PANEL_DEPTH - 1):
                    tcod.console_put_char_ex(self.con, a, constants.MSG_PANEL_START_Y + d, chr(196), foreground, background)
                # top corners of message box
                if a == 0 and d == 0:
                    tcod.console_put_char_ex(self.con, a, constants.MSG_PANEL_START_Y, chr(218), foreground, background)
                if a == constants.MSG_PANEL_WIDTH - 1 and d == 0:
                    tcod.console_put_char_ex(self.con, a, constants.MSG_PANEL_START_Y, chr(191), foreground, background)

                # down sides of message box
                if a == 0 and d > 0:
                    tcod.console_put_char_ex(self.con, a, constants.MSG_PANEL_START_Y + d, chr(179), foreground, background)
                if a == constants.MSG_PANEL_WIDTH - 1 and d > 0:
                    tcod.console_put_char_ex(self.con, a, constants.MSG_PANEL_START_Y + d, chr(179), foreground, background)

                # bottom corners of message box
                if a == 0 and d == constants.MSG_PANEL_DEPTH - 1:
                    tcod.console_put_char_ex(self.con, a, constants.MSG_PANEL_START_Y + d, chr(192), foreground, background)
                if a == constants.MSG_PANEL_WIDTH - 1 and d == constants.MSG_PANEL_DEPTH - 1:
                    tcod.console_put_char_ex(self.con, a, constants.MSG_PANEL_START_Y + d, chr(217), foreground, background)

        # test code - to be deleted
        tcod.console_set_default_foreground(self.con, tcod.light_blue)
        for y in range(constants.MSG_PANEL_LINES):
            tcod.console_print_ex(self.con, 1, 1 + constants.MSG_PANEL_START_Y + y, tcod.BKGND_NONE, tcod.LEFT,
                                  'Message line ' + str(y))

    def render_v_bar(self, posx, posy, bottom_side, border_colour, fill_colour, hp_lost):

        foreground = border_colour
        background = tcod.black

        tcod.console_put_char_ex(self.con, posx, posy, chr(218), foreground, background)
        tcod.console_put_char_ex(self.con, posx + 1, posy, chr(196), foreground, background)
        tcod.console_put_char_ex(self.con, posx + 2, posy, chr(191), foreground, background)

        tcod.console_put_char_ex(self.con, posx, bottom_side, chr(192), foreground, background)
        tcod.console_put_char_ex(self.con, posx + 1, bottom_side, chr(196), foreground, background)
        tcod.console_put_char_ex(self.con, posx + 2, bottom_side, chr(217), foreground, background)

        for y in range(constants.V_BAR_DEPTH):
            tcod.console_put_char_ex(self.con, posx, (posy + 1) + y, chr(179), foreground, background)
            tcod.console_put_char_ex(self.con, posx + 2, (posy + 1) + y, chr(179), foreground, background)

    def render_h_bar(self, posx, posy, right_side, border_colour):

        foreground = border_colour
        background = tcod.black

        tcod.console_put_char_ex(self.con, posx, posy, chr(218), foreground, background)
        tcod.console_put_char_ex(self.con, posx, posy + 1, chr(179), foreground, background)
        tcod.console_put_char_ex(self.con, posx, posy + 2, chr(192), foreground, background)

        tcod.console_put_char_ex(self.con, right_side, posy, chr(191), foreground, background)
        tcod.console_put_char_ex(self.con, right_side, posy + 1, chr(179), foreground, background)
        tcod.console_put_char_ex(self.con, right_side, posy + 2, chr(217), foreground, background)

        for x in range(constants.BO_CO_CO_WIDTH):
            if x % 2:
                tcod.console_put_char_ex(self.con, (posx + 1) + x, posy, chr(194), foreground, background)
                tcod.console_put_char_ex(self.con, (posx + 1) + x, posy + 2, chr(193), foreground, background)
            else:
                tcod.console_put_char_ex(self.con, (posx + 1) + x, posy, chr(196), foreground, background)
                tcod.console_put_char_ex(self.con, (posx + 1) + x, posy + 2, chr(196), foreground, background)

    def render_entity(self, posx, posy, glyph, fg, bg):
        tcod.console_put_char_ex(self.con, posx, posy, glyph, fg, bg)

    # clear the entity from the screen - this is used in conjunction with the Renderable component
    def clear_entity(self):
        for ent, (rend, pos, desc) in self.world.get_components(mobiles.Renderable, mobiles.Position, mobiles.Describable):
            if rend.isVisible:
                self.render_entity(pos.x, pos.y, ' ', desc.foreground, desc.background)
        # tcod.console_put_char(self.con, posx, posy, ' ', tcod.BKGND_NONE)

    def render_player_status_effects_content(self, posx, posy, glyph, foreground):
        x = 0
        for a in range(10):
            self.render_entity(1 + posx + x, posy + 1, glyph, foreground, tcod.black)
            if a < 9:
                x += 1
                self.render_entity(1 + posx + x, posy + 1, chr(179), tcod.darker_gray, tcod.black)
            x += 1

    def render_player_life_bar_content(self, posx, posy, value, foreground, background):

        for y in range(constants.V_BAR_DEPTH - value):
            tcod.console_put_char_ex(self.con, posx + 1, (posy + constants.V_BAR_DEPTH) - y, chr(176), foreground, background)

        # displays % amount at bottom of bar
        tcod.console_set_default_foreground(self.con, tcod.white)
        hp = 100 - value
        tcod.console_print_ex(self.con, posx, (posy + constants.V_BAR_DEPTH) + 2, tcod.BKGND_NONE, tcod.LEFT, str(hp) + '%')


class RenderInventory(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        pass


class RenderGameStartScreen(esper.Processor):
    def __init__(self, con):
        self.image = tcod.image_load('static/images/menu_background.png')
        self.title = constants.GAME_WINDOW_TITLE
        self.author = '(c) 2019 Steven Devonport'
        self.con = con
        super().__init__()

    def process(self):
        # get opening image & blit it
        tcod.image_blit_2x(self.image, self.con, 0, 0)

        # display Game information
        tcod.console_set_default_foreground(self.con, tcod.yellow)
        tcod.console_print_ex(self.con, 10, 20, tcod.BKGND_NONE, tcod.LEFT, self.title)
        tcod.console_print_ex(self.con, 10, 22, tcod.BKGND_NONE, tcod.LEFT, self.author)
        # display game options

        tcod.console_blit(self.con, 0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, 0, 0, 0)


class RenderPlayerCharacterScreen(esper.Processor):
    def __init__(self, ):
        super().__init__()

    def process(self):
        pass


