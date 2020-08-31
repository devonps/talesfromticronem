import random

from loguru import logger
from components import spells, items, mobiles
from utilities import configUtilities, formulas
from utilities.common import CommonUtils
from utilities.gamemap import GameMapUtilities
from utilities.input_handlers import handle_game_keys
from utilities.itemsHelp import ItemUtilities
from utilities.jsonUtilities import read_json_file
from utilities.mobileHelp import MobileUtilities
from bearlibterminal import terminal


class SpellUtilities:

    # -------------------------------------------
    #  Methods used by enemies of the player
    # -------------------------------------------

    @staticmethod
    def get_spell_list_for_enemy_by_weapon_type(gameworld, weapons_equipped, weapon_type):
        spells_to_choose_from = []

        spell_bar = 0

        if weapon_type in ['sword', 'staff']:
            spells_to_choose_from.append(SpellUtilities.get_spell_entity_from_slot_one(gameworld=gameworld, spellbar=spell_bar))
            spells_to_choose_from.append(SpellUtilities.get_spell_entity_from_slot_two(gameworld=gameworld, spellbar=spell_bar))
            spells_to_choose_from.append(SpellUtilities.get_spell_entity_from_slot_three(gameworld=gameworld, spellbar=spell_bar))
            spells_to_choose_from.append(SpellUtilities.get_spell_entity_from_slot_four(gameworld=gameworld, spellbar=spell_bar))
            spells_to_choose_from.append(SpellUtilities.get_spell_entity_from_slot_five(gameworld=gameworld, spellbar=spell_bar))

        if weapon_type in ['wand', 'scepter', 'dagger']:
            spells_to_choose_from.append(SpellUtilities.get_spell_entity_from_slot_one(gameworld=gameworld, spellbar=spell_bar))
            spells_to_choose_from.append(SpellUtilities.get_spell_entity_from_slot_two(gameworld=gameworld, spellbar=spell_bar))
            spells_to_choose_from.append(SpellUtilities.get_spell_entity_from_slot_three(gameworld=gameworld, spellbar=spell_bar))

        if weapon_type in ['rod', 'focus']:
            spells_to_choose_from.append(SpellUtilities.get_spell_entity_from_slot_four(gameworld=gameworld, spellbar=spell_bar))
            spells_to_choose_from.append(SpellUtilities.get_spell_entity_from_slot_five(gameworld=gameworld, spellbar=spell_bar))

        return spells_to_choose_from

    @staticmethod
    def get_list_of_spells_for_enemy(gameworld, weapon_type, mobile_class):
        # get list of spells for that weapon and mobile class
        spell_list = []

        for ent, (cl, wpn) in gameworld.get_components(spells.ClassName, spells.WeaponType):
            if (wpn.label == weapon_type) and (cl.label == mobile_class):
                spell_list.append(ent)

        return spell_list

    @staticmethod
    def can_mobile_cast_a_spell(gameworld, entity_id, target_entity):
        """
        What to check for...
        Do we have any spells in the spell bar
        Are all our spells on cooldown
        Are there any status effects that stop us from casting

        :param gameworld:
        :param entity_id:
        :return:
        """
        can_cast_a_spell = False
        remaining_spells = None
        weapon_type = ''

        weapons_equipped = MobileUtilities.get_weapons_equipped(gameworld=gameworld, entity=entity_id)
        if len(weapons_equipped) != weapons_equipped.count(weapons_equipped[0]):
            weapon_type = ItemUtilities.get_equipped_weapon_for_enemy(gameworld=gameworld,
                                                                      weapons_equipped=weapons_equipped)

            # get list of spells to choose from
            spells_to_choose_from = SpellUtilities.get_spell_list_for_enemy_by_weapon_type(gameworld=gameworld,
                                                                                           weapon_type=weapon_type,
                                                                                           weapons_equipped=weapons_equipped)

            logger.info('Spells enemy can choose from {}', spells_to_choose_from)
            # check for spells on cooldown and check spell range
            available_spells = SpellUtilities.check_for_spells_on_cooldown(gameworld=gameworld,
                                                                           spells_to_choose_from=spells_to_choose_from)
            remaining_spells = SpellUtilities.check_spells_for_range_to_target(gameworld=gameworld,
                                                                               spells_to_choose_from=available_spells,
                                                                               entity_id=entity_id,
                                                                               target_entity=target_entity)

            if len(remaining_spells) > 0:
                can_cast_a_spell = True
        else:
            logger.info('No weapons equipped.')

        return can_cast_a_spell, remaining_spells, weapon_type

    @staticmethod
    def check_for_spells_on_cooldown(gameworld, spells_to_choose_from):
        logger.info('spells being checked {}', spells_to_choose_from)
        for spell in spells_to_choose_from:
            is_spell_on_cooldown = SpellUtilities.get_spell_cooldown_status(gameworld=gameworld, spell_entity=spell)
            logger.debug('spell {} cooldown status {}', spell, is_spell_on_cooldown)
            if is_spell_on_cooldown:
                idx = spells_to_choose_from.index(spell)
                spells_to_choose_from[idx] = 0
                logger.debug('spell {} popped from list', spell)
        logger.info('remaining spells {}', spells_to_choose_from)

        spells_to_choose_from = SpellUtilities.remove_not_needed_spells_from_list(spells_to_choose_from)

        return spells_to_choose_from

    @staticmethod
    def remove_not_needed_spells_from_list(spells_to_choose_from):
        myspells = []
        for i, item in enumerate(spells_to_choose_from):
            if item != 0:
                myspells.append(item)

        return myspells

    @staticmethod
    def enemy_choose_random_spell_to_cast(spells_to_choose_from, weapon_type):
        spell_chosen = False
        spell_to_cast = 0
        spell_bar_slot_id = None
        while not spell_chosen:
            # choose random spell from available list
            spell_to_cast = random.choice(spells_to_choose_from)
            if weapon_type in ['sword', 'staff', 'dagger', 'wand', 'scepter']:
                spell_bar_slot_id = spells_to_choose_from.index(spell_to_cast)
                spell_chosen = True
            else:
                spell_bar_slot_id = 3 + spells_to_choose_from.index(spell_to_cast)
                spell_chosen = True
        logger.debug('Random spell for casting id is {}', spell_to_cast)

        return spell_to_cast, spell_bar_slot_id

    @staticmethod
    def check_spells_for_range_to_target(gameworld, spells_to_choose_from, entity_id, target_entity):
        distance_to_target = formulas.calculate_distance_to_target(gameworld=gameworld, from_entity=entity_id,
                                                                   to_entity=target_entity)
        logger.info('available spells {}', spells_to_choose_from)
        for spell in spells_to_choose_from:
            spell_range = SpellUtilities.get_spell_max_range(gameworld=gameworld, spell_entity=spell)
            if distance_to_target > spell_range:
                logger.debug('spell popped off due to range {}', spell)
                idx = spells_to_choose_from.index(spell)
                spells_to_choose_from[idx] = 0
        logger.info('spells left to cast {}', spells_to_choose_from)

        spells_to_choose_from = SpellUtilities.remove_not_needed_spells_from_list(spells_to_choose_from)

        return spells_to_choose_from

    @staticmethod
    def get_spell_type(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.SpellType).label

    @staticmethod
    def cast_spell(slot, gameworld, player, game_config, game_map):
        spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=gameworld, slot=slot,
                                                                          player_entity=player)

        logger.warning('Casting spell with entity id {} from slot {}', spell_entity, slot)

        # check if spell is on cool-down
        is_spell_on_cooldown = SpellUtilities.get_spell_cooldown_status(gameworld=gameworld, spell_entity=spell_entity)

        if not is_spell_on_cooldown:
            # spell targeting
            spell_target_entity = SpellUtilities.spell_targeting(gameworld=gameworld, game_map=game_map, player=player, spell_entity=spell_entity)
            logger.debug('Entity id targeted is {}', spell_target_entity)
        else:
            spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=spell_entity)
            CommonUtils.fire_event("spell-cooldown", gameworld=gameworld, spell_name=spell_name)

    @staticmethod
    def spell_targeting(gameworld, game_map, player, spell_entity):
        game_config = configUtilities.load_config()
        spell_target_entity = 0
        targeting_a_spell = True
        targeting_cursor_centre_x = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=player)
        targeting_cursor_centre_y = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=player)
        targeting_cursor = CommonUtils.get_ascii_to_unicode(game_config=game_config,
                                                            parameter='ASCII_SPELL_TARGETING_CURSOR')
        move_target_cursor = ['left', 'right', 'up', 'down']
        targeting_cursor_colour = '[font=dungeon][color=SPELLINFO_FRAME_COLOUR]'
        string_to_print = ''
        screen_offset_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='SCREEN_OFFSET_X')
        screen_offset_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='SCREEN_OFFSET_Y')

        while targeting_a_spell:
            entity_at_targeting_cursor_position = GameMapUtilities.get_mobile_entity_at_this_location(game_map=game_map,
                                                                                                      x=targeting_cursor_centre_x,
                                                                                                      y=targeting_cursor_centre_y)
            oldx = targeting_cursor_centre_x
            oldy = targeting_cursor_centre_y
            # display targeting cursor
            terminal.printf(x=screen_offset_x + targeting_cursor_centre_x,
                            y=screen_offset_y + targeting_cursor_centre_y,
                            s=targeting_cursor_colour + '[' + targeting_cursor + ']')

            # refresh terminal
            terminal.refresh()

            # get keyboard command
            event_to_be_processed, event_action = handle_game_keys()
            if event_action == 'quit':
                targeting_a_spell = False
            if event_action in move_target_cursor:
                this_x, this_y = SpellUtilities.move_spell_targetting_cursor(direction=event_action,
                                                                             curx=targeting_cursor_centre_x,
                                                                             cury=targeting_cursor_centre_y)
                is_the_targeting_cursor_blocked = SpellUtilities.check_for_blocked_movement(game_map=game_map,
                                                                                            newx=this_x,
                                                                                            newy=this_y)
                if not is_the_targeting_cursor_blocked:
                    targeting_cursor_centre_x = this_x
                    targeting_cursor_centre_y = this_y
                # draw entity back to screen
                string_to_print = SpellUtilities.determine_if_need_to_draw_entity(gameworld=gameworld,
                                                                                  game_map=game_map, oldx=oldx,
                                                                                  oldy=oldy,
                                                                                  target_entity=entity_at_targeting_cursor_position)
            terminal.printf(x=screen_offset_x + oldx, y=screen_offset_y + oldy, s=string_to_print)
            if event_action == 'enter':
                SpellUtilities.set_spell_cooldown_true(gameworld=gameworld, spell_entity=spell_entity)
                targeting_a_spell = False
                spell_target_entity = GameMapUtilities.get_mobile_entity_at_this_location(game_map=game_map,
                                                                                          x=targeting_cursor_centre_x,
                                                                                          y=targeting_cursor_centre_y)
        return spell_target_entity


    @staticmethod
    def determine_if_need_to_draw_entity(gameworld, game_map, oldx, oldy, target_entity):
        game_config = configUtilities.load_config()
        config_prefix_floor = 'ASCII_FLOOR_'
        tile_type_floor = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='TILE_TYPE_FLOOR')
        string_to_print = ''
        if target_entity > 0:
            char_to_display = MobileUtilities.get_mobile_glyph(gameworld=gameworld,
                                                               entity=target_entity)
            fg = MobileUtilities.get_mobile_fg_render_colour(gameworld=gameworld,
                                                             entity=target_entity)
            bg = MobileUtilities.get_mobile_bg_render_colour(gameworld=gameworld,
                                                             entity=target_entity)
            string_to_print = "[color=" + fg + "][font=dungeon][bkcolor=" + bg + "]" + char_to_display

        else:
            tile = game_map.tiles[oldx][oldy].type_of_tile
            if tile == tile_type_floor:
                char_to_display = CommonUtils.get_unicode_ascii_char(game_config=game_config,
                                                                     config_prefix=config_prefix_floor,
                                                                     tile_assignment=0)
                colour_code = configUtilities.get_config_value_as_string(configfile=game_config,
                                                                         section='colorCodes',
                                                                         parameter='FLOOR_INSIDE_FOV')
                string_to_print = colour_code + '[' + char_to_display + ']'

        return string_to_print

    @staticmethod
    def move_spell_targetting_cursor(direction, curx, cury):
        if direction == 'left':
            curx -= 1
        if direction == 'right':
            curx += 1
        if direction == 'up':
            cury -= 1
        if direction == 'down':
            cury += 1

        return curx, cury

    @staticmethod
    def check_for_blocked_movement(game_map, newx, newy):
        return GameMapUtilities.is_tile_blocked(game_map, newx, newy)

    @staticmethod
    def get_valid_targets_for_spell(gameworld, casting_entity, spell_entity):
        # get game map x/y position of spell casting entity
        spell_caster_x_pos = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=casting_entity)
        spell_caster_y_pos = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=casting_entity)

        spell_range = SpellUtilities.get_spell_max_range(gameworld=gameworld, spell_entity=spell_entity)

        from_x = spell_caster_x_pos - spell_range
        to_x = (spell_caster_x_pos + spell_range) + 1
        from_y = spell_caster_y_pos - spell_range
        to_y = (spell_caster_y_pos + spell_range) + 1
        # get list of targets within the range of the spell - I scan a square around the spell caster
        valid_targets = []
        for ent, (pos, name, desc) in gameworld.get_components(mobiles.Position, mobiles.Name,
                                                               mobiles.Describable):

            if (pos.x in range(from_x, to_x) and pos.y in range(from_y, to_y)) and ent != casting_entity:
                # is this a valid target for the spell?
                valid_targets.append((ent, name.first, desc.glyph, desc.foreground, desc.background))

        return valid_targets

    @staticmethod
    def get_spell_cooldown_status(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.CoolDown).is_true

    @staticmethod
    def set_spell_cooldown_true(gameworld, spell_entity):
        spell_cooldown_component = gameworld.component_for_entity(spell_entity, spells.CoolDown)
        spell_cooldown_component.is_true = True

    @staticmethod
    def set_spell_cooldown_false(gameworld, spell_entity):
        spell_cooldown_component = gameworld.component_for_entity(spell_entity, spells.CoolDown)
        spell_cooldown_component.is_true = False

    @staticmethod
    def get_spell_name_in_weapon_slot(gameworld, weapon_equipped, slotid):
        """
        Returns the spell name from weapon slot
        :param weapon_equipped:
        :param slotid:
        :return:
        """
        spell_name = 'no spell'
        spell = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld, weapon_equipped, slotid)
        if int(spell) > 0:
            spell_name = gameworld.component_for_entity(spell, spells.Name).label

        return spell_name

    @staticmethod
    def get_spell_entity_at_weapon_slot(gameworld, weapon_equipped, slotid):

        spell_entity = 0

        if slotid == 1:
            spell_entity = gameworld.component_for_entity(weapon_equipped, items.Spells).slot_one
        if slotid == 2:
            spell_entity = gameworld.component_for_entity(weapon_equipped, items.Spells).slot_two
        if slotid == 3:
            spell_entity = gameworld.component_for_entity(weapon_equipped, items.Spells).slot_three
        if slotid == 4:
            spell_entity = gameworld.component_for_entity(weapon_equipped, items.Spells).slot_four
        if slotid == 5:
            spell_entity = gameworld.component_for_entity(weapon_equipped, items.Spells).slot_five

        return spell_entity

    @staticmethod
    def setup_mobile_empty_spellbar(gameworld, player_entity):
        spell_bar = MobileUtilities.get_next_entity_id(gameworld=gameworld)

        MobileUtilities.set_spellbar_for_entity(gameworld=gameworld, entity=player_entity, spellbar_entity=spell_bar)

    @staticmethod
    def get_class_heal_spell(gameworld, player_entity):
        spell_entity = 0
        player_class = MobileUtilities.get_character_class(gameworld=gameworld, entity=player_entity)
        for ent, (cl, typ) in gameworld.get_components(spells.ClassName, spells.SpellType):
            if typ.label == 'heal' and cl.label == player_class:
                spell_entity = ent
        return spell_entity

    @staticmethod
    def add_utility_spell_to_spellbar(gameworld, player_entity, slot_id, spell_entity):
        spellbar = MobileUtilities.get_spellbar_id_for_entity(gameworld=gameworld, entity=player_entity)
        if slot_id == 7:
            SpellUtilities.set_spell_entity_in_slot_seven(gameworld=gameworld, spellbar=spellbar, spell_entity=spell_entity)

        if slot_id == 8:
            SpellUtilities.set_spell_entity_in_slot_eight(gameworld=gameworld, spellbar=spellbar,
                                                          spell_entity=spell_entity)

        if slot_id == 9:
            SpellUtilities.set_spell_entity_in_slot_nine(gameworld=gameworld, spellbar=spellbar,
                                                          spell_entity=spell_entity)

    # below is the old/original way of tracking the spells - it needs to be deprecated
    @staticmethod
    def populate_spell_bar_initially(gameworld, player_entity):

        spellbar = MobileUtilities.get_next_entity_id(gameworld=gameworld)

        MobileUtilities.set_spellbar_for_entity(gameworld=gameworld, entity=player_entity, spellbar_entity=spellbar)
        weapons_equipped = MobileUtilities.get_weapons_equipped(gameworld=gameworld, entity=player_entity)

        if len(weapons_equipped) != 0:
            main_hand_weapon = weapons_equipped[0]
            off_hand_weapon = weapons_equipped[1]
            both_hands_weapon = weapons_equipped[2]
            SpellUtilities.helper_both_hands_weapon(gameworld=gameworld, player_entity=player_entity,
                                                    both_hands_weapon=both_hands_weapon)
            SpellUtilities.helper_main_hand_weapon(gameworld=gameworld, player_entity=player_entity,
                                                   main_hand_weapon=main_hand_weapon)
            SpellUtilities.helper_off_hand_weapon(gameworld=gameworld, player_entity=player_entity,
                                                  off_hand_weapon=off_hand_weapon)
        else:
            logger.warning('no weapons equipped')

        # now get the heal skill
        player_class = MobileUtilities.get_character_class(gameworld=gameworld, entity=player_entity)
        for ent, (cl, typ) in gameworld.get_components(spells.ClassName, spells.SpellType):
            if typ.label == 'heal' and cl.label == player_class:
                SpellUtilities.set_spellbar_slot(gameworld=gameworld, player_entity=player_entity,
                                                 spell_entity=ent, slot=6)

    @staticmethod
    def helper_both_hands_weapon(gameworld, player_entity, both_hands_weapon):
        if both_hands_weapon > 0:
            slotid = 1
            for _ in range(5):
                this_spell_entity = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld,
                                                                                   weapon_equipped=both_hands_weapon,
                                                                                   slotid=slotid)
                SpellUtilities.set_spellbar_slot(gameworld=gameworld, player_entity=player_entity,
                                                 spell_entity=this_spell_entity, slot=slotid)
                slotid += 1

    @staticmethod
    def helper_main_hand_weapon(gameworld, player_entity, main_hand_weapon):
        if main_hand_weapon > 0:
            slotid = 1
            for _ in range(3):
                this_spell_entity = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld,
                                                                                   weapon_equipped=main_hand_weapon,
                                                                                   slotid=slotid)
                SpellUtilities.set_spellbar_slot(gameworld=gameworld, player_entity=player_entity,
                                                 spell_entity=this_spell_entity, slot=slotid)
                slotid += 1

    @staticmethod
    def helper_off_hand_weapon(gameworld, player_entity, off_hand_weapon):
        if off_hand_weapon > 0:
            slotid = 4
            for _ in range(2):
                this_spell_entity = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld,
                                                                                   weapon_equipped=off_hand_weapon,
                                                                                   slotid=slotid)
                SpellUtilities.set_spellbar_slot(gameworld=gameworld, player_entity=player_entity,
                                                 spell_entity=this_spell_entity, slot=slotid)
                slotid += 1

    @staticmethod
    def get_spell_name(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.Name).label

    @staticmethod
    def get_spell_cast_time(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.CastTime).number_of_turns

    @staticmethod
    def get_spell_cooldown_time(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.CoolDown).number_of_turns

    @staticmethod
    def set_spell_cooldown_time(gameworld, spell_entity, value):
        spell_cooldown_component = gameworld.component_for_entity(spell_entity, spells.CoolDown)
        spell_cooldown_component.number_of_turns = value

    @staticmethod
    def get_spell_cooldown_remaining_turns(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.CoolDown).remaining_turns

    @staticmethod
    def set_spell_cooldown_remaining_turns(gameworld, spell_entity, value):
        spell_cooldown_component = gameworld.component_for_entity(spell_entity, spells.CoolDown)
        spell_cooldown_component.remaining_turns = value

    @staticmethod
    def get_spell_description(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.Description).label

    @staticmethod
    def get_spell_short_description(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.ShortDescription).label

    @staticmethod
    def get_spell_max_targets(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.MaxTargets).number_of_targets

    @staticmethod
    def get_spell_max_range(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.MaxRange).max_range

    @staticmethod
    def get_spell_damage_coeff(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.DamageCoefficient).is_set_to

    @staticmethod
    def get_spell_healing_coeff(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.HealingCoef).value

    @staticmethod
    def add_status_effect_condi(gameworld, spell_entity, status_effect):

        current_condis = SpellUtilities.get_all_condis_for_spell(gameworld=gameworld, spell_entity=spell_entity)
        current_condis.append(status_effect)
        status_effect_component = gameworld.component_for_entity(spell_entity, spells.StatusEffect)
        status_effect_component.condis = current_condis

    @staticmethod
    def get_all_condis_for_spell(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.StatusEffect).condis

    @staticmethod
    def add_status_effect_boon(gameworld, spell_entity, status_effect):
        current_boons = SpellUtilities.get_all_boons_for_spell(gameworld=gameworld, spell_entity=spell_entity)
        current_boons.append(status_effect)
        status_effect_component = gameworld.component_for_entity(spell_entity, spells.StatusEffect)
        status_effect_component.boons = current_boons

    @staticmethod
    def get_all_boons_for_spell(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.StatusEffect).boons

    @staticmethod
    def add_status_effect_control(gameworld, spell_entity, status_effect):
        current_controls = SpellUtilities.get_all_controls_for_spell(gameworld=gameworld, spell_entity=spell_entity)
        current_controls.append(status_effect)
        status_effect_component = gameworld.component_for_entity(spell_entity, spells.StatusEffect)
        status_effect_component.controls = current_controls

    @staticmethod
    def get_all_controls_for_spell(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.StatusEffect).controls

    @staticmethod
    def add_resources_to_spell(gameworld, spell_entity, resource):
        current_resources = SpellUtilities.get_all_resources_for_spell(gameworld=gameworld, spell_entity=spell_entity)
        current_resources.append(resource)
        status_effect_component = gameworld.component_for_entity(spell_entity, spells.StatusEffect)
        status_effect_component.resources = current_resources

    @staticmethod
    def get_spell_aoe_status(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.AreaOfEffect).use_area_of_effect

    @staticmethod
    def get_spell_aoe_size(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.AreaOfEffectSize).area_of_effect_size

    @staticmethod
    def get_all_resources_for_spell(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.StatusEffect).resources

    @staticmethod
    def apply_condis_to_target(gameworld, target_entity, list_of_condis):

        game_config = configUtilities.load_config()

        current_condis = MobileUtilities.get_current_condis_applied_to_mobile(gameworld=gameworld, entity=target_entity)
        target_names = MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=target_entity)
        target_class = MobileUtilities.get_character_class(gameworld=gameworld, entity=target_entity)

        # read the conditions.json file
        conditions_file_path = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                          parameter='CONDITIONSFILE')
        conditions_file = read_json_file(conditions_file_path)

        for condi in list_of_condis:

            for condition in conditions_file['conditions']:
                if condi == condition['condition_status_effect']:
                    z = {'name': condi, 'duration': int(condition['default_exists_for_turns']),
                         'baseDamage': int(condition['base_damage_per_stack']),
                         'condDamageMod': float(condition['condition_damage_modifier']),
                         'weaponLevelMod': float(condition['weapon_level_modifier']), 'image': int(condition['image']),
                         'dialogue': condition['dialogue_options'][0][target_class],
                         'displayChar': condition['char'], 'shortcode': condi[:4]}

                    # add dialog for condition damage to message log
                    CommonUtils.fire_event("condi-applied", gameworld=gameworld, target=target_names[0],
                                           effect_dialogue=condition['dialogue_options'][0][
                                               target_class])

                    current_condis.append(z)

            status_effects_component = gameworld.component_for_entity(target_entity, mobiles.StatusEffects)
            status_effects_component.conditions = current_condis

        logger.debug('Condis applied to {} is {}', target_names[0], current_condis)

    @staticmethod
    def apply_boons_to_target(gameworld, target_entity, list_of_boons, spell_caster):

        game_config = configUtilities.load_config()

        current_boons = MobileUtilities.get_current_boons_applied_to_mobile(gameworld=gameworld, entity=target_entity)
        target_names = MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=target_entity)
        target_class = MobileUtilities.get_character_class(gameworld=gameworld, entity=target_entity)

        # read the boons.json file
        boons_file_path = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                     parameter='BOONSFILE')
        boons_file = read_json_file(boons_file_path)

        for boon in list_of_boons:

            for file_boon in boons_file['boons']:
                if boon == file_boon['boon_status_effect']:
                    b = {'name': boon, 'duration': int(file_boon['default_exists_for_turns']),
                         'dialogue': file_boon['dialogue_options'][0][target_class], 'image': file_boon['image'],
                         'displayChar': file_boon['char'], 'shortcode': boon[:4]}
                    if boon == 'fury':
                        b['improvement'] = 'crit_chance_increased'
                        b['increased_by'] = file_boon['crit_chance_improved']
                        target_entity = spell_caster
                        current_boons = MobileUtilities.get_current_boons_applied_to_mobile(gameworld=gameworld,
                                                                                            entity=target_entity)

                    # add dialog for boon effect to message log
                    CommonUtils.fire_event("boon-applied", gameworld=gameworld, target=target_names[0],
                                           effect_dialogue=file_boon['dialogue_options'][0][target_class])

                    # current_boons is a map
                    current_boons.append(b)
        if len(current_boons) != 0:
            status_effects_component = gameworld.component_for_entity(target_entity, mobiles.StatusEffects)
            status_effects_component.boons = current_boons
            logger.debug('Boons applied to {} is {}', target_names[0], current_boons)

    @staticmethod
    def get_spell_image(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.Image).id

    @staticmethod
    def get_spell_entity_from_spellbar_slot(gameworld, slot, player_entity):
        current_spells = SpellUtilities.get_current_spellbar_spells(gameworld=gameworld, player_entity=player_entity)
        return current_spells[slot]

    @staticmethod
    def set_spellbar_slot(gameworld, spell_entity, slot, player_entity):
        current_spells = SpellUtilities.get_current_spellbar_spells(gameworld=gameworld, player_entity=player_entity)
        logger.debug('current spells in spell bar are {}', current_spells)
        if len(current_spells) > 0:
            current_spells[slot] = spell_entity
        else:
            current_spells[0] = spell_entity

        spellbar_slots_component = gameworld.component_for_entity(player_entity, mobiles.SpellBar)
        spellbar_slots_component.slots = current_spells

    @staticmethod
    def get_current_spellbar_spells(gameworld, player_entity):
        return gameworld.component_for_entity(player_entity, mobiles.SpellBar).slots

    @staticmethod
    def get_spell_info_details(gameworld, spell_entity):
        spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=spell_entity)
        spell_range = str(SpellUtilities.get_spell_max_range(gameworld=gameworld, spell_entity=spell_entity))
        spell_is_on_cooldown = SpellUtilities.get_spell_cooldown_status(gameworld=gameworld,
                                                                        spell_entity=spell_entity)
        if spell_is_on_cooldown:
            spell_cooldown_value = SpellUtilities.get_spell_cooldown_time(gameworld=gameworld,
                                                                          spell_entity=spell_entity)
        else:
            spell_cooldown_value = 0
        if len(spell_range) < 2:
            sp_range = ' ' + spell_range
        else:
            sp_range = spell_range

        return spell_name, sp_range, spell_cooldown_value


    @staticmethod
    def render_off_hand_spells(gameworld, player_entity, game_config, this_row):
        unicode_section_headers = configUtilities.get_config_value_as_string(configfile=game_config, section='colorCodes', parameter='SPELL_UI_SECTION_HEADERS')
        slot = 3
        this_letter = 52
        slot_spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=gameworld, slot=slot,
                                                                               player_entity=player_entity)
        start_list_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                   parameter='START_LIST_X')
        if slot_spell_entity == 0:
            off_hand_weapon = 'Off Hand (Nothing)'
        else:
            weapon_name = ''
            # List of items equipped in main, off, and both hands
            equipped_weapons = MobileUtilities.get_weapons_equipped(gameworld=gameworld, entity=player_entity)
            if equipped_weapons[1] > 0:
                weapon_name = ItemUtilities.get_item_name(gameworld=gameworld, entity=equipped_weapons[1])
            if equipped_weapons[2] > 0:
                weapon_name = ItemUtilities.get_item_name(gameworld=gameworld, entity=equipped_weapons[2])
            off_hand_weapon = 'Off Hand (' + weapon_name + ')'
        this_row += 1
        terminal.printf(x=start_list_x, y=this_row, s=unicode_section_headers + off_hand_weapon)
        this_row += 2

        for _ in range(2):
            SpellUtilities.render_spells_in_hand(gameworld=gameworld, slot=slot, player_entity=player_entity, start_list_x=start_list_x, this_row=this_row, this_letter=this_letter, game_config=game_config)
            this_row += 1
            this_letter += 1
            slot += 1
        return this_row, this_letter

    @staticmethod
    def render_spells_in_hand(gameworld, slot, player_entity, start_list_x, this_row, this_letter, game_config):
        unicode_cooldown_disabled = configUtilities.get_config_value_as_string(configfile=game_config, section='colorCodes', parameter='SPELL_COOLDOWN_DISABLED')
        unicode_cooldown_enabled = configUtilities.get_config_value_as_string(configfile=game_config, section='colorCodes', parameter='SPELL_COOLDOWN_ENABLED')
        unicode_white_colour = configUtilities.get_config_value_as_string(configfile=game_config, section='colorCodes', parameter='SPELL_CURRENTLY_ACTIVE')
        slot_spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=gameworld, slot=slot,
                                                                               player_entity=player_entity)
        if slot_spell_entity > 0:
            cooldown_string_x = start_list_x + 1
            name_string_x = start_list_x + 4
            range_string_x = start_list_x + 31

            spell_name, spell_range, spell_cooldown_value = SpellUtilities.get_spell_info_details(
                gameworld=gameworld, spell_entity=slot_spell_entity)

            if spell_cooldown_value > 0:
                cooldown_colour = unicode_cooldown_enabled
            else:
                spell_cooldown_value = 0
                cooldown_colour = unicode_cooldown_disabled

            cooldown_string = cooldown_colour + ' ' + str(spell_cooldown_value)
            name_string = unicode_white_colour + spell_name
            range_string = unicode_white_colour + spell_range
            terminal.printf(x=cooldown_string_x, y=this_row, s=cooldown_string)
            terminal.printf(x=name_string_x, y=this_row, s=name_string)
            terminal.printf(x=range_string_x, y=this_row, s=range_string)

        terminal.printf(x=start_list_x, y=this_row, s=chr(this_letter))

    @staticmethod
    def render_main_hand_spells(gameworld, player_entity, game_config, this_row):
        this_letter = 49
        slot = 0
        unicode_section_headers = configUtilities.get_config_value_as_string(configfile=game_config, section='colorCodes', parameter='SPELL_UI_SECTION_HEADERS')

        slot_spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=gameworld, slot=slot,
                                                                               player_entity=player_entity)
        start_list_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='spellinfo',
                                                                   parameter='START_LIST_X')
        if slot_spell_entity == 0:
            main_hand_weapon = 'Main Hand (Nothing)'
        else:
            weapon_name = ''
            # List of items equipped in main, off, and both hands
            equipped_weapons = MobileUtilities.get_weapons_equipped(gameworld=gameworld, entity=player_entity)
            if equipped_weapons[0] > 0:
                weapon_name = ItemUtilities.get_item_name(gameworld=gameworld, entity=equipped_weapons[0])
            if equipped_weapons[2] > 0:
                weapon_name = ItemUtilities.get_item_name(gameworld=gameworld, entity=equipped_weapons[2])
            main_hand_weapon = 'Main Hand (' + weapon_name + ')'
        this_row += 2
        terminal.printf(x=start_list_x, y=this_row, s=unicode_section_headers + main_hand_weapon)
        this_row += 2

        for _ in range(3):
            SpellUtilities.render_spells_in_hand(gameworld=gameworld, slot=slot, player_entity=player_entity, start_list_x=start_list_x, this_row=this_row, this_letter=this_letter, game_config=game_config)
            this_row += 1
            this_letter += 1
            slot += 1
        return this_row, this_letter

    @staticmethod
    def get_list_of_utility_spells_for_player(gameworld, player_entity):
        utility_spells_list = []
        player_class = MobileUtilities.get_character_class(gameworld=gameworld, entity=player_entity)
        for ent, (cl, typ) in gameworld.get_components(spells.ClassName, spells.SpellType):
            if typ.label == 'utility' and cl.label == player_class:
                utility_spells_list.append(ent)
        return utility_spells_list

    @staticmethod
    def get_list_of_weapon_spells_for_player(gameworld, player_entity, weapon_type):
        utility_spells_list = []
        player_class = MobileUtilities.get_character_class(gameworld=gameworld, entity=player_entity)
        for ent, (cl, typ, weapon) in gameworld.get_components(spells.ClassName, spells.SpellType, spells.WeaponType):
            if typ.label == 'combat' and cl.label == player_class and weapon.label == weapon_type:
                utility_spells_list.append(ent)
        return utility_spells_list
