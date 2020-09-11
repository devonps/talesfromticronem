import esper

from components import mobiles, spells
from utilities import formulas
from utilities.common import CommonUtils
from utilities.mobileHelp import MobileUtilities
from loguru import logger

from utilities.spellHelp import SpellUtilities
from utilities.weaponManagement import WeaponUtilities


class CastSpells(esper.Processor):
    def __init__(self, gameworld, game_map):
        self.gameworld = gameworld
        self.game_map = game_map

    def process(self, game_config, advance_game_turn):
        if advance_game_turn:
            # method to reduce spell cooldowns
            self.reduce_spell_cool_downs()
            # method to check if any spells should be cast this turn
            self.check_for_spells_to_be_cast_this_turn()

    def check_for_spells_to_be_cast_this_turn(self):
        for ent, mob in self.gameworld.get_component(mobiles.SpellCast):
            if mob.has_cast_a_spell:
                spell_entity = mob.spell_entity
                caster_entity = mob.spell_caster
                spell_bar_slot_used = mob.spell_bar_slot
                target_entities = mob.spell_target
                spell_type = SpellUtilities.get_spell_type(gameworld=self.gameworld, spell_entity=spell_entity)
                condis_to_apply_list = SpellUtilities.get_all_condis_for_spell(gameworld=self.gameworld,
                                                                               spell_entity=spell_entity)
                boons_to_apply_list = SpellUtilities.get_all_boons_for_spell(gameworld=self.gameworld,
                                                                             spell_entity=spell_entity)
                spell_status_effects = [boons_to_apply_list, condis_to_apply_list]

                self.set_spell_cooldown_value(spell_entity=spell_entity)

                if spell_type == 'combat':
                    self.process_combat_spells(target_entities=target_entities,
                                               caster_entity=caster_entity, slot_used=spell_bar_slot_used,
                                               spell_entity=spell_entity, spell_status_effects=spell_status_effects)
                if spell_type == 'heal':
                    self.process_healing_spell(spell_type=spell_type)

                MobileUtilities.stop_double_casting_same_spell(gameworld=self.gameworld, entity=ent)

    def set_spell_cooldown_value(self, spell_entity):
        SpellUtilities.set_spell_cooldown_true(gameworld=self.gameworld, spell_entity=spell_entity)
        number_of_turns = SpellUtilities.get_spell_cooldown_time(gameworld=self.gameworld,
                                                                 spell_entity=spell_entity)

        SpellUtilities.set_spell_cooldown_remaining_turns(gameworld=self.gameworld,
                                                          spell_entity=spell_entity, value=number_of_turns - 1)

    def process_combat_spells(self, target_entities, caster_entity, slot_used, spell_entity, spell_status_effects):
        boons_to_apply = spell_status_effects[0]
        condis_to_apply = spell_status_effects[1]

        target_names = MobileUtilities.get_mobile_name_details(gameworld=self.gameworld, entity=target_entities[0])
        spell_blocked = SpellUtilities.check_for_spell_cast_blocks(gameworld=self.gameworld, target_name=target_names[0], target_entity=caster_entity)

        if not spell_blocked:
            if target_entities[0] > 0:
                # spell has a target entity to work against
                for target_entity in range(len(target_entities)):
                    self.apply_damage_to_target(caster_entity=caster_entity, target_entity=target_entities[target_entity],
                                                spell_entity=spell_entity, slot_used=slot_used)
                    MobileUtilities.set_combat_status_to_true(gameworld=self.gameworld, entity=target_entities[target_entity])
                    MobileUtilities.set_combat_status_to_true(gameworld=self.gameworld, entity=caster_entity)
                    self.apply_spell_effects(caster_entity=caster_entity, target_entity=target_entities[target_entity],
                                             condis_to_apply=condis_to_apply, boons_to_apply=boons_to_apply)
            else:
                # no target entity
                # this is where ground based spells come into force
                this_spell_is_ground_based = SpellUtilities.get_spell_ground_targeted_status(gameworld=self.gameworld, spell_entity=spell_entity)
                if this_spell_is_ground_based:
                    logger.info('Spell {} uses ground based targeting - fix it', spell_entity)
                else:
                    # it's not ground based that means the player has misplaced the cursor!
                    logger.warning('Came to an empty code section for spell {} - is that correct?', spell_entity)

    def apply_spell_effects(self, caster_entity, target_entity, condis_to_apply, boons_to_apply):
        # Are there any conditions to apply to the target - regardless of damage caused
        if len(condis_to_apply) != 0:
            SpellUtilities.apply_condis_to_target(gameworld=self.gameworld, target_entity=target_entity,
                                                  list_of_condis=condis_to_apply)

        # are there any boons to apply to the spell caster - regardless of damage caused
        if len(boons_to_apply) != 0:
            SpellUtilities.apply_boons_to_target(gameworld=self.gameworld, target_entity=target_entity,
                                                 list_of_boons=boons_to_apply, spell_caster=caster_entity)

    def apply_damage_to_target(self, caster_entity, target_entity, spell_entity, slot_used):
        spell_name = SpellUtilities.get_spell_name(gameworld=self.gameworld, spell_entity=spell_entity)
        target_names = MobileUtilities.get_mobile_name_details(gameworld=self.gameworld,
                                                               entity=target_entity)
        caster_names = MobileUtilities.get_mobile_name_details(gameworld=self.gameworld, entity=caster_entity)
        damage_done_to_target = self.cast_combat_spell(spell_caster=caster_entity, spell=spell_entity,
                                                       spell_target=target_entity, weapon_used=slot_used)
        if damage_done_to_target > 0:
            # apply damage to target --> current health is used when in combat
            MobileUtilities.set_current_health_during_combat(gameworld=self.gameworld, entity=target_entity,
                                                             damage_to_apply=damage_done_to_target)

            CommonUtils.fire_event("spell-causes-damage", gameworld=self.gameworld, caster=caster_names[0],
                                   target=target_names[0], damage=str(damage_done_to_target), spell_name=spell_name)

    def process_healing_spell(self, spell_type):
        if spell_type == 'heal':
            self.cast_healing_spell()

    def reduce_spell_cool_downs(self):
        for spell_entity, cool_down in self.gameworld.get_component(spells.CoolDown):

            cd_turns = int(cool_down.remaining_turns)
            if cd_turns > 0:
                cd_turns -= 1
                SpellUtilities.set_spell_cooldown_remaining_turns(gameworld=self.gameworld, spell_entity=spell_entity,
                                                                  value=cd_turns)
            else:
                SpellUtilities.set_spell_cooldown_false(gameworld=self.gameworld, spell_entity=spell_entity)

    def get_weapon_damage_used_in_casting(self, spell_caster, weapon_used):
        equipped_weapons = MobileUtilities.get_weapons_equipped(gameworld=self.gameworld, entity=spell_caster)
        if equipped_weapons[2] != 0:
            weapon = equipped_weapons[2]
        else:
            if weapon_used <= 2:
                weapon = equipped_weapons[0]
            else:
                weapon = equipped_weapons[1]

        weapon_strength = WeaponUtilities.calculate_weapon_strength(gameworld=self.gameworld, weapon=weapon)

        return weapon_strength

    def cast_combat_spell(self, spell_caster, spell, spell_target, weapon_used):
        caster_power = MobileUtilities.get_mobile_primary_power(gameworld=self.gameworld, entity=spell_caster)
        spell_coeff = float(SpellUtilities.get_spell_damage_coeff(gameworld=self.gameworld, spell_entity=spell))

        weapon_strength = self.get_weapon_damage_used_in_casting(spell_caster=spell_caster, weapon_used=weapon_used)

        outgoing_base_damage = formulas.outgoing_base_damage(weapon_strength=weapon_strength, power=caster_power,
                                                             spell_coefficient=spell_coeff)

        critical_damage_to_be_applied = 0

        logger.debug('weapon strength {}', weapon_strength)
        logger.debug('spell coeff {}', spell_coeff)
        logger.debug('base damage {}', outgoing_base_damage)

        target_defense = MobileUtilities.get_mobile_derived_armour_value(gameworld=self.gameworld, entity=spell_target)
        critical_hit_chance = MobileUtilities.get_mobile_derived_critical_hit_chance(gameworld=self.gameworld, entity=spell_caster)

        if critical_hit_chance >= 100:
            apply_critical_hit = True
        else:
            apply_critical_hit = formulas.get_chance_of_critical_hit(critical_hit_chance=critical_hit_chance)

        if apply_critical_hit:
            critical_damage_to_be_applied = formulas.calculate_critical_hit_damage(crit_hit_chance=critical_hit_chance, base_damage=outgoing_base_damage, ferocity_stat=1)
        logger.info('Critical hit has popped')
        logger.info('Critical damage is {}', critical_damage_to_be_applied)

        damage_done_before_modification = int(outgoing_base_damage / target_defense)
        current_damage = damage_done_before_modification
        # 'weakness' applied to the caster - each attack deals 50% less damage
        condi_is_attached_to_player = CommonUtils.check_if_entity_has_condi_applied(gameworld=self.gameworld,
                                                                                    target_entity=spell_caster,
                                                                                    condi_being_checked='weakness')
        if condi_is_attached_to_player:
            current_damage = current_damage / 2
            logger.info('damage modified by weakness')

        # 'vulnerability' is applied to the target - increases damage by 1% per stack
        condi_is_attached_to_the_target = CommonUtils.check_if_entity_has_condi_applied(gameworld=self.gameworld,
                                                                                    target_entity=spell_target,
                                                                                    condi_being_checked='vulnerability')
        if condi_is_attached_to_the_target:
            # in this formula the '1' has to be replaced with the number of stacks
            damage_to_add = formulas.calculate_percentage(low_number=1, max_number=current_damage)
            current_damage += damage_to_add
            logger.info('Incoming damage to the target modified by vulnerability is {}', current_damage )

        # 'protection' is applied to the target - reduces incoming damage by 33%
        protection = -99

        logger.debug('target defense rating {}', target_defense)
        logger.debug('Calculated damage - after armour {}', damage_done_before_modification)


        logger.info('damage modified by vulnerability {}', vulnerability)
        logger.info('damage modified by protection {}', protection)

        return damage_done

    def cast_healing_spell(self):
        # not yet started
        pass
