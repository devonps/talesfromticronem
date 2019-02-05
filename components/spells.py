from newGame import constants


class Name:
    def __init__(self, text='undefined'):
        self.label = text


class Description:
    def __init__(self, text='no description'):
        self.label = text


class WeaponType:
    def __init__(self, text='no such weapon'):
        self.label = text


class WeaponSlot:
    def __init__(self, slot=0):
        self.slot = slot


class ClassName:
    def __init__(self, text='no such class'):
        self.label = text


class CastTime:
    def __init__(self, number_of_turns=1):
        self.number_of_turns = number_of_turns


class CoolDown:
    def __init__(self, number_of_turns=1):
        self.number_of_turns = number_of_turns


class LivesFor:
    def __init__(self, number_of_turns=1 ):
        self.number_of_turns = number_of_turns


class MaxTargets:
    def __init__(self, number_of_targets=1):
        self.number_of_targets = number_of_targets


class GroundTargeted:
    def __init__(self, uses_ground_targeting=False):
        self.uses_ground_targeting = uses_ground_targeting


class MaxRange:
    def __init__(self, max_range=constants.SPELL_DIST_PERSONAL):
        self.max_range = max_range


class AreaOfEffect:
    def __init__(self, use_area_of_effect=False):
        self.use_area_of_effect = use_area_of_effect


class AreaOfEffectSize:
    def __init__(self, area_of_effect_size=1):
        self.area_of_effect_size = area_of_effect_size
