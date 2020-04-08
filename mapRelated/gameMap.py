import random
from enum import Enum, auto

from mapRelated.tile import Tile
from mapRelated.rectangle import Rect
from components import mobiles
from loguru import logger
from utilities import configUtilities


class RenderLayer(Enum):
    MAP = auto()  # dungeon floors, walls, furniture, spell effects??
    ENTITIES = auto()  # player, enemies, items, etc
    HUD = auto()  # hp, mana, f1 bars, hotkeys, etc
    SPELLBAR = auto()  # spell bar
    STATUSEFFECTS = auto()  # effects player is suffering from
    VALIDTARGETS = auto()  # used to show valid targets for the spells


class GameMap:
    def __init__(self, mapwidth, mapheight):
        self.width = mapwidth
        self.height = mapheight
        self.tiles = self.initialize_tiles()

        # MAP PROPERTIES #
        self.listRooms = []
        self.listRegions = []

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        logger.info('Tiles width {} height {}', self.width, self.height)

        return tiles

    @staticmethod
    def assign_tiles(game_map):
        for x in range(game_map.width - 1):
            for y in range(game_map.height - 1):
                tile_is_wall = GameMap.is_blocked(game_map, x, y)
                if tile_is_wall:
                    tile_assigned = 0
                    if GameMap.is_blocked(game_map, x, y - 1):
                        tile_assigned += 1
                    if GameMap.is_blocked(game_map, x+1, y):
                        tile_assigned += 2
                    if GameMap.is_blocked(game_map, x, y+1):
                        tile_assigned += 4
                    if GameMap.is_blocked(game_map, x-1, y):
                        tile_assigned += 8

                    game_map.tiles[x][y].assignment = tile_assigned


    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, gameworld, player, game_config):
        """
        This function creates the entire dungeon floor, including the bits that cannot be seen by the player
        :return:
        """
        rooms = []
        num_rooms = 0
        tile_type_floor = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='TILE_TYPE_FLOOR')

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

            # logger.info('Room r {}. x {} / y {} / w {}/ h {}', r, x,y,w,h)

            new_room = Rect(x, y, w, h)
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                self.create_room(new_room, tile_type_floor)
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    # place player in the first room
                    # player = MobileUtilities.get_player_entity(gameworld)
                    gameworld.add_component(player, mobiles.Position(
                        x=new_x,
                        y=new_y,
                        hasMoved=True))
                else:
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()
                    # flip a coin (random number that is either 0 or 1)
                    # 2 is chosen so that I get either 0 or 1 returned
                    # if self.dungeon_seed.get_next_number_in_range(0, 2) == 1:
                    if random.randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y, tile_type_floor)
                        self.create_v_tunnel(prev_y, new_y, new_x, tile_type_floor)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x, tile_type_floor)
                        self.create_h_tunnel(prev_x, new_x, new_y, tile_type_floor)

                # finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

    def get_type_of_tile(self, x, y):
        return self.tiles[x][y].type_of_tile

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False

    def create_h_tunnel(self, x1, x2, y, tile_type):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False
            self.tiles[x][y].type_of_tile = tile_type

    def create_v_tunnel(self, y1, y2, x, tile_type):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False
            self.tiles[x][y].type_of_tile = tile_type

    def create_room(self, room, tile_type):
        for x in range(room.x + 1, room.w):
            for y in range(room.y + 1, room.h):
                self.tiles[x][y].type_of_tile = tile_type
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False
