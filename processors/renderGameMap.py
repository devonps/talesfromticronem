import esper
import tcod

from components import mobiles
from utilities import configUtilities, colourUtilities
from utilities.mobileHelp import MobileUtilities


class RenderGameMap(esper.Processor):
    def __init__(self, con, game_map, gameworld):
        self.con = con
        self.game_map = game_map
        self.gameworld = gameworld

    def process(self, game_config):
        # GUI viewport and message box borders
        # self.render_viewport(game_config)
        # self.render_message_box(game_config)
        # self.render_spell_bar(game_config)
        # self.render_player_status_effects(game_config)
        # self.render_player_vitals(game_config)

        # render the game map
        self.render_map(self.con, self.gameworld, game_config, self.game_map)

        # draw the entities
        # self.render_items(game_config)
        self.render_entities(self.con, game_config, self.gameworld)

        # blit the console
        self.blit_the_console(self.con, game_config)

    @staticmethod
    def render_map(console, gameworld, game_config, game_map):

        map_view_across = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MAP_VIEW_DRAW_X')
        map_view_down = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MAP_VIEW_DRAW_Y')
        tile_type_wall = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon', parameter='TILE_TYPE_WALL')
        tile_type_floor = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon', parameter='TILE_TYPE_FLOOR')
        tile_type_door = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon', parameter='TILE_TYPE_DOOR')
        tile_type_corridor = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon', parameter='TILE_TYPE_CORRIDOR')
        dng_wall = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon', parameter='DNG_WALL')
        dng_floor = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon', parameter='DNG_FLOOR')
        dng_door = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon', parameter='DNG_DOOR')
        dwl = configUtilities.get_config_value_as_string(configfile=game_config, section='colours', parameter='DUNGEON_WALL_LIGHT')
        dwd = configUtilities.get_config_value_as_string(configfile=game_config, section='colours', parameter='DUNGEON_WALL_DARK')
        dfl = configUtilities.get_config_value_as_string(configfile=game_config, section='colours', parameter='DUNGEON_FLOOR_LIGHT')
        dfd = configUtilities.get_config_value_as_string(configfile=game_config, section='colours', parameter='DUNGEON_FLOOR_DARK')

        player_has_moved = MobileUtilities.has_player_moved(gameworld, game_config)

        if player_has_moved:
            bgnd = colourUtilities.BLACK

            dng_wall_light = colourUtilities.colors[dwl]
            dng_light_ground = colourUtilities.colors[dfl]
            dng_dark_ground = colourUtilities.colors[dfd]
            dng_dark_wall = colourUtilities.colors[dwd]

            for y in range(game_map.height):
                for x in range(game_map.width):
                    isVisible = True
                    draw_pos_x = map_view_across + x
                    draw_pos_y = map_view_down + y
                    tile = game_map.tiles[x][y].type_of_tile
                    if isVisible:

                        if tile == 32:
                            tcod.console_put_char_ex(console, draw_pos_x, draw_pos_y, dng_floor, dng_light_ground, bgnd)
                        elif tile == 43:
                            tcod.console_put_char_ex(console, draw_pos_x, draw_pos_y, dng_door, dng_light_ground, bgnd)
                        else:
                            tcod.console_put_char_ex(console, draw_pos_x, draw_pos_y, chr(tile), dng_light_ground, bgnd)


                        # if tile == tile_type_wall:
                        #     tcod.console_put_char_ex(console, draw_pos_x, draw_pos_y, dng_wall, dng_wall_light, bgnd)
                        # elif tile == tile_type_floor:
                        #     tcod.console_put_char_ex(console, draw_pos_x, draw_pos_y, dng_floor, dng_light_ground, bgnd)
                        # elif tile == tile_type_door:
                        #     tcod.console_put_char_ex(console, draw_pos_x, draw_pos_y, dng_door, dng_light_ground, bgnd)
                        # elif tile == tile_type_corridor:
                        #     tcod.console_put_char_ex(console, draw_pos_x, draw_pos_y, dng_floor, dng_light_ground, bgnd)

                    else:
                        if tile == tile_type_wall:
                            tcod.console_put_char_ex(console, draw_pos_x, draw_pos_y, dng_wall, dng_dark_wall, bgnd)
                        elif tile == tile_type_floor:
                            tcod.console_put_char_ex(console, draw_pos_x, draw_pos_y, dng_floor, dng_dark_ground, bgnd)
                        elif tile == tile_type_door:
                            tcod.console_put_char_ex(console, draw_pos_x, draw_pos_y, dng_door, dng_dark_ground, bgnd)
                        elif tile == tile_type_corridor:
                            tcod.console_put_char_ex(console, draw_pos_x, draw_pos_y, dng_floor, dng_dark_ground, bgnd)

    @staticmethod
    def render_entities(con, game_config, gameworld):
        px = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MAP_VIEW_DRAW_X')
        py = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MAP_VIEW_DRAW_Y')

        for ent, (rend, pos, desc) in gameworld.get_components(mobiles.Renderable, mobiles.Position, mobiles.Describable):
            if rend.isVisible:
                draw_pos_x = px + pos.x
                draw_pos_y = py + pos.y
                RenderGameMap.render_entity(con, draw_pos_x, draw_pos_y, desc.glyph, desc.foreground, desc.background)

    # @staticmethod
    # def render_items(game_config):
        # px = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MAP_VIEW_DRAW_X')
        # py = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MAP_VIEW_DRAW_Y')
        #
        # for ent, (rend, loc, desc) in self.world.get_components(items.RenderItem, items.Location, items.Describable):
        #     if rend.isTrue:
        #         draw_pos_x = px + loc.posx
        #         draw_pos_y = py + loc.posy
        #         self.render_entity(draw_pos_x, draw_pos_y, desc.glyph, desc.fg, desc.bg)

    @staticmethod
    def blit_the_console(con, game_config):
        # update console with latest changes
        scr_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='tcod', parameter='SCREEN_WIDTH')
        scr_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='tcod', parameter='SCREEN_HEIGHT')

        # blit changes to root console
        tcod.console_blit(con, 0, 0, scr_width, scr_height, 0, 0, 0)
        tcod.console_flush()
        # todo stop drawing on the root console and create a game map console!

    @staticmethod
    def render_entity(con, posx, posy, glyph, fg, bg):
        tcod.console_put_char_ex(con, posx, posy, glyph, fg, bg)