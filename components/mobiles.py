from utilities import colourUtilities


class Name:
    def __init__(self, first='undefined', suffix='undefined'):
        self.first = first
        self.suffix = suffix


class Describable:
    def __init__(self, description='undefined', glyph='@', foreground=colourUtilities.get('ORANGE'), background=colourUtilities.get('BLACK'),
                 personality='Unpredictable', gender='undefined', image=0):
        self.description = description
        self.glyph = glyph
        self.foreground = foreground
        self.background = background
        self.personality_title = personality
        self.gender = gender
        self.image = image


# This class holds the image id that correspond to what the mobile is wearing or wielding
# Some of these settings are exclusive to each other
# For example: front is designed to hold items such as robes and cannot be used with chest or legs
#
class ClothingImage:
    def __init__(self, head=0, back=0, front=0, feet=0, weapon=0, hands=0, shield=0, legs=0, chest=0, shoulders=0):
        self.head = head
        self.back = back
        self.front = front
        self.feet = feet
        self.weapon = weapon
        self.hands = hands
        self.shield = shield
        self.legs = legs
        self.chest = chest
        self.shoulders = shoulders


class Personality:
    def __init__(self, charm_level=33, dignity_level=33, ferocity_level=33):
        self.charm_level = charm_level
        self.dignity_level = dignity_level
        self.ferocity_level = ferocity_level


class Race:
    def __init__(self, race='undefined', size='normal'):
        self.label = race
        self.size = size


class CharacterClass:
    def __init__(self, label='undefined', base_health=99, style='balanced', spellfile=''):
        self.label = label
        self.baseHealth = base_health
        self.style = style
        self.spellfile = spellfile


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
        self.currentvalue = valuecurrent
        self.maximumvalue = valuemaximum


class SpellBar:
    def __init__(self, entityId=0):
        self.entityId = entityId


class Viewport:
    def __init__(self, entityId=0):
        self.entityId = entityId


class Inventory:
    def __init__(self, exists=False):
        self.exists = exists
        self.bags = []  # this is a list of the bag 'entities'
        self.items = []  # this is a list of the items in each bag [bag_number:entity_number]


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
    def __init__(self, left_ear=0, right_ear=0, neck=0, left_hand=0, right_hand=0):
        self.left_ear = left_ear
        self.right_ear = right_ear
        self.neck = neck
        self.left_hand = left_hand
        self.right_hand = right_hand


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

    def __init__(self, armour=0, boonDuration=0, criticalChance=0, CriticalDamage=0, conditionDuration=0,
                 maximumHealth=0):
        self.armour = armour
        self.boonDuration = boonDuration
        self.criticalChance = criticalChance
        self.criticalDamage = CriticalDamage
        self.conditionDuration = conditionDuration
        self.maximumHealth = maximumHealth
        self.currentHealth = maximumHealth
