
from enum import Enum, auto

from mapRelated.tile import Tile

from utilities.gamemap import GameMapUtilities


class RenderLayer(Enum):
    MAP = auto()  # dungeon floors, walls, furniture, spell effects??
    ENTITIES = auto()  # player, enemies, items, etc
    HUD = auto()  # hp, f1 bars, hotkeys, etc
    SPELLBAR = auto()  # spell bar
    STATUSEFFECTS = auto()  # effects player is suffering from
    VALIDTARGETS = auto()  # used to show valid targets for the spells


class GameMap:
    def __init__(self, mapwidth, mapheight):
        self.width = mapwidth
        self.height = mapheight
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(False) for _ in range(self.height)] for _ in range(self.width)]

        return tiles

    @staticmethod
    def assign_tiles(game_map):
        for x in range(game_map.width):
            for y in range(game_map.height):
                tile_is_wall = GameMapUtilities.is_tile_blocked(game_map, x, y)
                if tile_is_wall:
                    tile_assigned = 0
                    tile_assigned += GameMap.check_if_north_tile_is_blocked(game_map=game_map, posx=x, posy=y)
                    tile_assigned += GameMap.check_if_east_tile_is_blocked(game_map=game_map, posx=x, posy=y)
                    tile_assigned += GameMap.check_if_south_tile_is_blocked(game_map=game_map, posx=x, posy=y)
                    tile_assigned += GameMap.check_if_west_tile_is_blocked(game_map=game_map, posx=x, posy=y)
                    game_map.tiles[x][y].assignment = tile_assigned

    @staticmethod
    def check_if_north_tile_is_blocked(game_map, posx, posy):
        bit_value = 0
        blocked_north = False
        if posy > 0:
            blocked_north = GameMapUtilities.is_tile_blocked(game_map, posx, posy - 1)

        if blocked_north:
            bit_value = 1

        return bit_value

    @staticmethod
    def check_if_east_tile_is_blocked(game_map, posx, posy):
        bit_value = 0
        blocked_south = False
        if posx < game_map.width - 1:
            blocked_south = GameMapUtilities.is_tile_blocked(game_map, posx + 1, posy)

        if blocked_south:
            bit_value = 2

        return bit_value

    @staticmethod
    def check_if_south_tile_is_blocked(game_map, posx, posy):
        bit_value = 0
        blocked_south = False
        if posy < game_map.height - 1:
            blocked_south = GameMapUtilities.is_tile_blocked(game_map, posx, posy + 1)

        if blocked_south:
            bit_value = 4

        return bit_value


    @staticmethod
    def check_if_west_tile_is_blocked(game_map, posx, posy):
        bit_value = 0
        blocked_west = False
        if posx > 0:
            blocked_west = GameMapUtilities.is_tile_blocked(game_map, posx - 1, posy)

        if blocked_west:
            bit_value = 8

        return bit_value


