
from utilities import configUtilities
from utilities.externalfileutilities import Externalfiles
from loguru import logger


def load_prefab():
    game_config = configUtilities.load_config()
    file_name = 'startArea.csv'

    prefab_folder = configUtilities.get_config_value_as_string(game_config, 'files', 'PREFABFOLDER')

    filepath = prefab_folder + file_name

    # does file exist
    file_exists = Externalfiles.does_file_exist(filepath)

    logger.info('Checking if external file exists...{}', file_exists)

    # load the file and check the contents
    csv_content = Externalfiles.read_prefab_from_csv(filename=filepath)
    for row in csv_content:
        logger.info(row)

