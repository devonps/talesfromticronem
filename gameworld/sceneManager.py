from components import mobiles
from mapRelated.gameMap import GameMap
from processors.move_entities import MoveEntities
from processors.renderGameMap import RenderGameMap
from processors.updateEntities import UpdateEntitiesProcessor
from utilities import configUtilities, colourUtilities
from loguru import logger

from utilities.externalfileutilities import Externalfiles
from utilities.jsonUtilities import read_json_file
from utilities.mobileHelp import MobileUtilities


class SceneManager:

    @staticmethod
    def newScene(console, currentscene, gameConfig, gameworld):
        SceneManager.loadSceneCard(console=console, currentscene=currentscene, game_config=gameConfig, gameworld=gameworld)
        SceneManager.generateGameMap()

    @staticmethod
    def loadSceneCard(console, currentscene, game_config, gameworld):
        # load scene list into memory
        sceneList = configUtilities.get_config_value_as_list(game_config, 'game', 'SCENES')
        sceneFound = False
        thisScene = 0
        prefabFolder = ''

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
                    if 'loadMap' in sceneKey:
                        # load game_map from external file - setup variables
                        mapAreaFile = sceneKey['loadMap']
                        mapAreaMaxX = int(sceneKey['mapx'])
                        mapAreaMaxY = int(sceneKey['mapy'])
                        prefabFolder = configUtilities.get_config_value_as_string(game_config, 'default',
                                                                                  'PREFABFOLDER')
                        game_map = GameMap(mapwidth=mapAreaMaxX, mapheight=mapAreaMaxY)

                    logger.debug('The {} scene exits to the {}', scene_name,  scene_exits)

                    if mapAreaFile != '':
                        # now load the game_map from the external file/csv
                        filepath = prefabFolder + mapAreaFile + '.csv'
                        csvContent = Externalfiles.read_prefab_from_csv(filename=filepath)
                        for row in csvContent:
                            posx = int(row[0])
                            posy = int(row[1])
                            char = int(row[2])
                            fg = row[3]
                            bg = row[4]
                            game_map.tiles[posx][posy].type_of_tile = char
                            game_map.tiles[posx][posy].blocked = False
                            game_map.tiles[posx][posy].block_sight = False

                            if char > 184:
                                # wall tile
                                game_map.tiles[posx][posy].blocked = True

                            if char == 115:
                                # place the player
                                game_map.tiles[posx][posy].type_of_tile = 32
                                playerEntity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
                                gameworld.add_component(playerEntity, mobiles.Position(x=posx, y=posy, hasMoved=True))

                        logger.info('Scene uses external file called {}', mapAreaFile)
                        logger.info('The map dimensions are {} by {}', mapAreaMaxX, mapAreaMaxY)

        if currentscene == 1:
            renderGameMapProcessor = RenderGameMap(con=console, game_map=game_map, gameworld=gameworld)
            move_entities_processor = MoveEntities(gameworld=gameworld, game_map=game_map)
            update_entities_processor = UpdateEntitiesProcessor(gameworld=gameworld)
            gameworld.add_processor(renderGameMapProcessor)
            gameworld.add_processor(move_entities_processor)
            gameworld.add_processor(update_entities_processor)

    @staticmethod
    def generateGameMap():
        pass