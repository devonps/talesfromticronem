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


# defines the available actions based on the type of item
class Actionlist:
    def __init__(self, action_list=''):
        self.actions = action_list


class Describable:
    def __init__(self, name='', description='', glyph='', fg=tcod.white, bg=tcod.black, displayname=''):
        self.name = name
        self.description = description
        self.glyph = glyph
        self.fg = fg
        self.bg = bg
        self.displayname = displayname


# physical location on the game map
# obviously no location means the item is not on the game map
class Location:
    def __init__(self, x=0, y=0):
        self.posx = x
        self.posy = y


# what is the item made of
# this might not be used as a game mechanic, but it will at least add some flavour
class Material:
    def __init__(self, texture='cloth', component1='', component2='', component3=''):
        self.texture = texture
        self.component1 = component1
        self.component2 = component2
        self.component3 = component3


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


class WeaponType:
    def __init__(self, label=''):
        self.label = label


# hallmarks are a way to add a different bonus to an existing weapon
class Hallmarks:
    def __init__(self, hallmark_slot_one=0, hallmark_slot_two=0):
        self.hallmark_slot_one = hallmark_slot_one
        self.hallmark_slot_two = hallmark_slot_two


# can this item be held in the hands
# the true_or_false parameter drives this
class Wielded:
    def __init__(self, hands='both', true_or_false=True):
        self.hands = hands
        self.true_or_false = true_or_false


# which spells are loaded into the weapon
class Spells:
    def __init__(self, slot_one=0, slot_two=0, slot_three=0, slot_four=0, slot_five=0 ):
        self.slot_one = slot_one
        self.slot_two = slot_two
        self.slot_three = slot_three
        self.slot_four = slot_four
        self.slot_five = slot_five
        self.slot_one_disabled = False
        self.slot_two_disabled = False
        self.slot_three_disabled = False
        self.slot_four_disabled = False
        self.slot_five_disabled = False


# weapon damage range
class DamageRange:
    def __init__(self, ranges=''):
        self.ranges = ranges



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
    def __init__(self, chest=False, head=False, hands=False, feet=False, legs=False):
        self.chest = chest
        self.head = head
        self.hands = hands
        self.feet = feet
        self.legs = legs


# what bonus does this piece of armour add and to which attribute
class AttributeBonus:
    def __init__(self, majorname='', majorbonus=0, minoronename='', minoronebonus=0):
        self.majorName = majorname
        self.majorBonus = majorbonus
        self.minorOneName = minoronename
        self.minorOneBonus = minoronebonus


# If this piece of armour belongs to an armour set it, the set name will
# be found here
class ArmourSet:
    def __init__(self, label='', prefix='', level=0):
        self.name = label
        self.prefix = prefix
        self.level = level


# Is the armour being worn
class ArmourBeingWorn:
    def __init__(self, status=False):
        self.status = status

####################################################
#
#   JEWELLERY
#
####################################################


# this defines the stat(s) the piece of jewellery improves
# the dictionary is in the format:{stat_name, bonus_value}
class JewelleryStatBonus:
    def __init__(self, statname='', statbonus=0):
        self.statName = statname
        self.statBonus = statbonus


# where on the body can this piece of jewellery be worn
# neck = Amulets, fingers = Rings, ears=Earrings
class JewelleryBodyLocation:
    def __init__(self, fingers=False, neck=False, ears=False):
        self.fingers = fingers
        self.neck = neck
        self.ears = ears


# Is the piece of jewellery already equipped
class JewelleryEquipped:
    def __init__(self, istrue=False):
        self.istrue = istrue
