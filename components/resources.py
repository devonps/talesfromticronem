

#
# life force is used by the Necromancer and Witch doctor classes
# It power their F1 bar (special ability)
# It is gained from killing foes (% of their vitality attribute) and spell effects being triggered
#

class Lifeforce:
    def __init__(self, text='lifeforce', resource_status_effect='Lifeforce steal', ondeath=10, onhit=4):
        self.label = text
        self.onDeath = ondeath
        self.onHit = onhit
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


class TransferConditions:
    pass


#
# Strikes for informs the game how many times the targets are hit for
#


class Strikesfor:
    pass
