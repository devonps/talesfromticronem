from newGame import constants


class Tile:

    def __init__(self, type_of_tile=constants.TILE_TYPE_EMPTY, block_sight=True, block_path=True, explored=False):
        self.type_of_tile = type_of_tile
        self.block_sight = block_sight
        self.block_path = block_path
        self.explored = explored
        self.status_effects = []
        self.placed_spells = []

    def does_tile_block_sight(self):
        return self.block_sight

    def does_tile_block_path(self):
        return self.block_path

    def has_tile_been_explored(self):
        return self.explored

