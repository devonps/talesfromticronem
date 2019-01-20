
from loguru import logger
from newGame.initialiseNewGame import setup_game, generate_player_character, load_weapon_with_spells, create_wizard
from components import spells, weapons, mobiles
from newGame.ClassWeapons import WeaponClass

from utilities.spellHelp import SpellUtilities
from utilities.mobileHelp import MobileUtilities


def for_testing(gameworld):
    for _, (name, desc, slot) in gameworld.get_components(weapons.Name, weapons.Describable, weapons.Spells):

        spell_name_component = gameworld.component_for_entity(slot.slot_four, spells.Name)
        print(name.label, spell_name_component.label)
        spell_name_component = gameworld.component_for_entity(slot.slot_five, spells.Name)
        print(name.label, spell_name_component.label)


def main():

#    logger.add(constants.LOGFILE, format=constants.LOGFORMAT)

    logger.info('********************')
    logger.info('* New game started *')
    logger.info('********************')

    gameworld = setup_game()

    # for_testing(world)

    # create the player
    player = generate_player_character(gameworld, 'necromancer')
    player_name = gameworld.component_for_entity(player, mobiles.Name)
    class_component = gameworld.component_for_entity(player, mobiles.CharacterClass)

    # confirm the weapon is equipped
    # get the entity id for the equipped weapon
    # weapon_equipped = List of weapons equipped always returned in order: main, off, both hands

    weapons_equipped = MobileUtilities.get_weapons_equipped(gameworld, player)

    wpns = ''

    if weapons_equipped[0] > 0:
        wpn_name = gameworld.component_for_entity(weapons_equipped[0], weapons.Name)
        wpns = wpn_name.label + ' in his main hand'

    if weapons_equipped[1] > 0:
        if weapons_equipped[0] > 0:
            wpns = wpns + ' and a '
        wpn_name = gameworld.component_for_entity(weapons_equipped[1], weapons.Name)
        wpns = wpns + wpn_name.label + ' in his off hand'

    if weapons_equipped[2] > 0:
        wpn_name = gameworld.component_for_entity(weapons_equipped[2], weapons.Name)
        wpns = wpn_name.label + ' in both his hands'

    print(player_name.first + ' the ' + class_component.label + ' is holding a ' + wpns)

    thiswizard = create_wizard(gameworld)

    wizard_name = gameworld.component_for_entity(thiswizard, mobiles.Name)
    class_component = gameworld.component_for_entity(thiswizard, mobiles.CharacterClass)

    # get the weapon name component

    weapons_equipped = MobileUtilities.get_weapons_equipped(gameworld, thiswizard)

    wpns = ''

    if weapons_equipped[0] > 0:
        wpn_name = gameworld.component_for_entity(weapons_equipped[0], weapons.Name)
        wpns = wpn_name.label + ' in his main hand'

    if weapons_equipped[1] > 0:
        if weapons_equipped[0] > 0:
            wpns = wpns + ' and a '
        wpn_name = gameworld.component_for_entity(weapons_equipped[1], weapons.Name)
        wpns = wpns + wpn_name.label + ' in his off hand'

    if weapons_equipped[2] > 0:
        wpn_name = gameworld.component_for_entity(weapons_equipped[2], weapons.Name)
        wpns = wpn_name.label + ' in both his hands'

    print(wizard_name.first + ' the ' + class_component.label + ' is holding a ' + wpns)


if __name__ == '__main__':
    main()