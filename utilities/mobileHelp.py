from abc import ABC

from components import mobiles, items
from loguru import logger
from mapRelated import fov
from static.data import constants
from utilities import world, configUtilities

import numbers

from utilities.gamemap import GameMapUtilities


class MobileUtilities(numbers.Real, ABC):
    #
    # general methods
    #

    @staticmethod
    def get_mobile_type(gameworld, entity):
        mobile_component = gameworld.component_for_entity(entity, mobiles.MobileType)
        return mobile_component.label

    @staticmethod
    def set_mobile_type(gameworld, entity, value):
        mobile_component = gameworld.component_for_entity(entity, mobiles.MobileType)
        mobile_component.label = value

    @staticmethod
    def can_i_see_the_other_entity(gameworld, game_map, from_entity, to_entity):
        can_i_see_the_entity = True
        from_x = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=from_entity)
        from_y = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=from_entity)

        to_x = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=to_entity)
        to_y = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=to_entity)

        cells_in_line = fov.FieldOfView.get_line((from_x, from_y), (to_x, to_y))

        for cell in cells_in_line:
            tile_is_blocked = GameMapUtilities.is_tile_blocked(game_map=game_map, x=cell[0], y=cell[1])
            if tile_is_blocked:
                can_i_see_the_entity = False

        return can_i_see_the_entity

    @staticmethod
    def add_armour_modifier(gameworld, entity_id, armour_modifier, px_bonus):
        if armour_modifier.lower() == 'healer':
            MobileUtilities.set_mobile_secondary_healing_power(gameworld=gameworld, entity=entity_id, value=px_bonus)

        if armour_modifier.lower() == 'malign':
            MobileUtilities.set_mobile_secondary_condition_damage(gameworld=gameworld, entity=entity_id,
                                                                  value=px_bonus)

        if armour_modifier.lower() == 'mighty':
            MobileUtilities.set_mobile_primary_power(gameworld=gameworld, entity=entity_id, value=px_bonus)

        if armour_modifier.lower() == 'precise':
            MobileUtilities.set_mobile_primary_precision(gameworld=gameworld, entity=entity_id, value=px_bonus)

        if armour_modifier.lower() == 'resilient':
            MobileUtilities.set_mobile_primary_toughness(gameworld=gameworld, entity=entity_id, value=px_bonus)

        if armour_modifier.lower() == 'vital':
            MobileUtilities.set_mobile_primary_vitality(gameworld=gameworld, entity=entity_id, value=px_bonus)

    @staticmethod
    def set_mobile_gender(gameworld, entity, gender):
        describable_component = gameworld.component_for_entity(entity, mobiles.MobileGender)
        describable_component.label = gender

    @staticmethod
    def get_mobile_gender(gameworld, entity):
        gender = gameworld.component_for_entity(entity, mobiles.MobileGender).label
        return gender

    @staticmethod
    def setup_racial_attributes(gameworld, entity, selected_race, race_size, bg, race_names):
        MobileUtilities.set_mobile_bg_render_colour(gameworld=gameworld, entity=entity, value=bg)

        race_component = gameworld.component_for_entity(entity, mobiles.Race)
        race_component.label = selected_race
        race_component.size = race_size
        race_component.name_singular = race_names[0]
        race_component.name_plural = race_names[1]
        race_component.name_name_adjective = race_names[2]

    @staticmethod
    def setup_class_attributes(gameworld, player, selected_class, health, spellfile):

        gameworld.component_for_entity(player, mobiles.CharacterClass).label = selected_class
        gameworld.component_for_entity(player, mobiles.CharacterClass).spellfile = spellfile
        gameworld.component_for_entity(player, mobiles.CharacterClass).base_health = health

    @staticmethod
    def get_player_entity(gameworld):
        player_ai = constants.AI_LEVEL_PLAYER

        player = 0
        for ent, ai in gameworld.get_component(mobiles.AILevel):
            if ai.label == player_ai:
                player = ent

        return player

    @staticmethod
    def get_mobile_ai_level(gameworld, entity_id):
        return gameworld.component_for_entity(entity_id, mobiles.AILevel).label

    @staticmethod
    def get_mobile_ai_description(gameworld, entity_id):
        return gameworld.component_for_entity(entity_id, mobiles.AILevel).description

    @staticmethod
    def get_number_as_a_percentage(lower_value, maximum_value):
        return int((lower_value / maximum_value) * 100)

    @staticmethod
    def get_bar_count(lower_value, bar_depth):
        return (lower_value / 100) * bar_depth

    @staticmethod
    def has_player_moved(gameworld, game_config):
        entity = MobileUtilities.get_player_entity(gameworld)

        position_component = gameworld.component_for_entity(entity, mobiles.Position)

        return position_component.has_moved

    @staticmethod
    def set_mobile_position(gameworld, entity, posx, posy):
        gameworld.add_component(entity, mobiles.Position(x=posx, y=posy, has_moved=True))

    @staticmethod
    def get_mobile_x_position(gameworld, entity):
        position_component = gameworld.component_for_entity(entity, mobiles.Position)

        return position_component.x

    @staticmethod
    def get_mobile_y_position(gameworld, entity):
        position_component = gameworld.component_for_entity(entity, mobiles.Position)

        return position_component.y

    @staticmethod
    def set_direction_velocity_towards_player(gameworld, game_config, enemy_entity):
        player_entity = MobileUtilities.get_player_entity(gameworld=gameworld)

        current_player_xpos = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=player_entity)
        current_player_ypos = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=player_entity)

        current_enemy_xpos = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=enemy_entity)
        current_enemy_ypos = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=enemy_entity)

        if current_enemy_ypos < current_player_ypos:
            MobileUtilities.set_mobile_velocity(gameworld=gameworld, entity=enemy_entity, direction='down', speed=1)
        if current_enemy_ypos > current_player_ypos:
            MobileUtilities.set_mobile_velocity(gameworld=gameworld, entity=enemy_entity, direction='up', speed=1)

        if current_enemy_xpos < current_player_xpos:
            MobileUtilities.set_mobile_velocity(gameworld=gameworld, entity=enemy_entity, direction='right', speed=1)
        if current_enemy_xpos > current_player_xpos:
            MobileUtilities.set_mobile_velocity(gameworld=gameworld, entity=enemy_entity, direction='left', speed=1)

    @staticmethod
    def set_direction_velocity_away_from_player(gameworld, game_config, enemy_entity):
        player_entity = MobileUtilities.get_player_entity(gameworld=gameworld)

        current_player_xpos = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=player_entity)
        current_player_ypos = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=player_entity)

        current_enemy_xpos = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=enemy_entity)
        current_enemy_ypos = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=enemy_entity)

        if current_enemy_ypos < current_player_ypos:
            MobileUtilities.set_mobile_velocity(gameworld=gameworld, entity=enemy_entity, direction='up', speed=1)
        if current_enemy_ypos > current_player_ypos:
            MobileUtilities.set_mobile_velocity(gameworld=gameworld, entity=enemy_entity, direction='down', speed=1)

        if current_enemy_xpos < current_player_xpos:
            MobileUtilities.set_mobile_velocity(gameworld=gameworld, entity=enemy_entity, direction='left', speed=1)
        if current_enemy_xpos > current_player_xpos:
            MobileUtilities.set_mobile_velocity(gameworld=gameworld, entity=enemy_entity, direction='right', speed=1)

    @staticmethod
    def set_mobile_velocity(gameworld, entity, direction, speed):
        mobile_velocity_component = gameworld.component_for_entity(entity, mobiles.Velocity)
        dx = 0
        dy = 0
        if direction == 'left':
            dx = -speed
            dy = 0
        if direction == 'right':
            dx = speed
            dy = 0
        if direction == 'up':
            dx = 0
            dy = -speed
        if direction == 'down':
            dx = 0
            dy = speed

        mobile_velocity_component.dx = dx
        mobile_velocity_component.dy = dy

    @staticmethod
    def get_mobile_velocity(gameworld, entity):
        player_velocity_component = gameworld.component_for_entity(entity, mobiles.Velocity)
        return player_velocity_component.dx, player_velocity_component.dy

    @staticmethod
    def set_mobile_has_moved(gameworld, mobile, status):
        position_component = gameworld.component_for_entity(mobile, mobiles.Position)
        position_component.has_moved = status

    @staticmethod
    def get_mobile_current_location(gameworld, mobile):
        location_component = gameworld.component_for_entity(mobile, mobiles.Position)
        return location_component.x, location_component.y

    @staticmethod
    def get_mobile_name_details(gameworld, entity):
        name_component = gameworld.component_for_entity(entity, mobiles.Name)
        names = [name_component.first, name_component.suffix]
        return names

    @staticmethod
    def set_mobile_first_name(gameworld, entity, name):
        firstname_component = gameworld.component_for_entity(entity, mobiles.Name)
        firstname_component.first = name

    @staticmethod
    def set_mobile_last_name(gameworld, entity, name):
        firstname_component = gameworld.component_for_entity(entity, mobiles.Name)
        firstname_component.suffix = name

    @staticmethod
    def get_mobile_race_details(gameworld, entity):
        race_component = gameworld.component_for_entity(entity, mobiles.Race)
        racial = [race_component.label, race_component.size, race_component.name_singular, race_component.name_plural,
                  race_component.name_name_adjective]
        return racial

    @staticmethod
    def get_mobile_personality_title(gameworld, entity):
        return 'Diplomatic'

    @staticmethod
    def set_mobile_derived_personality(gameworld, entity):
        player_entity = entity

        player_current_personality_component = gameworld.component_for_entity(player_entity, mobiles.Personality)
        player_current_personality_component.label = 'Diplomatic'

    # check ALL hand combos: main, off, and both hands
    @staticmethod
    def get_weapons_equipped(gameworld, entity):
        """

        :param gameworld:
        :param entity:
        :return: List of items equipped in main, off, and both hands
        """
        equipped = []
        main_hand = gameworld.component_for_entity(entity, mobiles.Equipped).main_hand
        off_hand = gameworld.component_for_entity(entity, mobiles.Equipped).off_hand
        both_hands = gameworld.component_for_entity(entity, mobiles.Equipped).both_hands

        equipped.append(main_hand)
        equipped.append(off_hand)
        equipped.append(both_hands)

        return equipped

    @staticmethod
    def equip_weapon(gameworld, entity, weapon, hand):

        if hand == 'main':
            gameworld.component_for_entity(entity, mobiles.Equipped).main_hand = weapon
        if hand == 'off':
            gameworld.component_for_entity(entity, mobiles.Equipped).off_hand = weapon
        if hand == 'both':
            gameworld.component_for_entity(entity, mobiles.Equipped).both_hands = weapon

    @staticmethod
    def unequip_all_weapons(gameworld, entity):
        MobileUtilities.unequip_weapon(gameworld, entity, 'main')
        MobileUtilities.unequip_weapon(gameworld, entity, 'off')
        MobileUtilities.unequip_weapon(gameworld, entity, 'both')

    @staticmethod
    def unequip_weapon(gameworld, entity, hand):

        if hand == 'main':
            gameworld.component_for_entity(entity, mobiles.Equipped).main_hand = 0
        if hand == 'off':
            gameworld.component_for_entity(entity, mobiles.Equipped).off_hand = 0
        if hand == 'both':
            gameworld.component_for_entity(entity, mobiles.Equipped).both_hands = 0

    @staticmethod
    def get_next_entity_id(gameworld):
        entity = world.get_next_entity_id(gameworld=gameworld)

        return entity

    @staticmethod
    def create_base_mobile(gameworld, entity_id):
        ai = constants.AI_LEVEL_NONE

        gameworld.add_component(entity_id, mobiles.MobileGender())
        gameworld.add_component(entity_id, mobiles.MobileDescription())
        gameworld.add_component(entity_id, mobiles.MobileGlyph())
        gameworld.add_component(entity_id, mobiles.MobileForeColour())
        gameworld.add_component(entity_id, mobiles.MobileBackColour())
        MobileUtilities.set_mobile_glyph(gameworld=gameworld, entity=entity_id, value='@')
        MobileUtilities.set_mobile_gender(gameworld=gameworld, entity=entity_id, gender='neutral')
        MobileUtilities.set_mobile_description(gameworld=gameworld, entity=entity_id, value='something')
        gameworld.add_component(entity_id,
                                mobiles.CharacterClass(label='', base_health=0, style='balanced', spellfile=''))
        gameworld.add_component(entity_id, mobiles.AILevel(ailevel=ai, description='none'))
        gameworld.add_component(entity_id, mobiles.Inventory())
        gameworld.add_component(entity_id, mobiles.Armour())
        gameworld.add_component(entity_id, mobiles.Jewellery())
        gameworld.add_component(entity_id, mobiles.Equipped())
        gameworld.add_component(entity_id, mobiles.Velocity())
        gameworld.add_component(entity_id, mobiles.SpecialBar(valuecurrent=10, valuemaximum=100))
        gameworld.add_component(entity_id, mobiles.Renderable(is_visible=True))
        gameworld.add_component(entity_id, mobiles.StatusEffects())
        gameworld.add_component(entity_id, mobiles.PrimaryAttributes())
        gameworld.add_component(entity_id, mobiles.SecondaryAttributes())
        gameworld.add_component(entity_id, mobiles.DerivedAttributes())
        gameworld.add_component(entity_id, mobiles.SpellBar(entity_id=0))
        gameworld.add_component(entity_id, mobiles.Race(race='', size=''))
        gameworld.add_component(entity_id, mobiles.Position())
        gameworld.add_component(entity_id, mobiles.Name())
        gameworld.add_component(entity_id, mobiles.ClassSpecific())
        gameworld.add_component(entity_id, mobiles.Personality())
        gameworld.add_component(entity_id, mobiles.DialogFlags())
        gameworld.add_component(entity_id, mobiles.NpcType())
        gameworld.add_component(entity_id, mobiles.MobileType())
        gameworld.add_component(entity_id, mobiles.Senses())
        gameworld.add_component(entity_id, mobiles.AIMemory())
        gameworld.add_component(entity_id, mobiles.PhysicalState())

    @staticmethod
    def is_mobile_a_shopkeeper(gameworld, target_entity):
        npctype_component = gameworld.component_for_entity(target_entity, mobiles.NpcType)
        return npctype_component.shopkeeper

    @staticmethod
    def get_type_of_shopkeeper(gameworld, target_entity):
        npctype_component = gameworld.component_for_entity(target_entity, mobiles.NpcType)
        return npctype_component.type_of_shopkeeper

    @staticmethod
    def set_type_of_shopkeeper(gameworld, target_entity, shopkeeper_type):
        npctype_component = gameworld.component_for_entity(target_entity, mobiles.NpcType)
        npctype_component.type_of_shopkeeper = shopkeeper_type
        npctype_component.shopkeeper = True

    @staticmethod
    def is_mobile_a_tutor(gameworld, target_entity):
        npctype_component = gameworld.component_for_entity(target_entity, mobiles.NpcType)
        return npctype_component.tutor

    @staticmethod
    def get_type_of_tutor(gameworld, target_entity):
        npctype_component = gameworld.component_for_entity(target_entity, mobiles.NpcType)
        return npctype_component.type_of_tutor

    @staticmethod
    def set_type_of_tutor(gameworld, target_entity, tutor_type):
        npctype_component = gameworld.component_for_entity(target_entity, mobiles.NpcType)
        npctype_component.type_of_tutor = tutor_type
        npctype_component.tutor = True

    @staticmethod
    def set_talk_to_me_flag(gameworld, target_entity):
        dialog_component = gameworld.component_for_entity(target_entity, mobiles.DialogFlags)
        dialog_component.talk_to_me = True

    @staticmethod
    def clear_talk_to_me_flag(gameworld, target_entity):
        dialog_component = gameworld.component_for_entity(target_entity, mobiles.DialogFlags)
        dialog_component.talk_to_me = False

    @staticmethod
    def get_talk_to_me_flag(gameworld, target_entity):
        dialog_component = gameworld.component_for_entity(target_entity, mobiles.DialogFlags)
        return dialog_component.talk_to_me

    @staticmethod
    def set_spoken_to_before_flag_to_true(gameworld, target_entity):
        dialog_component = gameworld.component_for_entity(target_entity, mobiles.DialogFlags)
        dialog_component.spoken_to_before = True

    @staticmethod
    def set_dialog_welcome_flag_to_false(gameworld, target_entity):
        dialog_component = gameworld.component_for_entity(target_entity, mobiles.DialogFlags)
        dialog_component.welcome = False

    @staticmethod
    def get_spoken_to_before_flag(gameworld, target_entity):
        dialog_component = gameworld.component_for_entity(target_entity, mobiles.DialogFlags)
        return dialog_component.spoken_to_before

    @staticmethod
    def set_player_last_known_position(gameworld, map_position, source_entity):
        gameworld.component_for_entity(source_entity, mobiles.AIMemory).player_last_known_position = map_position

    @staticmethod
    def get_player_last_known_position(gameworld, source_entity):
        ai_memory_component = gameworld.component_for_entity(source_entity, mobiles.AIMemory)
        return ai_memory_component.player_last_known_position

    @staticmethod
    def set_ai_visible_entities(gameworld, target_entity, visible_entities):
        gameworld.component_for_entity(target_entity, mobiles.AIMemory).visible_entities = visible_entities

    @staticmethod
    def get_ai_visible_entities(gameworld, target_entity):
        ai_visible_component = gameworld.component_for_entity(target_entity, mobiles.AIMemory)
        return ai_visible_component.visible_entities

    @staticmethod
    def add_enemy_components(gameworld, game_config, entity_id, min_range, max_range):

        min_text = 'SPELL_DIST_' + min_range
        max_text = 'SPELL_DIST_' + max_range
        minimum_range = configUtilities.get_config_value_as_integer(configfile=game_config, section='spells',
                                                                    parameter=min_text)
        maximum_range = configUtilities.get_config_value_as_integer(configfile=game_config, section='spells',
                                                                    parameter=max_text)

        if minimum_range == 0:
            logger.warning('ENTITY PREFERRED MIN RANGE SET TO ZERO')
        else:
            logger.debug('ENTITY PREFERRED MIN RANGE SET TO {}', minimum_range)

        if maximum_range == 0:
            logger.warning('ENTITY PREFERRED MAX RANGE SET TO ZERO')
        else:
            logger.debug('ENTITY PREFERRED MAX RANGE SET TO {}', maximum_range)

        gameworld.add_component(entity_id, mobiles.EnemyPreferredAttackMinRange(value=minimum_range))
        gameworld.add_component(entity_id, mobiles.EnemyPreferredAttackMaxRange(value=maximum_range))
        gameworld.add_component(entity_id, mobiles.EnemyCombatRole(value='none'))
        gameworld.add_component(entity_id, mobiles.MobileType(label='enemy'))
        gameworld.add_component(entity_id,
                                mobiles.CombatKit(title='', glyph='', armourset='', armour_mod='', weapons='',
                                                  pendent='', ring1='', ring2='', ear1='', ear2=''))

    @staticmethod
    def create_player_character(gameworld, player_entity):
        player_ai = constants.AI_LEVEL_PLAYER
        MobileUtilities.set_mobile_glyph(gameworld=gameworld, entity=player_entity, value='@')
        MobileUtilities.set_mobile_derived_personality(gameworld=gameworld, entity=player_entity)
        MobileUtilities.set_mobile_gender(gameworld=gameworld, entity=player_entity, gender='neutral')
        MobileUtilities.set_mobile_description(gameworld=gameworld, entity=player_entity, value='something')

        gameworld.add_component(player_entity,
                                mobiles.CharacterClass(label='', base_health=0, style='balanced', spellfile=''))
        gameworld.add_component(player_entity, mobiles.Name(first='', suffix=''))
        gameworld.add_component(player_entity, mobiles.AILevel(ailevel=player_ai, description='player'))
        gameworld.add_component(player_entity, mobiles.SpellBar(entity_id=0))
        gameworld.add_component(player_entity, mobiles.Viewport())
        gameworld.add_component(player_entity, mobiles.SpellCast())
        gameworld.add_component(player_entity, mobiles.MobileType(label='player'))
        gameworld.add_component(player_entity, mobiles.Scene())

    @staticmethod
    def set_player_current_scene(gameworld, current_scene, player_entity):
        gameworld.add_component(player_entity, mobiles.Scene(current_scene=current_scene))

    @staticmethod
    def get_player_current_scene(gameworld, player_entity):
        player_scene_component = gameworld.component_for_entity(player_entity, mobiles.Scene)
        return player_scene_component.current_scene

    @staticmethod
    def set_player_current_scene_exit(gameworld, scene_exit, player_entity):
        gameworld.add_component(player_entity, mobiles.Scene(scene_exit=scene_exit))

    @staticmethod
    def get_player_current_scene_exit(gameworld, player_entity):
        player_scene_component = gameworld.component_for_entity(player_entity, mobiles.Scene)
        return player_scene_component.scene_exit

    @staticmethod
    def set_player_scene_change(gameworld, player_entity, value):
        gameworld.add_component(player_entity, mobiles.Scene(scene_change=value))

    @staticmethod
    def get_player_scene_change(gameworld, player_entity):
        player_scene_component = gameworld.component_for_entity(player_entity, mobiles.Scene)
        return player_scene_component.scene_change

    @staticmethod
    def set_enemy_preferred_min_distance_from_target(gameworld, entity, value):
        gameworld.add_component(entity, mobiles.EnemyPreferredAttackMinRange(value=value))

    @staticmethod
    def get_enemy_preferred_min_range(gameworld, entity):
        enemy_attributes_component = gameworld.component_for_entity(entity, mobiles.EnemyPreferredAttackMinRange)
        return enemy_attributes_component.value

    @staticmethod
    def set_enemy_preferred_max_distance_from_target(gameworld, entity, value):
        gameworld.add_component(entity, mobiles.EnemyPreferredAttackMaxRange(value=value))

    @staticmethod
    def get_enemy_preferred_max_range(gameworld, entity):
        enemy_attributes_component = gameworld.component_for_entity(entity, mobiles.EnemyPreferredAttackMaxRange)
        return enemy_attributes_component.value

    @staticmethod
    def get_enemy_combat_role(gameworld, entity):
        enemy_attributes_component = gameworld.component_for_entity(entity, mobiles.EnemyCombatRole)
        return enemy_attributes_component.value

    @staticmethod
    def set_enemy_combat_role(gameworld, entity, value):
        gameworld.add_component(entity, mobiles.EnemyCombatRole(value=value))

    @staticmethod
    def set_mobile_visible(gameworld, entity):
        gameworld.add_component(entity, mobiles.Renderable(is_visible=True))

    @staticmethod
    def set_mobile_invisible(gameworld, entity):
        gameworld.add_component(entity, mobiles.Renderable(is_visible=False))

    @staticmethod
    def get_mobile_renderstate(gameworld, entity):
        render_component = gameworld.component_for_entity(entity, mobiles.Renderable)
        return render_component.is_visible

    @staticmethod
    def set_mobile_description(gameworld, entity, value):
        gameworld.component_for_entity(entity, mobiles.MobileDescription).label = value

    @staticmethod
    def set_mobile_glyph(gameworld, entity, value):
        gameworld.component_for_entity(entity, mobiles.MobileGlyph).glyph = value

    @staticmethod
    def get_mobile_glyph(gameworld, entity):
        describe_component = gameworld.component_for_entity(entity, mobiles.MobileGlyph)

        return describe_component.glyph

    @staticmethod
    def get_mobile_fg_render_colour(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.MobileForeColour).fg

    @staticmethod
    def get_mobile_bg_render_colour(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.MobileBackColour).bg

    @staticmethod
    def set_mobile_fg_render_colour(gameworld, entity, value):
        gameworld.component_for_entity(entity, mobiles.MobileForeColour).fg = value

    @staticmethod
    def set_mobile_bg_render_colour(gameworld, entity, value):
        gameworld.component_for_entity(entity, mobiles.MobileBackColour).bg = value

    @staticmethod
    def set_mobile_ai_level(gameworld, entity, value):
        gameworld.component_for_entity(entity, mobiles.AILevel).label = value

    @staticmethod
    def set_mobile_ai_description(gameworld, entity, value):
        gameworld.component_for_entity(entity, mobiles.AILevel).description = value

    @staticmethod
    def set_mobile_senses_vision_range(gameworld, entity, value):
        gameworld.component_for_entity(entity, mobiles.Senses).vision_range = value

    @staticmethod
    def get_mobile_senses_vision_range(gameworld, entity):
        senses_component = gameworld.component_for_entity(entity, mobiles.Senses)

        return senses_component.vision_range

    @staticmethod
    def get_mobile_physical_hurt_status(gameworld, entity):
        physical_component = gameworld.component_for_entity(entity, mobiles.PhysicalState)
        return physical_component.am_i_hurt

    @staticmethod
    def set_mobile_physical_hurt_state_to_true(gameworld, entity):
        gameworld.component_for_entity(entity, mobiles.PhysicalState).am_i_hurt = True

    @staticmethod
    def set_mobile_physical_hurt_state_to_false(gameworld, entity):
        gameworld.component_for_entity(entity, mobiles.PhysicalState).am_i_hurt = False

    @staticmethod
    def set_spellbar_for_entity(gameworld, entity, spellbar_entity):
        gameworld.add_component(entity, mobiles.SpellBar(entity_id=spellbar_entity))

    @staticmethod
    def get_spellbar_id_for_entity(gameworld, entity):
        spellbar_component = gameworld.component_for_entity(entity, mobiles.SpellBar)

        return spellbar_component.entity_id

    @staticmethod
    def set_player_viewport_x(gameworld, entity, value):
        viewport_component = gameworld.component_for_entity(entity, mobiles.Viewport)
        viewport_component.posx = value

    @staticmethod
    def set_player_viewport_y(gameworld, entity, value):
        viewport_component = gameworld.component_for_entity(entity, mobiles.Viewport)
        viewport_component.posy = value

    @staticmethod
    def get_player_viewport_x(gameworld, entity):
        viewport_component = gameworld.component_for_entity(entity, mobiles.Viewport)
        return viewport_component.posx

    @staticmethod
    def get_player_viewport_y(gameworld, entity):
        viewport_component = gameworld.component_for_entity(entity, mobiles.Viewport)
        return viewport_component.posy

    @staticmethod
    def set_MessageLog_for_player(gameworld, entity, logid):
        gameworld.add_component(entity, mobiles.MessageLog(entity_id=logid, message_log_change=False))

    @staticmethod
    def get_MessageLog_id(gameworld, entity):
        messagelog_component = gameworld.component_for_entity(entity, mobiles.MessageLog)

        return messagelog_component.entity_id

    @staticmethod
    def set_view_message_log(gameworld, entity, view_value):
        messagelog_component = gameworld.component_for_entity(entity, mobiles.MessageLog)
        messagelog_component.message_log_change = view_value

    @staticmethod
    def get_view_message_log_value(gameworld, entity):
        messagelog_component = gameworld.component_for_entity(entity, mobiles.MessageLog)

        return messagelog_component.message_log_change

    @staticmethod
    def describe_the_mobile(gameworld, entity):
        player_name_component = gameworld.component_for_entity(entity, mobiles.Name)
        player_race_component = gameworld.component_for_entity(entity, mobiles.Race)
        player_class = MobileUtilities.get_character_class(gameworld, entity)
        player_gender = MobileUtilities.get_mobile_gender(gameworld, entity)
        player_style = MobileUtilities.get_character_style(gameworld, entity)

        return player_name_component.first + ' is a ' + player_gender + ' ' + player_race_component.label + ' ' + player_class + ' ( ' + player_style + ' )'

    @staticmethod
    def get_character_style(gameworld, entity):
        player_character_style_component = gameworld.component_for_entity(entity, mobiles.CharacterClass)
        return player_character_style_component.style

    @staticmethod
    def get_character_class(gameworld, entity):
        player_class_component = gameworld.component_for_entity(entity, mobiles.CharacterClass)
        return player_class_component.label

    @staticmethod
    def get_character_class_spellfilename(gameworld, entity):
        player_class_component = gameworld.component_for_entity(entity, mobiles.CharacterClass)
        return player_class_component.spellfile

    #
    # Mobile actions
    #

    # pick up item from dungeon floor
    @staticmethod
    def mobile_pick_up_item(gameworld, mobile):
        px, py = MobileUtilities.get_mobile_current_location(gameworld=gameworld, mobile=mobile)
        mobile_inventory_component = gameworld.component_for_entity(mobile, mobiles.Inventory)
        for ent, (rend, loc, desc) in gameworld.get_components(items.RenderItem, items.Location, items.Describable):
            if (loc.x == px and loc.y == py) and rend.is_true:
                # check if mobile has enough space in their inventory
                # remove item location data
                gameworld.remove_component(ent, items.Location)
                # add item entity to mobiles' inventory
                mobile_inventory_component.items.append(ent)
                logger.info('{} has been picked up', desc.name)

    @staticmethod
    def get_jewellery_already_equipped(gameworld, mobile):
        equipped = []

        lear = gameworld.component_for_entity(mobile, mobiles.Jewellery).left_ear
        equipped.append(lear)
        rear = gameworld.component_for_entity(mobile, mobiles.Jewellery).right_ear
        equipped.append(rear)
        lhand = gameworld.component_for_entity(mobile, mobiles.Jewellery).left_hand
        equipped.append(lhand)
        rhand = gameworld.component_for_entity(mobile, mobiles.Jewellery).right_hand
        equipped.append(rhand)
        neck = gameworld.component_for_entity(mobile, mobiles.Jewellery).neck
        equipped.append(neck)

        return equipped

    @staticmethod
    def stop_double_casting_same_spell(gameworld, entity):
        gameworld.remove_component(entity, mobiles.SpellCast)

    #
    # Get primary attributes
    #
    @staticmethod
    def get_mobile_primary_power(gameworld, entity):
        primary_components = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes)
        return primary_components.power

    @staticmethod
    def set_mobile_primary_power(gameworld, entity, value):
        current_stat_bonus = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).power
        new_stat_bonus = current_stat_bonus + value
        gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).power = new_stat_bonus

    @staticmethod
    def get_mobile_primary_precision(gameworld, entity):
        primary_components = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes)
        return primary_components.precision

    @staticmethod
    def set_mobile_primary_precision(gameworld, entity, value):
        current_stat_bonus = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).precision
        new_stat_bonus = current_stat_bonus + value
        gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).precision = new_stat_bonus

    @staticmethod
    def get_mobile_primary_toughness(gameworld, entity):
        primary_components = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes)
        return primary_components.toughness

    @staticmethod
    def set_mobile_primary_toughness(gameworld, entity, value):
        current_stat_bonus = MobileUtilities.get_mobile_primary_toughness(gameworld=gameworld, entity=entity)
        new_stat_bonus = current_stat_bonus + value
        gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).toughness = new_stat_bonus

    @staticmethod
    def get_mobile_primary_vitality(gameworld, entity):
        primary_components = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes)
        return primary_components.vitality

    @staticmethod
    def set_mobile_primary_vitality(gameworld, entity, value):
        current_stat_bonus = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).vitality
        new_stat_bonus = current_stat_bonus + value
        gameworld.component_for_entity(entity, mobiles.PrimaryAttributes).vitality = new_stat_bonus

    #
    # Get secondary attributes
    #
    @staticmethod
    def get_mobile_secondary_concentration(gameworld, entity):
        secondary_components = gameworld.component_for_entity(entity, mobiles.SecondaryAttributes)
        return secondary_components.concentration

    @staticmethod
    def set_mobile_secondary_concentration(gameworld, entity, value):
        gameworld.component_for_entity(entity, mobiles.SecondaryAttributes).concentration = value

    @staticmethod
    def get_mobile_secondary_condition_damage(gameworld, entity):
        secondary_components = gameworld.component_for_entity(entity, mobiles.SecondaryAttributes)
        return secondary_components.condition_damage

    @staticmethod
    def set_mobile_secondary_condition_damage(gameworld, entity, value):
        current_stat_bonus = gameworld.component_for_entity(entity, mobiles.SecondaryAttributes).condition_damage
        new_stat_bonus = current_stat_bonus + value
        gameworld.component_for_entity(entity, mobiles.SecondaryAttributes).condition_damage = new_stat_bonus

    @staticmethod
    def get_mobile_secondary_expertise(gameworld, entity):
        secondary_components = gameworld.component_for_entity(entity, mobiles.SecondaryAttributes)
        return secondary_components.expertise

    @staticmethod
    def set_mobile_secondary_expertise(gameworld, entity, value):
        gameworld.component_for_entity(entity, mobiles.SecondaryAttributes).expertise = value

    @staticmethod
    def get_mobile_secondary_ferocity(gameworld, entity):
        secondary_components = gameworld.component_for_entity(entity, mobiles.SecondaryAttributes)
        return secondary_components.ferocity

    @staticmethod
    def set_mobile_secondary_ferocity(gameworld, entity, value):
        gameworld.component_for_entity(entity, mobiles.SecondaryAttributes).ferocity = value

    @staticmethod
    def get_mobile_secondary_healing_power(gameworld, entity):
        secondary_components = gameworld.component_for_entity(entity, mobiles.SecondaryAttributes)
        return secondary_components.healing_power

    @staticmethod
    def set_mobile_secondary_healing_power(gameworld, entity, value):
        current_stat_bonus = gameworld.component_for_entity(entity, mobiles.SecondaryAttributes).healing_power
        new_stat_bonus = current_stat_bonus + value
        gameworld.component_for_entity(entity, mobiles.SecondaryAttributes).healing_power = new_stat_bonus

    @staticmethod
    def get_full_armourset_ids_from_entity(gameworld, entity):
        armour_equipped = []
        head = MobileUtilities.is_entity_wearing_head_armour(gameworld=gameworld, entity=entity)
        chest = MobileUtilities.is_entity_wearing_chest_armour(gameworld=gameworld, entity=entity)
        legs = MobileUtilities.is_entity_wearing_legs_armour(gameworld=gameworld, entity=entity)
        feet = MobileUtilities.is_entity_wearing_feet_armour(gameworld=gameworld, entity=entity)
        hands = MobileUtilities.is_entity_wearing_hands_armour(gameworld=gameworld, entity=entity)

        armour_equipped.append(chest)
        armour_equipped.append(head)
        armour_equipped.append(legs)
        armour_equipped.append(feet)
        armour_equipped.append(hands)

        return armour_equipped

    @staticmethod
    def is_entity_wearing_armour(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.DerivedAttributes).armour

    @staticmethod
    def is_entity_wearing_head_armour(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.Armour).head

    @staticmethod
    def is_entity_wearing_chest_armour(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.Armour).chest

    @staticmethod
    def is_entity_wearing_legs_armour(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.Armour).legs

    @staticmethod
    def is_entity_wearing_feet_armour(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.Armour).feet

    @staticmethod
    def is_entity_wearing_hands_armour(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.Armour).hands

    #
    # Calculate derived attributes
    #
    @staticmethod
    def set_mobile_derived_attributes(gameworld, entity):
        MobileUtilities.set_mobile_derived_boon_duration(gameworld, entity)
        MobileUtilities.set_mobile_derived_condition_duration(gameworld, entity)
        MobileUtilities.set_mobile_derived_critical_damage(gameworld, entity)
        MobileUtilities.set_mobile_derived_critical_hit_chance(gameworld, entity)
        MobileUtilities.set_mobile_derived_max_health(gameworld, entity)
        MobileUtilities.set_mobile_derived_current_health(gameworld, entity)
        MobileUtilities.set_mobile_derived_special_bar_current_value(gameworld, entity)

    @staticmethod
    def set_mobile_derived_special_bar_current_value(gameworld, entity):
        pass
        # do nothing yet

    @staticmethod
    def set_mobile_derived_boon_duration(gameworld, entity):

        entity_secondary_component = gameworld.component_for_entity(entity, mobiles.SecondaryAttributes)

        concentration_value = entity_secondary_component.concentration

        boon_duration_value = min(100, int(concentration_value / 15))

        gameworld.component_for_entity(entity, mobiles.DerivedAttributes).boon_duration = boon_duration_value

    @staticmethod
    def set_mobile_derived_critical_hit_chance(gameworld, entity):
        base_value = 5  # every hit has a 5% chance of causing a critical hit

        primary_attribute_component = gameworld.component_for_entity(entity, mobiles.PrimaryAttributes)

        precision_value = primary_attribute_component.precision
        # now cycle through the list of applied_boons looking for fury
        boon_fury_bonus = 0

        precision_bonus = int(precision_value / 21)

        stat_based_critical_hit_chance = base_value + boon_fury_bonus + precision_bonus

        critical_chance_value = min(100, stat_based_critical_hit_chance)

        gameworld.component_for_entity(entity, mobiles.DerivedAttributes).critical_chance = critical_chance_value

    @staticmethod
    def set_mobile_derived_critical_damage(gameworld, entity):
        base_value = 150
        entity_secondary_component = gameworld.component_for_entity(entity, mobiles.SecondaryAttributes)

        ferocity_value = entity_secondary_component.ferocity

        critical_damage_bonus = int(ferocity_value / 15)

        critical_damage_value = base_value + critical_damage_bonus

        gameworld.component_for_entity(entity, mobiles.DerivedAttributes).critical_damage = critical_damage_value

    @staticmethod
    def set_mobile_derived_condition_duration(gameworld, entity):
        entity_secondary_component = gameworld.component_for_entity(entity, mobiles.SecondaryAttributes)
        expertise_value = entity_secondary_component.expertise

        cond_duration = int(expertise_value / 15)

        cond_duration_bonus = min(100, cond_duration)
        gameworld.component_for_entity(entity, mobiles.DerivedAttributes).condition_duration = cond_duration_bonus

    @staticmethod
    def set_mobile_derived_max_health(gameworld, entity):

        # get primary attributes component
        vitality_value = MobileUtilities.get_mobile_primary_vitality(gameworld=gameworld, entity=entity)

        # get character class attributes component
        entity_class_component = gameworld.component_for_entity(entity, mobiles.CharacterClass)
        class_base_health = entity_class_component.base_health
        vitality_calculated_health = vitality_value * 10
        health_value = vitality_calculated_health + class_base_health
        gameworld.component_for_entity(entity, mobiles.DerivedAttributes).maximum_health = health_value

    @staticmethod
    def set_mobile_derived_current_health(gameworld, entity):

        maximum_health = gameworld.component_for_entity(entity, mobiles.DerivedAttributes).maximum_health
        # check boons --> increase health
        # check conditions --> reduce health
        # check controls --> can affect it either way
        # check traits
        # check jewellery
        # check armour
        # check weapons

        gameworld.component_for_entity(entity, mobiles.DerivedAttributes).current_health = maximum_health

    #
    # Get derived attributes
    #

    @staticmethod
    def get_mobile_derived_armour_value(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.DerivedAttributes).armour

    @staticmethod
    def get_mobile_derived_boon_duration(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.DerivedAttributes).boon_duration

    @staticmethod
    def get_mobile_derived_critical_hit_chance(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.DerivedAttributes).critical_chance

    @staticmethod
    def get_mobile_derived_critical_damage(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.DerivedAttributes).critical_damage

    @staticmethod
    def get_mobile_derived_condition_duration(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.DerivedAttributes).condition_duration

    @staticmethod
    def get_mobile_derived_maximum_health(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.DerivedAttributes).maximum_health

    @staticmethod
    def get_mobile_derived_current_health(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.DerivedAttributes).current_health

    @staticmethod
    def get_mobile_derived_special_bar_current_value(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.SpecialBar).currentvalue

    @staticmethod
    def get_mobile_derived_special_bar_max_value(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.SpecialBar).maximumvalue

    @staticmethod
    def get_combat_status(gameworld, entity):
        status_effects_component = gameworld.component_for_entity(entity, mobiles.StatusEffects)
        return status_effects_component.in_combat

    #
    # Set derived attributes
    #
    @staticmethod
    def set_current_health_during_combat(gameworld, entity, damage_to_apply):
        target_current_health = MobileUtilities.get_mobile_derived_current_health(gameworld=gameworld, entity=entity)
        target_new_health = target_current_health - damage_to_apply
        gameworld.component_for_entity(entity, mobiles.DerivedAttributes).current_health = target_new_health

    @staticmethod
    def set_combat_status_to_true(gameworld, entity):
        status_effects_component = gameworld.component_for_entity(entity, mobiles.StatusEffects)
        status_effects_component.in_combat = True

    @staticmethod
    def set_combat_status_to_false(gameworld, entity):
        status_effects_component = gameworld.component_for_entity(entity, mobiles.StatusEffects)
        status_effects_component.in_combat = False

    @staticmethod
    def get_current_condis_applied_to_mobile(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.StatusEffects).conditions

    @staticmethod
    def get_current_boons_applied_to_mobile(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.StatusEffects).boons

    @staticmethod
    def get_current_controls_applied_to_mobile(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.StatusEffects).controls

    #
    # COMBAT KITS
    #
    @staticmethod
    def set_combat_kit_title(gameworld, entity, title_string):
        combat_kit_component = gameworld.component_for_entity(entity, mobiles.CombatKit)
        combat_kit_component.title = title_string

    @staticmethod
    def get_combat_kit_title(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.CombatKit).title

    @staticmethod
    def set_combat_kit_glyph(gameworld, entity, glyph):
        combat_kit_component = gameworld.component_for_entity(entity, mobiles.CombatKit)
        combat_kit_component.glyph = glyph

    @staticmethod
    def get_combat_kit_glyph(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.CombatKit).glyph

    @staticmethod
    def set_combat_kit_ear1(gameworld, entity, ear1):
        combat_kit_component = gameworld.component_for_entity(entity, mobiles.CombatKit)
        combat_kit_component.ear1 = ear1

    @staticmethod
    def get_combat_kit_ear1(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.CombatKit).ear1

    @staticmethod
    def set_combat_kit_ear2(gameworld, entity, ear2):
        combat_kit_component = gameworld.component_for_entity(entity, mobiles.CombatKit)
        combat_kit_component.ear2 = ear2

    @staticmethod
    def get_combat_kit_ear2(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.CombatKit).ear2

    @staticmethod
    def set_combat_kit_weapons(gameworld, entity, weapons):
        combat_kit_component = gameworld.component_for_entity(entity, mobiles.CombatKit)
        combat_kit_component.weapons = weapons

    @staticmethod
    def get_combat_kit_weapons(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.CombatKit).weapons

    @staticmethod
    def set_combat_kit_armourset(gameworld, entity, armourset):
        combat_kit_component = gameworld.component_for_entity(entity, mobiles.CombatKit)
        combat_kit_component.armourset = armourset

    @staticmethod
    def get_combat_kit_armourset(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.CombatKit).armourset

    @staticmethod
    def set_combat_kit_armour_mod(gameworld, entity, armour_mod):
        combat_kit_component = gameworld.component_for_entity(entity, mobiles.CombatKit)
        combat_kit_component.armour_mod = armour_mod

    @staticmethod
    def get_combat_kit_armour_mod(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.CombatKit).armour_mod

    @staticmethod
    def set_combat_kit_ring1(gameworld, entity, ring1):
        combat_kit_component = gameworld.component_for_entity(entity, mobiles.CombatKit)
        combat_kit_component.ring1 = ring1

    @staticmethod
    def get_combat_kit_ring1(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.CombatKit).ring1

    @staticmethod
    def set_combat_kit_ring2(gameworld, entity, ring2):
        combat_kit_component = gameworld.component_for_entity(entity, mobiles.CombatKit)
        combat_kit_component.ring2 = ring2

    @staticmethod
    def get_combat_kit_ring2(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.CombatKit).ring2

    @staticmethod
    def set_combat_kit_pendant(gameworld, entity, pendent):
        combat_kit_component = gameworld.component_for_entity(entity, mobiles.CombatKit)
        combat_kit_component.pendent = pendent

    @staticmethod
    def get_combat_kit_pendent(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.CombatKit).pendent

    @staticmethod
    def set_combat_kit_jewelleryset(gameworld, entity, jewelleryset):
        combat_kit_component = gameworld.component_for_entity(entity, mobiles.CombatKit)
        combat_kit_component.jewelleryset = jewelleryset

    @staticmethod
    def get_combat_kit_jewelleryset(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.CombatKit).jewelleryset

    @staticmethod
    def set_movement_status(gameworld, entity, status):
        mobile_component = gameworld.component_for_entity(entity, mobiles.AIMemory)
        mobile_component.can_i_move = status

    @staticmethod
    def get_movement_status(gameworld, entity):
        return gameworld.component_for_entity(entity, mobiles.AIMemory).can_i_move
