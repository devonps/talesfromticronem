import random

from utilities import common, mobileHelp
from utilities.formulas import calculate_distance_to_target
from utilities.mobileHelp import MobileUtilities
from utilities.spellHelp import SpellUtilities


class AIUtilities:

    @staticmethod
    def pick_a_spell_to_cast(gameworld, entity_id, remaining_spells, player_entity):

        target_map_x = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=player_entity)
        target_map_y = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=player_entity)
        cast_spell = False
        spell_to_cast = -99
        index_to_cast = -99
        if len(remaining_spells) == 1:
            # cast the spell
            spell_to_cast = remaining_spells[0]
            index_to_cast = 0
            # do range check
            cast_spell = True
        else:
            # choose a random spell to cast
            number_of_spells = len(remaining_spells)
            # do we have any spells in range of the target

            for a in range(number_of_spells):
                this_spell_range = SpellUtilities.get_spell_max_range(gameworld=gameworld,
                                                                      spell_entity=remaining_spells[a])
                dist_to_target = AIUtilities.can_i_see_my_target(gameworld=gameworld, from_entity=entity_id,
                                                                 to_entity=player_entity)
                if this_spell_range >= dist_to_target:
                    index_to_cast = random.randrange(0, number_of_spells)
                    spell_to_cast = remaining_spells[index_to_cast]
                    cast_spell = True
        if cast_spell:
            spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=spell_to_cast)
            spell_cast_at = [target_map_x, target_map_y]

            SpellUtilities.set_spell_to_cast_this_turn(gameworld=gameworld, mobile_entity=entity_id,
                                                       spell_entity=spell_to_cast,
                                                       spell_target_entity=[player_entity], slot=index_to_cast,
                                                       map_coords_list=spell_cast_at)

            SpellUtilities.set_spell_cooldown_to_true(gameworld=gameworld, spell_entity=spell_to_cast)

        else:
            spell_name = 'no spell'
        return spell_name

    @staticmethod
    def can_i_move(gameworld, source_entity):
        list_of_conditions = MobileUtilities.get_current_condis_applied_to_mobile(gameworld=gameworld,
                                                                                  entity=source_entity)
        if ['crippled', 'immobilize', 'stunned', 'dazed'] in list_of_conditions:
            return False
        else:
            return True

    @staticmethod
    def what_can_i_see_around_me(gameworld, source_entity, game_map):
        range_of_vision = MobileUtilities.get_mobile_senses_vision_range(gameworld=gameworld, entity=source_entity)
        from_x = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=source_entity)
        from_y = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=source_entity)

        min_x_range = max(1, (from_x - range_of_vision))
        max_x_range = min(game_map.width, (from_x + game_map.width))
        min_y_range = max(1, (from_y - range_of_vision))
        max_y_range = min(game_map.height, (from_y + game_map.height))
        visible_entities = []

        for across in range(min_x_range, max_x_range):
            for down in range(min_y_range, max_y_range):
                entity_id = game_map.tiles[across][down].entity
                if entity_id > 0 and entity_id != source_entity:
                    visible_entities.append(entity_id)
        MobileUtilities.set_visible_entities(gameworld=gameworld, target_entity=source_entity,
                                             visible_entities=visible_entities)

    @staticmethod
    def have_i_taken_damage(gameworld, source_entity):

        current_health = MobileUtilities.get_mobile_derived_current_health(gameworld=gameworld, entity=source_entity)
        max_health = MobileUtilities.get_mobile_derived_maximum_health(gameworld=gameworld, entity=source_entity)

        if current_health != max_health:
            MobileUtilities.set_mobile_physical_hurt_state_to_true(gameworld=gameworld, entity=source_entity)
        else:
            MobileUtilities.set_mobile_physical_hurt_state_to_false(gameworld=gameworld, entity=source_entity)

    @staticmethod
    def can_i_cast_a_spell(gameworld, entity_id, target_entity):
        can_cast_a_spell, remaining_spells, weapon_type = SpellUtilities.can_mobile_cast_a_spell(gameworld, entity_id,
                                                                                                 target_entity)

        return can_cast_a_spell, remaining_spells, weapon_type

    @staticmethod
    def can_i_see_my_target(gameworld, from_entity, to_entity):
        tile_distance = calculate_distance_to_target(gameworld, from_entity, to_entity)
        return int(tile_distance)

    @staticmethod
    def let_me_say(gameworld, message):
        common.CommonUtils.fire_event('dialog-general', gameworld=gameworld, dialog=message)

    @staticmethod
    def cast_a_spell(gameworld, game_config, enemy_list, player_entity, game_map, spell_has_aoe):
        # Spell to cast has already been decided upon, based on current AI values/settings

        # draw graphics of spell being cast
        tg_x = mobileHelp.MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=player_entity)
        tg_y = mobileHelp.MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=player_entity)

        caster_map_x = tg_x
        caster_map_y = tg_y

        # these hold the screen coords
        (targeting_cursor_centre_x, targeting_cursor_centre_y) = common.CommonUtils.to_camera_coordinates(
            game_config=game_config, game_map=game_map, x=tg_x, y=tg_y, gameworld=gameworld)

        # do spell casting visual effects at screen coords
        SpellUtilities.draw_spell_casting_visual_effects(gameworld=gameworld, game_config=game_config,
                                                         caster_coords=[caster_map_x, caster_map_y],
                                                         target_coords=[targeting_cursor_centre_x,
                                                                        targeting_cursor_centre_y],
                                                         target_list=enemy_list, player_entity=player_entity,
                                                         spell_has_aoe=spell_has_aoe, game_map=game_map)

    @staticmethod
    def move_away_from_target(gameworld, target_entity, source_entity):
        pass
        # this will find the next tile away from the target

    @staticmethod
    def move_towards_target(gameworld, target_entity, source_entity):
        pass
        # not yet implemented

