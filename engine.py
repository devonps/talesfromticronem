
from loguru import logger
from newGame.initialiseNewGame import setup_game, generate_player_character, load_weapon_with_spells
from components import spells, weapons, mobiles
from newGame.ClassWeapons import WeaponClass

from utilities.spellHelp import SpellUtilities


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

    world = setup_game()

    # for_testing(world)

    # create the player
    player = generate_player_character(world, 'necromancer')
    player_name = world.component_for_entity(player, mobiles.Name)
    class_component = world.component_for_entity(player, mobiles.CharacterClass)

    # create a new weapon for the player
    weapon = WeaponClass.create_weapon(world, 'sword')
    weapon_type = world.component_for_entity(weapon, weapons.Name)
    # parameters are: gameworld, weapon object, weapon type as a string, mobile class
    load_weapon_with_spells(world, weapon, weapon_type.label, class_component.label)

    # equip player with weapon
    world.component_for_entity(player, mobiles.Equipped).both_hands = weapon

    # confirm the weapon is equipped
    # get the entity id for the equipped weapon
    weapon_equipped = world.component_for_entity(player, mobiles.Equipped).both_hands

    # get the weapon name component
    wpn_name = world.component_for_entity(weapon_equipped, weapons.Name)

    print(player_name.first + ' the ' + class_component.label + ' is holding a ' + wpn_name.label)
    print('Weapon slot 4 has ' + SpellUtilities.get_spell_name_in_weapon_slot(world, weapon_equipped, 4))


if __name__ == '__main__':
    main()