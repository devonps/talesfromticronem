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
        message_log_just_viewed = MobileUtilities.get_view_message_log_value(gameworld=self.gameworld,
                                                                             entity=player_entity)

        if not message_log_just_viewed:
            message_log_id = MobileUtilities.get_MessageLog_id(gameworld=self.gameworld, entity=player_entity)

            for ent, ai in self.gameworld.get_component(mobiles.AI):
                in_combat = MobileUtilities.get_combat_status(self.gameworld, entity=ent)
                entity_names = MobileUtilities.get_mobile_name_details(gameworld=self.gameworld, entity=ent)

                self.apply_conditions(entity_names=entity_names, player_entity=player_entity,
                                      message_log_id=message_log_id, target_entity=ent)
                self.apply_boons(entity_names=entity_names, player_entity=player_entity, message_log_id=message_log_id,
                                 target_entity=ent)
                # apply controls
                # gain resources from spells

                if not in_combat:
                    MobileUtilities.set_mobile_derived_derived_attributes(self.gameworld, entity=ent)

    def apply_conditions(self, entity_names, player_entity, message_log_id, target_entity):

        current_turn = MobileUtilities.get_current_turn(gameworld=self.gameworld, entity=player_entity)
        formatted_turn_number = CommonUtils.format_game_turn_as_string(current_turn=current_turn)
        current_condis = MobileUtilities.get_current_condis_applied_to_mobile(gameworld=self.gameworld,
                                                                              entity=target_entity)
        if len(current_condis) != 0:
            logger.warning('Current entity name being processed is {} who has {} applied', entity_names[0],
                           current_condis)

            condition_damage_stat_value = MobileUtilities.get_mobile_secondary_condition_damage(gameworld=self.gameworld,
                                                                                                entity=player_entity)
            ps = 0
            for condi in current_condis:
                condi_name = condi['name']
                duration = condi['duration']
                duration -= 1
                current_condis[ps]['duration'] = duration
                base_damage_per_stack = condi['baseDamage']
                condition_damage_mod = condi['condDamageMod']
                weapon_level_mod = condi['weaponLevelMod']

                damage_applied_this_turn = formulas.base_condi_damage(condition_damage_modifier=condition_damage_mod,
                                                                      condition_damage_stat=condition_damage_stat_value,
                                                                      weapon_level_modifier=weapon_level_mod,
                                                                      base_damage_per_stack=base_damage_per_stack,
                                                                      weapon_level=1)

                # add message to combat log showing how much damage has been applied to the target
                message_text = formatted_turn_number + ":" + entity_names[0] + " takes [color=MSGLOG_COMBAT_DAMAGE_OUTGOING]" + str(
                    damage_applied_this_turn) + " damage [/color]from [color=MSGLOG_COMBAT_DAMAGE_OUTGOING][[" + condi_name + "]][/color]"

                msg = Message(text=message_text, msgclass=1, fg="white", bg="black", fnt="")
                log_message = formatted_turn_number + ":" + entity_names[0] + " takes " + str(damage_applied_this_turn) + " damage from [" + condi_name + "]"
                CommonUtils.add_message(gameworld=self.gameworld, message=msg, logid=message_log_id, message_for_export=log_message)

                if duration <= 0:
                    self.remove_condition(entity_name=entity_names[0], current_condis=current_condis, message_log_id=message_log_id, ps=ps, condi_name=condi_name, entity_id=player_entity)
                else:
                    status_effects_component = self.gameworld.component_for_entity(target_entity, mobiles.StatusEffects)
                    status_effects_component.conditions = current_condis

                logger.debug('Condis applied to {} is {}', entity_names[0], current_condis)
                ps += 1

    def apply_boons(self, entity_names, player_entity, message_log_id, target_entity):

        current_turn = MobileUtilities.get_current_turn(gameworld=self.gameworld, entity=player_entity)
        formatted_turn_number = CommonUtils.format_game_turn_as_string(current_turn=current_turn)
        current_boons = MobileUtilities.get_current_boons_applied_to_mobile(gameworld=self.gameworld, entity=target_entity)
        if len(current_boons) != 0:
            ps = 0
            for boon in current_boons:
                boon_name = boon['name']
                duration = boon['duration']
                duration -= 1
                current_boons[ps]['duration'] = duration

                msg_stat = 555

                if boon_name == 'fury':
                    msg_stat = boon['improvement']

                # add message to combat log showing effect
                message_text = formatted_turn_number + ":" + entity_names[0] + " gains [color=MSGLOG_GAME_APPLY_BOON]" + str(msg_stat) + " [/color]from [color=MSGLOG_GAME_APPLY_BOON][[" + boon_name + "]][/color]"
                msg = Message(text=message_text, msgclass=1, fg="white", bg="black", fnt="")
                log_message = formatted_turn_number + ":" + entity_names[0] + " gains " + str(msg_stat) + " from [" + boon_name + "]"
                CommonUtils.add_message(gameworld=self.gameworld, message=msg, logid=message_log_id, message_for_export=log_message)

                if duration <= 0:
                    self.remove_boon(entity_name=entity_names[0], current_boons=current_boons, message_log_id=message_log_id, ps=ps, boon_name=boon_name, entity_id=player_entity)
                else:
                    status_effects_component = self.gameworld.component_for_entity(target_entity, mobiles.StatusEffects)
                    status_effects_component.boons = current_boons
                    current_boons = MobileUtilities.get_current_boons_applied_to_mobile(gameworld=self.gameworld,
                                                                                        entity=target_entity)
                ps += 1

    def remove_boon(self, entity_name, current_boons, message_log_id, ps, boon_name, entity_id):
        del current_boons[ps]
        current_turn = MobileUtilities.get_current_turn(gameworld=self.gameworld, entity=entity_id)
        formatted_turn_number = CommonUtils.format_game_turn_as_string(current_turn=current_turn)

        # add message to combat log showing loss of effect
        message_text = formatted_turn_number + ":" + entity_name + " loses [color=MSGLOG_GAME_REMOVE_BOON][[" + boon_name + "]][/color]"
        msg = Message(text=message_text, msgclass=1, fg="white", bg="black", fnt="")
        log_message = formatted_turn_number + ":" + entity_name + " loses [" + boon_name + "]"
        CommonUtils.add_message(gameworld=self.gameworld, message=msg, logid=message_log_id, message_for_export=log_message)

    def remove_condition(self, entity_name, current_condis, message_log_id, ps, condi_name, entity_id):
        del current_condis[ps]
        current_turn = MobileUtilities.get_current_turn(gameworld=self.gameworld, entity=entity_id)
        formatted_turn_number = CommonUtils.format_game_turn_as_string(current_turn=current_turn)

        # add message to combat log showing loss of effect
        message_text = formatted_turn_number + ":" + entity_name + " is no longer [color=MSGLOG_GAME_REMOVE_CONDITION]" + condi_name + "[/color]"
        msg = Message(text=message_text, msgclass=1, fg="white", bg="black", fnt="")
        log_message = formatted_turn_number + ":" + entity_name + " is no longer " + condi_name
        CommonUtils.add_message(gameworld=self.gameworld, message=msg, logid=message_log_id, message_for_export=log_message)