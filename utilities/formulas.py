
def base_direct_damage(weapon_strength, power, spell_coefficient, target_armour):

    base_damage = (weapon_strength * power * spell_coefficient) / target_armour

    return base_damage


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


def calculate_armour(defense_stat, toughness_stat):
    armour = defense_stat + toughness_stat

    return armour
