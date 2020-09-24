from mapRelated.gameMap import GameMap
from newGame.Entities import Entity
from processors.castSpells import CastSpells
from processors.move_entities import MoveEntities
from processors.renderUI import RenderUI
from processors.updateEntities import UpdateEntitiesProcessor
from processors.renderMessageLog import RenderMessageLog
from processors.renderSpellInfoPanel import RenderSpellInfoPanel
from utilities import configUtilities
from loguru import logger
from utilities.externalfileutilities import Externalfiles
from utilities.jsonUtilities import read_json_file
from utilities.mobileHelp import MobileUtilities


class SceneManager:

    @staticmethod
    def get_current_scene(currentscene):
        this_scene = ''
        scene_found = False
        game_config = configUtilities.load_config()
        scene_list = configUtilities.get_config_value_as_list(game_config, 'game', 'SCENES')

        for scene_id, scene_name in enumerate(scene_list, 1):
            if scene_id == currentscene:
                logger.debug('Current scene set to {}', scene_name)
                scene_found = True
                this_scene = scene_name
        return scene_found, this_scene

    @staticmethod
    def new_scene(currentscene, gameworld):

        gm, mx, my = SceneManager.load_scene_card(currentscene=currentscene, gameworld=gameworld)
        SceneManager.generate_game_map()

        return gm

    @staticmethod
    def load_scene_card(currentscene, gameworld):
        # load scene list into memory
        map_area_max_x = 0
        map_area_max_y = 0
        game_map = []
        scene_found, this_scene = SceneManager.get_current_scene(currentscene=currentscene)

        if scene_found:
            map_area_file = ''
            scene_file = 'new_scenes.json'
            scene_file = read_json_file('static/scenes/' + scene_file)
            for scene_key in scene_file['scenes']:
                if scene_key['name'] == this_scene:
                    scene_name = scene_key['name']
                    scene_exits = scene_key['sceneExits']
                    logger.debug('The {} scene exits to the {}', scene_name, scene_exits)
                    if 'loadMap' in scene_key:
                        # load game_map from external file - setup variables
                        map_area_file = scene_key['loadMap']
                        map_area_max_x = int(scene_key['mapx'])
                        map_area_max_y = int(scene_key['mapy'])
                        game_map = GameMap(mapwidth=map_area_max_x, mapheight=map_area_max_y)

                    if map_area_file != '':
                        SceneManager.build_static_scene(gameworld=gameworld, game_map=game_map,
                                                        map_area_file=map_area_file, scene_key=scene_key)
                        GameMap.assign_tiles(game_map=game_map)
                    else:
                        # generate random map
                        pass

        SceneManager.create_ecs_systems_yes_no(gameworld=gameworld, currentscene=currentscene, game_map=game_map)

        return game_map, map_area_max_x - 1, map_area_max_y - 1

    @staticmethod
    def create_ecs_systems_yes_no(gameworld, currentscene, game_map):
        if currentscene == 1:
            update_entities_processor = UpdateEntitiesProcessor(gameworld=gameworld, game_map=game_map)
            move_entities_processor = MoveEntities(gameworld=gameworld, game_map=game_map)
            cast_spells_processor = CastSpells(gameworld=gameworld, game_map=game_map)
            render_ui_processor = RenderUI(game_map=game_map, gameworld=gameworld)
            render_message_log_processor = RenderMessageLog(gameworld=gameworld)
            spell_info_processor = RenderSpellInfoPanel(gameworld=gameworld, game_map=game_map)
            gameworld.add_processor(move_entities_processor, priority=80)
            gameworld.add_processor(cast_spells_processor, priority=100)
            gameworld.add_processor(update_entities_processor, priority=90)
            gameworld.add_processor(render_ui_processor, priority=70)
            gameworld.add_processor(render_message_log_processor, priority=60)
            gameworld.add_processor(spell_info_processor, priority=50)

    @staticmethod
    # haven't created the proc-gen routines for this
    def generate_game_map():
        pass

    @staticmethod
    def build_static_scene(gameworld, game_map, map_area_file, scene_key):
        # get config items
        game_config = configUtilities.load_config()
        prefab_folder = configUtilities.get_config_value_as_string(game_config, 'files', 'PREFABFOLDER')
        tile_type_wall = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                     parameter='TILE_TYPE_WALL')
        tile_type_floor = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='TILE_TYPE_FLOOR')
        tile_type_door = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                     parameter='TILE_TYPE_DOOR')
        tile_type_empty = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='TILE_TYPE_EMPTY')

        # now load the game_map from the external file/csv
        filepath = prefab_folder + map_area_file + '.txt'

        file_content = Externalfiles.load_existing_file(filename=filepath)
        posy = 0
        for row in file_content:
            posx = 0
            for cell in row:
                SceneManager.place_floor_tile_yes_no(cell=cell, game_map=game_map, posx=posx, posy=posy,
                                                     tile_type=tile_type_floor)
                SceneManager.place_door_tile_yes_no(cell=cell, game_map=game_map, posx=posx, posy=posy,
                                                    tile_type=tile_type_door)
                SceneManager.place_wall_tile_yes_no(cell=cell, game_map=game_map, posx=posx, posy=posy,
                                                    tile_type=tile_type_wall)
                SceneManager.place_empty_tile_yes_no(cell=cell, game_map=game_map, posx=posx, posy=posy, tile_type=tile_type_empty)
                player_placed = SceneManager.place_player_tile_yes_no(cell=cell, game_map=game_map, posx=posx, posy=posy,
                                                      tile_type=tile_type_floor)

                if player_placed:
                    SceneManager.setup_viewport(gameworld=gameworld, posx=posx, posy=posy)
                    game_map.tiles[posx][posy].entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)

                    # add named NPCs to scene
                if cell in 'ABCDEFG':
                    entity_created = Entity.create_named_mobile(npcs_for_scene=scene_key['npcs'], posx=posx, posy=posy, cellid=cell, gameworld=gameworld, game_config=game_config)
                    game_map.tiles[posx][posy].type_of_tile = tile_type_floor
                    game_map.tiles[posx][posy].entity = entity_created
                    SceneManager.place_floor_tile_yes_no(cell=cell, posx=posx, posy=posy, tile_type=tile_type_floor, game_map=game_map)
                posx += 1
            posy += 1

    @staticmethod
    def place_empty_tile_yes_no(cell, game_map, posx, posy, tile_type):
        if cell == ' ':
            game_map.tiles[posx][posy].type_of_tile = tile_type
            game_map.tiles[posx][posy].image = 4
            game_map.tiles[posx][posy].blocked = False
            game_map.tiles[posx][posy].block_sight = False

    @staticmethod
    def place_floor_tile_yes_no(cell, game_map, posx, posy, tile_type):
        if cell == '.':
            game_map.tiles[posx][posy].type_of_tile = tile_type
            game_map.tiles[posx][posy].image = 4
            game_map.tiles[posx][posy].blocked = False
            game_map.tiles[posx][posy].block_sight = False

    @staticmethod
    def place_door_tile_yes_no(cell, game_map, posx, posy, tile_type):
        if cell == '+':
            game_map.tiles[posx][posy].type_of_tile = tile_type
            game_map.tiles[posx][posy].image = 10
            game_map.tiles[posx][posy].blocked = True
            game_map.tiles[posx][posy].block_sight = True

    @staticmethod
    def place_wall_tile_yes_no(cell, game_map, posx, posy, tile_type):
        if cell == '#':
            game_map.tiles[posx][posy].type_of_tile = tile_type
            game_map.tiles[posx][posy].image = 9
            game_map.tiles[posx][posy].blocked = True
            game_map.tiles[posx][posy].block_sight = True

    @staticmethod
    def place_player_tile_yes_no(cell, game_map, posx, posy, tile_type):
        player_placed = False
        if cell == '@':
            game_map.tiles[posx][posy].type_of_tile = tile_type
            game_map.tiles[posx][posy].blocked = False
            game_map.tiles[posx][posy].image = 11
            game_map.tiles[posx][posy].block_sight = False
            player_placed = True
        return player_placed

    @staticmethod
    def setup_viewport(gameworld, posx, posy):
        game_config = configUtilities.load_config()
        player_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
        MobileUtilities.set_mobile_position(gameworld=gameworld, entity=player_entity, posx=posx, posy=posy)

