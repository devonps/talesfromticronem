class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w =  x + w
        self.h = y + h

    def center(self):
        center_x = int((self.x + self.w) / 2)
        center_y = int((self.y + self.h) / 2)
        return (center_x, center_y)

    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return (self.x <= other.w and self.w >= other.x and
                self.y <= other.h and self.h >= other.y)


class obj_Room:

    ''' This is a rectangle that lives on the map '''

    def __init__(self, coords, size):

        self.x1, self.y1 = coords
        self.w, self.h = size

        self.x2 = self.x1 + self.w
        self.y2 = self.y1 + self.h

    @property
    def center(self):
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2

        return center_x, center_y

    def intersect(self, other):

        # return True if other obj intersects with this one
        objects_intersect = (self.x1 <= other.x2 and self.x2 >= other.x1 and
                             self.y1 <= other.y2 and self.y2 >= other.y1)

        return objects_intersect