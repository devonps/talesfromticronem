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
        self.fov_radius = 0  # FOV Radius
        self.fov_light_walls = True
        self.fov_algo = 0


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

