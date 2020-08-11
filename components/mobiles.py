from utilities import colourUtilities


class Viewport:
    def __init__(self, posx=0, posy=0):
        self.posx = posx
        self.posy = posy


class CurrentTurn:
    def __init__(self, current_turn=0):
        self.current_turn = current_turn


class MessageLog:
    def __init__(self, entity_id=0, message_log_change=False):
        self.entity_id = entity_id
        self.message_log_change = message_log_change


# ----------------------------------------------
# dialogue components
# ----------------------------------------------
# initiate is used by the PC to talk to this NPC
# spoken_to_before is used by the game to understand if the PC has spoken to this NPC before
# welcome is a one time flag to start 'welcome' text for the PC
class DialogFlags:
    def __init__(self, welcome=False, spoken_to_before=False, talk_to_me=False):
        self.talk_to_me = talk_to_me
        self.welcome = welcome
        self.spoken_to_before = spoken_to_before


# ----------------------------------------------
# mobile combat components
# ----------------------------------------------
class EnemyPreferredAttackMinRange:
    def __init__(self, value=0):
        self.value = value


class EnemyPreferredAttackMaxRange:
    def __init__(self, value=0):
        self.value = value


class VisibleEntities:
    def __init__(self):
        self.list = []


class EnemyCombatRole:
    def __init__(self, value='none'):
        self.value = value


# ----------------------------------------------
# describe the mobile components
# ----------------------------------------------
class Name:
    def __init__(self, first='undefined', suffix='undefined'):
        self.first = first
        self.suffix = suffix


class ClassSpecific:
    def __init__(self, attunement='fire'):
        self.fire = attunement


class Describable:
    def __init__(self):
        self.description = 'undefined'
        self.glyph = ''
        self.foreground = colourUtilities.get('ORANGE')
        self.background = colourUtilities.get('BLACK')
        self.personality_title = 'Unpredictable'
        self.gender = 'undefined'
        self.image = 0


class Personality:
    def __init__(self, charm_level=33, dignity_level=33, ferocity_level=33):
        self.charm_level = charm_level
        self.dignity_level = dignity_level
        self.ferocity_level = ferocity_level


class Race:
    def __init__(self, race='undefined', size='normal'):
        self.label = race
        self.size = size
        self.name_singular = ''
        self.name_plural = ''
        self.name_adjective = ''


class CharacterClass:
    def __init__(self, label='undefined', base_health=99, style='balanced', spellfile=''):
        self.label = label
        self.base_health = base_health
        self.style = style
        self.spellfile = spellfile


class AI:
    def __init__(self, ailevel=0, description='none'):
        self.ailevel = ailevel
        self.description = description


class NpcType:
    def __init__(self, shopkeeper=False, tutor=False):
        self.shopkeeper = shopkeeper
        self.type_of_shopkeeper = ''
        self.tutor = tutor
        self.type_of_tutor = ''


# ----------------------------------------------
# spell/magic components
# ----------------------------------------------
class SpecialBar:
    def __init__(self, maxstages=3, currentstage=0, valuecurrent=0, valuemaximum=0):
        self.maxstages = maxstages
        self.currentstage = currentstage
        self.currentvalue = valuecurrent
        self.maximumvalue = valuemaximum


class SpellBar:
    def __init__(self, entity_id=0):
        self.entity_id = entity_id
        self.slots = [0] * 10


class StatusEffects:
    def __init__(self):
        self.boons = []
        self.conditions = []
        self.controls = []
        self.in_combat = False


class SpellCast:
    def __init__(self, truefalse=False, spell_entity=0, spell_target=0, spell_bar_slot=-99, spell_caster=0):
        self.truefalse = truefalse
        self.spell_entity = spell_entity
        self.spell_target = spell_target
        self.spell_bar_slot = spell_bar_slot
        self.spell_caster = spell_caster


# ----------------------------------------------
# Inventory components
# ----------------------------------------------
class Inventory:
    def __init__(self, exists=False):
        self.exists = exists
        self.bags = []  # this is a list of the bag 'entities'
        self.items = []  # this is a list of the items in each bag [bag_number:entity_number]


# ----------------------------------------------
# equipment components
# ----------------------------------------------
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


# weapons
class Equipped:
    def __init__(self, main_hand=0, off_hand=0, both_hands=0):
        self.main_hand = main_hand
        self.off_hand = off_hand
        self.both_hands = both_hands


# ----------------------------------------------
# game map components
# ----------------------------------------------
class Renderable:
    def __init__(self, is_visible=True):
        self.is_visible = is_visible


class Position:
    def __init__(self, x=0, y=0, has_moved=False):
        self.x = x
        self.y = y
        self.has_moved = has_moved


class Velocity:
    def __init__(self, dx=0, dy=0):
        self.dx = dx
        self.dy = dy


# ----------------------------------------------
# mobile attributes components
# ----------------------------------------------
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

    def __init__(self, concentration=0, condition_damage=0, expertise=0, ferocity=0, healing_power=0):
        self.concentration = concentration
        self.condition_damage = condition_damage
        self.expertise = expertise
        self.ferocity = ferocity
        self.healing_power = healing_power


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

    def __init__(self, armour=0, boon_duration=0, critical_chance=0, critical_damage=0, condition_duration=0,
                 maximum_health=0):
        self.armour = armour
        self.boon_duration = boon_duration
        self.critical_chance = critical_chance
        self.critical_damage = critical_damage
        self.condition_duration = condition_duration
        self.maximum_health = maximum_health
        self.current_health = maximum_health
