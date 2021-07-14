import math
import random

from loguru import logger
from utilities.mobileHelp import MobileUtilities


def calculate_condi_confusion_damage(gameworld, caster_entity, current_weapon_level):
    condi_damage = MobileUtilities.get_mobile_secondary_condition_damage(gameworld=gameworld, entity=caster_entity)

    current_condis = MobileUtilities.get_current_condis_applied_to_mobile(gameworld=gameworld,
                                                                          entity=caster_entity)

    confusion_damage = 0

    for condi in current_condis:
        condi_name = condi['name']
        if condi_name == 'confusion':
            base_damage_per_stack = condi['baseDamage']
            condition_damage_modifier = condi['condDamageMod']
            weapon_level_modifier = condi['weaponLevelMod']

            confusion_damage = (condition_damage_modifier * condi_damage) + (
                    weapon_level_modifier * current_weapon_level) + base_damage_per_stack

    return confusion_damage


def calculate_percentage(low_number, max_number):
    return int((low_number / max_number) * 100)


def calculate_distance_to_target(gameworld, from_entity, to_entity):
    from_x = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=from_entity)
    from_y = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=from_entity)
    to_x = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=to_entity)
    to_y = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=to_entity)

    dx = to_x - from_x
    dy = to_y - from_y
    return int(math.sqrt(dx ** 2 + dy ** 2))


def distance_between_two_tiles(from_coords, to_coords):
    from_x = from_coords[0]
    from_y = from_coords[1]

    to_x = to_coords[0]
    to_y = to_coords[1]

    dx = to_x - from_x
    dy = to_y - from_y
    return int(math.sqrt(dx ** 2 + dy ** 2))


def outgoing_base_damage(weapon_strength, power, spell_coefficient):
    # weapon strength - random number representing potential damage for that weapon
    # power - mobile's current power attribute
    # spell coefficient - modifier taken from the spell
    return int(weapon_strength * power * spell_coefficient)


def base_condi_damage(condition_damage_modifier, condition_damage_stat, weapon_level_modifier, base_damage_per_stack,
                      weapon_level):
    base_damage = (condition_damage_modifier * condition_damage_stat) + (
            weapon_level_modifier * weapon_level) + base_damage_per_stack
    logger.debug('Condition damage of ' + str(base_damage) + ' is calculated as: (' + str(
        condition_damage_modifier) + ' * ' + str(condition_damage_stat) + ') + (' + str(
        weapon_level_modifier) + ' * ' + str(weapon_level) + ') + ' + str(base_damage_per_stack))

    return base_damage


def calculate_critical_damage_percentage(ferocity_stat):
    base_crit_damage = 150

    modifier = int(ferocity_stat / 15)

    crit_damage = base_crit_damage + modifier

    return crit_damage


def calculate_critical_hit_damage(base_damage, ferocity_stat):
    crit_damage_percentage = calculate_critical_damage_percentage(ferocity_stat)

    crit_damage_to_be_added = calculate_percentage(low_number=base_damage,  max_number=crit_damage_percentage)

    critical_hit__damage = base_damage + crit_damage_to_be_added

    return critical_hit__damage


def get_chance_of_critical_hit(critical_hit_chance):
    critical_hit = False
    rng = random.randrange(0, 100)

    if critical_hit_chance > rng:
        critical_hit = True

    return critical_hit


# TODO calculate defense forumla


def calculate_defense():
    pass
