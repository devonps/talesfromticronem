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
        for ent, ai in self.gameworld.get_component(mobiles.AI):
            inCombat = MobileUtilities.get_combat_status(self.gameworld, entity=ent)
            entity_names = MobileUtilities.get_mobile_name_details(gameworld=self.gameworld, entity=ent)
            player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=game_config)
            message_log_id = MobileUtilities.get_MessageLog_id(gameworld=self.gameworld, entity=player_entity)
            condition_damage_stat_value = MobileUtilities.get_mobile_condition_damage(gameworld=self.gameworld, entity=player_entity)

            # apply condition damage to those entities that have it

            # get list of condis applied to current entity
            current_condis = MobileUtilities.get_current_condis_applied_to_mobile(gameworld=self.gameworld, entity=ent)
            if len(current_condis) != 0:
                # logger.warning('Current entity name being processed is {} who has {} applied', entity_names[0], current_condis)
                ps = 0
                for condi in current_condis:
                    condi_name = condi['name']
                    duration = condi['duration']
                    duration -= 1
                    current_condis[ps]['duration'] = duration
                    baseDamagePerStack = condi['baseDamage']
                    conditionDamageMod = condi['condDamageMod']
                    weaponLevelMod = condi['weaponLevelMod']

                    damage_applied_this_turn = formulas.base_condi_damage(condition_damage_modifier=conditionDamageMod, condition_damage_stat=condition_damage_stat_value, weapon_level_modifier=weaponLevelMod, base_damage_per_stack=baseDamagePerStack, weapon_level=1)
                    dialogue = condi['dialogue']

                    # add dialog for condition damage to message log
                    # msg = Message(text=entity_names[0] + " screams: " + dialogue, msgclass="all", fg="white", bg="black", fnt="")
                    # CommonUtils.add_message(gameworld=self.gameworld, message=msg, logid=message_log_id)

                    # add message to combat log showing how much damage has been applied to the target
                    msg = Message(text=entity_names[0] + " takes [color=orange]" + str(damage_applied_this_turn) + " [/color]from [[" + condi_name + "]]", msgclass="combat", fg="white", bg="black", fnt="")
                    CommonUtils.add_message(gameworld=self.gameworld, message=msg, logid=message_log_id)

                    if duration <= 0:
                        del current_condis[ps]
                    else:
                        status_effects_component = self.gameworld.component_for_entity(ent, mobiles.StatusEffects)
                        status_effects_component.conditions = current_condis

                    logger.debug('Condis applied to {} is {}', entity_names[0], current_condis)

            # apply buffs
            current_boons = MobileUtilities.get_current_boons_applied_to_mobile(gameworld=self.gameworld, entity=ent)
            if len(current_boons) != 0:
                pass

            # apply controls

            # gain resources from spells

            if not inCombat:
                MobileUtilities.calculate_derived_attributes(self.gameworld, entity=ent)

