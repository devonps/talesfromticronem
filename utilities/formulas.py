
def outgoing_base_damage(weapon_strength, power, spell_coefficient):
    # weapon strength - random number representing potential damage for that weapon
    # power - mobile's current power attribute
    # spell coefficient - modifier taken from the spell
    return int(weapon_strength * power * spell_coefficient)


def calculate_duration_per_condition(condition_duration):
    base_duration = 5
    duration_percent = 0
    if condition_duration > 0:
        duration_percent = (base_duration / condition_duration) * 100
    calculated_duration = base_duration * (1 + duration_percent)

    return calculated_duration


def base_condi_damage(condition_damage_modifier, condition_damage_stat, weapon_level_modifier, base_damage_per_stack, weapon_level):

    base_damage = (condition_damage_modifier * condition_damage_stat) + (weapon_level_modifier * weapon_level) + base_damage_per_stack

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

