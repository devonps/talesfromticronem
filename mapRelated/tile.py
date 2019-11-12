
class Tile:

    def __init__(self, blocked, block_sight=None, explored=False):

        # type_of_tile=constants.TILE_TYPE_WALL - some hackery magic going on below
        self.type_of_tile = 5
        self.blocked = blocked
        if block_sight is None:
                block_sight = blocked
        self.block_sight = block_sight
        self.explored = explored
        self.status_effects = []
        self.placed_spells = []
        self.region = 0
        self.flow_x = 0
        self.flow_y = 0
        self.posx = 0
        self.posy = 0
        self.glyph = ''
        self.image = -99

    def does_tile_block_sight(self):
        return self.block_sight

    def does_tile_block_path(self):
        return self.blocked

    def has_tile_been_explored(self):
        return self.explored

    def get_tile_image(self):
        return self.image
