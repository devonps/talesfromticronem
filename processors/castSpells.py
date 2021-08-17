import esper

from components import mobiles, spells
from utilities import formulas, common, mobileHelp, scorekeeper, spellHelp, weaponManagement
from loguru import logger

from utilities.mobileHelp import MobileUtilities


class CastSpells(esper.Processor):
    def __init__(self, gameworld, game_map):
        self.gameworld = gameworld
        self.game_map = game_map

    def process(self, game_config, advance_game_turn):
        if advance_game_turn:
            # method to reduce spell cooldowns
            self.reduce_spell_cool_downs()
            # method to check if any spells should be cast this turn
            self.check_for_spells_to_be_cast_this_turn(game_config=game_config)

    def check_for_spells_to_be_cast_this_turn(self, game_config):
        current_area_tag = scorekeeper.ScorekeeperUtilities.get_current_area(gameworld=self.gameworld)
        player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=game_config)
        for ent, mob in self.gameworld.get_component(mobiles.SpellCast):
            if mob.has_cast_a_spell:
                spell_entity = mob.spell_entity
                caster_entity = mob.spell_caster
                target_entities = mob.spell_target
                spell_type = spellHelp.SpellUtilities.get_spell_type(gameworld=self.gameworld,
                                                                     spell_entity=spell_entity)
                condis_to_apply_list = spellHelp.SpellUtilities.get_all_condis_for_spell(gameworld=self.gameworld,
                                                                                         spell_entity=spell_entity)
                boons_to_apply_list = spellHelp.SpellUtilities.get_all_boons_for_spell(gameworld=self.gameworld,
                                                                                       spell_entity=spell_entity)
                spell_status_effects = [boons_to_apply_list, condis_to_apply_list]
                spell_name = spellHelp.SpellUtilities.get_spell_name(gameworld=self.gameworld,
                                                                     spell_entity=spell_entity)

                # increase meta-event spell casting value
                if ent == player_entity:
                    updated_spell_name = spell_name.replace(" ", "_")
                    updated_spell_name = current_area_tag + '_' + updated_spell_name + "_cast"
                    lower_spell_name = updated_spell_name.lower()
                    scorekeeper.ScorekeeperUtilities.increase_meta_event_by_value(gameworld=self.gameworld,
                                                                                  event_name=lower_spell_name, value=1)

                if spell_type == 'combat':
                    self.process_combat_spells(target_entities=target_entities,
                                               caster_entity=caster_entity,
                                               spell_entity=spell_entity, spell_status_effects=spell_status_effects)
                if spell_type == 'heal':
                    self.process_healing_spell(spell_type=spell_type)

                if spell_type == 'utility':
                    self.process_utility_spells(spell_name=spell_name)

                mobileHelp.MobileUtilities.stop_double_casting_same_spell(gameworld=self.gameworld, entity=ent)

    def process_utility_spells(self, spell_name):
        if spell_name == 'area portal':
            logger.debug('++++++++++++++++++++++++++')
            logger.debug('Area Portal spell has been cast')
            logger.debug('++++++++++++++++++++++++++')

            # get current scene id
            # get exit details
            # store exit details

        else:
            pass

    def process_combat_spells(self, target_entities, caster_entity, spell_entity, spell_status_effects):
        boons_to_apply = spell_status_effects[0]
        condis_to_apply = spell_status_effects[1]

        target_names = mobileHelp.MobileUtilities.get_mobile_name_details(gameworld=self.gameworld,
                                                                          entity=target_entities[0])
        spell_blocked = spellHelp.SpellUtilities.check_for_effects_stopping_spell_being_cast(gameworld=self.gameworld,
                                                                                             target_name=target_names[
                                                                                                 0],
                                                                                             target_entity=caster_entity)

        if not spell_blocked:
            if target_entities[0] > 0:
                # spell has a target entity to work against
                for target_entity in range(len(target_entities)):
                    self.apply_damage_to_target(caster_entity=caster_entity,
                                                target_entity=target_entities[target_entity],
                                                spell_entity=spell_entity)
                    mobileHelp.MobileUtilities.set_combat_status_to_true(gameworld=self.gameworld,
                                                                         entity=target_entities[target_entity])
                    mobileHelp.MobileUtilities.set_combat_status_to_true(gameworld=self.gameworld, entity=caster_entity)
                    self.apply_spell_effects(caster_entity=caster_entity, target_entity=target_entities[target_entity],
                                             condis_to_apply=condis_to_apply, boons_to_apply=boons_to_apply)
            else:
                # no target entity
                # this is where ground based spells come into force
                this_spell_is_ground_based = spellHelp.SpellUtilities.get_spell_ground_targeted_status(
                    gameworld=self.gameworld, spell_entity=spell_entity)
                if this_spell_is_ground_based:
                    logger.info('Spell {} uses ground based targeting - fix it', spell_entity)
                else:
                    # it's not ground based that means the player has misplaced the cursor!
                    logger.warning('Came to an empty code section for spell {} - is that correct?', spell_entity)

    def apply_spell_effects(self, caster_entity, target_entity, condis_to_apply, boons_to_apply):
        # Are there any conditions to apply to the target - regardless of damage caused
        if len(condis_to_apply) != 0:
            spellHelp.SpellUtilities.apply_condis_to_target(gameworld=self.gameworld, target_entity=target_entity,
                                                            list_of_condis=condis_to_apply)

        # are there any boons to apply to the spell caster - regardless of damage caused
        if len(boons_to_apply) != 0:
            spellHelp.SpellUtilities.apply_boons_to_target(gameworld=self.gameworld, target_entity=target_entity,
                                                           list_of_boons=boons_to_apply, spell_caster=caster_entity)

    def apply_damage_to_target(self, caster_entity, target_entity, spell_entity):
        spell_name = spellHelp.SpellUtilities.get_spell_name(gameworld=self.gameworld, spell_entity=spell_entity)
        target_names = mobileHelp.MobileUtilities.get_mobile_name_details(gameworld=self.gameworld,
                                                                          entity=target_entity)
        caster_names = mobileHelp.MobileUtilities.get_mobile_name_details(gameworld=self.gameworld,
                                                                          entity=caster_entity)

        equipped_weapons = mobileHelp.MobileUtilities.get_weapons_equipped(gameworld=self.gameworld,
                                                                           entity=caster_entity)
        main_weapon = equipped_weapons[0]
        off_weapon = equipped_weapons[1]
        both_weapons = equipped_weapons[2]

        if both_weapons > 0:
            current_weapon = both_weapons
        elif main_weapon > 0:
            current_weapon = main_weapon
        else:
            current_weapon = off_weapon

        damage_done_to_target, damage_applied_to_caster = self.cast_combat_spell(spell_caster=caster_entity,
                                                                                 spell=spell_entity,
                                                                                 spell_target=target_entity,
                                                                                 weapon_used=current_weapon)
        if damage_done_to_target > 0:
            # apply damage to target --> current health is used when in combat
            mobileHelp.MobileUtilities.set_current_health_during_combat(gameworld=self.gameworld, entity=target_entity,
                                                                        damage_to_apply=damage_done_to_target)

            common.CommonUtils.fire_event("spell-causes-damage", gameworld=self.gameworld, caster=caster_names[0],
                                          target=target_names[0], damage=str(damage_done_to_target),
                                          spell_name=spell_name)

        if damage_applied_to_caster > 0:
            # apply damage to caster due to status effect --> current health is used when in combat
            mobileHelp.MobileUtilities.set_current_health_during_combat(gameworld=self.gameworld, entity=caster_entity,
                                                                        damage_to_apply=damage_applied_to_caster)

            common.CommonUtils.fire_event("spell-causes-damage", gameworld=self.gameworld, caster=caster_names[0],
                                          target=caster_names[0], damage=str(damage_applied_to_caster),
                                          spell_name=spell_name)

    def process_healing_spell(self, spell_type):
        if spell_type == 'heal':
            self.cast_healing_spell()

    def reduce_spell_cool_downs(self):
        logger.warning('Spell Cooldown process activated')
        for spell_entity, (cool_down, spell_name) in self.gameworld.get_components(spells.CoolDown, spells.Name):

            cd_turns = int(cool_down.remaining_turns)
            if cd_turns > 0:
                logger.info('Spell {} is on cooldown', spell_name.label)
                logger.info('Remaining turns are {} before reduction', cd_turns)
                cd_turns -= 1
                spellHelp.SpellUtilities.set_spell_cooldown_remaining_turns(gameworld=self.gameworld,
                                                                            spell_entity=spell_entity,
                                                                            value=cd_turns)
            else:
                spellHelp.SpellUtilities.set_spell_cooldown_false(gameworld=self.gameworld, spell_entity=spell_entity)

    def get_weapon_damage_used_in_casting(self, spell_caster, weapon_used):
        equipped_weapons = mobileHelp.MobileUtilities.get_weapons_equipped(gameworld=self.gameworld,
                                                                           entity=spell_caster)
        if equipped_weapons[2] != 0:
            weapon = equipped_weapons[2]
        else:
            if weapon_used <= 2:
                weapon = equipped_weapons[0]
            else:
                weapon = equipped_weapons[1]

        weapon_strength = weaponManagement.WeaponUtilities.calculate_weapon_strength(gameworld=self.gameworld,
                                                                                     weapon=weapon)

        return weapon_strength

    def cast_combat_spell(self, spell_caster, spell, spell_target, weapon_used):
        caster_power = mobileHelp.MobileUtilities.get_mobile_primary_power(gameworld=self.gameworld,
                                                                           entity=spell_caster)
        spell_coeff = float(
            spellHelp.SpellUtilities.get_spell_damage_coeff(gameworld=self.gameworld, spell_entity=spell))
        spell_name = spellHelp.SpellUtilities.get_spell_name(gameworld=self.gameworld, spell_entity=spell)

        weapon_strength = self.get_weapon_damage_used_in_casting(spell_caster=spell_caster, weapon_used=weapon_used)
        weapon_level = weaponManagement.WeaponUtilities.get_weapon_experience_values(gameworld=self.gameworld,
                                                                                     entity=weapon_used)
        current_weapon_level = weapon_level[0]

        outgoing_base_damage = formulas.outgoing_base_damage(weapon_strength=weapon_strength, power=caster_power,
                                                             spell_coefficient=spell_coeff)
        logger.warning('------ STARTING COMBAT SPELL DAMAGE CALCULATIONS -------')
        logger.debug('Casting spell {}', spell_name)
        logger.debug('caster power {}', caster_power)
        logger.debug('weapon strength {}', weapon_strength)
        logger.debug('weapon level {}', current_weapon_level)
        logger.debug('spell coeff {}', spell_coeff)
        logger.debug('outgoing base damage {} [{} * {} * {}]', outgoing_base_damage, weapon_strength, caster_power,
                     spell_coeff)

        target_defense = mobileHelp.MobileUtilities.get_mobile_derived_armour_value(gameworld=self.gameworld,
                                                                                    entity=spell_target)
        logger.debug('target current defense rating {}', target_defense)
        if target_defense > 0:
            damage_done_before_modification = int(outgoing_base_damage / target_defense)
        else:
            damage_done_before_modification = outgoing_base_damage
        logger.debug('base damage before status effects modification {} [{} / {}]', damage_done_before_modification,
                     outgoing_base_damage, target_defense)
        current_damage = damage_done_before_modification
        damage_applied_to_caster = 0

        # 'vulnerability' is applied to the target - increases damage by 1% per stack
        spell_target_is_vulnerable, condi_stack_count = common.CommonUtils.check_if_entity_has_condi_applied(
            gameworld=self.gameworld,
            target_entity=spell_target,
            condi_being_checked='vulnerability')
        if spell_target_is_vulnerable:
            damage_to_add = formulas.calculate_percentage(low_number=condi_stack_count, max_number=current_damage)
            logger.debug('Target is vulnerable, base damage will be increased by {}% or {}', condi_stack_count,
                         damage_to_add)
            current_damage += damage_to_add
            logger.debug('Incoming damage to the target has been increased to {}', current_damage)

        # 'confusion' is applied to the caster - cannot be mitigated
        spell_caster_is_confused, condi_stack_count = common.CommonUtils.check_if_entity_has_condi_applied(
            gameworld=self.gameworld,
            target_entity=spell_caster,
            condi_being_checked='confusion')
        if spell_caster_is_confused:
            damage_to_add = formulas.calculate_condi_confusion_damage(gameworld=self.gameworld,
                                                                      caster_entity=spell_caster,
                                                                      current_weapon_level=current_weapon_level)
            logger.debug('Spell caster is confused and will suffer {} pts of direct damage for casting this spell',
                         damage_to_add)
            damage_applied_to_caster = damage_to_add

        # now check for critical damage
        critical_hit_chance = mobileHelp.MobileUtilities.get_mobile_derived_critical_hit_chance(
            gameworld=self.gameworld, entity=spell_caster)
        if critical_hit_chance >= 100:
            apply_critical_hit = True
        else:
            apply_critical_hit = formulas.get_chance_of_critical_hit(critical_hit_chance=critical_hit_chance)

        if apply_critical_hit:
            critical_damage_to_be_applied = formulas.calculate_critical_hit_damage(base_damage=current_damage,
                                                                                   ferocity_stat=1)
            logger.debug('Target has been hit with a critical strike')
            logger.debug('Critical damage is {}', critical_damage_to_be_applied)
            current_damage += critical_damage_to_be_applied

        # 'weakness' applied to the caster - each attack deals 50% less damage
        spell_caster_is_weak, condi_count = common.CommonUtils.check_if_entity_has_condi_applied(
            gameworld=self.gameworld,
            target_entity=spell_caster,
            condi_being_checked='weakness')
        if spell_caster_is_weak:
            current_damage = int(current_damage / 2)
            logger.debug('Spell caster is weak, outgoing damage has been reduced to {}', current_damage)

        # 'protection' is applied to the target - reduces incoming damage by 33%
        target_is_protected = common.CommonUtils.check_if_entity_has_boon_applied(gameworld=self.gameworld,
                                                                                  target_entity=spell_target,
                                                                                  boon_being_checked='protection')
        if target_is_protected:
            percentage_of_damage_to_remove = 33
            damage_to_be_removed = formulas.calculate_percentage(low_number=percentage_of_damage_to_remove,
                                                                 max_number=current_damage)
            logger.debug('Spell target is under protection, incoming damage will be reduced by {}% or {}pts',
                         percentage_of_damage_to_remove, damage_to_be_removed)
            current_damage -= damage_to_be_removed

        logger.debug('After all calculations damage applied to the target is {}', current_damage)
        if damage_applied_to_caster > 0:
            logger.debug('AND damage applied to the spell caster is {}', damage_applied_to_caster)

        logger.warning('------ ENDING COMBAT SPELL DAMAGE CALCULATIONS -------')
        return current_damage, damage_applied_to_caster

    def cast_healing_spell(self):
        # not yet started
        pass
