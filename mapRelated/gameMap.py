import tcod
import random
import tcod.bsp

from mapRelated.tile import Tile
from mapRelated.rectangle import Rect
from components import mobiles
from newGame import constants
from loguru import logger
from utilities.randomNumberGenerator import PCG32Generator


class GameMap:
    def __init__(self, mapwidth, mapheight):
        self.width = mapwidth
        self.height = mapheight
        self.tiles = self.initialize_tiles()

        # MAP PROPERTIES #
        self.listRooms = []
        self.listRegions = []
        self.dungeon_seed = PCG32Generator(constants.WORLD_SEED, constants.PRNG_STREAM_DUNGEONS)

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        logger.info('Tiles width {} height {}', self.width, self.height)

        return tiles


    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, gameworld, player):
        """
        This function creates the entire dungeon floor, including the bits that cannot be seen by the player
        :return:
        """
        rooms = []
        num_rooms = 0

        # for r in range(max_rooms):
        #     w = self.dungeon_seed.get_next_number_in_range(room_min_size, room_max_size)
        #     h = self.dungeon_seed.get_next_number_in_range(room_min_size, room_max_size)
        #     x = self.dungeon_seed.get_next_uint(map_width - w - 1)
        #     y = self.dungeon_seed.get_next_uint(map_height - h - 1)

        for r in range(max_rooms):
            # random width and height
            w = random.randint(room_min_size, room_max_size)
            h = random.randint(room_min_size, room_max_size)
            # random position without going out of the boundaries of the map
            x = random.randint(0, map_width - w - 1)
            y = random.randint(0, map_height - h - 1)

            logger.info('Room r {}. x {} / y {} / w {}/ h {}', r, x,y,w,h)

            new_room = Rect(x, y, w, h)
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                self.create_room(new_room)
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    # place player in the first room
                    gameworld.component_for_entity(player, mobiles.Position).x = new_x
                    gameworld.component_for_entity(player, mobiles.Position).y = new_y
                else:
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()
                    # flip a coin (random number that is either 0 or 1)
                    # 2 is chosen so that I get either 0 or 1 returned
                    #if self.dungeon_seed.get_next_number_in_range(0, 2) == 1:
                    if random.randint(0,1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                # finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

    def test_map(self):
        rooms = []

        room1 = Rect(20,15,10,15)
        room2 = Rect(35,15,10,15)

        self.create_room(room1)
        self.create_room(room2)

        self.create_h_tunnel(25,40,23)

    @staticmethod
    def xcreate_fov_map(game_map):
        fov_map = tcod.map_new(game_map.width, game_map.height)

        for mapx, mapy, tile in game_map:
            if tile == constants.TILE_TYPE_WALL:
                tcod.map_set_properties(fov_map, mapx, mapy, isTrans=False, isWalk=False)
            if tile == constants.TILE_TYPE_FLOOR:
                tcod.map_set_properties(fov_map, mapx, mapy, isTrans=True, isWalk=True)
            if tile == constants.TILE_TYPE_CORRIDOR:
                tcod.map_set_properties(fov_map, mapx, mapy, isTrans=True, isWalk=True)
            if tile == constants.TILE_TYPE_DOOR:
                tcod.map_set_properties(fov_map, mapx, mapy, isTrans=False, isWalk=True)



    @staticmethod
    def make_fov_map(game_map):
        fov_map = tcod.map_new(game_map.width, game_map.height)

        for y in range(game_map.height):
            for x in range(game_map.width):

                # tcod.map_set_properties(fov_map, x, y, not game_map.tiles[x][y].type_of_tile,
                #                         not game_map.tiles[x][y].block_path)
                tcod.map_set_properties(fov_map, x, y, isTrans=True, isWalk=True)
        return fov_map

    @staticmethod
    def calculate_fov(fov_map, x, y, radius, light_walls=False, algo=0):
        tcod.map_compute_fov(m=fov_map, x=x, y=y, radius=radius, light_walls=light_walls, algo=algo)

    # def create_h_tunnel(self, x1, x2, y):
    #     for x in range(min(x1, x2), max(x1, x2) + 1):
    #         self.tiles[x][y].block_path = False
    #         self.tiles[x][y].block_sight = False
    #
    # def create_v_tunnel(self, y1, y2, x):
    #     for y in range(min(y1, y2), max(y1, y2) + 1):
    #         self.tiles[x][y].block_path = False
    #         self.tiles[x][y].block_sight = False
    #
    # def vline(self, x, y1, y2):
    #     if y1 > y2:
    #         y1, y2 = y2, y1
    #
    #     for y in range(y1, y2 + 1):
    #         self.tiles[x][y].block_path = False
    #         self.tiles[x][y].block_sight = False
    #
    # def vline_up(self, x, y):
    #     while y >= 0 and self.tiles[x][y].block_path == True:
    #         self.tiles[x][y].block_path = False
    #         self.tiles[x][y].block_sight = False
    #         y -= 1
    #
    # def vline_down(self, x, y):
    #     while y < constants.MAP_HEIGHT and self.tiles[x][y].block_path == True:
    #         self.tiles[x][y].block_path = False
    #         self.tiles[x][y].block_sight = False
    #         y += 1
    #
    # def hline(self, x1, y, x2):
    #     if x1 > x2:
    #         x1, x2 = x2, x1
    #     for x in range(x1, x2 + 1):
    #         self.tiles[x][y].block_path = False
    #         self.tiles[x][y].block_sight = False
    #
    # def hline_left(self, x, y):
    #     while x >= 0 and self.tiles[x][y].block_path == True:
    #         self.tiles[x][y].block_path = False
    #         self.tiles[x][y].block_sight = False
    #         x -= 1
    #
    # def hline_right(self, x, y):
    #     while x < constants.MAP_WIDTH and self.tiles[x][y].block_path == True:
    #         self.tiles[x][y].block_path = False
    #         self.tiles[x][y].block_sight = False
    #         x += 1

    def get_type_of_tile(self, x, y):
        return self.tiles[x][y].type_of_tile

    def is_blocked(self, x, y):
        #if self.tiles[x][y].type_of_tile == constants.TILE_TYPE_WALL:
        if self.grid[x][y] == constants.TILE_TYPE_WALL:
            return True

    def create_room(self, room):
        for x in range(room.x + 1, room.w):
            for y in range(room.y + 1, room.h):
                self.tiles[x][y].type_of_tile = constants.TILE_TYPE_FLOOR

