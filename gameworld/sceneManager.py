from components import mobiles
from mapRelated.gameMap import GameMap
from newGame.Entities import Entity
from processors.move_entities import MoveEntities
from processors.renderGameMap import RenderGameMap
from processors.updateEntities import UpdateEntitiesProcessor
from processors.renderMessageLog import RenderMessageLog
from utilities import configUtilities
from loguru import logger

from utilities.common import CommonUtils
from utilities.externalfileutilities import Externalfiles
from utilities.jsonUtilities import read_json_file
from utilities.mobileHelp import MobileUtilities
from mapRelated.camera import Camera


class SceneManager:

    @staticmethod
    def newScene(currentscene, gameworld):

        gm, mx, my = SceneManager.loadSceneCard(currentscene=currentscene, gameworld=gameworld)
        SceneManager.prettify_the_map(game_map=gm, maxX=mx, maxY=my)
        SceneManager.generateGameMap()

    @staticmethod
    def loadSceneCard(currentscene, gameworld):
        # load scene list into memory
        # get config items
        game_config = configUtilities.load_config()

        sceneList = configUtilities.get_config_value_as_list(game_config, 'game', 'SCENES')
        sceneFound = False
        thisScene = 0
        prefabFolder = ''
        tile_type_wall = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                     parameter='TILE_TYPE_WALL')
        tile_type_floor = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='TILE_TYPE_FLOOR')
        tile_type_door = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                     parameter='TILE_TYPE_DOOR')
        # if currentscene == 1:
        #     map_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='game',
        #                                                             parameter='MAP_WIDTH')
        #     map_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='game',
        #                                                              parameter='MAP_HEIGHT')
        for sceneID, sceneName in enumerate(sceneList, 1):
            if sceneID == currentscene:
                logger.debug('Current scene set to {}', sceneName)
                sceneFound = True
                thisScene = sceneName

        if sceneFound:
            mapAreaFile = ''
            mapAreaMaxX = 0
            mapAreaMaxY = 0
            sceneFile = 'scenes.json'
            scene_file = read_json_file('static/scenes/' + sceneFile)
            for sceneKey in scene_file['scenes']:
                if sceneKey['name'] == thisScene:
                    scene_name = sceneKey['name']
                    scene_exits = sceneKey['sceneExits']
                    logger.debug('The {} scene exits to the {}', scene_name,  scene_exits)
                    if 'loadMap' in sceneKey:
                        # load game_map from external file - setup variables
                        mapAreaFile = sceneKey['loadMap']
                        mapAreaMaxX = int(sceneKey['mapx'])
                        mapAreaMaxY = int(sceneKey['mapy'])
                        prefabFolder = configUtilities.get_config_value_as_string(game_config, 'default',
                                                                                  'PREFABFOLDER')
                        game_map = GameMap(mapwidth=mapAreaMaxX, mapheight=mapAreaMaxY)

                    if mapAreaFile != '':
                        # now load the game_map from the external file/csv
                        filepath = prefabFolder + mapAreaFile + '.txt'

                        fileContent = Externalfiles.load_existing_file(filename=filepath)
                        posy = 0

                        for row in fileContent:
                            posx = 0
                            for cell in row:
                                # floor tile
                                if cell == '.':
                                    game_map.tiles[posx][posy].type_of_tile = tile_type_floor
                                    game_map.tiles[posx][posy].image = 4
                                    game_map.tiles[posx][posy].blocked = False
                                    game_map.tiles[posx][posy].block_sight = False
                                if cell == '+':
                                    # door tile
                                    game_map.tiles[posx][posy].type_of_tile = tile_type_door
                                    game_map.tiles[posx][posy].image = 10
                                    game_map.tiles[posx][posy].blocked = True
                                    game_map.tiles[posx][posy].block_sight = True
                                    logger.debug('closed door x/y {}/{}', posx, posy)
                                if cell == '#':
                                    # wall tile
                                    game_map.tiles[posx][posy].type_of_tile = tile_type_wall
                                    game_map.tiles[posx][posy].image = 9
                                    game_map.tiles[posx][posy].blocked = True
                                    game_map.tiles[posx][posy].block_sight = True

                                if cell == '@':
                                    # place the player
                                    game_map.tiles[posx][posy].type_of_tile = tile_type_floor
                                    game_map.tiles[posx][posy].blocked = False
                                    game_map.tiles[posx][posy].image = 11
                                    game_map.tiles[posx][posy].block_sight = False
                                    playerEntity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
                                    viewport_entity = MobileUtilities.get_viewport_id(gameworld=gameworld,entity=playerEntity)
                                    MobileUtilities.set_mobile_position(gameworld=gameworld, entity=playerEntity, posx=posx, posy=posy)

                                    vpx = MobileUtilities.get_mobile_x_position(gameworld=gameworld,entity=playerEntity)
                                    vpy = MobileUtilities.get_mobile_y_position(gameworld=gameworld,entity=playerEntity)

                                    CommonUtils.set_player_viewport_position_x(gameworld=gameworld, viewport_id=viewport_entity,
                                                                               posx=vpx)
                                    CommonUtils.set_player_viewport_position_y(gameworld=gameworld, viewport_id=viewport_entity,
                                                                               posy=vpy)
                                if cell in 'ABCDEFG':
                                    npcs = sceneKey['npcs']
                                    npc_name = npcs[0]['displayName']
                                    logger.debug('NPC Name {}', npc_name)
                                    enemyObject = Entity(gameworld=gameworld)
                                    enemy_id = enemyObject.create_new_entity()
                                    enemyObject.create_new_enemy(entity_id=enemy_id)

                                    plx = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=playerEntity)
                                    ply = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=playerEntity)

                                    MobileUtilities.set_mobile_position(gameworld=gameworld, entity=enemy_id, posx=plx + 5,
                                                                        posy=ply + 5)

                                posx += 1
                            posy += 1
                    else:
                        # generate random map
                        pass

        if currentscene == 1:
            renderGameMapProcessor = RenderGameMap(game_map=game_map, gameworld=gameworld)
            move_entities_processor = MoveEntities(gameworld=gameworld, game_map=game_map)
            update_entities_processor = UpdateEntitiesProcessor(gameworld=gameworld)
            gameworld.add_processor(renderGameMapProcessor)
            renderMessageLogProcessor = RenderMessageLog(gameworld=gameworld)
            gameworld.add_processor(move_entities_processor)
            gameworld.add_processor(update_entities_processor)
            gameworld.add_processor(renderMessageLogProcessor)

        return game_map, mapAreaMaxX - 1, mapAreaMaxY - 1

    @staticmethod
    def generateGameMap():
        pass

    @staticmethod
    def prettify_the_map(game_map, maxX, maxY):
        game_config = configUtilities.load_config()
        render_style = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                   parameter='render_style')

        tile_type_wall = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                     parameter='TILE_TYPE_WALL')
        tile_type_floor = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',parameter='TILE_TYPE_FLOOR')
        FLOOR_TOP_LEFT = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='FLOOR_TOP_LEFT')
        FLOOR_TOP_MIDDLE = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='FLOOR_TOP_MIDDLE')
        FLOOR_TOP_RIGHT = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='FLOOR_TOP_RIGHT')
        FLOOR_LEFT = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='FLOOR_LEFT')
        FLOOR_MIDDLE = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='FLOOR_MIDDLE')
        FLOOR_RIGHT = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='FLOOR_RIGHT')
        FLOOR_BOTTOM_LEFT = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='FLOOR_BOTTOM_LEFT')
        FLOOR_BOTTOM_MIDDLE = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='FLOOR_BOTTOM_MIDDLE')
        FLOOR_BOTTOM_RIGHT = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='FLOOR_BOTTOM_RIGHT')
        WALL_TOP = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='WALL_TOP')
        CLOSED_DOOR = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='CLOSED_DOOR')
        WALL_TOP_LEFT = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='WALL_TOP_LEFT')
        WALL_TOP_RIGHT = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='WALL_TOP_RIGHT')
        WALL_CENTRAL = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='WALL_CENTRAL')
        WALL_BOTTOM_LEFT = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='WALL_BOTTOM_LEFT')
        WALL_BOTTOM_RIGHT = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='WALL_BOTTOM_RIGHT')
        WALL_T_JUNCTION_RIGHT = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='WALL_T_JUNCTION_RIGHT')
        WALL_T_JUNCTION_LEFT = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='WALL_T_JUNCTION_LEFT')
        WALL_T_JUNCTION_TOP = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='WALL_T_JUNCTION_TOP')
        WALL_T_JUNCTION_BOTTOM = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='WALL_T_JUNCTION_BOTTOM')

        logger.info('mx my {} {}', maxX, maxY)
        for yy in range(maxY):
            for xx in range(maxX):
                if game_map.tiles[xx][yy].type_of_tile == tile_type_floor:
                    # top left
                    if (game_map.tiles[xx - 1][yy].blocked is True) and (game_map.tiles[xx][yy - 1].blocked is True) and \
                            (game_map.tiles[xx + 1][yy].blocked is False) and (game_map.tiles[xx][yy + 1].blocked is False):
                        game_map.tiles[xx][yy].image = FLOOR_TOP_LEFT
                    # top middle
                    if (game_map.tiles[xx - 1][yy].blocked is False) and (game_map.tiles[xx][yy - 1].blocked is True) and \
                            (game_map.tiles[xx + 1][yy].blocked is False) and (game_map.tiles[xx][yy + 1].blocked is False):
                        game_map.tiles[xx][yy].image = FLOOR_TOP_MIDDLE
                    # top right
                    if (game_map.tiles[xx - 1][yy].blocked is False) and (game_map.tiles[xx][yy - 1].blocked is True) and \
                            (game_map.tiles[xx + 1][yy].blocked is True) and (game_map.tiles[xx][yy + 1].blocked is False):
                        game_map.tiles[xx][yy].image = FLOOR_TOP_RIGHT
                    # middle left
                    if (game_map.tiles[xx - 1][yy].blocked is True) and (game_map.tiles[xx][yy - 1].blocked is False) and \
                            (game_map.tiles[xx + 1][yy].blocked is False) and (game_map.tiles[xx][yy + 1].blocked is False):
                        game_map.tiles[xx][yy].image = FLOOR_LEFT
                    # middle middle
                    if (game_map.tiles[xx - 1][yy].blocked is False) and (game_map.tiles[xx][yy - 1].blocked is False) and \
                            (game_map.tiles[xx + 1][yy].blocked is False) and (game_map.tiles[xx][yy + 1].blocked is False):
                        game_map.tiles[xx][yy].image = FLOOR_MIDDLE
                    # middle right
                    if (game_map.tiles[xx - 1][yy].blocked is False) and (game_map.tiles[xx][yy - 1].blocked is False) and \
                            (game_map.tiles[xx + 1][yy].blocked is True) and (game_map.tiles[xx][yy + 1].blocked is False):
                        game_map.tiles[xx][yy].image = FLOOR_RIGHT
                    # bottom left
                    if (game_map.tiles[xx - 1][yy].blocked is True) and (game_map.tiles[xx][yy - 1].blocked is False) and \
                            (game_map.tiles[xx + 1][yy].blocked is False) and (game_map.tiles[xx][yy + 1].blocked is True):
                        game_map.tiles[xx][yy].image = FLOOR_BOTTOM_LEFT
                    # bottom middle
                    if (game_map.tiles[xx - 1][yy].blocked is False) and (game_map.tiles[xx][yy - 1].blocked is False) and \
                            (game_map.tiles[xx + 1][yy].blocked is False) and (game_map.tiles[xx][yy + 1].blocked is True):
                        game_map.tiles[xx][yy].image = FLOOR_BOTTOM_MIDDLE
                    # bottom right
                    if (game_map.tiles[xx - 1][yy].blocked is False) and (game_map.tiles[xx][yy - 1].blocked is False) and \
                            (game_map.tiles[xx + 1][yy].blocked is True) and (game_map.tiles[xx][yy + 1].blocked is True):
                        game_map.tiles[xx][yy].image = FLOOR_BOTTOM_RIGHT

                if game_map.tiles[xx][yy].type_of_tile == tile_type_wall:
                    # top left
                    if xx == 0 and yy == 0:
                        game_map.tiles[xx][yy].image = WALL_TOP_LEFT
                    # top right
                    if xx == maxX - 1 and yy == 0:
                        game_map.tiles[xx][yy].image = WALL_TOP_RIGHT
                    # bottom left
                    if xx == 0 and yy == maxY - 1:
                        game_map.tiles[xx][yy + 1].image = WALL_BOTTOM_LEFT
                    # bottom right
                    if xx == maxX - 1 and yy == maxY - 1:
                        game_map.tiles[xx][yy + 1].image = WALL_BOTTOM_RIGHT
                        logger.info('wall bottom right')
                    # left edge wall
                    if xx == 0 and (yy > 0 and maxY - 2):
                        if game_map.tiles[xx + 1][yy].type_of_tile == tile_type_floor:
                            game_map.tiles[xx][yy].image = WALL_CENTRAL
                    # top edge wall
                    if xx > 0 and yy == 0:
                        game_map.tiles[xx][yy].image = WALL_TOP

                    # vertical central wall flanked by floor both sides
                    if xx > 0 and (0 < yy < maxY):
                        if game_map.tiles[xx - 1][yy].type_of_tile == tile_type_floor and game_map.tiles[xx + 1][yy].type_of_tile == tile_type_floor:
                            game_map.tiles[xx][yy].image = WALL_CENTRAL
                    # right wall
                    if xx == maxX - 1 and (0 < yy < maxY):
                        game_map.tiles[xx][yy].image = WALL_CENTRAL
                    # inside top left
                    if xx > 0 and yy > 0:
                        if game_map.tiles[xx - 1][yy].type_of_tile == tile_type_floor and game_map.tiles[xx + 1][yy].type_of_tile == tile_type_wall:
                            if game_map.tiles[xx][yy - 1].type_of_tile == tile_type_floor and game_map.tiles[xx][yy + 1].type_of_tile == tile_type_wall:
                                game_map.tiles[xx][yy].image = WALL_TOP_LEFT
                    # inside top right
                    if xx > 0 and yy > 0:
                        if game_map.tiles[xx - 1][yy].type_of_tile == tile_type_wall and game_map.tiles[xx + 1][yy].type_of_tile == tile_type_floor:
                            if game_map.tiles[xx][yy - 1].type_of_tile == tile_type_floor and game_map.tiles[xx][yy + 1].type_of_tile == tile_type_wall:
                                game_map.tiles[xx][yy].image = WALL_TOP_RIGHT

                    # inside bottom left
                    if xx > 0 and yy > 0:
                        if game_map.tiles[xx - 1][yy].type_of_tile == tile_type_floor and game_map.tiles[xx + 1][yy].type_of_tile == tile_type_wall:
                            if game_map.tiles[xx][yy - 1].type_of_tile == tile_type_wall and game_map.tiles[xx][yy + 1].type_of_tile == tile_type_floor:
                                game_map.tiles[xx][yy].image = WALL_BOTTOM_LEFT
                    # inside bottom right
                    if xx > 0 and yy > 0:
                        if game_map.tiles[xx - 1][yy].type_of_tile == tile_type_wall and game_map.tiles[xx + 1][yy].type_of_tile == tile_type_floor:
                            if game_map.tiles[xx][yy - 1].type_of_tile == tile_type_wall and game_map.tiles[xx][yy + 1].type_of_tile == tile_type_floor:
                                game_map.tiles[xx][yy].image = WALL_BOTTOM_RIGHT

                    # |- junction
                    if 0 < yy < maxY:
                        if xx < maxX - 1:
                            if game_map.tiles[xx][yy - 1].type_of_tile == tile_type_wall and game_map.tiles[xx][yy + 1].type_of_tile == tile_type_wall:
                                if game_map.tiles[xx + 1][yy].type_of_tile == tile_type_wall:
                                    game_map.tiles[xx][yy].image = WALL_T_JUNCTION_RIGHT
                    # -| junction
                    if 0 < yy < maxY:
                        if xx > 0:
                            if game_map.tiles[xx][yy - 1].type_of_tile == tile_type_wall and game_map.tiles[xx][yy + 1].type_of_tile == tile_type_wall:
                                if game_map.tiles[xx -1][yy].type_of_tile == tile_type_wall:
                                    game_map.tiles[xx][yy].image = WALL_T_JUNCTION_LEFT
                    # T junction
                    if 0 < xx < maxX - 1:
                        if game_map.tiles[xx - 1][yy].type_of_tile == tile_type_wall and game_map.tiles[xx + 1][yy].type_of_tile == tile_type_wall:
                            if game_map.tiles[xx][yy + 1].type_of_tile == tile_type_wall:
                                game_map.tiles[xx][yy].image = WALL_T_JUNCTION_TOP

                    # _|_ junction
                    if 0 < xx < maxX - 1:
                        if 0 < yy < maxY - 1:
                            if game_map.tiles[xx - 1][yy].type_of_tile == tile_type_wall and game_map.tiles[xx + 1][yy].type_of_tile == tile_type_wall:
                                if game_map.tiles[xx][yy - 1].type_of_tile == tile_type_wall:
                                    game_map.tiles[xx][yy].image = WALL_T_JUNCTION_BOTTOM

