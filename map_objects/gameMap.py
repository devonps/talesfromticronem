import tcod

from map_objects.tile import Tile
from newGame import constants


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height

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

    def make_bsp(self):
        global map, objects, stairs, bsp_rooms

        objects = [player]

        map = [[Tile(True) for y in range(constants.MAP_HEIGHT)] for x in range(constants.MAP_WIDTH)]

        # Empty global list for storing room coordinates
        bsp_rooms = []

        # New root node
        bsp = tcod.bsp_new_with_size(0, 0, constants.MAP_WIDTH, constants.MAP_HEIGHT)

        # Split into nodes
        tcod.bsp_split_recursive(bsp, 0, constants.BSP_DEPTH, constants.BSP_NODE_MIN_SIZE + 1,
                                 constants.BSP_NODE_MIN_SIZE + 1, 1.5, 1.5)

        # Traverse the nodes and create rooms
        tcod.bsp_traverse_inverted_level_order(bsp, GameMap.traverse_node)

    def traverse_node(node, dat):
        global map, bsp_rooms

        # Create rooms
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
            if not constants.BSP_FULL_ROOMS:
                minx = tcod.random_get_int(None, minx, maxx - constants.BSP_NODE_MIN_SIZE + 1)
                miny = tcod.random_get_int(None, miny, maxy - constants.BSP_NODE_MIN_SIZE + 1)
                maxx = tcod.random_get_int(None, minx + constants.BSP_NODE_MIN_SIZE - 2, maxx)
                maxy = tcod.random_get_int(None, miny + constants.BSP_NODE_MIN_SIZE - 2, maxy)

            node.x = minx
            node.y = miny
            node.w = maxx - minx + 1
            node.h = maxy - miny + 1

            # Dig room
            for x in range(minx, maxx + 1):
                for y in range(miny, maxy + 1):
                    map[x][y].blocked = False
                    map[x][y].block_sight = False

            # Add center coordinates to the list of rooms
            bsp_rooms.append(((minx + maxx) / 2, (miny + maxy) / 2))

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
                    GameMap.vline_up(map, x1, y - 1)
                    GameMap.hline(map, x1, y, x2)
                    GameMap.vline_down(map, x2, y + 1)

                else:
                    minx = max(left.x, right.x)
                    maxx = min(left.x + left.w - 1, right.x + right.w - 1)
                    x = tcod.random_get_int(None, minx, maxx)

                    # catch out-of-bounds attempts
                    while x > constants.MAP_WIDTH - 1:
                        x -= 1

                        GameMap.vline_down(map, x, right.y)
                        GameMap.vline_up(map, x, right.y - 1)

            else:
                if left.y + left.h - 1 < right.y or right.y + right.h - 1 < left.y:
                    y1 = tcod.random_get_int(None, left.y, left.y + left.h - 1)
                    y2 = tcod.random_get_int(None, right.y, right.y + right.h - 1)
                    x = tcod.random_get_int(None, left.x + left.w, right.x)
                    GameMap.hline_left(map, x - 1, y1)
                    GameMap.vline(map, x, y1, y2)
                    GameMap.hline_right(map, x + 1, y2)
                else:
                    miny = max(left.y, right.y)
                    maxy = min(left.y + left.h - 1, right.y + right.h - 1)
                    y = tcod.random_get_int(None, miny, maxy)

                    # catch out-of-bounds attempts
                    while y > constants.MAP_HEIGHT - 1:
                        y -= 1

                        GameMap.hline_left(map, right.x - 1, y)
                        GameMap.hline_right(map, right.x, y)
        return True

    def vline(map, x, y1, y2):
        if y1 > y2:
            y1, y2 = y2, y1

        for y in range(y1, y2 + 1):
            map[x][y].blocked = False
            map[x][y].block_sight = False

    def vline_up(map, x, y):
        while y >= 0 and map[x][y].blocked == True:
            map[x][y].blocked = False
            map[x][y].block_sight = False
            y -= 1

    def vline_down(map, x, y):
        while y < constants.MAP_HEIGHT and map[x][y].blocked == True:
            map[x][y].blocked = False
            map[x][y].block_sight = False
            y += 1

    def hline(map, x1, y, x2):
        if x1 > x2:
            x1, x2 = x2, x1
        for x in range(x1, x2 + 1):
            map[x][y].blocked = False
            map[x][y].block_sight = False

    def hline_left(map, x, y):
        while x >= 0 and map[x][y].blocked == True:
            map[x][y].blocked = False
            map[x][y].block_sight = False
            x -= 1

    def hline_right(map, x, y):
        while x < constants.MAP_WIDTH and map[x][y].blocked == True:
            map[x][y].blocked = False
            map[x][y].block_sight = False
            x += 1

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
