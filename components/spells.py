class Name:
    def __init__(self, text='undefined'):
        self.label = text


class SpellType:
    def __init__(self, text='undefined'):
        self.label = text


class Image:
    def __init__(self, image=0):
        self.id = image


class Description:
    def __init__(self, text='no description'):
        self.label = text


class ShortDescription:
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
    def __init__(self, number_of_turns=0, is_true=False):
        self.number_of_turns = number_of_turns
        self.is_true = is_true
        self.remaining_turns = 0


class LivesFor:
    def __init__(self, number_of_turns=1):
        self.number_of_turns = number_of_turns


class MaxTargets:
    def __init__(self, number_of_targets=1):
        self.number_of_targets = number_of_targets


class GroundTargeted:
    def __init__(self, uses_ground_targeting=False):
        self.uses_ground_targeting = uses_ground_targeting


class MaxRange:
    def __init__(self, max_range=0):
        self.max_range = max_range


class AreaOfEffect:
    def __init__(self, use_area_of_effect=False):
        self.use_area_of_effect = use_area_of_effect


class AreaOfEffectSize:
    def __init__(self, area_of_effect_size=1):
        self.area_of_effect_size = area_of_effect_size


class DamageDuration:
    def __init__(self, duration=1):
        self.is_set_to = duration


class DamageCoefficient:
    def __init__(self, value=0.0):
        self.is_set_to = value


class HealingDuration:
    def __init__(self, duration=0):
        self.value = duration


class HealingCoef:
    def __init__(self, coef=0.0):
        self.value = coef


class ItemType:
    def __init__(self, label=''):
        self.label = label


class ItemLocation:
    def __init__(self, label=''):
        self.label = label


class StatusEffect:

    def __init__(self, condis=None, boons=None, controls=None, resources=None):
        if controls is None:
            controls = []
        if boons is None:
            boons = []
        if condis is None:
            condis = []
        if resources is None:
            resources = []
        self.condis = condis
        self.boons = boons
        self.controls = controls
        self.resources = resources
