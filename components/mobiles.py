import tcod


class Name:
    def __init__(self, first='undefined', suffix='undefined'):
        self.first = first
        self.suffix = suffix


class Describable:
    def __init__(self, description='undefined', glyph='@', foreground=tcod.white, background=tcod.black):
        self.description = description
        self.glyph = glyph
        self.foreground = foreground
        self.background = background


class Race:
    def __init__(self, race='human'):
        self.label = race


class CharacterClass:
    def __init__(self, label='undefined'):
        self.label = label


class AI:
    def __init__(self, ailevel=0, behaviour='none'):
        self.ailevel = ailevel
        self.behaviour = behaviour


class Health:
    def __init__(self, current=0, maximum=0):
        self.current = current
        self.maximum = maximum


class Inventory:
    def __init__(self, exists=False):
        self.exists = exists


class Armour:
    def __init__(self, head=0, chest=0, legs=0, feet=0, back=0):
        self.head = head
        self.chest = chest
        self.legs = legs
        self.feet = feet
        self.back = back


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
    pass