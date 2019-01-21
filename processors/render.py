import esper
import tcod
from newGame import constants


class RenderProcessor(esper.Processor):
    def __init__(self, con):
        super().__init__()
        self.con = con

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
            tcod.console_put_char(self.con, constants.VIEWPORT_WIDTH -1, (constants.MSG_PANEL_START_Y + y) + 1, 'O', tcod.BKGND_NONE)

        # draw the spell bar

        # draw the boons, conditions, and controls panels

        tcod.console_set_default_foreground(self.con, tcod.white)
        tcod.console_put_char(self.con, 10, 10, '@', tcod.BKGND_NONE)

        tcod.console_print_ex(self.con, int(constants.SCREEN_WIDTH / 2), int(constants.SCREEN_HEIGHT / 2) + 8, tcod.BKGND_NONE,
                                 tcod.CENTER, '(c) Steven Devonport 2018')

        tcod.console_blit(self.con, 0,0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, 0, 0, 0)

        tcod.console_flush()


