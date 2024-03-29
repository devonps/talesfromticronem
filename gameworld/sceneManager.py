import random

from mapRelated.gameMap import GameMap
from newGame.Entities import NewEntity
from processors import castSpells, move_entities, renderUI, updateEntities, renderMessageLog, renderSpellInfoPanel
from static.data import constants
from utilities import configUtilities, externalfileutilities, jsonUtilities, mobileHelp, scorekeeper
from loguru import logger

from utilities.gamemap import GameMapUtilities


class SceneManager:

    @staticmethod
    def get_current_scene(currentscene):
        this_scene = ''
        scene_found = False
        game_config = configUtilities.load_config()
        scene_list = configUtilities.get_config_value_as_list(game_config, 'game', 'SCENES')

        for scene_id, scene_name in enumerate(scene_list, 1):
            if scene_id == currentscene:
                logger.debug('Current scene changed to {}', scene_name)
                scene_found = True
                this_scene = scene_name
        return scene_found, this_scene

    @staticmethod
    def new_scene(currentscene, gameworld):

        game_map, mx, my, scene_exit = SceneManager.load_scene_card(currentscene=currentscene, gameworld=gameworld)
        logger.info('Current scene is {}', currentscene)
        if scene_exit == 0:
            logger.warning('No valid scene exits from current scene')
        else:
            logger.debug('CURRENT SCENE EXIT IS {}', scene_exit)
        return game_map, scene_exit

    @staticmethod
    def load_scene_card(currentscene, gameworld):
        # load scene list into memory
        map_area_max_x = 0
        map_area_max_y = 0
        scene_exit = 0
        game_map = []
        scene_found, this_scene = SceneManager.get_current_scene(currentscene=currentscene)
        logger.info('Scene found set to {}, this scene is {}', scene_found, this_scene)
        current_area_tag = ''
        if scene_found:
            map_area_file = ''
            scene_file = 'new_scenes.json'
            scene_file = jsonUtilities.read_json_file('static/scenes/' + scene_file)
            for scene_key in scene_file['scenes']:
                if scene_key['name'] == this_scene:
                    scene_exit = int(scene_key['sceneExits'])
                    current_area_tag = scene_key['area_tag']
                    if 'loadMap' in scene_key:
                        # load game_map from external file - setup variables
                        map_area_file = scene_key['loadMap']
                        map_area_max_x = int(scene_key['mapx'])
                        map_area_max_y = int(scene_key['mapy'])
                        game_map = GameMap(mapwidth=map_area_max_x, mapheight=map_area_max_y)
                        logger.info('Map Area File is set to {}', map_area_file)
                    if map_area_file != '':
                        SceneManager.build_static_scene(gameworld=gameworld, game_map=game_map,
                                                        map_area_file=map_area_file, this_scene=scene_key)
                        GameMap.assign_tiles(game_map=game_map)
                    else:
                        # generate random map
                        SceneManager.generate_game_map(game_map=game_map)
            scorekeeper.ScorekeeperUtilities.set_current_area(gameworld=gameworld, current_area_tag=current_area_tag)
        SceneManager.create_ecs_systems_yes_no(gameworld=gameworld, currentscene=currentscene, game_map=game_map)

        return game_map, map_area_max_x - 1, map_area_max_y - 1, scene_exit

    @staticmethod
    def create_ecs_systems_yes_no(gameworld, currentscene, game_map):
        if currentscene == 1:
            update_entities_processor = updateEntities.UpdateEntitiesProcessor(gameworld=gameworld, game_map=game_map)
            move_entities_processor = move_entities.MoveEntities(gameworld=gameworld, game_map=game_map)
            cast_spells_processor = castSpells.CastSpells(gameworld=gameworld, game_map=game_map)
            render_message_log_processor = renderMessageLog.RenderMessageLog(gameworld=gameworld)
            spell_info_processor = renderSpellInfoPanel.RenderSpellInfoPanel(gameworld=gameworld, game_map=game_map)
            gameworld.add_processor(cast_spells_processor, priority=100)
            gameworld.add_processor(update_entities_processor, priority=90)
            gameworld.add_processor(move_entities_processor, priority=80)
            gameworld.add_processor(render_message_log_processor, priority=60)
            gameworld.add_processor(spell_info_processor, priority=50)

        render_ui_processor = renderUI.RenderUI(game_map=game_map, gameworld=gameworld)
        gameworld.add_processor(render_ui_processor, priority=70)

    @staticmethod
    # haven't created the proc-gen routines for this
    def generate_game_map(game_map):
        pass

    @staticmethod
    def build_static_scene(gameworld, game_map, map_area_file, this_scene):
        # get config items
        significant_npcs = this_scene['npcs']
        all_races = this_scene['races']
        game_config = configUtilities.load_config()
        prefab_folder = constants.FILE_PREFABFOLDER
        tile_type_wall = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                     parameter='TILE_TYPE_WALL')
        tile_type_floor = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='TILE_TYPE_FLOOR')
        tile_type_door = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                     parameter='TILE_TYPE_DOOR')
        tile_type_empty = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='TILE_TYPE_EMPTY')
        tile_type_dungeon_entrance = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='TILE_TYPE_DUNGEON_ENTRANCE')
        tile_type_guard_hut = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='TILE_TYPE_GUARD_HUT')
        # now load the game_map from the external file/csv
        filepath = prefab_folder + map_area_file + '.txt'

        file_content = externalfileutilities.Externalfiles.load_existing_file(filename=filepath)
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
                SceneManager.place_empty_tile_yes_no(cell=cell, game_map=game_map, posx=posx, posy=posy,
                                                     tile_type=tile_type_empty)
                player_placed = SceneManager.place_player_tile_yes_no(cell=cell, game_map=game_map, posx=posx,
                                                                      posy=posy, tile_type=tile_type_floor)

                if player_placed:
                    player_entity = mobileHelp.MobileUtilities.get_player_entity(gameworld=gameworld)
                    SceneManager.setup_viewport(gameworld=gameworld, posx=posx, posy=posy, player_entity=player_entity)
                    GameMapUtilities.set_entity_at_this_map_location(game_map=game_map, x=posx, y=posy, entity=player_entity)
                    logger.debug('Player placed at map pos {} / {}', posx, posy)

                # add named NPCs to scene
                npc_list_ids = "ABCEDFG"
                if cell.upper() in npc_list_ids:
                    cc = cell.upper()
                    idx = npc_list_ids.index(cc)
                    this_npc = significant_npcs[idx]
                    new_entity = NewEntity.build_named_npc(gameworld=gameworld, game_config=game_config, posx=posx, posy=posy, this_npc=this_npc, cell=cell)
                    # --- PLACE NEW ENTITY ON TO GAME MAP -
                    if new_entity > 0:
                        GameMapUtilities.set_entity_at_this_map_location(game_map=game_map, x=posx, y=posy,
                                                                         entity=new_entity)
                        SceneManager.place_floor_tile_yes_no(cell=cell, posx=posx, posy=posy, tile_type=tile_type_floor,
                                                             game_map=game_map)
                # add stationary building
                buildings = "123456789"
                if cell in buildings:
                    this_building = int(cell)
                    if this_building == tile_type_dungeon_entrance:
                        SceneManager.place_dungeon_entrance_yes_or_no(cell=this_building, game_map=game_map, posx=posx, posy=posy, tile_type=tile_type_dungeon_entrance)
                    else:
                        SceneManager.place_guard_hut_yes_or_no(cell=this_building, game_map=game_map, posx=posx, posy=posy, tile_type=tile_type_guard_hut)

                # create random enemy
                if cell.upper() == 'X':
                    # set enemy race
                    allowed_races = []

                    for rc in all_races:
                        if rc['available'] == 'true':
                            allowed_races.append(rc['name'])
                    if len(allowed_races) > 0:
                        chosen_race_id = random.randrange(len(allowed_races))
                        chosen_race_name = allowed_races[chosen_race_id]
                    else:
                        logger.warning('NO AVAILABLE RACES FOR THIS SCENE')

                    new_entity = NewEntity.build_random_enemy(gameworld=gameworld, cell=cell, game_config=game_config, posx=posx, posy=posy, chosen_race_name=chosen_race_name)
                    # --- PLACE NEW ENTITY ON TO GAME MAP -
                    if new_entity > 0:
                        GameMapUtilities.set_entity_at_this_map_location(game_map=game_map, x=posx, y=posy,
                                                                         entity=new_entity)
                        SceneManager.place_floor_tile_yes_no(cell=cell, posx=posx, posy=posy, tile_type=tile_type_floor,
                                                             game_map=game_map)
                posx += 1
            posy += 1

    @staticmethod
    def place_guard_hut_yes_or_no(cell, game_map, posx, posy, tile_type):
        if cell == 9:
            game_map.tiles[posx][posy].type_of_tile = tile_type
            game_map.tiles[posx][posy].image = 10
            game_map.tiles[posx][posy].blocked = True
            game_map.tiles[posx][posy].block_sight = True

    @staticmethod
    def place_dungeon_entrance_yes_or_no(cell, game_map, posx, posy, tile_type):
        if cell == 9:
            game_map.tiles[posx][posy].type_of_tile = tile_type
            game_map.tiles[posx][posy].image = 11
            game_map.tiles[posx][posy].blocked = True
            game_map.tiles[posx][posy].block_sight = True

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
    def setup_viewport(gameworld, posx, posy, player_entity):
        mobileHelp.MobileUtilities.set_mobile_position(gameworld=gameworld, entity=player_entity, posx=posx, posy=posy)
