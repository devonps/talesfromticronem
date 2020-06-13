
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
    def __init__(self, name='Blind', condition_status_effect='Blinded', max_stacks=10, dialog="I'm blind",
                 lasts_for=5, next_attack_misses=True, stacks_applied=1):
        self.label = name
        self.condition_status_effect = 'Blinded'
        self.max_stacks = 10
        self.dialog = dialog
        self.lasts_for = lasts_for
        self.next_attack_misses = next_attack_misses
        self.stacks_applied = stacks_applied


class Chill:
    def __init__(self, name='Chill', condition_status_effect='Chilled', movement_speed_penalty=33,
                 max_stacks=10, dialog='F-f-freezing', lasts_for=5, spell_recharge_penalty=33, stacks_applied=1):
        self.label = name
        self.condition_status_effect = condition_status_effect
        self.movement_speed_penalty = movement_speed_penalty
        self.max_stacks = max_stacks
        self.dialog = dialog
        self.lasts_for = lasts_for
        self.spell_recharge_penalty = spell_recharge_penalty
        self.stacks_applied = stacks_applied


class Cripple:
    def __init__(self, name='Cripple', condition_status_effect='Crippled', movement_speed_penalty=50,
                 max_stacks=10, dialog='Not the legs!', lasts_for=5, stacks_applied=1):
        self.label = name
        self.condition_status_effect = condition_status_effect
        self.movement_speed_penalty = movement_speed_penalty
        self.max_stacks = max_stacks
        self.dialog = dialog
        self.lasts_for = lasts_for
        self.stacks_applied = stacks_applied


class Fear:
    def __init__(self, name='Fear', condition_status_effect='Feared', run_away=True,
                 no_actions=True, max_stacks=10, dialog="Fall back!",
                 lasts_for=5, stacks_applied=1):
        self.label = name
        self.condition_status_effect = condition_status_effect
        self.run_away = run_away
        self.no_actions = no_actions
        self.max_stacks = max_stacks
        self.dialog = dialog
        self.lasts_for = lasts_for
        self.stacks_applied = stacks_applied


class Immobilize:
    def __init__(self, name='Immobilize', condition_status_effect='Immobilized', no_movement=True,
                 no_actions=True, max_stacks=10, dialog="I feel petrified",
                 lasts_for=5, stacks_applied=1):
        self.label = name
        self.condition_status_effect = condition_status_effect
        self.no_movement = no_movement
        self.no_actions = no_actions
        self.max_stacks = max_stacks
        self.dialog = dialog
        self.lasts_for = lasts_for
        self.stacks_applied = stacks_applied


class Vulnerability:
    def __init__(self, name='Vulnerable', condition_status_effect='Vulnerable', incoming_damage_increased=1.5,
                 max_stacks=10, dialog="Feeling vulnerable",
                 lasts_for=5, stacks_applied=1):
        self.label = name
        self.condition_status_effect = condition_status_effect
        self.incoming_damage_increased = incoming_damage_increased
        self.max_stacks = max_stacks
        self.dialog = dialog
        self.lasts_for = lasts_for
        self.stacks_applied = stacks_applied


class Selfbleeding:
    def __init__(self, name='Bleed', condition_status_effect='Bleeding', base_damage_per_stack=2,
                 condition_damage_modifier=0.06, weapon_level_modifier=0.25, max_stacks=10, dialog="I'm bleeding",
                 lasts_for=3, stacks_applied=1):
        self.label = name
        self.condition_status_effect = condition_status_effect
        self.base_damage_per_stack = base_damage_per_stack
        self.condition_damage_modifier = condition_damage_modifier
        self.weapon_level_modifier = weapon_level_modifier
        self.max_stacks = max_stacks
        self.dialog = dialog
        self.lasts_for = lasts_for
        self.stacks_applied = stacks_applied