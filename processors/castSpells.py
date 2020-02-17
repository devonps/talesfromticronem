import esper

from components import mobiles
from components.messages import Message
from utilities import formulas
from utilities.common import CommonUtils
from utilities.itemsHelp import ItemUtilities
from utilities.mobileHelp import MobileUtilities
from utilities.replayGame import ReplayGame
from loguru import logger

from utilities.spellHelp import SpellUtilities


class CastSpells(esper.Processor):
    def __init__(self, gameworld, game_map):
        super().__init__()
        self.gameworld = gameworld
        self.game_map = game_map

    def process(self, game_config):
        player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=game_config)
        message_log_id = MobileUtilities.get_MessageLog_id(gameworld=self.gameworld, entity=player_entity)

        for ent, mob in self.gameworld.get_component(mobiles.SpellCast):
            if mob.truefalse:
                spell_name = SpellUtilities.get_spell_name(gameworld=self.gameworld, spell_entity=mob.spell_entity)
                target_names = MobileUtilities.get_mobile_name_details(gameworld=self.gameworld, entity=mob.spell_target)
                logger.warning('Danger will robinson! spell being cast is:{}', spell_name)
                logger.warning('against {}', target_names[0])
                msg = Message(text=target_names[0] + " has been targeted.", msgclass="all", fg="white", bg="black", fnt="")
                CommonUtils.add_message(gameworld=self.gameworld, message=msg, logid=message_log_id)
                MobileUtilities.stop_double_casting_same_spell(gameworld=self.gameworld, entity=player_entity)
                spell_type = SpellUtilities.get_spell_type(gameworld=self.gameworld, spell_entity=mob.spell_entity)
                slotUsed = mob.spell_bar_slot
                if spell_type == 'combat':
                    # set inCombat to true for the target and the player --> stops health being recalculated
                    # automatically, amongst other things
                    MobileUtilities.set_combat_status_to_true(gameworld=self.gameworld, entity=mob.spell_target)
                    MobileUtilities.set_combat_status_to_true(gameworld=self.gameworld, entity=player_entity)

                    damage_done_to_target = self.cast_combat_spell(player=player_entity, spell_name=spell_name, spell=mob.spell_entity, target=mob.spell_target, weapon_used=slotUsed, message_log_id=message_log_id)
                    if damage_done_to_target > 0:
                        # apply damage to target --> current health is used when in combat
                        MobileUtilities.set_current_health_during_combat(gameworld=self.gameworld, entity=mob.spell_target, damageToApply=damage_done_to_target)

                        # display message in combat log
                        CommonUtils.format_combat_log_message(gameworld=self.gameworld, target=target_names[0],
                                                              damage_done_to_target=damage_done_to_target,
                                                              spell_name=spell_name, message_log_id=message_log_id)

                if spell_type == 'heal':
                    self.cast_healing_spell()

    def cast_combat_spell(self, player, spell, target, weapon_used, spell_name, message_log_id):
        equipped_weapons = MobileUtilities.get_weapons_equipped(gameworld=self.gameworld, entity=player)
        caster_power = MobileUtilities.get_mobile_power(gameworld=self.gameworld, entity=player)
        spell_coeff = float(SpellUtilities.get_spell_DamageCoeff(gameworld=self.gameworld, spell_entity=spell))

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

        target_defense = MobileUtilities.get_derived_armour_value(gameworld=self.gameworld, entity=target)
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
        pass
