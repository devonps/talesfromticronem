import random

from loguru import logger

from utilities import common, mobileHelp
from utilities.formulas import calculate_distance_to_target
from utilities.mobileHelp import MobileUtilities
from utilities.spellHelp import SpellUtilities


class AIUtilities:

    @staticmethod
    def dump_ai_debugging_information(gameworld, ai_debugging_first_name, target_entity, entity_combat_role):
        visible_entities = MobileUtilities.get_ai_visible_entities(gameworld=gameworld, target_entity=target_entity)
        vision_range = MobileUtilities.get_mobile_senses_vision_range(gameworld=gameworld, entity=target_entity)

        visible_entity_names = []
        if len(visible_entities) > 0:
            for a in range(len(visible_entities)):
                entity_names = MobileUtilities.get_mobile_name_details(gameworld=gameworld,
                                                                       entity=visible_entities[a])
                mobile_first_name = entity_names[0]
                visible_entity_names.append(mobile_first_name)

        logger.debug('=== AI Debugging information ===')
        logger.info('mobile AI name: {}', ai_debugging_first_name)
        logger.info('mobile AI combat role: {}', entity_combat_role)
        logger.info('mobile intrinsic information')
        damage_string = 'Has mobile taken damage:'
        damage_status = ' no'
        logger.info(damage_string + damage_status)
        logger.info('mobile vision range: {}', vision_range)
        logger.info('What can the mobile see around them')
        logger.info('list of entities: {}', visible_entity_names)

    @staticmethod
    def attack_the_target(player_entity, gameworld, monster_entity, game_map, game_config):
        bully_text = "It's your lucky day punk!"
        target_attacked = False

        i_can_cast_a_combat_spell, remaining_spells = AIUtilities.can_i_cast_a_spell(gameworld=gameworld,
                                                                                     entity_id=monster_entity,
                                                                                     target_entity=player_entity)
        if i_can_cast_a_combat_spell:
            AIUtilities.pick_random_spell_to_cast(gameworld=gameworld, entity_id=monster_entity,
                                                  remaining_spells=remaining_spells, game_config=game_config,
                                                  game_map=game_map)
            target_attacked = True
        else:
            # I'm in combat range but can't cast a spell because I don't have a weapon or they're all on
            # cooldown
            AIUtilities.let_me_say(gameworld=gameworld, message=bully_text)
        return target_attacked

    @staticmethod
    def move_towards_or_away_from_target(too_far, too_close, source_entity, target_entity, gameworld):
        i_can_move = AIUtilities.can_i_move(gameworld=gameworld, source_entity=source_entity)
        if i_can_move:
            if too_far:
                AIUtilities.prep_move_towards_target(gameworld=gameworld, target_entity=target_entity,
                                                     source_entity=source_entity)
                AIUtilities.let_me_say(gameworld=gameworld, message="I'm coming for you!")
            if too_close:
                AIUtilities.move_away_from_target(gameworld=gameworld, target_entity=target_entity,
                                                  source_entity=source_entity)
                AIUtilities.let_me_say(gameworld=gameworld, message="I need some room.")

    @staticmethod
    def pick_random_spell_to_cast(gameworld, entity_id, remaining_spells, game_config, game_map):

        player_entity = MobileUtilities.get_player_entity(gameworld=gameworld)
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

        if spell_name != 'no spell':
            spell_cast_message = 'I choose to cast ' + spell_name
            AIUtilities.draw_spell_targeting_effects(gameworld=gameworld, game_config=game_config,
                                                     caster_entity=entity_id,
                                                     enemy_list=[player_entity],
                                                     game_map=game_map, spell_has_aoe=False)
            AIUtilities.let_me_say(gameworld=gameworld, message=spell_cast_message)
        else:
            AIUtilities.let_me_say(gameworld=gameworld, message='Im not in spell range, time to hustle!')

    @staticmethod
    def can_i_move(gameworld, source_entity):
        return MobileUtilities.get_movement_status(gameworld=gameworld, entity=source_entity)

    @staticmethod
    def is_the_player_visible(player_entity, visible_entities):
        if player_entity in visible_entities:
            return True
        else:
            return False

    @staticmethod
    def distance_to_target(gameworld, source_entity, target_entity):
        min_attack_range = MobileUtilities.get_enemy_preferred_min_range(gameworld=gameworld, entity=source_entity)
        max_attack_range = MobileUtilities.get_enemy_preferred_max_range(gameworld=gameworld, entity=source_entity)
        dist_to_target = AIUtilities.can_i_see_my_target(gameworld=gameworld, from_entity=source_entity,
                                                         to_entity=target_entity)
        too_close_to_player = AIUtilities.am_i_too_close_to_the_target(dist_to_target=dist_to_target,
                                                                       min_attack_range=min_attack_range)
        too_far_from_player = AIUtilities.am_i_too_far_from_the_target(dist_to_target=dist_to_target,
                                                                       max_attack_range=max_attack_range)

        ideal_distance_from_target = (not too_far_from_player and not too_close_to_player)

        return too_close_to_player, too_far_from_player, ideal_distance_from_target

    @staticmethod
    def am_i_too_close_to_the_target(dist_to_target, min_attack_range):
        if dist_to_target < min_attack_range:
            return True
        else:
            return False

    @staticmethod
    def am_i_too_far_from_the_target(dist_to_target, max_attack_range):
        if dist_to_target > max_attack_range:
            return True
        else:
            return False

    @staticmethod
    def move_towards_target_or_not(gameworld, player_entity, monster_entity):
        r = random.randrange(0, 100)
        if r < 90:
            AIUtilities.prep_move_towards_target(gameworld=gameworld, target_entity=player_entity,
                                                 source_entity=monster_entity)
            AIUtilities.let_me_say(gameworld=gameworld, message='Time to get hustling.')
        else:
            AIUtilities.let_me_say(gameworld=gameworld, message='I choose not to move.')

    @staticmethod
    def do_something_non_combat(gameworld, monster_entity):
        monster_is_hurt = MobileUtilities.get_mobile_physical_hurt_status(gameworld=gameworld, entity=monster_entity)
        if monster_is_hurt:
            AIUtilities.let_me_say(gameworld=gameworld, message='I am hurting, medic!')
        else:
            AIUtilities.let_me_say(gameworld=gameworld, message='I feel good!')

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
        can_cast_a_spell, remaining_spells = SpellUtilities.can_mobile_cast_a_spell(gameworld, entity_id,
                                                                                    target_entity)

        return can_cast_a_spell, remaining_spells

    @staticmethod
    def can_i_see_my_target(gameworld, from_entity, to_entity):
        tile_distance = calculate_distance_to_target(gameworld, from_entity, to_entity)
        return int(tile_distance)

    @staticmethod
    def let_me_say(gameworld, message):
        common.CommonUtils.fire_event('dialog-general', gameworld=gameworld, dialog=message)

    @staticmethod
    def draw_spell_targeting_effects(gameworld, game_config, enemy_list, caster_entity, game_map, spell_has_aoe):
        # Spell to cast has already been decided upon, based on current AI values/settings
        # get list of enemies at map target location
        # do spell casting visual effects at screen coords
        player_entity = MobileUtilities.get_player_entity(gameworld=gameworld)
        # get map position of target
        tg_x = mobileHelp.MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=player_entity)
        tg_y = mobileHelp.MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=player_entity)

        # get caster map position
        cg_x = mobileHelp.MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=caster_entity)
        cg_y = mobileHelp.MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=caster_entity)
        caster_map_x = cg_x
        caster_map_y = cg_y

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
        # movement options
        # where is the target in relation to me (the source entity)
        from_x = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=source_entity)
        from_y = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=source_entity)
        to_x = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=target_entity)
        to_y = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=target_entity)

        target_is_north_of_me = False
        target_is_south_of_me = False
        target_is_west_of_me = False
        target_is_east_of_me = False
        i_have_moved = False

        if from_x > to_x:
            target_is_west_of_me = True
        elif from_x < to_x:
            target_is_east_of_me = True

        if from_y > to_y:
            target_is_north_of_me = True
        elif from_y < to_y:
            target_is_south_of_me = True

        # do the reverse of move towards the target to move away from the target
        if target_is_north_of_me:
            MobileUtilities.set_mobile_velocity(gameworld=gameworld, entity=source_entity, direction='down', speed=1)
            i_have_moved = True

        if target_is_east_of_me and not i_have_moved:
            MobileUtilities.set_mobile_velocity(gameworld=gameworld, entity=source_entity, direction='right', speed=1)
            i_have_moved = True

        if target_is_south_of_me and not i_have_moved:
            MobileUtilities.set_mobile_velocity(gameworld=gameworld, entity=source_entity, direction='up', speed=1)
            i_have_moved = True

        if target_is_west_of_me and not i_have_moved:
            MobileUtilities.set_mobile_velocity(gameworld=gameworld, entity=source_entity, direction='left', speed=1)

    @staticmethod
    def prep_move_towards_target(gameworld, target_entity, source_entity):

        # movement options
        # where is the target in relation to me (the source entity)
        from_x = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=source_entity)
        from_y = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=source_entity)
        to_x = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=target_entity)
        to_y = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=target_entity)

        AIUtilities.move_towards_location(gameworld=gameworld, source_entity=source_entity, from_x=from_x, to_x=to_x,
                                          from_y=from_y, to_y=to_y)

    @staticmethod
    def prep_move_to_specific_location(gameworld, source_entity, px, py):
        from_x = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=source_entity)
        from_y = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=source_entity)
        AIUtilities.move_towards_location(gameworld=gameworld, source_entity=source_entity, from_x=from_x, to_x=px,
                                          from_y=from_y, to_y=py)

    @staticmethod
    def move_towards_location(gameworld, source_entity, from_x, to_x, from_y, to_y):
        target_is_north_of_me = False
        target_is_south_of_me = False
        target_is_west_of_me = False
        target_is_east_of_me = False
        i_have_moved = False

        if from_x > to_x:
            target_is_east_of_me = True
        elif from_x < to_x:
            target_is_west_of_me = True

        if from_y > to_y:
            target_is_north_of_me = True
        elif from_y < to_y:
            target_is_south_of_me = True

        if target_is_north_of_me:
            MobileUtilities.set_mobile_velocity(gameworld=gameworld, entity=source_entity, direction='up', speed=1)
            i_have_moved = True

        if target_is_east_of_me and not i_have_moved:
            MobileUtilities.set_mobile_velocity(gameworld=gameworld, entity=source_entity, direction='left', speed=1)
            i_have_moved = True

        if target_is_south_of_me and not i_have_moved:
            MobileUtilities.set_mobile_velocity(gameworld=gameworld, entity=source_entity, direction='down', speed=1)
            i_have_moved = True

        if target_is_west_of_me and not i_have_moved:
            MobileUtilities.set_mobile_velocity(gameworld=gameworld, entity=source_entity, direction='right', speed=1)

    @staticmethod
    def move_to_player_last_position(gameworld, monster_entity):
        player_last_known_position = MobileUtilities.get_player_last_known_position(gameworld=gameworld,
                                                                                    source_entity=monster_entity)
        # can I move
        i_can_move = AIUtilities.can_i_move(gameworld=gameworld, source_entity=monster_entity)
        if i_can_move and player_last_known_position != (0, 0):
            px = player_last_known_position(0)
            py = player_last_known_position(1)
            AIUtilities.prep_move_to_specific_location(gameworld=gameworld, source_entity=monster_entity, px=px, py=py)