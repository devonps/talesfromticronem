
class Aegis:
    def __init__(self, name='Aegis', boon_status_effect='Aegis', lasts_for=3, max_stacks=10,
                 dialog="You will not hit me", next_attack_blocked=True):
        self.name = name
        self.boon_status_effect = boon_status_effect
        self.lasts_for = lasts_for
        self.max_stacks = max_stacks
        self.dialog = dialog
        self.next_attack_blocked = next_attack_blocked


class Alacrity:
    def __init__(self, name='Alacrity', boon_status_effect='Alacrity', lasts_for=3, max_stacks=5,
                 dialog="You're so slow!", spell_recharge_improved=20):
        self.name = name
        self.boon_status_effect = boon_status_effect
        self.lasts_for = lasts_for
        self.max_stacks = max_stacks
        self.dialog = dialog
        self.spell_recharge_improved = spell_recharge_improved


class Fury:
    def __init__(self, name='Fury', boon_status_effect='Fury', lasts_for=3, max_stacks=5,
                 dialog="fury rising!", crit_chance_improved=20):
        self.name = name
        self.boon_status_effect = boon_status_effect
        self.lasts_for = lasts_for
        self.max_stacks = max_stacks
        self.dialog = dialog
        self.crit_chance_improved = crit_chance_improved


class Might:
    def __init__(self, name='Might', boon_status_effect='Might', lasts_for=3, max_stacks=5,
                 dialog="There's the power", base_damage_per_stack=5, weapon_level_modifier=0.3125):
        self.name = name
        self.boon_status_effect = boon_status_effect
        self.lasts_for = lasts_for
        self.max_stacks = max_stacks
        self.dialog = dialog
        self.base_damage_per_stack = base_damage_per_stack
        self.weapon_level_modifier = weapon_level_modifier


class Protection:
    def __init__(self, name='Protection', boon_status_effect='Protection', lasts_for=3, max_stacks=10,
                 dialog="Armour enhanced", incoming_damage_reduction=33):
        self.name = name
        self.boon_status_effect = boon_status_effect
        self.lasts_for = lasts_for
        self.max_stacks = max_stacks
        self.dialog = dialog
        self.incoming_damage_reduction = incoming_damage_reduction


class Regeneration:
    def __init__(self, name='Regeneration', boon_status_effect='Regeneration', lasts_for=3, max_stacks=10,
                 dialog="Invigorating", base_heal_per_turn=5, heal_modifier=0.125):
        self.name = name
        self.boon_status_effect = boon_status_effect
        self.lasts_for = lasts_for
        self.max_stacks = max_stacks
        self.dialog = dialog
        self.base_heal_per_turn = base_heal_per_turn
        self.heal_modifier = heal_modifier


class Resistance:
    def __init__(self, name='Resistance', boon_status_effect='Resistance', lasts_for=3, max_stacks=10,
                 dialog="Ahh! You don't scare me", conditions_are_disabled=True):
        self.name = name
        self.boon_status_effect = boon_status_effect
        self.lasts_for = lasts_for
        self.max_stacks = max_stacks
        self.dialog = dialog
        self.conditions_are_disabled = conditions_are_disabled


class Retaliation:
    def __init__(self, name='Retaliation', boon_status_effect='Retaliation', lasts_for=3, max_stacks=10,
                 dialog="Hit me, if you dare!", reflect_taken_damage=100):
        self.name = name
        self.boon_status_effect = boon_status_effect
        self.lasts_for = lasts_for
        self.max_stacks = max_stacks
        self.dialog = dialog
        self.reflect_taken_damage = reflect_taken_damage


class Stability:
    def __init__(self, name='Stability', boon_status_effect='Stability', lasts_for=3, max_stacks=10,
                 dialog="You can't control me!", cannot_be_controlled=True):
        self.name = name
        self.boon_status_effect = boon_status_effect
        self.lasts_for = lasts_for
        self.max_stacks = max_stacks
        self.dialog = dialog
        self.cannot_be_controlled = cannot_be_controlled


class Swiftness:
    def __init__(self, name='Swiftness', boon_status_effect='Swiftness', lasts_for=3, max_stacks=10,
                 dialog="Catch me if you can!", movement_speed_bonus=50):
        self.name = name
        self.boon_status_effect = boon_status_effect
        self.lasts_for = lasts_for
        self.max_stacks = max_stacks
        self.dialog = dialog
        self.movement_speed_bonus = movement_speed_bonus
