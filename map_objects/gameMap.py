import tcod

from map_objects.tile import Tile
from newGame import constants


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self):
        """
        This function creates the entire dungeon floor, including the bits that cannot be seen by the player
        :return:
        """
        rooms = []
        pass

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
