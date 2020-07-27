
class Bleeding:
    def __init__(self):
        self.label = 'Bleed'
        self.condition_status_effect = 'Bleeding'
        self.base_damage_per_stack = 2
        self.condition_damage_modifier = 0.06
        self.weapon_level_modifier = 0.25
        self.max_stacks = 10
        self.dialog = "I'm bleeding"
        self.lasts_for = 3
        self.stacks_applied = 1


class Burning:
    def __init__(self):

        self.label = 'Burn'
        self.condition_status_effect = 'Burning'
        self.base_damage_per_stack = 7
        self.condition_damage_modifier = 0.155
        self.weapon_level_modifier = 1.55
        self.max_stacks = 10
        self.dialog = 'It burns'
        self.lasts_for = 3
        self.stacks_applied = 1


class Confusion:
    def __init__(self):

        self.label = 'Confusion'
        self.condition_status_effect = 'Confused'
        self.base_damage_per_stack = 3.5
        self.condition_damage_modifier = 0.0975
        self.weapon_level_modifier = 1.575
        self.max_stacks = 10
        self.dialog = 'Where am I?'
        self.lasts_for = 3
        self.stacks_applied = 1


class Poison:
    def __init__(self):
        self.label = 'Poison'
        self.condition_status_effect = 'Poisoned'
        self.base_damage_per_stack = 3.5
        self.condition_damage_modifier = 0.06
        self.weapon_level_modifier = 0.375
        self.max_stacks = 20
        self.dialog = "I'm poisoned"
        self.lasts_for = 5
        self.healing_effectiveness_reduced = 33
        self.stacks_applied = 1


class Torment:
    def __init__(self):
        self.label = 'Torment'
        self.condition_status_effect = 'Tormented'
        self.base_damage_per_stack = 2
        self.condition_damage_modifier = 0.06
        self.weapon_level_modifier = 0.25
        self.max_stacks = 10
        self.dialog = 'Am I going mad?'
        self.lasts_for = 5
        self.velocity_base_damage = 5
        self.stacks_applied = 1


class Blind:
    def __init__(self):
        self.label = 'Blind'
        self.condition_status_effect = 'Blinded'
        self.max_stacks = 10
        self.dialog = "I'm blind"
        self.lasts_for = 5
        self.next_attack_misses = True
        self.stacks_applied = 1


class Chill:
    def __init__(self):
        self.label = 'Chill'
        self.condition_status_effect = "Chilled"
        self.movement_speed_penalty = 33
        self.max_stacks = 10
        self.dialog = 'F-f-freezing'
        self.lasts_for = 5
        self.spell_recharge_penalty = 33
        self.stacks_applied = 1


class Cripple:
    def __init__(self):
        self.label = 'Cripple'
        self.condition_status_effect = 'Crippled'
        self.movement_speed_penalty = 50
        self.max_stacks = 10
        self.dialog = 'Not the legs!'
        self.lasts_for = 5
        self.stacks_applied = 1


class Fear:
    def __init__(self):
        self.label = 'Fear'
        self.condition_status_effect = 'Feared'
        self.run_away = True
        self.no_actions = True
        self.max_stacks = 10
        self.dialog = "Fall back!"
        self.lasts_for = 5
        self.stacks_applied = 1


class Immobilize:
    def __init__(self):
        self.label = 'Immobilize'
        self.condition_status_effect = 'Immobilized'
        self.no_movement = True
        self.no_actions = True
        self.max_stacks = 10
        self.dialog = "I feel petrified"
        self.lasts_for = 5
        self.stacks_applied = 1


class Vulnerability:
    def __init__(self):
        self.label = 'Vulnerable'
        self.condition_status_effect = 'Vulnerable'
        self.incoming_damage_increased = 1.5
        self.max_stacks = 10
        self.dialog = "Feeling vulnerable"
        self.lasts_for = 5
        self.stacks_applied = 1
