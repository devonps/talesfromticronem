import json
from loguru import logger


def read_json_file(filename):

    logger.info('Reading Json file {}', filename)

    with open('static/data/mobiles.json') as f:
        data = json.loads(f.read())
        return data


# data is a json object
def write_to_json_file(data, filename):
    logger.info('Writing Json file {}', filename)
    with open('filename', 'w') as f:
        json.dump(data, f)