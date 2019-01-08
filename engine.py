
from loguru import logger
from newGame.initialiseNewGame import setup_game
from components import  spells


def main():

#    logger.add(constants.LOGFILE, format=constants.LOGFORMAT)

    logger.info('********************')
    logger.info('* New game started *')
    logger.info('********************')

    world = setup_game()

    for _, (name, cl, wpn, slot) in world.get_components(spells.Name, spells.ClassName, spells.WeaponType, spells.WeaponSlot):
        if cl.label == 'necromancer' and wpn.label == 'staff':
            print('Spell ' + name.label + ' is attached to a ' + cl.label + 's ' + wpn.label + ' in slot ' + str(slot.slot))


if __name__ == '__main__':
    main()