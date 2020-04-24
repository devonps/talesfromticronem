
from utilities import configUtilities
from utilities.externalfileutilities import Externalfiles
from loguru import logger


def loadPrefab():
    game_config = configUtilities.load_config()
    fileName = 'startArea.csv'

    prefabFolder = configUtilities.get_config_value_as_string(game_config, 'files', 'PREFABFOLDER')

    filepath = prefabFolder + fileName

    # does file exist
    fileExists = Externalfiles.does_file_exist(filepath)

    logger.info('Checking if external file exists...{}', fileExists)

    # load the file and check the contents
    csvContent = Externalfiles.read_prefab_from_csv(filename=filepath)
    for row in csvContent:
        logger.info(row)

