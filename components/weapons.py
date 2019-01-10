import tcod


class Name:
    def __init__(self, text='undefined'):
        self.label = text


class Describable:
    def __init__(self, description='undefined', display_name='undefined', glyph='/', foreground=tcod.white,
                 background=tcod.black):
        self.description = description
        self.display_name = display_name
        self.glyph = glyph
        self.foreground = foreground
        self.background = background


class Wielded:
    def __init__(self, main_hand=False, off_hand=False, both_hands=False, true_or_false=True):
        self.main_hand = main_hand
        self.off_hand = off_hand
        self.both_hands = both_hands
        self.true_or_false = true_or_false


class Spells:
    def __init__(self, slot_one=0, slot_two=0, slot_three=0, slot_four=0, slot_five=0):
        self.slot_one = slot_one
        self.slot_two = slot_two
        self.slot_three = slot_three
        self.slot_four = slot_four
        self.slot_five = slot_five
        self.slot_one_disabled = None
        self.slot_two_disabled = None
        self.slot_three_disabled = None
        self.slot_four_disabled = None
        self.slot_five_disabled = None


class Experience:
    def __init__(self, current_level=1):
        self.current_level = current_level
        self.max_level = 10


class Hallmarks:
    def __init__(self, hallmark_slot_one=0, hallmark_slot_two=0):
        self.hallmark_slot_one = hallmark_slot_one
        self.hallmark_slot_two = hallmark_slot_two


class Renderable:
    def __init__(self, is_visible=True):
        self.is_visible = is_visible


class Quality:
    def __init__(self, level='basic'):
        self.level = level
