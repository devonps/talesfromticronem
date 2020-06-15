
class Bleeding:
    def __init__(self, name='Bleed', dialog="I'm bleeding"):
        self.label = name
        self.condition_status_effect = 'Bleeding'
        self.base_damage_per_stack = 2
        self.condition_damage_modifier = 0.06
        self.weapon_level_modifier = 0.25
        self.max_stacks = 10
        self.dialog = dialog
        self.lasts_for = 3
        self.stacks_applied = 1


class Burning:
    def __init__(self, name='Burn', dialog='It burns'):

        self.label = name
        self.condition_status_effect = 'Burning'
        self.base_damage_per_stack = 7
        self.condition_damage_modifier = 0.155
        self.weapon_level_modifier = 1.55
        self.max_stacks = 10
        self.dialog = dialog
        self.lasts_for = 3
        self.stacks_applied = 1


class Confusion:
    def __init__(self, name='Confusion',  dialog='Where am I?'):

        self.label = name
        self.condition_status_effect = 'Confused'
        self.base_damage_per_stack = 3.5
        self.condition_damage_modifier = 0.0975
        self.weapon_level_modifier = 1.575
        self.max_stacks = 10
        self.dialog = dialog
        self.lasts_for = 3
        self.stacks_applied = 1


class Poison:
    def __init__(self, name='Poison', dialog="I'm poisoned"):
        self.label = name
        self.condition_status_effect = 'Poisoned'
        self.base_damage_per_stack = 3.5
        self.condition_damage_modifier = 0.06
        self.weapon_level_modifier = 0.375
        self.max_stacks = 20
        self.dialog = dialog
        self.lasts_for = 5
        self.healing_effectiveness_reduced = 33
        self.stacks_applied = 1


class Torment:
    def __init__(self, name='Torment', dialog='Am I going mad?'):
        self.label = name
        self.condition_status_effect = 'Tormented'
        self.base_damage_per_stack = 2
        self.condition_damage_modifier = 0.06
        self.weapon_level_modifier = 0.25
        self.max_stacks = 10
        self.dialog = dialog
        self.lasts_for = 5
        self.velocity_base_damage = 5
        self.stacks_applied = 1


class Blind:
    def __init__(self, name='Blind', dialog="I'm blind"):
        self.label = name
        self.condition_status_effect = 'Blinded'
        self.max_stacks = 10
        self.dialog = dialog
        self.lasts_for = 5
        self.next_attack_misses = True
        self.stacks_applied = 1


class Chill:
    def __init__(self, name='Chill', dialog='F-f-freezing'):
        self.label = name
        self.condition_status_effect = "Chilled"
        self.movement_speed_penalty = 33
        self.max_stacks = 10
        self.dialog = dialog
        self.lasts_for = 5
        self.spell_recharge_penalty = 33
        self.stacks_applied = 1


class Cripple:
    def __init__(self, name='Cripple', dialog='Not the legs!'):
        self.label = name
        self.condition_status_effect = 'Crippled'
        self.movement_speed_penalty = 50
        self.max_stacks = 10
        self.dialog = dialog
        self.lasts_for = 5
        self.stacks_applied = 1


class Fear:
    def __init__(self, name='Fear', dialog="Fall back!"):
        self.label = name
        self.condition_status_effect = 'Feared'
        self.run_away = True
        self.no_actions = True
        self.max_stacks = 10
        self.dialog = dialog
        self.lasts_for = 5
        self.stacks_applied = 1


class Immobilize:
    def __init__(self, name='Immobilize', dialog="I feel petrified"):
        self.label = name
        self.condition_status_effect = 'Immobilized'
        self.no_movement = True
        self.no_actions = True
        self.max_stacks = 10
        self.dialog = dialog
        self.lasts_for = 5
        self.stacks_applied = 1


class Vulnerability:
    def __init__(self, name='Vulnerable', dialog="Feeling vulnerable"):
        self.label = name
        self.condition_status_effect = 'Vulnerable'
        self.incoming_damage_increased = 1.5
        self.max_stacks = 10
        self.dialog = dialog
        self.lasts_for = 5
        self.stacks_applied = 1
