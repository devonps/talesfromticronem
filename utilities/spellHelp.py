from loguru import logger
from components import spells, items, mobiles
from components.messages import Message
from utilities import colourUtilities, configUtilities
from utilities.common import CommonUtils
from utilities.display import draw_simple_frame
from utilities.input_handlers import handle_game_keys
from utilities.jsonUtilities import read_json_file
from utilities.mobileHelp import MobileUtilities
from bearlibterminal import terminal
from mapRelated.gameMap import RenderLayer


class SpellUtilities:

    @staticmethod
    def get_spell_type(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.SpellType).label

    @staticmethod
    def cast_spell(slot, gameworld, message_log_id, player):

        spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=gameworld, slot=slot,
                                                                          player_entity=player)

        current_turn = MobileUtilities.get_current_turn(gameworld=gameworld, entity=player)

        msg_turn_number = str(current_turn) + ":"

        logger.info('Casting spell with entity id {} from slot {}', spell_entity, slot)

        # check if spell is on cool-down
        is_spell_on_cooldown = SpellUtilities.get_spell_cooldown_status(gameworld=gameworld, spell_entity=spell_entity)

        if not is_spell_on_cooldown:
            # spell isn't on cooldown
            valid_targets = SpellUtilities.get_valid_targets_for_spell(gameworld=gameworld,
                                                                       player=player, spell_entity=spell_entity)

            # display list of valid targets and wait for the player
            # to select one of them
            lft = 10
            tp = 15
            height = 5 + len(valid_targets) + 1
            width = 26

            terminal.clear_area(lft, tp, width, height)
            prev_layer = terminal.state(terminal.TK_LAYER)
            terminal.layer(RenderLayer.VALIDTARGETS.value)

            draw_simple_frame(startx=lft, starty=tp, width=width, height=height, title='| Valid Targets |',
                              fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))

            entity_tag = tp + 3
            target_letters = []
            SpellUtilities.helper_print_valid_targets(valid_targets=valid_targets, lft=lft, entity_tag=entity_tag, target_letters=target_letters, tp=tp, height=height)

            terminal.layer(prev_layer)

            # blit the terminal
            terminal.refresh()

            # wait for user key press
            # validTargets[ent, name.first, desc.glyph, desc.foreground, desc.background]
            player_not_pressed_a_key = True
            while player_not_pressed_a_key:
                event_to_be_processed, event_action = handle_game_keys()
                if event_to_be_processed == 'keypress':
                    if event_action == 'quit':
                        player_not_pressed_a_key = False
                    if len(target_letters) != 0:
                        key_pressed = chr(97 + event_action)
                        player_not_pressed_a_key, target = SpellUtilities.has_valid_target_been_selected(gameworld=gameworld, player_entity=player, target_letters=target_letters, key_pressed=key_pressed, spell_entity=spell_entity, valid_targets=valid_targets)
                        SpellUtilities.helper_add_valid_target_to_message_log(gameworld=gameworld, msg_turn_number=msg_turn_number, valid_targets=valid_targets, target=target, message_log_id=message_log_id, player_not_pressed_a_key=player_not_pressed_a_key)
        else:
            msg = Message(text=msg_turn_number + "Spell is on cooldown ", msgclass="all", fg="white", bg="black",
                          fnt="")
            log_message = "[all]" + msg_turn_number + "Spell is on cooldown "
            CommonUtils.add_message(gameworld=gameworld, message=msg, logid=message_log_id,
                                    message_for_export=log_message)

    @staticmethod
    def has_valid_target_been_selected(gameworld, player_entity, target_letters, key_pressed, spell_entity, valid_targets):
        player_not_pressed_a_key = True
        target = 0
        if key_pressed in target_letters:
            target = target_letters.index(key_pressed)
            player_not_pressed_a_key = False

            # add component covering spell has been cast
            gameworld.add_component(player_entity,
                                    mobiles.SpellCast(truefalse=True, spell_entity=spell_entity,
                                                      spell_target=valid_targets[target][0], spell_bar_slot=1))

        return player_not_pressed_a_key, target

    @staticmethod
    def helper_add_valid_target_to_message_log(gameworld, msg_turn_number, valid_targets, target, message_log_id, player_not_pressed_a_key):
        if not player_not_pressed_a_key:
            str_to_print = msg_turn_number + valid_targets[target][1] + " has been targeted."
            msg = Message(text=str_to_print, msgclass="all", fg="yellow", bg="", fnt="")
            log_message = "[all]" + str_to_print
            CommonUtils.add_message(gameworld=gameworld, message=msg, logid=message_log_id,
                                    message_for_export=log_message)


    @staticmethod
    def helper_print_valid_targets(valid_targets, lft, entity_tag, target_letters, tp, height):
        xx = 0
        if len(valid_targets) == 0:
            str_to_print = "[color=white][font=dungeon]" + 'No valid targets'
            terminal.printf(x=lft + 3, y=entity_tag, s=str_to_print)
        else:
            for x in valid_targets:
                str_to_print = "[color=white]" + chr(97 + xx) + ") [color=" + x[3] + "][font=dungeon][bkcolor=" + x[
                    4] + "]" + x[2] + ' ' + x[1]
                terminal.printf(x=lft + 2, y=entity_tag, s=str_to_print)
                entity_tag += 1
                target_letters.append(chr(97 + xx))
                xx += 1
        str_to_print = "[color=white][font=dungeon]" + 'Press ESC to cancel'
        terminal.printf(x=lft + 3, y=tp + height, s=str_to_print)

    @staticmethod
    def get_valid_targets_for_spell(gameworld, player, spell_entity):

        # get x/y position of player character
        sx = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=player)
        sy = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=player)

        spell_range = SpellUtilities.get_spell_max_range(gameworld=gameworld, spell_entity=spell_entity)

        fx = sx - spell_range
        tx = (sx + spell_range) + 1
        fy = sy - spell_range
        ty = (sy + spell_range) + 1
        # get list of targets within the range of the spell - I scan a square around the player character
        valid_targets = []
        for xx in range(fx, tx):
            for yy in range(fy, ty):
                SpellUtilities.highlight_spell_range(sx, sy, xx, yy)
                for ent, (pos, name, desc) in gameworld.get_components(mobiles.Position, mobiles.Name,
                                                                       mobiles.Describable):
                    if (pos.x == xx and pos.y == yy) and ent != player:
                        # is this a valid target for the spell?
                        valid_targets.append((ent, name.first, desc.glyph, desc.foreground, desc.background))
        return valid_targets

    @staticmethod
    def highlight_spell_range(sx, sy, xx, yy):
        if xx != sx and yy != sy:
            str_to_print = "[font=dungeon][color=blue].[/color]"
            terminal.printf(x=xx, y=yy, s=str_to_print)

    @staticmethod
    def get_spell_cooldown_status(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.CoolDown).isTrue

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

        MobileUtilities.set_spellbar_for_entity(gameworld=gameworld, entity=player_entity, spellbarEntity=spellbar)
        weapons_equipped = MobileUtilities.get_weapons_equipped(gameworld=gameworld, entity=player_entity)

        if len(weapons_equipped) != 0:
            main_hand_weapon = weapons_equipped[0]
            off_hand_weapon = weapons_equipped[1]
            both_hands_weapon = weapons_equipped[2]
            SpellUtilities.helper_both_hands_weapon(gameworld=gameworld, player_entity=player_entity, both_hands_weapon=both_hands_weapon)
            SpellUtilities.helper_main_hand_weapon(gameworld=gameworld, player_entity=player_entity, main_hand_weapon=main_hand_weapon)
            SpellUtilities.helper_off_hand_weapon(gameworld=gameworld, player_entity=player_entity, off_hand_weapon=off_hand_weapon)

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
    def get_spell_description(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.Description).label

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
    def get_all_resources_for_spell(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.StatusEffect).resources

    @staticmethod
    def apply_condis_to_target(gameworld, target_entity, list_of_condis, msg_turn_number):

        game_config = configUtilities.load_config()

        current_condis = MobileUtilities.get_current_condis_applied_to_mobile(gameworld=gameworld, entity=target_entity)
        target_names = MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=target_entity)
        target_class = MobileUtilities.get_character_class(gameworld=gameworld, entity=target_entity)
        player_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
        message_log_id = MobileUtilities.get_MessageLog_id(gameworld=gameworld, entity=player_entity)

        # read the conditions.json file
        conditions_file_path = configUtilities.get_config_value_as_string(configfile=game_config, section='default',
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
                         'displayChar': condition['char']}

                    # add dialog for condition damage to message log
                    msg = Message(
                        text=msg_turn_number + target_names[0] + " screams: " + condition['dialogue_options'][0][
                            target_class],
                        msgclass="all", fg="white", bg="black", fnt="")
                    log_message = msg_turn_number + "[combat]" + target_names[0] + " screams: " + condition['dialogue_options'][0][
                        target_class]
                    CommonUtils.add_message(gameworld=gameworld, message=msg, logid=message_log_id,
                                            message_for_export=log_message)

                    current_condis.append(z)

            status_effects_component = gameworld.component_for_entity(target_entity, mobiles.StatusEffects)
            status_effects_component.conditions = current_condis

        logger.debug('Condis applied to {} is {}', target_names[0], current_condis)

    @staticmethod
    def apply_boons_to_target(gameworld, target_entity, list_of_boons, spell_caster, msg_turn_number):

        game_config = configUtilities.load_config()

        current_boons = MobileUtilities.get_current_boons_applied_to_mobile(gameworld=gameworld, entity=target_entity)
        target_names = MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=target_entity)
        target_class = MobileUtilities.get_character_class(gameworld=gameworld, entity=target_entity)
        player_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
        message_log_id = MobileUtilities.get_MessageLog_id(gameworld=gameworld, entity=player_entity)

        # read the boons.json file
        boons_file_path = configUtilities.get_config_value_as_string(configfile=game_config, section='default',
                                                                     parameter='BOONSFILE')
        boons_file = read_json_file(boons_file_path)

        for boon in list_of_boons:

            for file_boon in boons_file['boons']:
                if boon == file_boon['boon_status_effect']:
                    b = {'name': boon, 'duration': int(file_boon['default_exists_for_turns']),
                         'dialogue': file_boon['dialogue_options'][0][target_class], 'image': file_boon['image'],
                         'displayChar': file_boon['char']}
                    if boon == 'fury':
                        b['improvement'] = 'crit_chance_increased'
                        b['increased_by'] = file_boon['crit_chance_improved']
                        target_entity = spell_caster
                        current_boons = MobileUtilities.get_current_boons_applied_to_mobile(gameworld=gameworld,
                                                                                            entity=target_entity)

                    # add dialog for boon effect to message log
                    msg = Message(
                        text=msg_turn_number + target_names[0] + " " + file_boon['dialogue_options'][0][target_class],
                        msgclass="all", fg="white", bg="black", fnt="")
                    log_message = msg_turn_number + "[combat]" + target_names[0] + " " + file_boon['dialogue_options'][0][target_class]
                    CommonUtils.add_message(gameworld=gameworld, message=msg, logid=message_log_id, message_for_export=log_message)

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
