import random

from loguru import logger
from components import spells, items, mobiles
from utilities import colourUtilities, configUtilities, formulas
from utilities.common import CommonUtils
from utilities.display import draw_simple_frame
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

        if weapon_type in ['sword', 'staff']:
            spells_to_choose_from.append(
                ItemUtilities.get_weapon_spell_slot_one_entity(gameworld=gameworld, weapon_entity=weapons_equipped[2]))
            spells_to_choose_from.append(
                ItemUtilities.get_weapon_spell_slot_two_entity(gameworld=gameworld, weapon_entity=weapons_equipped[2]))
            spells_to_choose_from.append(ItemUtilities.get_weapon_spell_slot_three_entity(gameworld=gameworld,
                                                                                          weapon_entity=
                                                                                          weapons_equipped[2]))
            spells_to_choose_from.append(
                ItemUtilities.get_weapon_spell_slot_four_entity(gameworld=gameworld, weapon_entity=weapons_equipped[2]))
            spells_to_choose_from.append(
                ItemUtilities.get_weapon_spell_slot_five_entity(gameworld=gameworld, weapon_entity=weapons_equipped[2]))
        if weapon_type in ['wand', 'scepter', 'dagger']:
            spells_to_choose_from.append(
                ItemUtilities.get_weapon_spell_slot_one_entity(gameworld=gameworld, weapon_entity=weapons_equipped[0]))
            spells_to_choose_from.append(
                ItemUtilities.get_weapon_spell_slot_two_entity(gameworld=gameworld, weapon_entity=weapons_equipped[0]))
            spells_to_choose_from.append(ItemUtilities.get_weapon_spell_slot_three_entity(gameworld=gameworld,
                                                                                          weapon_entity=
                                                                                          weapons_equipped[0]))
        if weapon_type in ['rod', 'focus']:
            spells_to_choose_from.append(
                ItemUtilities.get_weapon_spell_slot_four_entity(gameworld=gameworld, weapon_entity=weapons_equipped[1]))
            spells_to_choose_from.append(
                ItemUtilities.get_weapon_spell_slot_five_entity(gameworld=gameworld, weapon_entity=weapons_equipped[1]))

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
    def cast_spell(slot, gameworld, player):

        spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=gameworld, slot=slot,
                                                                          player_entity=player)

        logger.warning('Casting spell with entity id {} from slot {}', spell_entity, slot)

        # check if spell is on cool-down
        is_spell_on_cooldown = SpellUtilities.get_spell_cooldown_status(gameworld=gameworld, spell_entity=spell_entity)

        if not is_spell_on_cooldown:
            # spell isn't on cooldown
            # display list of valid targets and wait for the player
            # to select one of them

            visible_entities = MobileUtilities.get_visible_entities(gameworld=gameworld, target_entity=player)
            target_letters = SpellUtilities.helper_print_valid_targets(gameworld=gameworld,
                                                                       valid_targets=visible_entities)

            # blit the terminal
            terminal.refresh()

            # wait for user key press
            player_not_pressed_a_key = True
            while player_not_pressed_a_key:
                event_to_be_processed, event_action = handle_game_keys()
                if event_to_be_processed == 'keypress':
                    if event_action == 'quit':
                        player_not_pressed_a_key = False

                    if event_action != 'quit':
                        key_pressed = chr(97 + event_action)

                        player_not_pressed_a_key, target = SpellUtilities.has_valid_target_been_selected(
                            gameworld=gameworld, player_entity=player, target_letters=target_letters,
                            key_pressed=key_pressed, spell_entity=spell_entity, valid_targets=visible_entities,
                            slotid=slot)
        else:
            spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=spell_entity)
            CommonUtils.fire_event("spell-cooldown", gameworld=gameworld, spell_name=spell_name)

    @staticmethod
    def has_valid_target_been_selected(gameworld, player_entity, target_letters, key_pressed, spell_entity,
                                       valid_targets, slotid):
        player_not_pressed_a_key = True
        target = 0
        if key_pressed in target_letters:
            target = target_letters.index(key_pressed)
            player_not_pressed_a_key = False

            # add component covering spell has been cast
            gameworld.add_component(player_entity,
                                    mobiles.SpellCast(truefalse=True, spell_entity=spell_entity,
                                                      spell_caster=player_entity,
                                                      spell_target=valid_targets[0], spell_bar_slot=slotid))

        return player_not_pressed_a_key, target

    @staticmethod
    def helper_print_valid_targets(gameworld, valid_targets):
        game_config = configUtilities.load_config()
        vp_x_offset = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                  parameter='VIEWPORT_START_X')
        vp_y_offset = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                  parameter='VIEWPORT_START_Y')

        height = 5 + len(valid_targets) + 1

        terminal.clear_area(vp_x_offset + 1, vp_y_offset + 1, 26, height)

        draw_simple_frame(start_panel_frame_x=vp_x_offset, start_panel_frame_y=vp_y_offset, start_panel_frame_width=26,
                          start_panel_frame_height=height, title='| Valid Targets |',
                          fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))

        lft = vp_x_offset + 1

        entity_tag = vp_y_offset + 2
        target_letters = []

        xx = 0
        base_str_to_print = "[color=white][font=dungeon]"
        if len(valid_targets) == 0:
            str_to_print = base_str_to_print + 'No valid targets'
            terminal.printf(x=vp_x_offset + 3, y=entity_tag, s=str_to_print)
        else:
            for x in valid_targets:
                entity_name = MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=x)
                entity_fg = MobileUtilities.get_mobile_fg_render_colour(gameworld=gameworld, entity=x)
                entity_bg = MobileUtilities.get_mobile_bg_render_colour(gameworld=gameworld, entity=x)

                str_to_print = base_str_to_print + chr(
                    97 + xx) + ") [color=" + entity_fg + "][bkcolor=" + entity_bg + "]" + "@" + ' ' + entity_name[0]
                terminal.printf(x=vp_x_offset + 2, y=entity_tag, s=str_to_print)
                entity_tag += 1
                target_letters.append(chr(97 + xx))
                xx += 1
        str_to_print = base_str_to_print + 'Press ESC to cancel'
        terminal.printf(x=vp_x_offset + (lft + 3), y=(vp_y_offset + height), s=str_to_print)

        return target_letters

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
        return current_spells[slot - 1]

    @staticmethod
    def set_spellbar_slot(gameworld, spell_entity, slot, player_entity):
        current_spells = SpellUtilities.get_current_spellbar_spells(gameworld=gameworld, player_entity=player_entity)
        logger.warning('current spells in spell bar are {}', current_spells)
        if len(current_spells) > 0:
            current_spells[slot - 1] = spell_entity
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
