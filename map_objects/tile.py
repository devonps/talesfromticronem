class Tile:

    def __init__(self, block_path, block_sight=None):
        self.block_path = block_path
        self.explored = False

        if block_sight is None:
            block_sight = block_path

        self.block_sight = block_sight

    def is_tile_walkable(self):
        pass
