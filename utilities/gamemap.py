class GameMapUtilities:

    @staticmethod
    def get_type_of_tile(game_map, x, y):
        return game_map.tiles[x][y].type_of_tile

    @staticmethod
    def is_tile_blocked(game_map, x, y):
        if game_map.tiles[x][y].blocked:
            return True
        return False

    @staticmethod
    def get_list_of_spells_at_this_map_location(game_map, x, y):
        return game_map.tiles[x][y].placed_spells

    @staticmethod
    def add_spell_entity_to_this_map_location(game_map, x, y, spell_entity):
        existing_spell_list = GameMapUtilities.get_list_of_spells_at_this_map_location(game_map=game_map, x=x, y=y)
        existing_spell_list.append(spell_entity)
        game_map.tiles[x][y].placed_spells = existing_spell_list

    @staticmethod
    def get_mobile_entity_at_this_location(game_map, x, y):
        return game_map.tiles[x][y].entity

    # remove mobile from current game map position
    @staticmethod
    def remove_mobile_from_map_position(game_map, px, py):
        game_map.tiles[px][py].entity = 0

    # add mobile entity to new game map position
    @staticmethod
    def add_mobile_to_map_position(game_map, px, py, entity):
        game_map.tiles[px][py].entity = entity