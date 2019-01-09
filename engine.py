
from loguru import logger
from newGame.initialiseNewGame import setup_game
from components import spells


def main():

#    logger.add(constants.LOGFILE, format=constants.LOGFORMAT)

    logger.info('********************')
    logger.info('* New game started *')
    logger.info('********************')

    world = setup_game()

    # the following code will get the entity id (stored in ent) for
    for ent, (name, cl, wpn, slot) in world.get_components(spells.Name, spells.ClassName, spells.WeaponType, spells.WeaponSlot):
        if cl.label == 'necromancer' and wpn.label == 'staff':
            print('Spell ' + name.label + '(' + str(ent) + ') is attached to a ' + cl.label + 's ' + wpn.label + ' in slot ' + str(slot.slot))


if __name__ == '__main__':
    main()