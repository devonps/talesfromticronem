import tcod
import random
import tcod.bsp

from map_objects.tile import Tile
from map_objects.rectangle import Rect, obj_Room
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
        tiles = [[Tile(True) for y in range(self.height)]
                                for x in range(self.width)]

        logger.info('Tiles width {} height {}', self.width, self.height)

        return tiles

    def generate_bsp_map(self):

        self.listRegions = [[obj_Room((0, 0), (constants.MAP_WIDTH, constants.MAP_HEIGHT))]]

        for a in range(constants.BSP_TIMES_SPLIT):
            templist = []

            for region in self.listRegions[-1]:
                # will return value between 0 and 1
                # splitNumber = self.dungeon_seed.get_next_number_in_range(constants.BSP_MIN_SPLIT, constants.BSP_MAX_SPLIT)
                splitpct = random.uniform(constants.BSP_MIN_SPLIT, constants.BSP_MAX_SPLIT)
                # splitpct = splitNumber / 100

                if a % 2 != 0 :
                    # split the region vertically
                    splitValue = int(region.w * splitpct)

                    logger.info('Split is vertical {}', splitValue)

                    region01 = obj_Room((region.x1, region.y1), (splitValue, region.h))
                    logger.info('Region 1 x1 {} / y1 {} / w {}/ h {}', region.x1, region.y1, splitValue, region.h)

                    region02 = obj_Room((region01.x1 + region01.w, region.y1), (region.w - splitValue, region.h))
                    logger.info('Region 2 x1 {} / y1 {} / w {}/ h {}', region01.x1 + region01.w, region.y1, region.w - splitValue, region.h)

                else:
                    # split the region horizontal
                    splitValue = int(region.h * splitpct)
                    logger.info('Split is horizontal {}', splitValue)

                    region01 = obj_Room((region.x1, region.y1),
                                        (region.w, splitValue))

                    logger.info('Region 1 x1 {} / y1 {} / w {}/ h {}', region.x1, region.y1, region.w, splitValue)

                    region02 = obj_Room((region.x1, region01.y1 + region01.h),
                                        (region.w, region.h - splitValue))
                    logger.info('Region 1 x1 {} / y1 {} / w {}/ h {}', region.x1, region01.y1 + region01.h, region.w, region.h - splitValue)

                templist.append(region01)
                templist.append(region02)
            self.listRegions.append(templist)

        for levelNumber, regionsInLevel in enumerate(self.listRegions):
            currentNumOfRegionsInGroup = len(regionsInLevel)
            neededNumOfRegionsInGroup = len(self.listRegions[-1]) // currentNumOfRegionsInGroup
            tempList = []

            for listNumber in range(currentNumOfRegionsInGroup):
                listStart = listNumber * neededNumOfRegionsInGroup
                listEnd = listStart + neededNumOfRegionsInGroup
                tempList.append(self.listRegions[-1][listStart:listEnd])

            self.listRegions[levelNumber] = tempList

            # delete the useless last level
        del self.listRegions[-1]

        for region in self.listRegions[0][0]:
            newRoom = obj_Room((region.x1, region.y1), (region.w , region.h ))

            self.digRoom(newRoom)
            self.listRooms.append(newRoom)

        for i, groupRegions in enumerate(reversed(self.listRegions)):
            numOfGroups = len(groupRegions)
            numOfItems = len(groupRegions[0])

            if numOfItems == 2:
                for pair in groupRegions:
                    self.digTunnels(pair[0].center, pair[1].center)

            if numOfItems < (2 ** constants.BSP_MAX_SPLIT):
                for x in range(int(numOfGroups / 2)):
                    setListBegin = x * 2
                    setListEnd = setListBegin + 2

                    roomChoice1 = random.choice(groupRegions[setListBegin:setListEnd][0])
                    roomChoice2 = random.choice(groupRegions[setListBegin:setListEnd][1])

                    self.digTunnels(roomChoice1.center, roomChoice2.center)

    def rogue_make_bsp_map(self):
        # objects = [player]
        bsp_rooms = []

        # dungeon_seed_stream = PCG32Generator(constants.WORLD_SEED, constants.PRNG_STREAM_DUNGEONS)

        # new root node
        bsp = tcod.bsp_new_with_size(x=0, y=0, w=constants.MAP_WIDTH, h=constants.MAP_HEIGHT)

        # split into nodes
        tcod.bsp_split_recursive(node=bsp,
                                 randomizer=None,
                                 nb=constants.BSP_TIMES_SPLIT,
                                 minHSize=constants.MAP_BSP_ROOM_MIN_SIZE + 1,
                                 minVSize=constants.MAP_BSP_ROOM_MIN_SIZE + 1,
                                 maxHRatio=1,
                                 maxVRatio=2)
        # traverse the nodes and create rooms
        tcod.bsp_traverse_inverted_level_order(node=bsp, callback=self.traverse_node, userData=bsp_rooms)

        # random room for the stairs
        # stairs_location = random.choice(bsp_rooms)
        # bsp_rooms.remove(stairs_location)
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

    def digRoom(self, new_room):
        for x in range(new_room.x1, new_room.x2):
            for y in range(new_room.y1, new_room.y2):
                try:
                    self.tiles[x][y].block_path = False
                except:
                    print((x, y))

    def digTunnels(self, coords1, coords2):

        coin_flip = (tcod.random_get_int(0, 0, 1) == 1)

        x1, y1 = coords1
        x2, y2 = coords2

        if coin_flip:

            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.tiles[x][y1].block_path = False

            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.tiles[x2][y].block_path = False

        else:

            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.tiles[x1][y].block_path = False

            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.tiles[x][y2].block_path = False

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

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].block_path = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].block_path = False
            self.tiles[x][y].block_sight = False

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



    def is_blocked(self, x, y):
        if self.tiles[x][y].block_path:
            return True

    def create_room(self, room):
        for x in range(room.x + 1, room.w):
            for y in range(room.y + 1, room.h):
                self.tiles[x][y].block_path = False
                self.tiles[x][y].block_sight = False

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
