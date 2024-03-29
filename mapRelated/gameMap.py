from mapRelated import tile
from utilities import gamemap
from utilities.gamemap import GameMapUtilities


class GameMap:
    def __init__(self, mapwidth, mapheight):
        self.width = mapwidth
        self.height = mapheight
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[tile.Tile(False) for _ in range(self.height)] for _ in range(self.width)]

        return tiles

    @staticmethod
    def assign_tiles(game_map):
        for x in range(game_map.width):
            for y in range(game_map.height):
                tile_is_wall = gamemap.GameMapUtilities.is_tile_blocked(game_map, x, y)
                if tile_is_wall:
                    tile_assigned = 0
                    tile_assigned += GameMap.check_if_north_tile_is_blocked(game_map=game_map, posx=x, posy=y)
                    tile_assigned += GameMap.check_if_east_tile_is_blocked(game_map=game_map, posx=x, posy=y)
                    tile_assigned += GameMap.check_if_south_tile_is_blocked(game_map=game_map, posx=x, posy=y)
                    tile_assigned += GameMap.check_if_west_tile_is_blocked(game_map=game_map, posx=x, posy=y)
                    GameMapUtilities.set_tile_assignment(game_map=game_map, x=x, y=y, value=tile_assigned)

    @staticmethod
    def check_if_north_tile_is_blocked(game_map, posx, posy):
        bit_value = 0
        blocked_north = False
        if posy > 0:
            blocked_north = gamemap.GameMapUtilities.is_tile_blocked(game_map, posx, posy - 1)

        if blocked_north:
            bit_value = 1

        return bit_value

    @staticmethod
    def check_if_east_tile_is_blocked(game_map, posx, posy):
        bit_value = 0
        blocked_south = False
        if posx < game_map.width - 1:
            blocked_south = gamemap.GameMapUtilities.is_tile_blocked(game_map, posx + 1, posy)

        if blocked_south:
            bit_value = 2

        return bit_value

    @staticmethod
    def check_if_south_tile_is_blocked(game_map, posx, posy):
        bit_value = 0
        blocked_south = False
        if posy < game_map.height - 1:
            blocked_south = gamemap.GameMapUtilities.is_tile_blocked(game_map, posx, posy + 1)

        if blocked_south:
            bit_value = 4

        return bit_value


    @staticmethod
    def check_if_west_tile_is_blocked(game_map, posx, posy):
        bit_value = 0
        blocked_west = False
        if posx > 0:
            blocked_west = gamemap.GameMapUtilities.is_tile_blocked(game_map, posx - 1, posy)

        if blocked_west:
            bit_value = 8

        return bit_value


