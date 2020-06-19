import tcod

from utilities import configUtilities


class FieldOfView:
    """
    Hand crafted field of view class with different FOV formulas, currently it has:
    Ray Casting

    Populates:
        fov_map - which is then used in the Render process

    Arguments:
        game_map, 2d list, this holds the current map the player is in
        startx, integer, the current X coord of the player
        stary, integerm the current Y coord of the player

    Returns:
        None
    """

    def __init__(self, game_map):
        self.game_map = game_map
        self.width = game_map.width
        self.height = game_map.height
        self.fov_radius = 20  # FOV Radius


    @staticmethod
    def get_line(start, end):
        """Bresenham's Line Algorithm
        Produces a list of tuples from start and end

        points tuple is: element 0 is x1 and element 1 is y1

        points1 = (0, 0), (3, 4)
        points2 = (3, 4), (0, 0)

        [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
        [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
        """
        # Setup initial conditions
        x1, y1 = start
        x2, y2 = end
        dx = x2 - x1
        dy = y2 - y1

        # Determine how steep the line is
        is_steep = abs(dy) > abs(dx)

        # Rotate line
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        # Swap start and end points if necessary and store swap state
        swapped = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            swapped = True

        # Recalculate differentials
        dx = x2 - x1
        dy = y2 - y1

        # Calculate error
        error = int(dx / 2.0)
        ystep = 1 if y1 < y2 else -1

        # Iterate over bounding box generating points between start and end
        y = y1
        points = []
        for x in range(x1, x2 + 1):
            coord = (y, x) if is_steep else (x, y)
            points.append(coord)
            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx

        # Reverse the list if the coordinates were swapped
        if swapped:
            points.reverse()

        return points

    #
    # THE METHODDS BELOW USE TCOD FOR FOV CALCULATIONS
    #

    @staticmethod
    def initialise_field_of_view(game_map):
        # this needs to be moved elsewhere and then brought into this processor
        fov_map = tcod.map_new(w=game_map.width, h=game_map.height)

        for y in range(game_map.height):
            for x in range(game_map.width):
                tcod.map_set_properties(fov_map, x, y, not game_map.tiles[x][y].block_sight,
                                        not game_map.tiles[x][y].blocked)

        return fov_map

    @staticmethod
    def recompute_field_of_view(fov_map, x, y, radius, light_walls=True, algorithm=0):
        tcod.map_compute_fov(m=fov_map, x=x, y=y, radius=radius, light_walls=light_walls, algo=algorithm)

