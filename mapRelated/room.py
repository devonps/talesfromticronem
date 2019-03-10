

class dungeonRoom:
    """
    a simple container for dungeon rooms
    since you may want to return to constructing a room, edit it, etc. it helps to have some way to save them
    without having to search through the whole game grid

    Args:
        x and y coodinates for the room
        width and height for the room

    Attributes:
        x, y: the starting coordinates in the 2d array
        width: the ammount of cells the room spans
        height: the ammount of cells the room spans
    """

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return (self.x <= other.width and self.width >= other.x and
                self.y <= other.height and self.height >= other.y)


