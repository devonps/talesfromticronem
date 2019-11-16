from components import mobiles
from mapRelated.gameMap import GameMap
from processors.move_entities import MoveEntities
from processors.renderGameMap import RenderGameMap
from processors.updateEntities import UpdateEntitiesProcessor
from utilities import configUtilities
from loguru import logger

from utilities.externalfileutilities import Externalfiles
from utilities.jsonUtilities import read_json_file
from utilities.mobileHelp import MobileUtilities


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
                                    gameworld.add_component(playerEntity, mobiles.Position(x=posx, y=posy, hasMoved=True))
                                posx += 1
                            posy += 1
                        logger.info('Scene uses external file called {}', mapAreaFile)
                        logger.info('The map dimensions are {} by {}', mapAreaMaxX, mapAreaMaxY)
                    else:
                        # generate random map
                        pass

        if currentscene == 1:
            renderGameMapProcessor = RenderGameMap(game_map=game_map, gameworld=gameworld)
            move_entities_processor = MoveEntities(gameworld=gameworld, game_map=game_map)
            update_entities_processor = UpdateEntitiesProcessor(gameworld=gameworld)
            gameworld.add_processor(renderGameMapProcessor)
            gameworld.add_processor(move_entities_processor)
            gameworld.add_processor(update_entities_processor)

        return game_map, mapAreaMaxX - 1, mapAreaMaxY - 1

    @staticmethod
    def generateGameMap():
        pass

    @staticmethod
    def prettify_the_map(game_map, maxX, maxY):
        game_config = configUtilities.load_config()
        tile_type_wall = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                     parameter='TILE_TYPE_WALL')
        tile_type_floor = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='TILE_TYPE_FLOOR')
        logger.info('mx my {} {}', maxX, maxY)
        for yy in range(maxY):
            for xx in range(maxX):
                if game_map.tiles[xx][yy].type_of_tile == tile_type_floor:
                    # top left
                    if (game_map.tiles[xx - 1][yy].blocked is True) and (game_map.tiles[xx][yy - 1].blocked is True) and \
                            (game_map.tiles[xx + 1][yy].blocked is False) and (game_map.tiles[xx][yy + 1].blocked is False):
                        game_map.tiles[xx][yy].image = 0
                    # top middle
                    if (game_map.tiles[xx - 1][yy].blocked is False) and (game_map.tiles[xx][yy - 1].blocked is True) and \
                            (game_map.tiles[xx + 1][yy].blocked is False) and (game_map.tiles[xx][yy + 1].blocked is False):
                        game_map.tiles[xx][yy].image = 1
                    # top right
                    if (game_map.tiles[xx - 1][yy].blocked is False) and (game_map.tiles[xx][yy - 1].blocked is True) and \
                            (game_map.tiles[xx + 1][yy].blocked is True) and (game_map.tiles[xx][yy + 1].blocked is False):
                        game_map.tiles[xx][yy].image = 2
                    # middle left
                    if (game_map.tiles[xx - 1][yy].blocked is True) and (game_map.tiles[xx][yy - 1].blocked is False) and \
                            (game_map.tiles[xx + 1][yy].blocked is False) and (game_map.tiles[xx][yy + 1].blocked is False):
                        game_map.tiles[xx][yy].image = 3
                    # middle middle
                    if (game_map.tiles[xx - 1][yy].blocked is False) and (game_map.tiles[xx][yy - 1].blocked is False) and \
                            (game_map.tiles[xx + 1][yy].blocked is False) and (game_map.tiles[xx][yy + 1].blocked is False):
                        game_map.tiles[xx][yy].image = 4
                    # middle right
                    if (game_map.tiles[xx - 1][yy].blocked is False) and (game_map.tiles[xx][yy - 1].blocked is False) and \
                            (game_map.tiles[xx + 1][yy].blocked is True) and (game_map.tiles[xx][yy + 1].blocked is False):
                        game_map.tiles[xx][yy].image = 5
                    # bottom left
                    if (game_map.tiles[xx - 1][yy].blocked is True) and (game_map.tiles[xx][yy - 1].blocked is False) and \
                            (game_map.tiles[xx + 1][yy].blocked is False) and (game_map.tiles[xx][yy + 1].blocked is True):
                        game_map.tiles[xx][yy].image = 6
                    # bottom middle
                    if (game_map.tiles[xx - 1][yy].blocked is False) and (game_map.tiles[xx][yy - 1].blocked is False) and \
                            (game_map.tiles[xx + 1][yy].blocked is False) and (game_map.tiles[xx][yy + 1].blocked is True):
                        game_map.tiles[xx][yy].image = 7
                    # bottom right
                    if (game_map.tiles[xx - 1][yy].blocked is False) and (game_map.tiles[xx][yy - 1].blocked is False) and \
                            (game_map.tiles[xx + 1][yy].blocked is True) and (game_map.tiles[xx][yy + 1].blocked is True):
                        game_map.tiles[xx][yy].image = 8

                if game_map.tiles[xx][yy].type_of_tile == tile_type_wall:
                    # top left
                    if xx == 0 and yy == 0:
                        game_map.tiles[xx][yy].image = 12
                    # top right
                    if xx == maxX - 1 and yy == 0:
                        game_map.tiles[xx][yy].image = 13
                    # bottom left
                    if xx == 0 and yy == maxY - 1:
                        game_map.tiles[xx][yy].image = 15
                    # bottom right
                    if xx == maxX - 1 and yy == maxY - 1:
                        game_map.tiles[xx][yy].image = 16
                    # left wall
                    if xx == 0 and yy > 0:
                        if game_map.tiles[xx + 1][yy].type_of_tile == tile_type_floor:
                            game_map.tiles[xx][yy].image = 14
                    # central wall flanked by floor both sides
                    if xx > 0 and yy > 0:
                        if game_map.tiles[xx - 1][yy].type_of_tile == tile_type_floor and game_map.tiles[xx + 1][yy].type_of_tile == tile_type_floor:
                            game_map.tiles[xx][yy].image = 14
                    # right wall
                    if xx == maxX - 1 and yy > 0:
                        game_map.tiles[xx][yy].image = 14
                    # inside top right
                    if xx > 0 and yy > 0:
                        if game_map.tiles[xx - 1][yy].type_of_tile == tile_type_wall and game_map.tiles[xx + 1][yy].type_of_tile == tile_type_floor:
                            if game_map.tiles[xx][yy - 1].type_of_tile == tile_type_floor and game_map.tiles[xx][yy + 1].type_of_tile == tile_type_wall:
                                game_map.tiles[xx][yy].image = 13
                    # |- junction
                    if 0 < yy < maxY:
                        if xx < maxX - 1:
                            if game_map.tiles[xx][yy - 1].type_of_tile == tile_type_wall and game_map.tiles[xx][yy + 1].type_of_tile == tile_type_wall:
                                if game_map.tiles[xx + 1][yy].type_of_tile == tile_type_wall:
                                    game_map.tiles[xx][yy].image = 17
                    # -| junction
                    if 0 < yy < maxY:
                        if xx > 0:
                            if game_map.tiles[xx][yy - 1].type_of_tile == tile_type_wall and game_map.tiles[xx][yy + 1].type_of_tile == tile_type_wall:
                                if game_map.tiles[xx -1][yy].type_of_tile == tile_type_wall:
                                    game_map.tiles[xx][yy].image = 18
                    # T junction
                    if xx > 0 and xx < maxX - 1:
                        if game_map.tiles[xx - 1][yy].type_of_tile == tile_type_wall and game_map.tiles[xx + 1][yy].type_of_tile == tile_type_wall:
                            if game_map.tiles[xx][yy + 1].type_of_tile == tile_type_wall:
                                game_map.tiles[xx][yy].image = 19
