#TODO Overall spell effects need coding

#
# life force is used by the Necromancer and Witch doctor classes
# It power their F1 bar (special ability)
# It is gained from killing foes (% of their vitality attribute) and spell effects being triggered
#

class Lifeforce:
    def __init__(self, text='lifeforce', resource_status_effect='Lifeforce steal', ondeath=10, onhit=4):
        self.label = text
        self.on_death = ondeath
        self.on_hit = onhit
        self.resource_status_effect = resource_status_effect

#
# This is the component for direct damage, it is triggered from multiple places
# It's an empty component by design, it is used to flag that damage should be applied to the target


class Damage:
    def __init__(self, coefficient=0.0):
        self.coefficient = coefficient

#
# This is the component for transfer conditions from caster to N targets
# It's an empty component by design, it is used to flag that damage should be applied to the target

# TODO Transfer conditions spell effect


class TransferConditions:
    pass


#
# Strikes for informs the game how many times the targets are hit for
#

# TODO Spell number of hits effect


class Strikesfor:
    pass


#
# Convert boons to conditions
#
# TODO convert boons to conditions effect


class ConvertBoons:
    pass


class Selfbleeding:
    def __init__(self, name='Bleed', dialog="I'm bleeding"):
        self.label = name
        self.condition_status_effect = 'Bleeding'
        self.base_damage_per_stack = 2
        self.condition_damage_modifier = 0.06
        self.weapon_level_modifier = 0.25
        self.max_stacks = 10
        self.dialog = dialog
        self.lasts_for = 3
        self.stacks_applied = 1