import tcod
import random

from map_objects.tile import Tile
from map_objects.rectangle import Rect
from components import mobiles
from newGame import constants
from utilities.randomNumberGenerator import PCG32Generator
from loguru import logger


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].block_path = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].block_path = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].block_path = False
            self.tiles[x][y].block_sight = False

    def is_blocked(self, x, y):
        if self.tiles[x][y].block_path:
            return True

    def make_bsp_map(self, player, gameworld):
        objects = [player]
        bsp_rooms = []

        # dungeon_seed_stream = PCG32Generator(constants.WORLD_SEED, constants.PRNG_STREAM_DUNGEONS)

        # new root node
        bsp = tcod.bsp_new_with_size(x=0, y=0, w=constants.MAP_WIDTH, h=constants.MAP_HEIGHT)

        # split into nodes
        tcod.bsp_split_recursive(node=bsp,
                                 randomizer=0,
                                 nb=constants.MAP_BSP_NO_SPLITS,
                                 minHSize=constants.MAP_BSP_ROOM_MIN_SIZE + 1,
                                 minVSize=constants.MAP_BSP_ROOM_MIN_SIZE + 1,
                                 maxHRatio=1.5,
                                 maxVRatio=1.5)
        # traverse the nodes and create rooms
        tcod.bsp_traverse_inverted_level_order(node=bsp, callback=self.traverse_node, userData=bsp_rooms)

        # random room for the stairs
        stairs_location = random.choice(bsp_rooms)
        bsp_rooms.remove(stairs_location)
        # stairs = object(stairs_location[0], stairs_location[1], '<', 'stairs', tcod.white, always_visible=True)
        # objects.append(stairs)


        # add monsters, etc

    def traverse_node(self, node, bp):

        # create rooms
        if tcod.bsp_is_leaf(node):
            minx = node.x + 1
            maxx = node.x + node.w - 1
            miny = node.y + 1
            maxy = node.y + node.h - 1

            if maxx == constants.MAP_WIDTH - 1:
                maxx -= 1
            if maxy == constants.MAP_HEIGHT - 1:
                maxy -= 1

            # If it's False the rooms sizes are random, else the rooms are filled to the node's size
            if not constants.MAP_BSP_FULL_ROOMS:
                minx = tcod.random_get_int(None, minx, maxx - constants.MAP_BSP_ROOM_MIN_SIZE + 1)
                miny = tcod.random_get_int(None, miny, maxy - constants.MAP_BSP_ROOM_MIN_SIZE + 1)
                maxx = tcod.random_get_int(None, minx + constants.MAP_BSP_ROOM_MIN_SIZE - 2, maxx)
                maxy = tcod.random_get_int(None, miny + constants.MAP_BSP_ROOM_MIN_SIZE - 2, maxy)

            node.x = minx
            node.y = miny
            node.w = maxx - minx + 1
            node.h = maxy - miny + 1

            # Dig room
            for x in range(minx, maxx + 1):
                for y in range(miny, maxy + 1):
                    self.tiles[x][y].block_path = False
                    self.tiles[x][y].block_sight = False

            # Add center coordinates to the list of rooms
            bp.append(((minx + maxx) / 2, (miny + maxy) / 2))
            # Create corridors
        else:
            left = tcod.bsp_left(node)
            right = tcod.bsp_right(node)
            node.x = min(left.x, right.x)
            node.y = min(left.y, right.y)
            node.w = max(left.x + left.w, right.x + right.w) - node.x
            node.h = max(left.y + left.h, right.y + right.h) - node.y
            if node.horizontal:
                if left.x + left.w - 1 < right.x or right.x + right.w - 1 < left.x:
                    x1 = tcod.random_get_int(None, left.x, left.x + left.w - 1)
                    x2 = tcod.random_get_int(None, right.x, right.x + right.w - 1)
                    y = tcod.random_get_int(None, left.y + left.h, right.y)
                    self.vline_up(x1, y - 1)
                    self.hline(x1, y, x2)
                    self.vline_down(x2, y + 1)

                else:
                    minx = max(left.x, right.x)
                    maxx = min(left.x + left.w - 1, right.x + right.w - 1)
                    x = tcod.random_get_int(None, minx, maxx)

                    # catch out-of-bounds attempts
                    while x > constants.MAP_WIDTH - 1:
                        x -= 1

                    self.vline_down(x, right.y)
                    self.vline_up(x, right.y - 1)

            else:
                if left.y + left.h - 1 < right.y or right.y + right.h - 1 < left.y:
                    y1 = tcod.random_get_int(None, left.y, left.y + left.h - 1)
                    y2 = tcod.random_get_int(None, right.y, right.y + right.h - 1)
                    x = tcod.random_get_int(None, left.x + left.w, right.x)
                    self.hline_left(x - 1, y1)
                    self.vline(x, y1, y2)
                    self.hline_right(x + 1, y2)
                else:
                    miny = max(left.y, right.y)
                    maxy = min(left.y + left.h - 1, right.y + right.h - 1)
                    y = tcod.random_get_int(None, miny, maxy)

                    # catch out-of-bounds attempts
                    while y > constants.MAP_HEIGHT - 1:
                        y -= 1

                    self.hline_left(right.x - 1, y)
                    self.hline_right(right.x, y)

        return True

    def vline(self, x, y1, y2):
        if y1 > y2:
            y1, y2 = y2, y1

        for y in range(y1, y2 + 1):
            self.tiles[x][y].block_path = False
            self.tiles[x][y].block_sight = False

    def vline_up(self, x, y):
        while y >= 0 and self.tiles[x][y].block_path == True:
            self.tiles[x][y].block_path = False
            self.tiles[x][y].block_sight = False
            y -= 1

    def vline_down(self, x, y):
        while y < constants.MAP_HEIGHT and self.tiles[x][y].block_path == True:
            self.tiles[x][y].block_path = False
            self.tiles[x][y].block_sight = False
            y += 1

    def hline(self, x1, y, x2):
        if x1 > x2:
            x1, x2 = x2, x1
        for x in range(x1, x2 + 1):
            self.tiles[x][y].block_path = False
            self.tiles[x][y].block_sight = False

    def hline_left(self, x, y):
        while x >= 0 and self.tiles[x][y].block_path == True:
            self.tiles[x][y].block_path = False
            self.tiles[x][y].block_sight = False
            x -= 1

    def hline_right(self, x, y):
        while x < constants.MAP_WIDTH and self.tiles[x][y].block_path == True:
            self.tiles[x][y].block_path = False
            self.tiles[x][y].block_sight = False
            x += 1

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, gameworld, player):
        """
        This function creates the entire dungeon floor, including the bits that cannot be seen by the player
        :return:
        """
        rooms = []
        num_rooms = 0

        dungeon_seed_stream = PCG32Generator(constants.WORLD_SEED, constants.PRNG_STREAM_DUNGEONS)

        for r in range(max_rooms):
            w = dungeon_seed_stream.get_next_number_in_range(room_min_size, room_max_size)
            h = dungeon_seed_stream.get_next_number_in_range(room_min_size, room_max_size)
            x = dungeon_seed_stream.get_next_uint(map_width - w - 1)
            y = dungeon_seed_stream.get_next_uint(map_height - h - 1)

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
                    if dungeon_seed_stream.get_next_number_in_range(0, 2) == 1:
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

    @staticmethod
    def make_fov_map(game_map):
        fov_map = tcod.map_new(game_map.width, game_map.height)

        for y in range(game_map.height):
            for x in range(game_map.width):
                tcod.map_set_properties(fov_map, x, y, not game_map.tiles[x][y].transparent,
                                        not game_map.tiles[x][y].block_path)
        return fov_map

    @staticmethod
    def calculate_fov(fov_map, x, y, radius, light_walls=True, algo =0):
        tcod.map_compute_fov(m=fov_map, x=x, y=y, radius=radius, light_walls=light_walls, algo=algo)