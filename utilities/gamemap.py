
class GameMapUtilities:

    @staticmethod
    def get_type_of_tile(game_map, x, y):
        return game_map.tiles[x][y].type_of_tile

    @staticmethod
    def is_tile_blocked(game_map, x, y):
        if game_map.tiles[x][y].blocked:
            return True
        return False
