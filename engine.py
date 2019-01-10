
from loguru import logger
from newGame.initialiseNewGame import setup_game
from components import spells, weapons


def main():

#    logger.add(constants.LOGFILE, format=constants.LOGFORMAT)

    logger.info('********************')
    logger.info('* New game started *')
    logger.info('********************')

    world = setup_game()

    for ent, (name, desc, slot) in world.get_components(weapons.Name, weapons.Describable, weapons.Spells):
        spell_name_component = world.component_for_entity(slot.slot_three, spells.Name)
        print(spell_name_component.label)


if __name__ == '__main__':
    main()