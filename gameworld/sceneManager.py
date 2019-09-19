from mapRelated.fov import FieldOfView
from mapRelated.gameMap import GameMap
from processors.move_entities import MoveEntities
from processors.render import RenderConsole
from processors.updateEntities import UpdateEntitiesProcessor
from utilities import configUtilities
from loguru import logger

from utilities.externalfileutilities import Externalfiles
from utilities.jsonUtilities import read_json_file


class SceneManager:

    @staticmethod
    def newScene(currentscene, gameConfig):
        SceneManager.loadSceneCard(currentscene=currentscene, game_config=gameConfig)
        SceneManager.generateGameMap()

    @staticmethod
    def loadSceneCard(currentscene, game_config):
        # load scene list into memory
        sceneList = configUtilities.get_config_value_as_list(game_config, 'game', 'SCENES')
        sceneFound = False
        thisScene = 0
        prefabFolder = ''
        # map_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='game',
        #                                                         parameter='MAP_WIDTH')
        # map_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='game',
        #                                                          parameter='MAP_HEIGHT')
        # game_map = GameMap(mapwidth=map_width, mapheight=map_height)

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
                    if 'loadMap' in sceneKey:
                        mapAreaFile = sceneKey['loadMap']
                        mapAreaMaxX = int(sceneKey['mapx'])
                        mapAreaMaxY = int(sceneKey['mapy'])
                        prefabFolder = configUtilities.get_config_value_as_string(game_config, 'default',
                                                                                  'PREFABFOLDER')

                    logger.debug('The {} scene exits to the {}', scene_name,  scene_exits)
                    # logger.info('game map height:' + str(game_map.height))
                    if mapAreaFile != '':
                        filepath = prefabFolder + mapAreaFile + '.csv'
                        csvContent = Externalfiles.read_prefab_from_csv(filename=filepath)
                        for row in csvContent:
                            posx = int(row[0])
                            posy = int(row[1])
                            char = int(row[2])
                            fg = row[3]
                            bg = row[4]
                            # game_map.tiles[posx][posy].type_of_tile = char
                            # game_map.tiles[posx][posy].blocked = False
                            # game_map.tiles[posx][posy].block_sight = False


                        logger.info('Scene uses external file called {}', mapAreaFile)
                        logger.info('The map dimensions are {} by {}', mapAreaMaxX, mapAreaMaxY)
                        # logger.info('game_map type is {}', type(game_map))
        # return game_map

    @staticmethod
    def generateGameMap():
        pass