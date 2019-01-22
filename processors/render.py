import esper
import tcod
import random

from newGame import constants


class RenderProcessor(esper.Processor):
    def __init__(self, con):
        super().__init__()
        self.con = con

    def render_v_bar(panel, posx, posy, bottom_side, border_colour, fill_colour, hp):
        tcod.console_set_default_foreground(panel, border_colour)
        tcod.console_put_char(panel, posx, posy, chr(218), tcod.BKGND_NONE)
        tcod.console_put_char(panel, posx + 1, posy, chr(196), tcod.BKGND_NONE)
        tcod.console_put_char(panel, posx + 2, posy, chr(191), tcod.BKGND_NONE)

        tcod.console_put_char(panel, posx, bottom_side, chr(192), tcod.BKGND_NONE)
        tcod.console_put_char(panel, posx + 1, bottom_side, chr(196), tcod.BKGND_NONE)
        tcod.console_put_char(panel, posx + 2, bottom_side, chr(217), tcod.BKGND_NONE)

        for y in range(constants.ALL_BAR_WIDTH):
            tcod.console_set_default_foreground(panel, border_colour)
            tcod.console_put_char(panel, posx, (posy + 1) + y, chr(179), tcod.BKGND_NONE)
            tcod.console_put_char(panel, posx + 2, (posy + 1) + y, chr(179), tcod.BKGND_NONE)

        for y in range(constants.ALL_BAR_WIDTH - hp):
            tcod.console_set_default_foreground(panel, fill_colour)
            tcod.console_put_char(panel, posx + 1, (posy + constants.ALL_BAR_WIDTH) - y, chr(176), tcod.BKGND_NONE)

    def render_h_bar(panel, posx, posy, right_side, border_colour, fill_colour, hp, msg):
        tcod.console_set_default_foreground(panel, border_colour)
        tcod.console_put_char(panel, posx, posy, chr(218), tcod.BKGND_NONE)
        tcod.console_put_char(panel, posx, posy + 1, chr(179), tcod.BKGND_NONE)
        tcod.console_put_char(panel, posx, posy + 2, chr(192), tcod.BKGND_NONE)

        tcod.console_put_char(panel, right_side, posy, chr(191), tcod.BKGND_NONE)
        tcod.console_put_char(panel, right_side, posy + 1, chr(179), tcod.BKGND_NONE)
        tcod.console_put_char(panel, right_side, posy + 2, chr(217), tcod.BKGND_NONE)

        for x in range(constants.BCC_WIDTH):
            tcod.console_set_default_foreground(panel, border_colour)
            tcod.console_put_char(panel, (posx + 1) + x, posy, chr(196), tcod.BKGND_NONE)
            tcod.console_put_char(panel, (posx + 1) + x, posy + 2, chr(196), tcod.BKGND_NONE)

        tcod.console_set_default_foreground(panel, fill_colour)
        tcod.console_print_ex(panel, posx + 1, posy + 1, tcod.BKGND_NONE, tcod.LEFT, msg)
        #
        # for x in range(constants.ALL_BAR_WIDTH - hp):
        #     tcod.console_set_default_foreground(panel, fill_colour)
        #     tcod.console_put_char(panel, (posx + 1) + x, posy + 1, chr(176), tcod.BKGND_NONE)


    def process(self):

        # draw the outer bounds of the map viewport
        tcod.console_set_default_foreground(self.con, tcod.red)
        for x in range(constants.VIEWPORT_WIDTH):
            tcod.console_put_char(self.con, x, 0, '#', tcod.BKGND_NONE)
            tcod.console_put_char(self.con, x, constants.VIEWPORT_HEIGHT +1, '#', tcod.BKGND_NONE)

        for y in range(constants.VIEWPORT_HEIGHT):
            tcod.console_put_char(self.con, 0, y+1, '#', tcod.BKGND_NONE)
            tcod.console_put_char(self.con, constants.VIEWPORT_WIDTH -1, y+1, '#', tcod.BKGND_NONE)

        # draw the message box area
        tcod.console_set_default_foreground(self.con, tcod.yellow)
        for x in range(constants.MSG_PANEL_WIDTH):
            tcod.console_put_char(self.con, x, constants.MSG_PANEL_START_Y, 'O', tcod.BKGND_NONE)
            tcod.console_put_char(self.con, x, constants.MSG_PANEL_START_Y + constants.MSG_PANEL_DEPTH, 'O', tcod.BKGND_NONE)
        for y in range(constants.MSG_PANEL_LINES):
            tcod.console_put_char(self.con, 0, (constants.MSG_PANEL_START_Y + y) + 1, 'O', tcod.BKGND_NONE)
            tcod.console_put_char(self.con, constants.MSG_PANEL_WIDTH - 1, (constants.MSG_PANEL_START_Y + y) + 1, 'O', tcod.BKGND_NONE)

        # draw the spell bar

        # draw the boons, conditions, and controls panels

        # draw the entities
        tcod.console_set_default_foreground(self.con, tcod.white)
        tcod.console_put_char(self.con, 10, 10, '@', tcod.BKGND_NONE)

        tcod.console_blit(self.con, 0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, 0, 0, 0)

        # draw the health, mana and F1 bar
        self.render_h_bar(constants.H_BAR_X, constants.H_BAR_Y, constants.BCC_BAR_RIGHT_SIDE,tcod.darker_gray, tcod.green, 3, 'Boons')
        self.render_h_bar(constants.H_BAR_X, constants.H_BAR_Y + 3, constants.BCC_BAR_RIGHT_SIDE, tcod.darker_gray, tcod.red, 25, 'Conditions')
        self.render_h_bar(constants.H_BAR_X, constants.H_BAR_Y + 6, constants.BCC_BAR_RIGHT_SIDE, tcod.darker_gray, tcod.white, 10, 'Controls')

        self.render_v_bar(constants.V_BAR_X, constants.V_BAR_Y, constants.V_BAR_D, tcod.darker_gray, tcod.red, 20)
        self.render_v_bar(constants.V_BAR_X + 3, constants.V_BAR_Y, constants.V_BAR_D, tcod.darker_gray, tcod.blue, 15)
        self.render_v_bar(constants.V_BAR_X + 6, constants.V_BAR_Y, constants.V_BAR_D, tcod.darker_gray, tcod.white, 5)