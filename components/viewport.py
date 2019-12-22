class Dimensions:
    def __init__(self, width=0, height=0):
        self.width = width
        self.height = height


class DisplayRange:
    def __init__(self, min_x=0, max_x=0, min_y=0, max_y=0):
        self.min_x = min_x
        self.max_x = max_x
        self.max_y = max_y
        self.min_y = min_y


class PlayerViewportPosition:
    def __init__(self, viewport_x=0, viewport_y=0):
        self.viewport_x = viewport_x
        self.viewport_y = viewport_y
