

#
# life force is used by the Necromancer and Witch doctor classes
# It power their F1 bar (special ability)
# It is gained from killing foes (% of their vitality attribute) and spell effects being triggered

class Lifeforce:
    def __init__(self, text='lifeforce', resource_status_effect='Lifeforce steal', ondeath=10, onhit=4):
        self.text = text
        self.onDeath = ondeath
        self.onHit = onhit
        self.resource_status_effect = resource_status_effect
