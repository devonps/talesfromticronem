from utilities import configUtilities, externalfileutilities
from loguru import logger


def load_prefab():
    game_config = configUtilities.load_config()
    file_name = 'startArea.csv'

    prefab_folder = configUtilities.get_config_value_as_string(game_config, 'files', 'PREFABFOLDER')

    filepath = prefab_folder + file_name

    # does file exist
    file_exists = externalfileutilities.Externalfiles.does_file_exist(filepath)

    logger.info('Checking if external file exists...{}', file_exists)

    # load the file and check the contents
    csv_content = externalfileutilities.Externalfiles.read_prefab_from_csv(filename=filepath)
    for row in csv_content:
        logger.info(row)

