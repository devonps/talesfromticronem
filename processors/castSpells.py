import esper

from components import mobiles, spells
from utilities import formulas, configUtilities
from utilities.common import CommonUtils
from utilities.gamemap import GameMapUtilities
from utilities.itemsHelp import ItemUtilities
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
                spell_name = SpellUtilities.get_spell_name(gameworld=self.gameworld, spell_entity=mob.spell_entity)
                target_names = MobileUtilities.get_mobile_name_details(gameworld=self.gameworld,
                                                                       entity=mob.spell_target)
                logger.warning('Danger will robinson! spell being cast is:{} by entity {}', spell_name, ent)
                logger.warning('against {}', target_names[0])
                spell_type = SpellUtilities.get_spell_type(gameworld=self.gameworld, spell_entity=mob.spell_entity)
                slot_used = mob.spell_bar_slot
                condis_to_apply = SpellUtilities.get_all_condis_for_spell(gameworld=self.gameworld,
                                                                          spell_entity=mob.spell_entity)
                boons_to_apply = SpellUtilities.get_all_boons_for_spell(gameworld=self.gameworld,
                                                                        spell_entity=mob.spell_entity)
                spell_cast_coords_list = SpellUtilities.get_spell_cast_center_coords(gameworld=self.gameworld,
                                                                                     mobile_entity=ent)

                logger.info('condis attached to spell {}', condis_to_apply)
                logger.info('boons attached to spell {}', boons_to_apply)

                SpellUtilities.set_spell_cooldown_true(gameworld=self.gameworld, spell_entity=mob.spell_entity)
                number_of_turns = SpellUtilities.get_spell_cooldown_time(gameworld=self.gameworld,
                                                                         spell_entity=mob.spell_entity)

                SpellUtilities.set_spell_cooldown_remaining_turns(gameworld=self.gameworld,
                                                                  spell_entity=mob.spell_entity, value=number_of_turns)
                if spell_type == 'combat':
                    self.process_combat_spells(spell_type=spell_type, target_entity=mob.spell_target,
                                               caster_entity=mob.spell_caster, slot_used=slot_used,
                                               spell_entity=mob.spell_entity, spell_cast_coords=spell_cast_coords_list)
                if spell_type == 'heal':
                    self.process_healing_spell(spell_type=spell_type)

                MobileUtilities.stop_double_casting_same_spell(gameworld=self.gameworld, entity=ent)

    def process_combat_spells(self, spell_type, target_entity, caster_entity, slot_used, spell_entity,
                              spell_cast_coords):
        game_config = configUtilities.load_config()
        condis_to_apply = SpellUtilities.get_all_condis_for_spell(gameworld=self.gameworld,
                                                                  spell_entity=spell_entity)
        boons_to_apply = SpellUtilities.get_all_boons_for_spell(gameworld=self.gameworld,
                                                                spell_entity=spell_entity)
        spell_has_aoe_effects = SpellUtilities.get_spell_aoe_status(gameworld=self.gameworld,
                                                                    spell_entity=spell_entity)

        if spell_has_aoe_effects == 'True':
            spell_aoe_size_string = SpellUtilities.get_spell_aoe_size(gameworld=self.gameworld,
                                                                      spell_entity=spell_entity)
            logger.debug('Spell entity {}, AoE size is {}', spell_entity, spell_aoe_size_string)
            spell_aoe_size_value = configUtilities.get_config_value_as_string(configfile=game_config,
                                                                              section='spells',
                                                                              parameter=spell_aoe_size_string.upper())
            logger.debug('and that is converted to {} tiles', spell_aoe_size_value)
            spell_centre_x = spell_cast_coords[0]
            spell_centre_y = spell_cast_coords[1]

            spell_min_x, spell_max_x, spell_min_y, spell_max_y = self.adjust_aoe_start_end_tile_locations(spell_centre_x=spell_centre_x, spell_centre_y=spell_centre_y, spell_aoe_size_value=int(spell_aoe_size_value))

            for outer_loop in range(spell_min_y, spell_max_y):
                for inner_loop in range(spell_min_x, spell_max_x):
                    entity_at_aoe_location = GameMapUtilities.get_mobile_entity_at_this_location(
                        game_map=self.game_map, x=inner_loop, y=outer_loop)

                    if entity_at_aoe_location > 0:
                        target_names = MobileUtilities.get_mobile_name_details(gameworld=self.gameworld,
                                                                               entity=entity_at_aoe_location)
                        logger.warning('NPC {} has been hit by the splash damage', target_names[0])
                        # the targeted enemy is now in combat with the caster
                        MobileUtilities.set_combat_status_to_true(gameworld=self.gameworld, entity=caster_entity)
                        # if entity is here then apply damage to that entity
                        self.apply_damage_to_target(caster_entity=caster_entity, target_entity=entity_at_aoe_location,
                                                    spell_entity=spell_entity, slot_used=slot_used)
                        # apply spell effects if any
                        self.apply_spell_effects(caster_entity=caster_entity, target_entity=entity_at_aoe_location,
                                                 condis_to_apply=condis_to_apply, boons_to_apply=boons_to_apply)

        else:
            # the spell has no AoE component...
            self.apply_damage_to_target(caster_entity=caster_entity, target_entity=target_entity,
                                        spell_entity=spell_entity, slot_used=slot_used)
            MobileUtilities.set_combat_status_to_true(gameworld=self.gameworld, entity=target_entity)
            MobileUtilities.set_combat_status_to_true(gameworld=self.gameworld, entity=caster_entity)
            self.apply_spell_effects(caster_entity=caster_entity, target_entity=target_entity,
                                     condis_to_apply=condis_to_apply, boons_to_apply=boons_to_apply)

    def adjust_aoe_start_end_tile_locations(self, spell_centre_x, spell_centre_y, spell_aoe_size_value):
        spell_min_x = spell_centre_x - spell_aoe_size_value
        spell_max_x = (spell_centre_x + spell_aoe_size_value) + 1
        spell_min_y = spell_centre_y - spell_aoe_size_value
        spell_max_y = (spell_centre_y + spell_aoe_size_value) + 1

        if spell_min_x < 1:
            spell_min_x = 1
        if spell_min_y < 1:
            spell_min_y = 1
        if spell_max_x > self.game_map.width:
            spell_max_x = self.game_map.width
        if spell_max_y > self.game_map.height:
            spell_max_y = self.game_map.height

        return spell_min_x, spell_max_x, spell_min_y, spell_max_y

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

        logger.debug('weapon strength {}', weapon_strength)
        logger.debug('spell coeff {}', spell_coeff)
        logger.debug('base damage {}', outgoing_base_damage)

        target_defense = MobileUtilities.get_mobile_derived_armour_value(gameworld=self.gameworld, entity=spell_target)
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
