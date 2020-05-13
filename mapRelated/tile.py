
class Tile:

    def __init__(self, blocked, block_sight=None):
        self.type_of_tile = 5
        self.blocked = blocked
        if block_sight is None:
                block_sight = blocked
        self.block_sight = block_sight
        self.explored = False
        self.status_effects = []
        self.placed_spells = []
        self.region = 0
        self.flow_x = 0
        self.flow_y = 0
        self.posx = 0
        self.posy = 0
        self.glyph = ''
        self.image = 0
        self.assignment = 0

