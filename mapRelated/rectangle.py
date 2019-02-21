class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = x + w
        self.h = y + h

    def center(self):
        center_x = int((self.x + self.w) / 2)
        center_y = int((self.y + self.h) / 2)
        return center_x, center_y

    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return (self.x <= other.w and self.w >= other.x and
                self.y <= other.h and self.h >= other.y)

