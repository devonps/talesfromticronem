
from loguru import logger
from newGame.initialiseNewGame import setup_game
from components import shared, condis, spellBoons


def main():

#    logger.add(constants.LOGFILE, format=constants.LOGFORMAT)

    logger.info('********************')
    logger.info('* New game started *')
    logger.info('********************')

    world = setup_game()

    for _, (name, desc, cond, boon) in world.get_components(shared.Name, shared.Description,
                                                                condis.Bleeding, spellBoons.Regeneration):
        print(name.text + ' lasts for: ' + str(cond.lasts_for) + ' turns.')
        print(name.text + ' regen max stacks: ' + str(boon.max_stacks))


if __name__ == '__main__':
    main()