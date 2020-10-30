import esper
from loguru import logger

from components import mobiles
from utilities import formulas, world
from utilities.armourManagement import ArmourUtilities
from utilities.common import CommonUtils
from utilities.mobileHelp import MobileUtilities


class UpdateEntitiesProcessor(esper.Processor):
    """
    This processor cycles through ALL MOBILES and calculates their attributes
    """

    def __init__(self, gameworld, game_map):
        self.gameworld = gameworld
        self.game_map = game_map

    def process(self, game_config, advance_game_turn):
        if advance_game_turn:
            player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=game_config)
            message_log_just_viewed = MobileUtilities.get_view_message_log_value(gameworld=self.gameworld,
                                                                                 entity=player_entity)

            if not message_log_just_viewed:
                message_log_id = MobileUtilities.get_MessageLog_id(gameworld=self.gameworld, entity=player_entity)

                for ent, ai in self.gameworld.get_component(mobiles.AI):
                    current_health = MobileUtilities.get_mobile_derived_current_health(gameworld=self.gameworld, entity=ent)

                    entity_names = MobileUtilities.get_mobile_name_details(gameworld=self.gameworld, entity=ent)

                    if current_health < 0:
                        self.entity_is_dead(dead_entity_id=ent)
                    else:
                        self.apply_conditions(entity_names=entity_names, player_entity=player_entity,
                                              message_log_id=message_log_id, target_entity=ent)
                        self.apply_boons(entity_names=entity_names, player_entity=player_entity, message_log_id=message_log_id,
                                         target_entity=ent)
                        # apply controls
                        # gain resources from spells
                        self.check_for_combat(entity_id=ent)

    def check_for_combat(self, entity_id):
        in_combat = MobileUtilities.get_combat_status(self.gameworld, entity=entity_id)
        if not in_combat:
            ArmourUtilities.set_mobile_derived_armour_attribute(gameworld=self.gameworld, entity=entity_id)
            MobileUtilities.set_mobile_derived_attributes(self.gameworld, entity=entity_id)

    def entity_is_dead(self, dead_entity_id):

        # gather equipped items

        # pick some random equipment to drop on to the game map
        logger.warning('An entity is dead')

        # And finally delete the entity + ALL associated components
        world.delete_entity(gameworld=self.gameworld, entity=dead_entity_id)

    def apply_conditions(self, entity_names, player_entity, message_log_id, target_entity):
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
                CommonUtils.fire_event("condi-damage", gameworld=self.gameworld, target=entity_names[0],
                                       damage=str(damage_applied_this_turn), condi_name=condi_name)

                if duration <= 0:
                    self.remove_condition(entity_name=entity_names[0], current_condis=current_condis, ps=ps, condi_name=condi_name)
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

                msg_stat = 555

                if boon_name == 'fury':
                    msg_stat = boon['improvement']

                # add message to combat log showing effect
                CommonUtils.fire_event("boon-benefit", gameworld=self.gameworld, target=entity_names[0],
                                       benefit=str(msg_stat), boon_name=boon_name)
                if duration <= 0:
                    self.remove_boon(entity_name=entity_names[0], current_boons=current_boons, ps=ps, boon_name=boon_name)
                else:
                    status_effects_component = self.gameworld.component_for_entity(target_entity, mobiles.StatusEffects)
                    status_effects_component.boons = current_boons
                    current_boons = MobileUtilities.get_current_boons_applied_to_mobile(gameworld=self.gameworld,
                                                                                        entity=target_entity)
                ps += 1

    def remove_boon(self, entity_name, current_boons, ps, boon_name):
        del current_boons[ps]

        # add message to combat log showing loss of effect
        CommonUtils.fire_event("boon-removal", gameworld=self.gameworld, target=entity_name, boon_name=boon_name)

    def remove_condition(self, entity_name, current_condis, ps, condi_name):
        del current_condis[ps]

        # add message to combat log showing loss of effect
        CommonUtils.fire_event("condi-removal", gameworld=self.gameworld, target=entity_name, condi_name=condi_name)