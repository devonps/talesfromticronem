import esper
import tcod

from newGame import constants
from components import mobiles


class RenderProcessor(esper.Processor):
    def __init__(self, con):
        super().__init__()
        self.con = con

    def process(self):

        self.render_viewport()
        self.render_message_box()
        # draw the spell bar

        # draw the boons, conditions, and controls panels
        self.render_boons()
        self.render_conditions()
        self.render_controls()

        # draw the entities

        for ent, (rend, pos, desc) in self.world.get_components(mobiles.Renderable, mobiles.Position, mobiles.Describable):
            if rend.isVisible:
                posx = pos.x
                posy = pos.y
                glyph = desc.glyph
                fg = desc.foreground
                bg = desc.background
                tcod.console_put_char_ex(self.con, posx, posy, glyph, fg, bg)

        # draw the health, mana and F1 bar
        self.render_health_bar()
        self.render_mana_bar()
        self.render_f1_bar()

        # update console with latest changes
        tcod.console_blit(self.con, 0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, 0, 0, 0)

    def render_boons(self):
        self.render_h_bar(constants.H_BAR_X, constants.H_BAR_Y, constants.BCC_BAR_RIGHT_SIDE,tcod.darker_gray, tcod.green,  'Boons')

    def render_conditions(self):
        self.render_h_bar(constants.H_BAR_X, constants.H_BAR_Y + 3, constants.BCC_BAR_RIGHT_SIDE, tcod.darker_gray, tcod.red, 'Conditions')

    def render_controls(self):
        self.render_h_bar(constants.H_BAR_X, constants.H_BAR_Y + 6, constants.BCC_BAR_RIGHT_SIDE, tcod.darker_gray, tcod.white, 'Controls')

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

        foreground = fill_colour

        for y in range(constants.V_BAR_DEPTH - hp_lost):
            tcod.console_put_char_ex(self.con, posx + 1, (posy + constants.V_BAR_DEPTH) - y, chr(176), foreground, background)

        tcod.console_set_default_foreground(self.con, tcod.white)
        hp = 100 - hp_lost
        tcod.console_print_ex(self.con, posx, (posy + constants.V_BAR_DEPTH) + 2, tcod.BKGND_NONE, tcod.LEFT, str(hp) + '%')

    def render_h_bar(self, posx, posy, right_side, border_colour, fill_colour, msg):

        foreground = border_colour
        background = tcod.black

        tcod.console_put_char_ex(self.con, posx, posy, chr(218), foreground, background)
        tcod.console_put_char_ex(self.con, posx, posy + 1, chr(179), foreground, background)
        tcod.console_put_char_ex(self.con, posx, posy + 2, chr(192), foreground, background)

        tcod.console_put_char_ex(self.con, right_side, posy, chr(191), foreground, background)
        tcod.console_put_char_ex(self.con, right_side, posy + 1, chr(179), foreground, background)
        tcod.console_put_char_ex(self.con, right_side, posy + 2, chr(217), foreground, background)

        for x in range(constants.BO_CO_CO_WIDTH):
            tcod.console_put_char_ex(self.con, (posx + 1) + x, posy, chr(196), foreground, background)
            tcod.console_put_char_ex(self.con, (posx + 1) + x, posy + 2, chr(196), foreground, background)

        tcod.console_set_default_foreground(self.con, fill_colour)
        tcod.console_print_ex(self.con, posx + 1, posy + 1, tcod.BKGND_NONE, tcod.LEFT, msg)