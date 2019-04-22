from newGame import constants


class Tile:

    def __init__(self, blocked, type_of_tile=constants.TILE_TYPE_WALL, block_sight=None, explored=False):
        self.type_of_tile = type_of_tile
        self.blocked = blocked
        if block_sight is None:
                block_sight = blocked
        self.block_sight = block_sight
        self.explored = explored
        self.status_effects = []
        self.placed_spells = []

    def does_tile_block_sight(self):
        return self.block_sight

    def does_tile_block_path(self):
        return self.blocked

    def has_tile_been_explored(self):
        return self.explored

