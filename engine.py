import tcod
import json

from newGame.initialiseNewGame import get_constants
from utilities.jsonUtilities import read_json_file
from loguru import logger


def main():

    constants = get_constants()

    logger.add(constants['logfile'], format=constants['logformat'])

    logger.info('********************')
    logger.info('* New game started *')
    logger.info('********************')

    weapons = read_json_file(constants['Json_file_path'] + 'weapons.json')
    for weapon in weapons['weapons']:
        print(weapon['display_name'])

    mobiles = read_json_file(constants['Json_file_path'] + 'mobiles.json')

    for mobile in mobiles['mobiles']:
        print('The ' + mobile['name'] + ' is a type of ' + mobile['type'], )
        if 'variations' in mobile:
            print('The ' + mobile['name'] + ' has variations')
            variations = mobile['variations']
            for k in variations:
                print('The ' + mobile['name'] + ' is now a ' + mobile['name'] + ' ' + k['suffix'] +
                      ' and is now equipped with a ' + k['equipment'])





if __name__ == '__main__':
    main()