import esper
from loguru import logger
from components import mobiles
from utilities import formulas, world, armourManagement, common, mobileHelp, scorekeeper
from utilities.mobileHelp import MobileUtilities
from utilities.spellHelp import SpellUtilities


class UpdateEntitiesProcessor(esper.Processor):
    """
    This processor cycles through ALL MOBILES and calculates their attributes
    """

    def __init__(self, gameworld, game_map):
        self.gameworld = gameworld
        self.game_map = game_map

    def process(self, game_config, advance_game_turn):
        if advance_game_turn:
            player_entity = mobileHelp.MobileUtilities.get_player_entity(gameworld=self.gameworld,
                                                                         game_config=game_config)
            message_log_just_viewed = mobileHelp.MobileUtilities.get_view_message_log_value(gameworld=self.gameworld,
                                                                                            entity=player_entity)

            if not message_log_just_viewed:
                for ent, ai in self.gameworld.get_component(mobiles.AILevel):
                    current_health = mobileHelp.MobileUtilities.get_mobile_derived_current_health(
                        gameworld=self.gameworld, entity=ent)

                    entity_names = mobileHelp.MobileUtilities.get_mobile_name_details(gameworld=self.gameworld,
                                                                                      entity=ent)

                    if current_health < 0:
                        self.entity_is_dead(dead_entity_id=ent, player_entity=player_entity)
                    else:
                        self.apply_conditions(entity_names=entity_names, player_entity=player_entity,
                                              target_entity=ent)
                        self.apply_boons(entity_names=entity_names, target_entity=ent)
                        # apply controls
                        # gain resources from spells
                        self.check_for_combat(entity_id=ent)
                        # what/who can the entity see around them
                        self.who_can_i_see_around_me(ent=ent)
                        # have i been stopped from moving next turn due to a condition
                        self.can_i_still_move(entity=ent)

    def can_i_still_move(self, entity):
        list_of_conditions = MobileUtilities.get_current_condis_applied_to_mobile(gameworld=self.gameworld,
                                                                                  entity=entity)
        if ['crippled', 'immobilize', 'stunned', 'dazed'] in list_of_conditions:
            MobileUtilities.set_movement_status(gameworld=self.gameworld, entity=entity, status=False)
        else:
            MobileUtilities.set_movement_status(gameworld=self.gameworld, entity=entity, status=True)

    def who_can_i_see_around_me(self, ent):
        range_of_vision = MobileUtilities.get_mobile_senses_vision_range(gameworld=self.gameworld,
                                                                         entity=ent)
        from_x = MobileUtilities.get_mobile_x_position(gameworld=self.gameworld, entity=ent)
        from_y = MobileUtilities.get_mobile_y_position(gameworld=self.gameworld, entity=ent)

        min_x_range = max(1, (from_x - range_of_vision))
        max_x_range = min(self.game_map.width, (from_x + self.game_map.width))
        min_y_range = max(1, (from_y - range_of_vision))
        max_y_range = min(self.game_map.height, (from_y + self.game_map.height))
        visible_entities = []

        for across in range(min_x_range, max_x_range):
            for down in range(min_y_range, max_y_range):
                entity_id = self.game_map.tiles[across][down].entity
                if entity_id > 0 and entity_id != ent:
                    visible_entities.append(entity_id)
        MobileUtilities.set_ai_visible_entities(gameworld=self.gameworld, target_entity=ent,
                                                visible_entities=visible_entities)

    def check_for_combat(self, entity_id):
        in_combat = mobileHelp.MobileUtilities.get_combat_status(self.gameworld, entity=entity_id)
        if not in_combat:
            armourManagement.ArmourUtilities.set_mobile_derived_armour_attribute(gameworld=self.gameworld,
                                                                                 entity=entity_id)
            mobileHelp.MobileUtilities.set_mobile_derived_attributes(self.gameworld, entity=entity_id)

    def entity_is_dead(self, dead_entity_id, player_entity):

        # gather equipped items

        # pick some random equipment to drop on to the game map

        health = mobileHelp.MobileUtilities.get_mobile_derived_current_health(gameworld=self.gameworld,
                                                                              entity=dead_entity_id)
        logger.warning('Entity {} is dead', dead_entity_id)
        logger.warning('Entity health at death {}', health)

        # add kill event
        npc_type = mobileHelp.MobileUtilities.get_mobile_type(gameworld=self.gameworld, entity=dead_entity_id)
        current_area_tag = scorekeeper.ScorekeeperUtilities.get_current_area(gameworld=self.gameworld)
        event_to_add = current_area_tag + '_' + npc_type + '_kill'
        # check if event type already exists
        event_already_exists = scorekeeper.ScorekeeperUtilities.has_event_already_been_added(gameworld=self.gameworld,
                                                                                             event_name=event_to_add)
        if not event_already_exists:
            scorekeeper.ScorekeeperUtilities.register_scorekeeper_meta_event(gameworld=self.gameworld,
                                                                             event_name=event_to_add,
                                                                             event_starting_value=1)
        else:
            scorekeeper.ScorekeeperUtilities.increase_meta_event_value(gameworld=self.gameworld,
                                                                       event_name=event_to_add, value=1)

        # And finally delete the entity + ALL associated components
        if dead_entity_id != player_entity:
            world.delete_entity(gameworld=self.gameworld, entity=dead_entity_id)

    def apply_conditions(self, entity_names, player_entity, target_entity):
        current_condis = mobileHelp.MobileUtilities.get_current_condis_applied_to_mobile(gameworld=self.gameworld,
                                                                                         entity=target_entity)
        if len(current_condis) != 0:

            condition_damage_stat_value = mobileHelp.MobileUtilities.get_mobile_secondary_condition_damage(
                gameworld=self.gameworld,
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
                common.CommonUtils.fire_event("condi-damage", gameworld=self.gameworld, target=entity_names[0],
                                              damage=str(damage_applied_this_turn), condi_name=condi_name)

                # update scorekeeper with condi damage
                current_area_tag = scorekeeper.ScorekeeperUtilities.get_current_area(gameworld=self.gameworld)
                updated_condi_name = condi_name.replace(" ", "_")
                updated_condi_name = current_area_tag + '_' + updated_condi_name + "_damage"
                lower_condi_name = updated_condi_name.lower()
                scorekeeper.ScorekeeperUtilities.increase_meta_event_value(gameworld=self.gameworld,
                                                                           event_name=lower_condi_name,
                                                                           value=damage_applied_this_turn)

                if duration <= 0:
                    self.remove_condition(entity_name=entity_names[0], current_condis=current_condis, ps=ps,
                                          condi_name=condi_name)
                else:
                    SpellUtilities.apply_condis_to_target(gameworld=self.gameworld, target_entity=target_entity, list_of_condis=current_condis)

                logger.debug('Condis applied to {} is {}', entity_names[0], current_condis)
                ps += 1

    def apply_boons(self, entity_names, target_entity):
        current_boons = mobileHelp.MobileUtilities.get_current_boons_applied_to_mobile(gameworld=self.gameworld,
                                                                                       entity=target_entity)
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
                common.CommonUtils.fire_event("boon-benefit", gameworld=self.gameworld, target=entity_names[0],
                                              benefit=str(msg_stat), boon_name=boon_name)
                if duration <= 0:
                    self.remove_boon(entity_name=entity_names[0], current_boons=current_boons, ps=ps,
                                     boon_name=boon_name)
                else:
                    status_effects_component = self.gameworld.component_for_entity(target_entity, mobiles.StatusEffects)
                    status_effects_component.boons = current_boons
                    current_boons = mobileHelp.MobileUtilities.get_current_boons_applied_to_mobile(
                        gameworld=self.gameworld,
                        entity=target_entity)
                ps += 1

    def remove_boon(self, entity_name, current_boons, ps, boon_name):
        del current_boons[ps]

        # add message to combat log showing loss of effect
        common.CommonUtils.fire_event("boon-removal", gameworld=self.gameworld, target=entity_name, boon_name=boon_name)

    def remove_condition(self, entity_name, current_condis, ps, condi_name):
        del current_condis[ps]

        # add message to combat log showing loss of effect
        common.CommonUtils.fire_event("condi-removal", gameworld=self.gameworld, target=entity_name,
                                      condi_name=condi_name)
