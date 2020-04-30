import random
import math
from mapRelated.tile import Tile

# copied over from PoC project: main.py
# mapGridWidth = 10
# mapGridHeight = 10
#
# game_map = CellGrid(width=mapGridWidth, height=mapGridHeight)
#
# game_map.make_cells()
# game_map.draw_game_grid()
# game_map.make_level_map()


class CellFlowMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = self.initialize_cells()
        self.gridCells = []

    def initialize_cells(self, cell=None):
        cells = [[cell() for _ in range(self.height)] for _ in range(self.width)]

        return cells

    def make_cells(self):

        max_no_cells = 9

        for cell_loop in range(max_no_cells):
            cell_id = cell_loop + 1
            cell_max_size = 3 + random.randint(0, 3)
            fx = 0
            fy = 0
            print("--- This is cell group " + str(cell_loop))
            print("--- This cell is n points " + str(cell_max_size))

            if cell_loop > 0:
                x, y = self.choose_rand_start_from_previous_cell(cell_id - 1)

            for cell in range(cell_max_size):
                if cell_loop == 0 and cell == 0:    # very first cell point
                    x, y = self.get_starting_grid_location()
                # get flow for next cell point
                fx, fy = self.determine_cell_flow(x, y)
                # add flow to current cell position
                self.cells[x][y].flow_x = fx
                self.cells[x][y].flow_y = fy

                # assign new cell point to current cell 'group'
                x = x + fx
                y = y + fy
                self.cells[x][y].id = cell_id
                self.gridCells.append([x, y, cell_id])

    def choose_rand_start_from_previous_cell(self, previous_cell):
        x = 0
        y = 0
        cell_count = 0
        chosen = []
        for gridcell in self.gridCells:
            if gridcell[2] <= previous_cell:
                px = gridcell[0]
                py = gridcell[1]
                cell_count += 1
                chosen.append([px, py])
        if cell_count > 0:
            print("Chosen cells " + str(chosen))
            zz = random.choice(chosen)

            x = zz[0]
            y = zz[1]

            print('pick_random_point_from_cell: chosen_x:' + str(x))
            print('pick_random_point_from_cell: chosen_y:' + str(y))

            return x, y

        return 0, 0

    def draw_game_grid(self):

        print('.0123456789')
        for y in range(self.height):
            if y < 10:
                xs = '0' + str(y)
            else:
                xs = str(y)
            for x in range(self.width):
                if self.cells[x][y].id == 0:
                    xs += '.'
                else:
                    xs += str(self.cells[x][y].id)
            print(xs)

        print('.0123456789')

    def determine_cell_flow(self, sx, sy):
        max_attempts = 100
        next_point_chosen = False
        attempts = 1
        xx = 0
        yy = 0
        while next_point_chosen is False and attempts < max_attempts:
            # print('determine_cell_flow: Attempt number:' + str(attempts))
            xx = 0
            yy = 0
            lgth = 0
            flowDir = random.randint(1, 2)
            # print('determine_cell_flow: flow direction:' + str(flowDir))

            while lgth == 0:
                lgth = random.randint(-1, 1)
            # print('determine_cell_flow: lgth:' + str(lgth))

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
                    if self.cells[sx + xx][sy + yy].id == 0:
                        next_point_chosen = True
                        # print(
                        #     'determine_cell_flow: next cell coords s/b :' + str(sx + xx) + '/' + str(
                        #         sy + yy))

            attempts += 1
        # print('determine_cell_flow: flow chosen x/y:' + str(xx) + '/' + str(yy))
        return xx, yy

    def get_starting_grid_location(self):
        x = 0
        y = 0
        maxX = self.width - 3
        maxY = self.height - 3

        while (x == 0 and x < self.width) and (y == 0 and y < self.height):
            x = random.randint(2, maxX)
            y = random.randint(2, maxY)

        return x, y

    def make_level_map(self):
        # for cell in self.gridCells:
        #     print('Cell:' + str(cell))
        #
        #     fx, fy = self.get_flow_for_this_area(cell)
        #     print('fx value: ' + str(fx))
        #     print('fy value: ' + str(fy))


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

        # self.temp_mark_flow_from_centre(mapSizeMod, level_map)

        self.add_doors_to_game_map(mapSizeMod, level_map, wallCell)

        self.draw_map_level(map_height, map_width, level_map)

    def temp_mark_flow_from_centre(self, mapSizeMod, level_map):

        cell_offset = math.floor(mapSizeMod / 2)
        cells_length = len(self.gridCells)
        for a in range(0, cells_length - 1):
            this_cell = self.gridCells[a]

            msx = this_cell[0] * mapSizeMod
            msy = this_cell[1] * mapSizeMod

            fx = self.cells[this_cell[0]][this_cell[1]].flow_x
            fy = self.cells[this_cell[0]][this_cell[1]].flow_y

            px = msx + cell_offset
            py = msy + cell_offset

            if fx == -1:
                level_map[px][py].glyph = '<'
            elif fx == 1:
                level_map[px][py].glyph = '>'
            elif fy == -1:
                level_map[px][py].glyph = '^'
            elif fy == 1:
                level_map[px][py].glyph = 'o'

            if fx == 0 and fy == 0:
                level_map[px][py].glyph = 'X'

            if fx == -1 and fy == -1:
                level_map[px][py].glyph = 'Y'

    def get_centre_of_the_area(self, mapSizeMod, this_cell):
        cell_offset = math.floor(mapSizeMod / 2)

        msx = this_cell[0] * mapSizeMod
        msy = this_cell[1] * mapSizeMod

        px = msx + cell_offset
        py = msy + cell_offset

        return px, py

    def get_flow_for_this_area(self, this_cell):

        fx = self.cells[this_cell[0]][this_cell[1]].flow_x
        fy = self.cells[this_cell[0]][this_cell[1]].flow_y

        return fx, fy

    def add_doors_to_game_map(self, mapSizeMod, level_map, wallcell):
        for cell in self.gridCells:
            px, py = self.get_centre_of_the_area(mapSizeMod, cell)
            fx, fy = self.get_flow_for_this_area(cell)

            ax = px
            ay = py
            # print('starting values ax/ay ' + str(ax) + '/' + str(ay))

            for a in range(mapSizeMod):

                if fx == -1:
                    ax -= 1
                elif fx == 1:
                    ax += 1
                elif fy == -1:
                    ay -= 1
                elif fy == 1:
                    ay += 1

                if level_map[ax][ay].glyph == wallcell:
                    level_map[ax][ay].glyph = '+'

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

    def add_the_floor_to_the_game_map(self, map_height, map_width, level_map, floorCell, blankCell, mapSizeMod):
        for y in range(0, map_height):
            for x in range(0, map_width):
                lmx = math.floor((x / mapSizeMod))
                lmy = math.floor((y / mapSizeMod))

                gridCell = int(self.cells[lmx][lmy].id)

                if gridCell > 0:
                    level_map[x][y].glyph = blankCell
                    level_map[x][y].region = gridCell
                else:
                    level_map[x][y].glyph = blankCell
                    level_map[x][y].region = 0

    def draw_map_level(self, map_height, map_width, level_map):

        path = 'map.txt'
        new_file = open(path, 'w')

        new_file.write(' 0....5....1....5....2....5....3....5....4....5....5\n')
        for y in range(map_height):
            if y < 10:
                xs = '0' + str(y)
            else:
                xs = str(y)
            for x in range(map_width):
                xs += str(level_map[x][y].glyph)
            new_file.write(xs+'\n')
        new_file.write('00....5.....1....5....2....5....3....5....4....5....5\n')
        new_file.close()