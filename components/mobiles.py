import tcod


class Name:
    def __init__(self, first='undefined', suffix='undefined'):
        self.first = first
        self.suffix = suffix


class Describable:
    def __init__(self, description='undefined', glyph='@', foreground=tcod.orange, background=tcod.black, personality='Unpredictable', gender=''):
        self.description = description
        self.glyph = glyph
        self.foreground = foreground
        self.background = background
        self.personality_title = personality
        self.gender = gender


class Personality:
    def __init__(self, charm_level=33, dignity_level=33, ferocity_level=33):
        self.charm_level = charm_level
        self.dignity_level = dignity_level
        self.ferocity_level = ferocity_level


class Race:
    def __init__(self, race='human', size='normal'):
        self.label = race
        self.size = size


class CharacterClass:
    def __init__(self, label='undefined', base_health=0):
        self.label = label
        self.baseHealth = base_health


class AI:
    def __init__(self, ailevel=0, behaviour='none'):
        self.ailevel = ailevel
        self.behaviour = behaviour


class ManaPool:
    def __init__(self, current=0, maximum=0):
        self.current = current
        self.maximum = maximum


class SpecialBar:
    def __init__(self, maxstages=3, currentstage=0, valuecurrent=0, valuemaximum=0):
        self.maxstages = maxstages
        self.currentstage = currentstage
        self.valuecurrent = valuecurrent
        self.valuemaximum = valuemaximum


class Inventory:
    def __init__(self, exists=False):
        self.exists = exists
        self.bags = []
        self.items_in_inventory = []


class Armour:
    """
    Each body location holds the defense value, typically this is based on the equipped piece of armour
    self.head --> holds an integer that represents a gameworld.entity
    from there I can get the individual components I need such as...
    defense.value
    """
    def __init__(self, head=0, chest=0, legs=0, feet=0, hands=0):
        self.head = head
        self.chest = chest
        self.legs = legs
        self.feet = feet
        self.hands = hands


class Jewellery:
    def __init__(self, ear_one=0, ear_two=0, amulet=0, ring_one=0, ring_two=0):
        self.ear_one = ear_one
        self.ear_two = ear_two
        self.amulet = amulet
        self.ring_one = ring_one
        self.ring_two = ring_two


class Equipped:
    def __init__(self, main_hand=0, off_hand=0, both_hands=0):
        self.main_hand = main_hand
        self.off_hand = off_hand
        self.both_hands = both_hands


class Renderable:
    def __init__(self, is_visible=True):
        self.isVisible = is_visible


class Position:
    def __init__(self, x=0, y=0, hasMoved=False):
        self.x = x
        self.y = y
        self.hasMoved = hasMoved


class Velocity:
    def __init__(self, dx=0, dy=0):
        self.dx = dx
        self.dy = dy


class StatusEffects:
    def __init__(self):
        self.boons = []
        self.conditions = []
        self.controls = []


class PrimaryAttributes:
    """
    power increases outgoing direct damage
    precision increases critical chance
    toughness increases armour
    vitality increases health
    """
    def __init__(self, power=37, precision=37, toughness=37, vitality=37):
        self.power = power
        self.precision = precision
        self.toughness = toughness
        self.vitality = vitality


class SecondaryAttributes:
    """
    concentration increases boon duration
    condition damage increases damage over time inflicted by conditions
    expertise increases condition duration
    ferocity increases critical damage
    healing power increases outgoing healiing, including self heals
    """
    def __init__(self, concentration=0, conditionDamage=0, expertise=0, ferocity=0, healingPower=0):
        self.concentration = concentration
        self.conditionDamage = conditionDamage
        self.expertise = expertise
        self.ferocity = ferocity
        self.healingPower = healingPower


class DerivedAttributes:
    """
    Armor: Decreases incoming direct damage. Increased by Toughness and Defense.
    Boon Duration: Increases the duration of all applied boons.
        It has a base value of 0%, and is increased by Concentration (15 Concentration = 1% Boon Duration).
    Critical Chance: Increases critical hit chance.
        At level 80, it has a base value of 5%, and is increased by Precision (21 Precision = 1% Critical Chance).
    Critical Damage: Increases critical hit damage.
        It has a base value of 150%, and is increased by Ferocity (15 Ferocity = 1% Critical Damage).
    Condition Duration: Increases the duration of all inflicted conditions.
        It has a base value of 0%, and is increased by Expertise (15 Expertise = 1% Condition Duration).
    Health: The character's maximum health.
        Base value is determined by profession and increases with level. Increased by Vitality (1 Vitality = 10 Health).
    """
    def __init__(self, armour=0, boonDuration=0, criticalChance=0, CriticalDamage=0, conditionDuration=0, maximumHealth=0):
        self.armour = armour
        self.boonDuration = boonDuration
        self.criticalChance = criticalChance
        self.criticalDamage = CriticalDamage
        self.conditionDuration = conditionDuration
        self.maximumHealth = maximumHealth
        self.currentHealth = maximumHealth
