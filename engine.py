
from loguru import logger
from newGame.initialiseNewGame import setup_game, generate_player_character
from components import spells, weapons, mobiles


def main():

#    logger.add(constants.LOGFILE, format=constants.LOGFORMAT)

    logger.info('********************')
    logger.info('* New game started *')
    logger.info('********************')

    world = setup_game()

    for ent, (name, desc, slot) in world.get_components(weapons.Name, weapons.Describable, weapons.Spells):

        spell_name_component = world.component_for_entity(slot.slot_four, spells.Name)
        print(name.label, spell_name_component.label)
        spell_name_component = world.component_for_entity(slot.slot_five, spells.Name)
        print(name.label, spell_name_component.label)

    player = generate_player_character(world)
    player_name = world.component_for_entity(player, mobiles.Name)
    ai_level = world.component_for_entity(player, mobiles.AI)

    print('Player name set as ' + player_name.first)
    print('Player AI set to ' + str(ai_level.ailevel))

if __name__ == '__main__':
    main()