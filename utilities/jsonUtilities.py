import json
from loguru import logger


def read_json_file(filename):

    logger.info('Reading Json file {}', filename)

    with open(filename) as f:
        data = json.loads(f.read())
        return data


# data is a json object
def write_to_json_file(data, filename):
    logger.info('Writing Json file {}', filename)
    with open('filename', 'w') as f:
        json.dump(data, f)


def get_count_of_items(filename, element):
    return len(filename[element])