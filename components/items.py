import tcod


####################################################
#
#   Components applicable to all types of items
#
####################################################

# what type of item is this entity
# this is primarily used in iterable statements as a filter
class TypeOfItem:
    def __init__(self, label=''):
        self.label = label


class Describable:
    def __init__(self, name='', description='', glyph='', fg=tcod.white, bg=tcod.black):
        self.name = name
        self.description = description
        self.glyph = glyph
        self.fg = fg
        self.bg = bg


# physical location on the game map
# obviously no location means the item is not on the game map
class Location:
    def __init__(self, x=0, y=0):
        self.posx = x
        self.posy = y


# what is the item made of
# this might not be used as a game mechanic, but it will at least add some flavour
class Material:
    def __init__(self, texture=''):
        self.texture = texture


# is this item visible on the game map
# YES means it can be seen by the player and any mobiles (unless they're blind)
# NO means: (1) it's invisible or (2) it's inside a container
class RenderItem:
    def __init__(self, istrue=True):
        self.isTrue = istrue


# what is the quality of this item
# this may be a game mechanic or not but it will at least be flavour
class Quality:
    def __init__(self, level='basic'):
        self.level = level
####################################################
#
#   BAGS
#
####################################################


# how many slots does this bag have
# populated indicates how many different slots contain at least one item
class SlotSize:
    def __init__(self, maxsize=26, populated=0):
        self.maxsize = maxsize
        self.populated = populated


####################################################
#
#   WEAPONS
#
####################################################
class Experience:
    def __init__(self, current_level=1):
        self.current_level = current_level
        self.max_level = 10


# hallmarks are a way to add a different bonus to an existing weapon
class Hallmarks:
    def __init__(self, hallmark_slot_one=0, hallmark_slot_two=0):
        self.hallmark_slot_one = hallmark_slot_one
        self.hallmark_slot_two = hallmark_slot_two


# can this item be held in the hands
# the true_or_false parameter drives this
class Wielded:
    def __init__(self, main_hand=False, off_hand=False, both_hands=False, true_or_false=True):
        self.main_hand = main_hand
        self.off_hand = off_hand
        self.both_hands = both_hands
        self.true_or_false = true_or_false

####################################################
#
#   ARMOUR
#
####################################################


# how heavy is this piece of armour
class Weight:
    def __init__(self, label=''):
        self.label = label


# what is the calculated defense value for this piece of armour
class Defense:
    def __init__(self, value=0):
        self.value = value


# where on the body can this piece of armour be placed
class ArmourBodyLocation:
    def __init__(self, text='undefined', chest=False, head=False, hands=False, feet=False, legs=False):
        self.label = text
        self.chest = chest
        self.head = head
        self.hands = hands
        self.feet = feet
        self.legs = legs


# what bonus does this piece of armour add and to which attribute
class AttributeBonus:
    def __init__(self, majorattribute={}, minorattribute={}):
        self.majorAttribute = majorattribute
        self.minorAttribute = minorattribute


# If this piece of armour belongs to an armour set it, the set name will
# be found here
class ArmourSet:
    def __init__(self, label=''):
        self.name = label

####################################################
#
#   JEWELLERY
#
####################################################


# this defines the stat(s) the piece of jewellery improves
# the dictionary is in the format:{stat_name, bonus_value}
class ImprovementTo:
    def __init__(self, stat={}):
        self.stat = stat


# where on the body can this piece of jewellery be worn
# neck = Amulets, fingers = Rings, ears=Earrings
class JewelleryBodyLocation:
    def __init__(self, fingers=False, neck=False, ears=False):
        self.fingers = fingers
        self.neck = neck
        self.ears = ears

####################################################
#
#   SPELLS
#
####################################################
