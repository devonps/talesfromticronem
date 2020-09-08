import math

from loguru import logger

from utilities.mobileHelp import MobileUtilities


def calculate_percentage(low_number, max_number):
    return int((low_number / max_number) * 100)


def calculate_distance_to_target(gameworld, from_entity, to_entity):
    from_x = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=from_entity)
    from_y = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=from_entity)
    to_x = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=to_entity)
    to_y = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=to_entity)

    dx = to_x - from_x
    dy = to_y - from_y
    return math.sqrt(dx ** 2 + dy ** 2)


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


def critical_damage_calculation(ferocity_stat):
    base_crit_damage = 150

    modifier = int(ferocity_stat / 15)

    crit_damage = base_crit_damage + modifier

    return crit_damage


def critical_hit_damage_modifier(crit_hit_chance, base_damage, ferocity_stat):
    crit_damage = critical_damage_calculation(ferocity_stat)

    average_damage = base_damage * (1 + crit_hit_chance * crit_damage - 1)

    return average_damage


# TODO calculate defense forumla


def calculate_defense():
    pass
