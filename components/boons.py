
class Aegis:
    def __init__(self):
        self.label = 'Aegis'
        self.boon_status_effect = 'Aegis'
        self.lasts_for = 3
        self.max_stacks = 10
        self.dialog = "You will not hit me"
        self.next_attack_blocked = True


class Alacrity:
    def __init__(self):
        self.label = 'Alacrity'
        self.boon_status_effect = 'Alacrity'
        self.lasts_for = 3
        self.max_stacks = 5
        self.dialog = "You're so slow!"
        self.spell_recharge_improved = 20


class Fury:
    def __init__(self):
        self.label = 'Fury'
        self.boon_status_effect = 'Fury'
        self.lasts_for = 3
        self.max_stacks = 5
        self.dialog = "fury rising!"
        self.crit_chance_improved = 20


class Might:
    def __init__(self):
        self.label = 'Might'
        self.boon_status_effect = 'Might'
        self.lasts_for = 3
        self.max_stacks = 5
        self.dialog = "There's the power"
        self.base_damage_per_stack = 5
        self.weapon_level_modifier = 0.3125


class Protection:
    def __init__(self):
        self.label = 'Protection'
        self.boon_status_effect = 'Protection'
        self.lasts_for = 3
        self.max_stacks = 10
        self.dialog = "Armour enhanced"
        self.incoming_damage_reduction = 33


class Regeneration:
    def __init__(self):
        self.label = 'Regeneration'
        self.boon_status_effect = 'Regeneration'
        self.lasts_for = 3
        self.max_stacks = 10
        self.dialog = "Invigorating"
        self.base_heal_per_turn = 5
        self.heal_modifier = 0.125


class Resistance:
    def __init__(self):
        self.label = 'Resistance'
        self.boon_status_effect = 'Resistance'
        self.lasts_for = 3
        self.max_stacks = 10
        self.dialog = "Ahh! You don't scare me"
        self.conditions_are_disabled = True


class Retaliation:
    def __init__(self):
        self.label = 'Retaliation'
        self.boon_status_effect = 'Retaliation'
        self.lasts_for = 3
        self.max_stacks = 10
        self.dialog = "Hit me, if you dare!"
        self.reflect_taken_damage = 100


class Stability:
    def __init__(self):
        self.label = 'Stability'
        self.boon_status_effect = 'Stability'
        self.lasts_for = 3
        self.max_stacks = 10
        self.dialog = "You can't control me!"
        self.cannot_be_controlled = True


class Swiftness:
    def __init__(self):
        self.label = 'Swiftness'
        self.boon_status_effect = 'Swiftness'
        self.lasts_for = 3
        self.max_stacks = 10
        self.dialog = "Catch me if you can!"
        self.movement_speed_bonus = 50
