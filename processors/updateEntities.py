import esper
from loguru import logger

from components import mobiles
from components.messages import Message
from utilities import formulas
from utilities.common import CommonUtils
from utilities.mobileHelp import MobileUtilities


class UpdateEntitiesProcessor(esper.Processor):
    """
    This processor cycles through ALL entities and calculates their attributes
    """

    def __init__(self, gameworld):
        self.gameworld = gameworld

    def process(self, game_config):

        player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=game_config)
        message_log_just_viewed = MobileUtilities.get_view_message_log_value(gameworld=self.gameworld, entity=player_entity)
        if not message_log_just_viewed:

            message_log_id = MobileUtilities.get_MessageLog_id(gameworld=self.gameworld, entity=player_entity)

            for ent, ai in self.gameworld.get_component(mobiles.AI):
                inCombat = MobileUtilities.get_combat_status(self.gameworld, entity=ent)
                entity_names = MobileUtilities.get_mobile_name_details(gameworld=self.gameworld, entity=ent)

                # get list of condis applied to current entity
                self.apply_conditions(entity_names=entity_names, player_entity=player_entity, message_log_id=message_log_id, target_entity=ent)
                self.apply_boons(entity_names=entity_names, player_entity=player_entity, message_log_id=message_log_id, target_entity=ent)
                # apply controls
                # gain resources from spells

                if not inCombat:
                    MobileUtilities.calculate_derived_attributes(self.gameworld, entity=ent)

    def apply_conditions(self, entity_names, player_entity, message_log_id, target_entity):
        current_condis = MobileUtilities.get_current_condis_applied_to_mobile(gameworld=self.gameworld, entity=target_entity)
        if len(current_condis) != 0:
            logger.warning('Current entity name being processed is {} who has {} applied', entity_names[0],
                           current_condis)

            condition_damage_stat_value = MobileUtilities.get_mobile_condition_damage(gameworld=self.gameworld,
                                                                                      entity=player_entity)
            ps = 0
            for condi in current_condis:
                condi_name = condi['name']
                duration = condi['duration']
                duration -= 1
                current_condis[ps]['duration'] = duration
                baseDamagePerStack = condi['baseDamage']
                conditionDamageMod = condi['condDamageMod']
                weaponLevelMod = condi['weaponLevelMod']

                damage_applied_this_turn = formulas.base_condi_damage(condition_damage_modifier=conditionDamageMod,
                                                                      condition_damage_stat=condition_damage_stat_value,
                                                                      weapon_level_modifier=weaponLevelMod,
                                                                      base_damage_per_stack=baseDamagePerStack,
                                                                      weapon_level=1)
                dialogue = condi['dialogue']

                # add dialog for condition damage to message log
                # msg = Message(text=entity_names[0] + " screams: " + dialogue, msgclass="all", fg="white", bg="black", fnt="")
                # CommonUtils.add_message(gameworld=self.gameworld, message=msg, logid=message_log_id)

                # add message to combat log showing how much damage has been applied to the target
                msg = Message(text=entity_names[0] + " takes [color=orange]" + str(
                    damage_applied_this_turn) + " [/color]from [[" + condi_name + "]]", msgclass="combat", fg="white",
                              bg="black", fnt="")
                CommonUtils.add_message(gameworld=self.gameworld, message=msg, logid=message_log_id)

                if duration <= 0:
                    del current_condis[ps]
                else:
                    status_effects_component = self.gameworld.component_for_entity(target_entity, mobiles.StatusEffects)
                    status_effects_component.conditions = current_condis

                logger.debug('Condis applied to {} is {}', entity_names[0], current_condis)
                ps += 1

    def apply_boons(self, entity_names, player_entity, message_log_id, target_entity):

        current_boons = MobileUtilities.get_current_boons_applied_to_mobile(gameworld=self.gameworld, entity=target_entity)

        if len(current_boons) != 0:
            ps = 0
            for boon in current_boons:
                boon_name = boon['name']
                duration = boon['duration']
                duration -= 1
                current_boons[ps]['duration'] = duration
                dialogue = boon['dialogue']

                msg_stat = '-nothing-'

                if boon_name == 'fury':
                    msg_stat = boon['improvement']

                # add message to combat log showing effect
                msg = Message(
                    text=entity_names[0] + " gains [color=orange]" + msg_stat + " [/color]from [[" + boon_name + "]]",
                    msgclass="combat",
                    fg="white", bg="black", fnt="")
                CommonUtils.add_message(gameworld=self.gameworld, message=msg, logid=message_log_id)

                if duration <= 0:
                    del current_boons[ps]
                    # add message to combat log showing loss of effect
                    msg = Message(text=entity_names[
                                           0] + " loses [color=orange]" + msg_stat + " [/color]from [[" + boon_name + "]]",
                                  msgclass="combat",
                                  fg="white", bg="black", fnt="")
                    CommonUtils.add_message(gameworld=self.gameworld, message=msg, logid=message_log_id)
                else:
                    status_effects_component = self.gameworld.component_for_entity(target_entity, mobiles.StatusEffects)
                    status_effects_component.boons = current_boons
                    current_boons = MobileUtilities.get_current_boons_applied_to_mobile(gameworld=self.gameworld,
                                                                                        entity=target_entity)
                ps += 1
