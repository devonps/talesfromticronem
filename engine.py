
from loguru import logger
from newGame.initialiseNewGame import setup_game, generate_player_character, load_weapon_with_spells
from components import spells, weapons, mobiles
from newGame.ClassWeapons import WeaponClass


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

    # create the player
    player = generate_player_character(world)
    player_name = world.component_for_entity(player, mobiles.Name)
    ai_level_component = world.component_for_entity(player, mobiles.AI)
    world.component_for_entity(player, mobiles.CharacterClass).label = 'necromancer'
    class_component = world.component_for_entity(player, mobiles.CharacterClass)

    # create a new weapon for the player
    weapon = WeaponClass.create_weapon(world, 'sword')
    weapon_type = world.component_for_entity(weapon, weapons.Name)
    # parameters are: gameworld, weapon object, weapon type as a string, mobile class
    load_weapon_with_spells(world, weapon, weapon_type.label, class_component.label)

    # equip player with weapon
    world.component_for_entity(player, mobiles.Equipped).both_hands = weapon

    # confirm the weapon is equipped
    weapon_equipped = world.component_for_entity(player, mobiles.Equipped).both_hands

    wpn_name = world.component_for_entity(weapon_equipped, weapons.Name)

    print('Player name set as ' + player_name.first)
    print('Player AI set to ' + str(ai_level_component.ailevel))
    print('Current behaviour is ' + ai_level_component.behaviour)
    print('Character class ' + class_component.label)
    print('hands ' + str(wpn_name.label))


if __name__ == '__main__':
    main()