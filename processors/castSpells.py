import esper

from components import mobiles
from utilities import formulas
from utilities.common import CommonUtils
from utilities.itemsHelp import ItemUtilities
from utilities.mobileHelp import MobileUtilities
from loguru import logger

from utilities.spellHelp import SpellUtilities


class CastSpells(esper.Processor):
    def __init__(self, gameworld, game_map):
        self.gameworld = gameworld
        self.game_map = game_map

    def process(self, game_config):
        player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=game_config)
        message_log_id = MobileUtilities.get_MessageLog_id(gameworld=self.gameworld, entity=player_entity)

        for ent, mob in self.gameworld.get_component(mobiles.SpellCast):
            if mob.truefalse:
                spell_name = SpellUtilities.get_spell_name(gameworld=self.gameworld, spell_entity=mob.spell_entity)
                target_names = MobileUtilities.get_mobile_name_details(gameworld=self.gameworld,
                                                                       entity=mob.spell_target)
                caster_name = MobileUtilities.get_mobile_name_details(gameworld=self.gameworld, entity=mob.spell_caster)
                logger.warning('Danger will robinson! spell being cast is:{} by entity {}', spell_name, ent)
                logger.warning('against {}', target_names[0])
                MobileUtilities.stop_double_casting_same_spell(gameworld=self.gameworld, entity=player_entity)
                spell_type = SpellUtilities.get_spell_type(gameworld=self.gameworld, spell_entity=mob.spell_entity)
                slot_used = mob.spell_bar_slot
                condis_to_apply = SpellUtilities.get_all_condis_for_spell(gameworld=self.gameworld,
                                                                          spell_entity=mob.spell_entity)
                boons_to_apply = SpellUtilities.get_all_boons_for_spell(gameworld=self.gameworld,
                                                                        spell_entity=mob.spell_entity)
                controls_to_apply = SpellUtilities.get_all_controls_for_spell(gameworld=self.gameworld,
                                                                              spell_entity=mob.spell_entity)
                resources_to_apply = SpellUtilities.get_all_resources_for_spell(gameworld=self.gameworld,
                                                                                spell_entity=mob.spell_entity)
                logger.info('condis attached to spell {}', condis_to_apply)
                logger.info('boons attached to spell {}', boons_to_apply)

                if spell_type == 'combat':
                    # set inCombat to true for the target and the player --> stops health being recalculated
                    # automatically, amongst other things
                    MobileUtilities.set_combat_status_to_true(gameworld=self.gameworld, entity=mob.spell_target)
                    MobileUtilities.set_combat_status_to_true(gameworld=self.gameworld, entity=player_entity)

                    damage_done_to_target = self.cast_combat_spell(spell_caster=player_entity,spell=mob.spell_entity,
                                                                   spell_target=mob.spell_target, weapon_used=slot_used)
                    if damage_done_to_target > 0:
                        # apply damage to target --> current health is used when in combat
                        MobileUtilities.set_current_health_during_combat(gameworld=self.gameworld,
                                                                         entity=mob.spell_target,
                                                                         damage_to_apply=damage_done_to_target)

                        CommonUtils.format_combat_log_message(gameworld=self.gameworld, caster_name=caster_name[0], target_name=target_names[0],
                                                              damage_done_to_target=damage_done_to_target,
                                                              spell_name=spell_name)
                if spell_type == 'heal':
                    self.cast_healing_spell()

                # Are there any conditions to apply to the target - regardless of damage caused
                if len(condis_to_apply) != 0:
                    SpellUtilities.apply_condis_to_target(gameworld=self.gameworld, target_entity=mob.spell_target,
                                                          list_of_condis=condis_to_apply)

                # are there any boons to apply to the spell caster - regardless of damage caused
                if len(boons_to_apply) != 0:
                    SpellUtilities.apply_boons_to_target(gameworld=self.gameworld, target_entity=mob.spell_target,
                                                         list_of_boons=boons_to_apply, spell_caster=ent)

    def cast_combat_spell(self, spell_caster, spell, spell_target, weapon_used):
        equipped_weapons = MobileUtilities.get_weapons_equipped(gameworld=self.gameworld, entity=spell_caster)
        caster_power = MobileUtilities.get_mobile_power(gameworld=self.gameworld, entity=spell_caster)
        spell_coeff = float(SpellUtilities.get_spell_damage_coeff(gameworld=self.gameworld, spell_entity=spell))

        if equipped_weapons[2] != 0:
            weapon = equipped_weapons[2]
        else:
            if weapon_used <= 2:
                weapon = equipped_weapons[0]
            else:
                weapon = equipped_weapons[1]

        weapon_strength = ItemUtilities.calculate_weapon_strength(gameworld=self.gameworld, weapon=weapon)
        outgoing_base_damage = formulas.outgoing_base_damage(weapon_strength=weapon_strength, power=caster_power,
                                                             spell_coefficient=spell_coeff)

        logger.debug('weapon strength {}', weapon_strength)
        logger.debug('spell coeff {}', spell_coeff)
        logger.debug('base damage {}', outgoing_base_damage)

        target_defense = MobileUtilities.get_derived_armour_value(gameworld=self.gameworld, entity=spell_target)
        critical_hit = -99
        weakness = -99
        vulnerability = -99
        protection = -99

        logger.debug('target defense rating {}', target_defense)

        damage_done = int(outgoing_base_damage / target_defense)

        logger.debug('Calculated damage - after armour - before further modification {}', damage_done)
        logger.info('damage modified by critical hits {}', critical_hit)
        logger.info('damage modified by weakness {}', weakness)
        logger.info('damage modified by vulnerability {}', vulnerability)
        logger.info('damage modified by protection {}', protection)

        return damage_done

    def cast_healing_spell(self):
        # not yet started
        pass
