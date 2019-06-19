import random
import math
from mapRelated.tile import Tile

# copied over from PoC project: main.py
# mapGridWidth = 20
# mapGridHeight = 20
#
# game_map = CellFlowMap(mapwidth=mapGridWidth, mapheight=mapGridHeight)
#
# game_map.make_game_grid()
#
# game_map.draw_game_grid()
# game_map.make_level_map()


class CellFlowMap:
    def __init__(self, mapwidth, mapheight):
        self.width = mapwidth
        self.height = mapheight
        self.tiles = self.initialize_tiles()
        self.gridCells = []

    def initialize_tiles(self):
        tiles = [[Tile(0) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_level_map(self):
        mapSizeMod = 5
        map_width = self.width * mapSizeMod
        map_height = self.height * mapSizeMod
        level_map = [[Tile(' ') for x in range(map_width)] for y in range(map_height)]

        floorCell = '.'
        wallCell = '#'
        blankCell = ' '

        self.add_the_floor_to_the_game_map(map_height, map_width, level_map, floorCell, blankCell, mapSizeMod)

        # add walls around rooms
        self.add_walls_to_game_map_rooms(map_height, map_width, level_map, wallCell)

        # add corner walls around rooms
        self.add_corner_walls_to_game_map_rooms(map_height, map_width, level_map, wallCell, blankCell)

        # now add the magical flow!
        # use the region id to track the flow through the map - as a debug tool

        # mark centre point for each region
        self.mark_centre_of_rooms_on_game_map(level_map, mapSizeMod)

        cell_offset = math.floor(mapSizeMod / 2)
        cells_length = len(self.gridCells)
        for a in range(0, cells_length - 1):
            this_cell = self.gridCells[a]

            msx = this_cell[0] * mapSizeMod
            msy = this_cell[1] * mapSizeMod

            px = msx + cell_offset
            py = msy + cell_offset

            fx = self.tiles[this_cell[0]][this_cell[1]].flow_x
            fy = self.tiles[this_cell[0]][this_cell[1]].flow_y

            next_cell = self.gridCells[a + 1]
            nsx = next_cell[0] * mapSizeMod
            nsy = next_cell[1] * mapSizeMod
            cx = px + fx
            cy = py + fy

            dist_to_travel = self.calculate_distance_between_two_centres(fx, fy, msx, nsx, msy, nsy)

            if dist_to_travel > 0:
                self.find_a_wall_to_put_a_door(dist_to_travel, fx, fy, cx, cy, level_map, wallCell)

        self.draw_map_level(map_height, map_width, level_map)

    def make_game_grid(self):
        maxCells = 9        # number of different 'groups' of cells
        cellSize = 5        # max size of cell 'group'

        # number of different cells on the grid
        for region in range(0, maxCells):

            region_id = region + 1

            print('--- game grid: Placing region ' + str(region_id))

            for i in range(0, cellSize):
                print('+++ working on cell ' + str(i))
                if i == 0 and region_id == 1:
                    x, y = self.get_starting_grid_location()
                if region_id > 1 and i == 0:
                    x, y = self.pick_random_point_from_cell(region=region_id)
                    print('New region starting grid x/y' + str(x) + '/' + str(y))
                    fx, fy = self.create_flow_from_current_cell(x, y)
                    self.set_flow_for_current_cell(x, y, fx, fy)
                else:
                    self.add_cell_to_game_grid(x, y, region_id)
                    fx, fy = self.create_flow_from_current_cell(x, y)
                    self.set_flow_for_current_cell(x, y, fx, fy)

                x = x + fx
                y = y + fy

                if i == cellSize - 1 and region == maxCells - 1:
                    self.add_cell_to_game_grid(x, y, region_id)

    def get_starting_grid_location(self):
        x = 0
        y = 0
        while (x == 0 and x < self.width) and (y == 0 and y < self.height):
            x = random.randint(2, self.width - 1)
            y = random.randint(2, self.height - 1)

        return x, y

    def add_cell_to_game_grid(self, cx, cy, cell_id):
        if cx < 0:
            cx = 0
        if cx > self.width - 1:
            cx = self.width - 1
        if cy < 0:
            cy = 0
        if cy > self.height - 1:
            cy = self.height - 1
        if self.tiles[cx][cy].region == 0:
            self.tiles[cx][cy].region = cell_id
            self.tiles[cx][cy].posx = cx
            self.tiles[cx][cy].posy = cy
            self.gridCells.append([cx, cy, cell_id])
            print('add_cell_to_game_grid: cell id set to ' + str(cell_id))
        else:
            print('add_cell_to_game_grid: Exception: cell x/y ' + str(cx) + '/' + str(cy))
            print('add_cell_to_game_grid: is in region ' + str(self.tiles[cx][cy].region))

    def create_flow_from_current_cell(self, sx, sy):

        max_attempts = 100
        next_cell_chosen = False
        attempts = 1
        xx = 0
        yy = 0
        while next_cell_chosen is False and attempts < max_attempts:
            print('create_flow_from_current_cell: Attempt number:' + str(attempts))
            xx = 0
            yy = 0
            lgth = 0
            flowDir = random.randint(1, 2)

            print('create_flow_from_current_cell: flow direction:' + str(flowDir))

            while lgth == 0:
                lgth = random.randint(-1, 1)
            print('create_flow_from_current_cell: lgth:' + str(lgth))

            if flowDir == 1:
                # move along the horizontal (X)
                xx += lgth
                if xx >= self.width:
                    xx = xx * -1
                yy = 0
            else:
                # move along the vertical (Y)
                yy += lgth
                if yy >= self.height:
                    yy = yy * -1
                xx = 0

            if (sx + xx > 0) and (sx + xx < self.width):
                if (sy + yy > 0) and (sy + yy < self.height):
                    if self.tiles[sx + xx][sy + yy].region == 0:
                        next_cell_chosen = True
                        print('create_flow_from_current_cell: next cell coords s/b :' + str(sx + xx) + '/' + str(sy + yy))

            attempts += 1
        print('create_flow_from_current_cell: flow chosen x/y:' + str(xx) + '/' + str(yy))
        return xx, yy

    def pick_random_point_from_cell(self, region):
        print('pick_random_point_from_cell: incoming region:' + str(region))
        x = 0
        y = 0
        cell_count = 0
        chosen = []
        for cell in self.gridCells:
            if cell[2] == region - 1:
                px = cell[0]
                py = cell[1]
                cell_count += 1
                chosen.append([px,py])

        if cell_count > 0:
            zz = random.choice(chosen)

            x = zz[0]
            y = zz[1]

            print('pick_random_point_from_cell: chosen_x:' + str(x))
            print('pick_random_point_from_cell: chosen_y:' + str(y))

            return x, y

    def draw_game_grid(self):

        print('.0123456789')
        for y in range(self.height):
            xs = str(y)
            for x in range(self.width):
                if self.tiles[x][y].region == 0:
                    xs += '.'
                else:
                    xs += str(self.tiles[x][y].region)
            print(xs)

        print('.0123456789')

        print(str(len(self.gridCells)))

    def set_flow_for_current_cell(self, curr_x, curr_y, flow_x, flow_y):
        self.tiles[curr_x][curr_y].flow_x = flow_x
        self.tiles[curr_x][curr_y].flow_y = flow_y

    def find_a_wall_to_put_a_door(self, dist_to_travel, fx, fy, cx, cy, level_map, wallCell):
        for cellFlow in range(0, dist_to_travel):

            if fx != 0:
                cx += fx
            if fy != 0:
                cy += fy

            if level_map[cx][cy].glyph == wallCell:
                level_map[cx][cy].glyph = '+'
                break
            # else:
            #     level_map[cx][cy].glyph = '/'

    def calculate_distance_between_two_centres(self, fx, fy, msx, nsx, msy, nsy):
        dist_to_travel = 0
        if fx == - 1:
            dist_to_travel = msx - nsx
        elif fx == 1:
            dist_to_travel = nsx - msx
        elif fy == -1:
            dist_to_travel = msy - nsy
        elif fy == 1:
            dist_to_travel = nsy - msy

        return dist_to_travel

    def mark_centre_of_rooms_on_game_map(self, level_map, mapSizeMod):
        cell_offset = math.floor(mapSizeMod / 2)
        cells_length = len(self.gridCells)
        for a in range(0, cells_length - 1):
            this_cell = self.gridCells[a]

            msx = this_cell[0] * mapSizeMod
            msy = this_cell[1] * mapSizeMod

            px = msx + cell_offset
            py = msy + cell_offset

            level_map[px][py].glyph = 'o'

    def add_the_floor_to_the_game_map(self, map_height, map_width, level_map, floorCell, blankCell, mapSizeMod):
        for y in range(0, map_height):
            for x in range(0, map_width):
                lmx = math.floor((x / mapSizeMod))
                lmy = math.floor((y / mapSizeMod))

                gridCell = int(self.tiles[lmx][lmy].region)

                if gridCell > 0:
                    level_map[x][y].glyph = floorCell
                    level_map[x][y].region = gridCell
                else:
                    level_map[x][y].glyph = blankCell
                    level_map[x][y].region = 0

    def add_walls_to_game_map_rooms(self, map_height, map_width, level_map, wallCell):
        for y in range(0, map_height - 1):
            for x in range(0, map_width - 1):

                thiscell_region = level_map[x][y].region
                thiscell_glyph = level_map[x][y].glyph

                n_cell_region = level_map[x][y - 1].region
                e_cell_region = level_map[x + 1][y].region
                s_cell_region = level_map[x][y + 1].region
                w_cell_region = level_map[x - 1][y].region
                n_cell_glyph = level_map[x][y - 1].glyph
                e_cell_glyph = level_map[x + 1][y].glyph
                s_cell_glyph = level_map[x][y + 1].glyph
                w_cell_glyph = level_map[x - 1][y].glyph

                if thiscell_region > 0:
                    if (n_cell_region != thiscell_region) and (n_cell_glyph != wallCell):
                        level_map[x][y].glyph = wallCell
                    if e_cell_region != thiscell_region and (e_cell_glyph != wallCell):
                        level_map[x][y].glyph = wallCell
                    if s_cell_region != thiscell_region and (s_cell_glyph != wallCell):
                        level_map[x][y].glyph = wallCell
                    if w_cell_region != thiscell_region and (w_cell_glyph != wallCell):
                        level_map[x][y].glyph = wallCell

                    if x == map_width - 2:
                        level_map[x + 1][y].glyph = wallCell

                    if y == map_height - 2:
                        level_map[x][y + 1].glyph = wallCell
                else:
                    level_map[x][y].glyph = ' '

    def add_corner_walls_to_game_map_rooms(self, map_height, map_width, level_map, wallCell, blankCell):
        for y in range(0, map_height - 1):
            for x in range(0, map_width - 1):

                thiscell_region = level_map[x][y].region
                thiscell_glyph = level_map[x][y].glyph
                ne_cell_region = level_map[x + 1][y - 1].region
                se_cell_region = level_map[x + 1][y + 1].region
                sw_cell_region = level_map[x - 1][y + 1].region
                nw_cell_region = level_map[x - 1][y - 1].region
                ne_cell_glyph = level_map[x + 1][y - 1].glyph
                se_cell_glyph = level_map[x + 1][y + 1].glyph
                sw_cell_glyph = level_map[x - 1][y + 1].glyph
                nw_cell_glyph = level_map[x - 1][y - 1].glyph

                if thiscell_glyph != wallCell:
                    if (ne_cell_region != thiscell_region) and (ne_cell_glyph == blankCell):
                        level_map[x + 1][y - 1].glyph = wallCell
                    if (se_cell_region != thiscell_region) and (se_cell_glyph == blankCell):
                        level_map[x + 1][y + 1].glyph = wallCell
                    if (sw_cell_region != thiscell_region) and (sw_cell_glyph == blankCell):
                        level_map[x - 1][y + 1].glyph = wallCell
                    if (nw_cell_region != thiscell_region) and (nw_cell_glyph == blankCell):
                        level_map[x - 1][y - 1].glyph = wallCell

    def draw_map_level(self, map_height, map_width, level_map):
        print(' 0....5....1....5....2....5....3....5....4....5....5')
        for y in range(map_height):
            if y < 10:
                xs = '0' + str(y)
            else:
                xs = str(y)
            for x in range(map_width):
                xs += str(level_map[x][y].glyph)
            print(xs)

        print('00....5.....1....5....2....5....3....5....4....5....5')