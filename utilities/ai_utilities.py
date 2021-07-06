import random

from utilities import common
from utilities.formulas import calculate_distance_to_target
from utilities.mobileHelp import MobileUtilities
from utilities.spellHelp import SpellUtilities


class AIUtilities:

    @staticmethod
    def pick_a_spell_to_cast(gameworld, entity_id, remaining_spells, player_entity):
        if len(remaining_spells) == 1:
            # cast the spell
            spell_to_cast = remaining_spells[0]
            index_to_cast = 0
        else:
            # choose a random spell to cast
            number_of_spells = len(remaining_spells)
            index_to_cast = random.randrange(0, number_of_spells)
            spell_to_cast = remaining_spells[index_to_cast]

        spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=spell_to_cast)

        target_map_x = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=player_entity)
        target_map_y = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=player_entity)

        spell_cast_at = [target_map_x, target_map_y]

        SpellUtilities.set_spell_to_cast_this_turn(gameworld=gameworld, mobile_entity=entity_id,
                                                   spell_entity=spell_to_cast,
                                                   spell_target_entity=[player_entity], slot=index_to_cast,
                                                   map_coords_list=spell_cast_at)

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
        can_cast_a_spell, remaining_spells, weapon_type = SpellUtilities.can_mobile_cast_a_spell(gameworld, entity_id, target_entity)

        return can_cast_a_spell, remaining_spells, weapon_type

    @staticmethod
    def can_i_see_my_target(gameworld, from_entity, to_entity):
        tile_distance = calculate_distance_to_target(gameworld, from_entity, to_entity)
        return int(tile_distance)

    @staticmethod
    def let_me_say(gameworld, message):
        common.CommonUtils.fire_event('dialog-general', gameworld=gameworld, dialog=message)
